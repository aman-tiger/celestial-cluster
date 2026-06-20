"""
Agent 3 — Writer
Calls claude CLI (subscription) with master prompt + research context.
Produces a full MDX article.
"""
import json
import subprocess
import sys
import tempfile
import os
from pathlib import Path

from config import MASTER_PROMPT_FILE, CLAUDE_CMD


def build_context_block(data: dict) -> str:
    keyword = data["keyword"]
    slug = data["slug"]
    category = data["category"]
    today = data["today"]
    volume = data.get("volume", 0)
    kd = data.get("kd", "")
    intent = data.get("intent", "")
    lsi = data.get("lsi_keywords", [])

    competitors = data.get("competitor_analysis", data.get("competitors", []))

    lines = [
        "=== RESEARCH CONTEXT FOR THIS ARTICLE ===",
        f"",
        f"PRIMARY KEYWORD: {keyword}",
        f"URL SLUG: {slug}",
        f"CATEGORY: {category}",
        f"TODAY'S DATE: {today}",
        f"SEARCH VOLUME: {volume}",
        f"KEYWORD DIFFICULTY: {kd}",
        f"SEARCH INTENT: {intent}",
        f"",
        f"LSI / RELATED KEYWORDS (use naturally, max 1 per 150 words):",
    ]
    for k in lsi:
        lines.append(f"  - {k}")

    lines.append("")
    lines.append("COMPETITOR ANALYSIS (top 3 organic results):")

    for i, comp in enumerate(competitors[:3], 1):
        lines.append(f"")
        lines.append(f"Competitor {i}: {comp.get('url', 'N/A')}")
        lines.append(f"  Title: {comp.get('title') or comp.get('original_title', 'N/A')}")
        lines.append(f"  Word count: {comp.get('word_count', 'N/A')}")
        headings = comp.get("headings", [])
        if headings:
            lines.append(f"  Headings structure:")
            for h in headings[:15]:
                lines.append(f"    {h}")
        faq_qs = comp.get("faq_questions", [])
        if faq_qs:
            lines.append(f"  FAQ questions found:")
            for q in faq_qs[:5]:
                lines.append(f"    - {q}")
        excerpt = comp.get("body_excerpt", "")
        if excerpt:
            lines.append(f"  Content excerpt (first 300 words):")
            words = excerpt.split()
            lines.append("    " + " ".join(words[:300]))

    lines.append("")
    lines.append("=== END OF RESEARCH CONTEXT ===")
    lines.append("")
    lines.append("Now write the complete MDX article following ALL rules in this prompt.")
    lines.append("Output ONLY the MDX file content. No explanations, no commentary.")
    lines.append("Start with the frontmatter block (---) and end with the JSON-LD schema.")

    return "\n".join(lines)


def run(research_data: dict) -> dict:
    master_prompt = MASTER_PROMPT_FILE.read_text(encoding="utf-8")
    context_block = build_context_block(research_data)

    # Replace placeholder in master prompt
    full_prompt = master_prompt.replace("{{RESEARCH_CONTEXT}}", context_block)

    print(f"[Agent 3] Calling claude CLI to write article for: {research_data['keyword']}")

    # Write prompt to temp file to avoid shell escaping issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(full_prompt)
        prompt_file = f.name

    try:
        result = subprocess.run(
            [CLAUDE_CMD, "-p", f"$(cat {prompt_file})"],
            capture_output=True,
            text=True,
            timeout=300,
            shell=False,
        )

        if result.returncode != 0:
            # Try alternative invocation
            result = subprocess.run(
                f'{CLAUDE_CMD} -p "$(cat {prompt_file})"',
                capture_output=True,
                text=True,
                timeout=300,
                shell=True,
            )

        mdx_content = result.stdout.strip()

        if not mdx_content or len(mdx_content) < 500:
            # fallback: pass content directly
            result = subprocess.run(
                [CLAUDE_CMD, "--print", full_prompt],
                capture_output=True,
                text=True,
                timeout=300,
            )
            mdx_content = result.stdout.strip()

    finally:
        os.unlink(prompt_file)

    if not mdx_content:
        print("[Agent 3] ERROR: claude returned empty output", file=sys.stderr)
        sys.exit(1)

    word_count = len(mdx_content.split())
    print(f"[Agent 3] Article written: {word_count} words")

    research_data["draft_mdx"] = mdx_content
    research_data["draft_word_count"] = word_count
    return research_data


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    result = run(data)
    # Don't print full MDX to stdout in pipeline — save to queue instead
    output = {k: v for k, v in result.items() if k != "competitor_analysis"}
    print(json.dumps(output, ensure_ascii=False, indent=2))
