"""
Orchestrator — runs 1-2 articles per topic category per day.

Cron (runs daily at 9:00 AM):
  0 9 * * * cd /home/ubuntu/celestial-cluster && /home/ubuntu/celestial-cluster/_SEO/venv/bin/python3 _SEO/agents/orchestrator.py >> _SEO/agents/cron.log 2>&1

Usage:
  python orchestrator.py              # full run: 1-2 articles per topic
  python orchestrator.py --dry-run    # show what would be picked, no writing
  python orchestrator.py --single     # exactly 1 article from 1 random topic
  python orchestrator.py --topic 02_vs  # 1-2 articles from specific topic only
"""
import importlib
import json
import os
import random
import subprocess
import sys
from datetime import date
from pathlib import Path

# Load .env
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

sys.path.insert(0, str(Path(__file__).parent))

from config import (
    KEYWORDS_DIR, ARTICLES_PER_DAY_MIN, ARTICLES_PER_DAY_MAX,
    TELEGRAM_BOT_TOKEN, CONTENT_DIR
)

agent1 = importlib.import_module("01_research")
agent2 = importlib.import_module("02_competitor")
agent3 = importlib.import_module("03_writer")
agent4 = importlib.import_module("04_editor")

try:
    from telegram_bot import send_article_sync
    TELEGRAM_AVAILABLE = bool(TELEGRAM_BOT_TOKEN)
except ImportError:
    TELEGRAM_AVAILABLE = False


def git_commit_and_push(mdx_path: str, keyword: str) -> None:
    """Commit the new article and push to GitHub."""
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPO", "aman-tiger/celestial-cluster")

    subprocess.run(["git", "add", mdx_path], capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"content: add article '{keyword}' [{date.today().isoformat()}]"],
        capture_output=True,
    )

    if token:
        remote_url = f"https://{token}@github.com/{repo}.git"
        subprocess.run(["git", "push", remote_url, "main"], capture_output=True)
        print(f"[Orchestrator] Pushed to GitHub: {repo}")
    else:
        print("[Orchestrator] No GITHUB_TOKEN — skipping push (commit done locally)")


def run_pipeline_for_keyword(keyword_data: dict, dry_run: bool = False) -> bool:
    """Run full 4-agent pipeline for one keyword."""
    print(f"\n  → Keyword: {keyword_data['keyword']} (vol: {keyword_data['volume']})")

    if dry_run:
        print("  [DRY RUN] Stopping here")
        return True

    # Agent 2: Scrape competitors
    keyword_data = agent2.run(keyword_data)

    # Agent 3: Write
    keyword_data = agent3.run(keyword_data)

    # Agent 4: Edit
    keyword_data = agent4.run(keyword_data)

    # Mark as published in CSV
    agent1.mark_as_published(keyword_data["csv_path"], keyword_data["csv_keyword"])

    if TELEGRAM_AVAILABLE:
        print("  [Orchestrator] Sending to Telegram...")
        send_article_sync(keyword_data)
        print("  [Orchestrator] Sent to Telegram for approval")
    else:
        # Save directly without approval
        out_dir = CONTENT_DIR / keyword_data["content_dir"]
        out_dir.mkdir(parents=True, exist_ok=True)
        mdx_path = out_dir / f"{keyword_data['slug']}.mdx"
        mdx_path.write_text(keyword_data["final_mdx"], encoding="utf-8")
        print(f"  [Orchestrator] Saved: {mdx_path}")
        git_commit_and_push(str(mdx_path), keyword_data["keyword"])

    return True


def get_topics() -> list[str]:
    """Return sorted list of topic folder names."""
    return sorted(p.name for p in KEYWORDS_DIR.iterdir() if p.is_dir())


def main():
    dry_run = "--dry-run" in sys.argv
    single = "--single" in sys.argv

    # Topic filter via --topic flag
    topic_filter = None
    if "--topic" in sys.argv:
        idx = sys.argv.index("--topic")
        if idx + 1 < len(sys.argv):
            topic_filter = sys.argv[idx + 1]

    topics = get_topics()
    if topic_filter:
        topics = [t for t in topics if t == topic_filter]
        if not topics:
            print(f"[Orchestrator] Topic '{topic_filter}' not found")
            sys.exit(1)

    if single:
        topics = [random.choice(topics)]

    print(f"[Orchestrator] Date: {date.today().isoformat()}")
    print(f"[Orchestrator] Topics to process: {len(topics)}")
    print(f"[Orchestrator] Articles per topic: {ARTICLES_PER_DAY_MIN}-{ARTICLES_PER_DAY_MAX}")

    total_ok = 0
    total_attempted = 0

    for topic in topics:
        count = random.randint(ARTICLES_PER_DAY_MIN, ARTICLES_PER_DAY_MAX)
        print(f"\n[Topic: {topic}] Writing {count} article(s)")

        for i in range(count):
            total_attempted += 1
            try:
                # Agent 1: pick keyword from this specific topic
                keyword_data = agent1.run_for_topic(topic)
                if not keyword_data:
                    print(f"  No unused keywords left in {topic}, skipping")
                    break

                ok = run_pipeline_for_keyword(keyword_data, dry_run=dry_run)
                if ok:
                    total_ok += 1

            except SystemExit:
                print(f"  [Topic {topic}] No keywords available, skipping")
                break
            except Exception as e:
                print(f"  [Topic {topic}] ERROR: {e}")
                import traceback
                traceback.print_exc()

    print(f"\n[Orchestrator] DONE: {total_ok}/{total_attempted} articles completed")
    if total_ok > 0:
        print(f"[Orchestrator] Check Telegram for approval or src/data/post/ for saved files")


if __name__ == "__main__":
    main()
