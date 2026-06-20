"""
Telegram approval bot
Sends article to your Telegram with 3 buttons: Approve / Reject / Edit
Listens for callback and text replies.

Run standalone: python telegram_bot.py
(keeps running, processes queue)
"""
import asyncio
import json
import sys
import os
from datetime import date
from pathlib import Path

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("Install: pip install python-telegram-bot", file=sys.stderr)
    sys.exit(1)

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, QUEUE_FILE, LOG_FILE, CONTENT_DIR


def load_queue() -> list:
    if QUEUE_FILE.exists():
        return json.loads(QUEUE_FILE.read_text())
    return []


def save_queue(queue: list) -> None:
    QUEUE_FILE.write_text(json.dumps(queue, ensure_ascii=False, indent=2))


def load_log() -> list:
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return []


def save_log(log: list) -> None:
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2))


def publish_article(item: dict) -> str:
    """Save MDX file to the content directory."""
    content_dir = CONTENT_DIR / item["content_dir"]
    content_dir.mkdir(parents=True, exist_ok=True)

    slug = item["slug"]
    mdx_path = content_dir / f"{slug}.mdx"
    mdx_path.write_text(item["final_mdx"], encoding="utf-8")

    log = load_log()
    log.append({
        "keyword": item["keyword"],
        "slug": slug,
        "category": item["category"],
        "published": date.today().isoformat(),
        "path": str(mdx_path),
    })
    save_log(log)
    return str(mdx_path)


async def send_article_for_approval(app, item: dict) -> None:
    """Send article preview to Telegram with approval buttons."""
    keyword = item["keyword"]
    word_count = item.get("final_word_count", "?")
    category = item["category"]
    slug = item["slug"]

    # Extract title and excerpt from MDX frontmatter
    mdx = item.get("final_mdx", "")
    title = keyword
    excerpt = ""
    for line in mdx.splitlines():
        if line.startswith("title:"):
            title = line.replace("title:", "").strip().strip('"')
        if line.startswith("excerpt:"):
            excerpt = line.replace("excerpt:", "").strip().strip('"')

    text = (
        f"New article ready for approval\n\n"
        f"Title: {title}\n"
        f"Keyword: {keyword}\n"
        f"Category: {category}\n"
        f"Slug: /{slug}\n"
        f"Words: {word_count}\n\n"
        f"Excerpt:\n{excerpt}\n\n"
        f"What do you want to do?"
    )

    keyboard = [
        [
            InlineKeyboardButton("Approve", callback_data=f"approve:{slug}"),
            InlineKeyboardButton("Reject", callback_data=f"reject:{slug}"),
        ],
        [
            InlineKeyboardButton("Edit (send your feedback as next message)", callback_data=f"edit:{slug}"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await app.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=text,
        reply_markup=markup,
    )

    # Also send first 1000 chars of article body
    body_preview = "\n".join(mdx.splitlines()[20:60])[:1000]
    if body_preview:
        await app.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f"Article preview:\n\n{body_preview}...",
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    action, slug = query.data.split(":", 1)
    queue = load_queue()
    item = next((i for i in queue if i["slug"] == slug), None)

    if not item:
        await query.edit_message_text(f"Article {slug} not found in queue.")
        return

    if action == "approve":
        path = publish_article(item)
        queue = [i for i in queue if i["slug"] != slug]
        save_queue(queue)
        await query.edit_message_text(
            f"Article published!\n\nFile: {path}\nCommit and deploy to make it live."
        )

    elif action == "reject":
        queue = [i for i in queue if i["slug"] != slug]
        save_queue(queue)
        await query.edit_message_text(f"Article '{slug}' rejected and removed from queue.")

    elif action == "edit":
        # Mark as waiting for edit feedback
        for i in queue:
            if i["slug"] == slug:
                i["status"] = "waiting_edit"
                i["edit_slug"] = slug
        save_queue(queue)
        context.user_data["editing_slug"] = slug
        await query.edit_message_text(
            f"Send your feedback / edit instructions for '{slug}' as the next message."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle edit feedback text from user."""
    slug = context.user_data.get("editing_slug")
    if not slug:
        return

    feedback = update.message.text
    queue = load_queue()
    item = next((i for i in queue if i["slug"] == slug), None)

    if not item:
        await update.message.reply_text(f"Article {slug} not found.")
        return

    await update.message.reply_text(
        f"Got it. Re-running editor with your feedback for '{slug}'.\nThis may take a minute..."
    )

    # Re-run agent 4 with feedback
    import subprocess
    import tempfile
    from config import CLAUDE_CMD

    prompt = (
        f"Edit this MDX article based on the following feedback:\n\n"
        f"FEEDBACK: {feedback}\n\n"
        f"ARTICLE:\n{item.get('final_mdx', item.get('draft_mdx', ''))}\n\n"
        f"Return ONLY the corrected MDX file. Start with frontmatter (---)."
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(prompt)
        pf = f.name

    try:
        result = subprocess.run(
            f'{CLAUDE_CMD} -p "$(cat {pf})"',
            capture_output=True, text=True, timeout=300, shell=True,
        )
        edited = result.stdout.strip()
    finally:
        os.unlink(pf)

    if edited and len(edited) > 500:
        for i in queue:
            if i["slug"] == slug:
                i["final_mdx"] = edited
                i["status"] = "ready_for_approval"
        save_queue(queue)
        context.user_data.pop("editing_slug", None)
        await update.message.reply_text("Article updated. Sending for re-approval...")

        app = context.application
        await send_article_for_approval(app, item)
    else:
        await update.message.reply_text("Edit failed. Try again or reject the article.")


def send_article_sync(item: dict) -> None:
    """Called from orchestrator to send article (non-async entry point)."""
    queue = load_queue()
    # Add or update in queue
    existing = next((i for i in queue if i["slug"] == item["slug"]), None)
    if existing:
        existing.update(item)
        existing["status"] = "ready_for_approval"
    else:
        item["status"] = "ready_for_approval"
        queue.append(item)
    save_queue(queue)

    async def _send():
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        async with app:
            await send_article_for_approval(app, item)

    asyncio.run(_send())


def main():
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("[Telegram Bot] Starting polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
