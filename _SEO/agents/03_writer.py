"""
Agent 3 — Writer
Calls claude CLI (subscription) with agent3_prompt.md + full research context.
"""
import json
import subprocess
import sys
import tempfile
import os
from datetime import date
from pathlib import Path

from config import PROMPTS_DIR, CLAUDE_CMD

PROMPT_FILE = PROMPTS_DIR / "agent3_prompt.md"


def build_full_context(data: dict) -> str:
    today_iso = data.get("today", date.today().isoformat())
    today_human = date.today().strftime("%B %d, %Y")
    utm_campaign = data.get("utm_campaign", data.get("slug", "borchani"))

    brief = data.get("research_brief", {})
    competitor_brief = data.get("competitor_brief", {})

    lines = [
        f"KEYWORD: {data['keyword']}",
        f"SLUG: {data['slug']}",
        f"TODAY ISO: {today_iso}",
        f"TODAY HUMAN: {today_human}",
        f"UTM CAMPAIGN: {utm_campaign}",
        f"TARGET WORD COUNT: {brief.get('target_word_count', 2000)}",
        f"CATEGORY: {brief.get('category', data.get('content_dir', 'blog'))}",
        f"TARGET AUDIENCE: {brief.get('target_audience', 'developers and indie founders')}",
        f"SEARCH INTENT: {brief.get('intent', data.get('intent', 'Informational'))}",
        "",
        "LSI KEYWORDS (use naturally, max 1 repeat per 150 words):",
    ]
    for k in (brief.get("lsi_keywords") or data.get("lsi_keywords", []))[:15]:
        lines.append(f"  - {k}")

    h2_questions = brief.get("h2_questions", [])
    if h2_questions:
        lines.append("")
        lines.append("H2 QUESTIONS TO USE AS HEADINGS:")
        for q in h2_questions:
            lines.append(f"  - {q}")

    faq_questions = brief.get("faq_questions", [])
    if faq_questions:
        lines.append("")
        lines.append("FAQ QUESTIONS:")
        for q in faq_questions:
            lines.append(f"  - {q}")

    unique_angle = brief.get("unique_angle", "")
    if unique_angle:
        lines.append("")
        lines.append(f"UNIQUE ANGLE FOR THIS ARTICLE: {unique_angle}")

    # External links from competitor agent
    ext_links = competitor_brief.get("external_links", [])
    if ext_links:
        lines.append("")
        lines.append("EXTERNAL LINKS TO USE (3-5, authoritative sources):")
        for lnk in ext_links[:5]:
            lines.append(f"  - Anchor: {lnk.get('anchor')} | URL: {lnk.get('url')} | Role: {lnk.get('role')} | Where: {lnk.get('context')}")

    # Image suggestions
    images = competitor_brief.get("image_suggestions", [])
    if images:
        lines.append("")
        lines.append("IMAGES TO EMBED:")
        for img in images[:5]:
            lines.append(f"  - Alt: {img.get('alt_text')} | URL: {img.get('unsplash_url')} | Placement: {img.get('placement')}")

    # Competitor must-cover topics
    must_cover = competitor_brief.get("must_cover_topics", [])
    if must_cover:
        lines.append("")
        lines.append("MUST COVER (competitor gap analysis):")
        for t in must_cover[:10]:
            lines.append(f"  - {t}")

    # Raw competitor excerpts
    competitors = data.get("competitor_analysis", data.get("competitors", []))
    if competitors:
        lines.append("")
        lines.append("COMPETITOR ARTICLES (for context, do not copy):")
        for i, comp in enumerate(competitors[:3], 1):
            lines.append(f"")
            lines.append(f"  Competitor {i}: {comp.get('url', 'N/A')}")
            lines.append(f"  Title: {comp.get('title') or comp.get('original_title', 'N/A')}")
            excerpt = comp.get("body_excerpt", "")
            if excerpt:
                lines.append(f"  Excerpt: {' '.join(excerpt.split()[:200])}")

    return "\n".join(lines)


def run(research_data: dict) -> dict:
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
    context = build_full_context(research_data)
    today_iso = research_data.get("today", date.today().isoformat())
    today_human = date.today().strftime("%B %d, %Y")
    utm = research_data.get("utm_campaign", research_data.get("slug", "borchani"))

    full_prompt = (
        prompt_template
        .replace("{{FULL_RESEARCH_CONTEXT}}", context)
        .replace("{{TODAY_ISO}}", today_iso)
        .replace("{{TODAY_HUMAN}}", today_human)
        .replace("{{UTM_CAMPAIGN}}", utm)
        .replace("{{READING_TIME}}", "8")
    )

    print(f"[Agent 3] Writing article: {research_data['keyword']}")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(full_prompt)
        pf = f.name

    try:
        result = subprocess.run(
            f'{CLAUDE_CMD} -p "$(cat {pf})"',
            capture_output=True, text=True, timeout=600, shell=True,
        )
        mdx = result.stdout.strip()

        if not mdx or len(mdx) < 500:
            result = subprocess.run(
                [CLAUDE_CMD, "--print", full_prompt],
                capture_output=True, text=True, timeout=600,
            )
            mdx = result.stdout.strip()
    finally:
        os.unlink(pf)

    if not mdx:
        print("[Agent 3] ERROR: empty output from claude", file=sys.stderr)
        sys.exit(1)

    # Fix reading time in the MDX
    wc = len(mdx.split())
    reading_time = max(1, round(wc / 250))
    mdx = mdx.replace("{{READING_TIME}}", str(reading_time))

    print(f"[Agent 3] Done: {wc} words, ~{reading_time} min read")
    research_data["draft_mdx"] = mdx
    research_data["draft_word_count"] = wc
    return research_data


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    result = run(data)
    out = {k: v for k, v in result.items() if k != "competitor_analysis"}
    print(json.dumps(out, ensure_ascii=False, indent=2))
