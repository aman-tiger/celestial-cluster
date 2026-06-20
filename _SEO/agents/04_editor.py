"""
Agent 4 — Editor & Humanizer
Reviews the draft MDX via claude CLI:
- Removes banned words/constructions
- Checks em dashes, sentence rhythm
- Adds 2 personal opinions if missing
- Returns polished MDX ready for approval
"""
import json
import subprocess
import sys
import tempfile
import os

from config import CLAUDE_CMD

EDITOR_PROMPT = """You are a senior editor reviewing an AI-generated blog article.
Your job is to make it sound genuinely human-written and pass a strict quality checklist.

=== CHECKLIST — FIX EVERY ISSUE FOUND ===

1. BANNED WORDS (replace with simpler alternatives):
   moreover, furthermore, delve, meticulous, ensure, utmost, leverage, synergy,
   robust, utilize, facilitate, implement, additionally, crucial, pivotal, enhance,
   fostering, intricate, tapestry, vibrant, testament, underscore, garner, showcase,
   landscape (abstract use), interplay, align with, enduring, seamless, groundbreaking,
   revolutionary, cutting-edge, state-of-the-art, game-changer, paradigm shift,
   unlock, empower, elevate, supercharge, key (as adjective)

2. EM DASHES AND EN DASHES (—  –):
   Search the entire text. Replace every em dash and en dash with:
   - a comma, OR
   - a colon, OR
   - parentheses, OR
   - a period (start new sentence)
   Zero tolerance.

3. BANNED CONSTRUCTIONS:
   - "It's not just X, it's Y" → rewrite directly
   - "serves as", "stands as", "boasts" → replace with "is" / "has"
   - Three-item lists (A, B, and C) → use two or four items
   - "Let's dive in", "Here's what you need to know" → cut
   - "In conclusion", "To sum up" → cut, rewrite conclusion directly
   - Trailing -ing fragments: "highlighting...", "ensuring..." → complete the sentence
   - Passive subjectless sentences: "No config needed" → "You don't need a config file"

4. PERSONAL OPINIONS (add if fewer than 2 exist):
   Add 2 specific personal opinions with micro-arguments. Examples:
   - "Honestly, I find the free tier too limited for anything beyond prototyping."
   - "I've tested three alternatives side by side — Cursor still wins on autocomplete."
   Make them SPECIFIC, not generic.

5. SENTENCE RHYTHM (fix if too uniform):
   Mix: ~30% short (3-8 words), ~50% medium (10-18), ~20% long (20-35).
   Break up 3+ consecutive sentences of similar length.

6. HEADINGS: sentence case only. No Title Case.

7. MDX STRUCTURE: keep all frontmatter and JSON-LD schema intact.

=== ARTICLE TO EDIT ===

{DRAFT}

=== OUTPUT ===

Return ONLY the corrected MDX file. No explanations. No "Here's the edited version:".
Start directly with the frontmatter (---) block.
"""


def run(research_data: dict) -> dict:
    draft = research_data.get("draft_mdx", "")
    if not draft:
        print("[Agent 4] No draft found", file=sys.stderr)
        sys.exit(1)

    prompt = EDITOR_PROMPT.replace("{DRAFT}", draft)

    print(f"[Agent 4] Editing article: {research_data['keyword']}")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(prompt)
        prompt_file = f.name

    try:
        result = subprocess.run(
            f'{CLAUDE_CMD} -p "$(cat {prompt_file})"',
            capture_output=True,
            text=True,
            timeout=300,
            shell=True,
        )
        edited = result.stdout.strip()

        if not edited or len(edited) < 500:
            result = subprocess.run(
                [CLAUDE_CMD, "--print", prompt],
                capture_output=True,
                text=True,
                timeout=300,
            )
            edited = result.stdout.strip()
    finally:
        os.unlink(prompt_file)

    if not edited:
        print("[Agent 4] WARNING: editor returned empty, keeping draft", file=sys.stderr)
        edited = draft

    # Quick sanity checks
    em_dash_count = edited.count("—") + edited.count("–")
    if em_dash_count > 0:
        print(f"[Agent 4] WARNING: {em_dash_count} em/en dashes still present")

    word_count = len(edited.split())
    print(f"[Agent 4] Edited article: {word_count} words, {em_dash_count} dashes remaining")

    research_data["final_mdx"] = edited
    research_data["final_word_count"] = word_count
    return research_data


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    result = run(data)
    output = {k: v for k, v in result.items() if k not in ("competitor_analysis", "draft_mdx")}
    print(json.dumps(output, ensure_ascii=False, indent=2))
