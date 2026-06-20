"""
Agent 4 — Editor & Humanizer
Uses agent4_prompt.md which contains all Blocks 7-11 rules.
"""
import json
import subprocess
import sys
import tempfile
import os
from pathlib import Path

from config import PROMPTS_DIR, CLAUDE_CMD

PROMPT_FILE = PROMPTS_DIR / "agent4_prompt.md"


def run(research_data: dict) -> dict:
    draft = research_data.get("draft_mdx", "")
    if not draft:
        print("[Agent 4] No draft found", file=sys.stderr)
        sys.exit(1)

    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
    full_prompt = prompt_template.replace("{{DRAFT_MDX}}", draft)

    print(f"[Agent 4] Editing: {research_data['keyword']}")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(full_prompt)
        pf = f.name

    try:
        result = subprocess.run(
            f'{CLAUDE_CMD} -p "$(cat {pf})"',
            capture_output=True, text=True, timeout=600, shell=True,
        )
        edited = result.stdout.strip()

        if not edited or len(edited) < 500:
            result = subprocess.run(
                [CLAUDE_CMD, "--print", full_prompt],
                capture_output=True, text=True, timeout=600,
            )
            edited = result.stdout.strip()
    finally:
        os.unlink(pf)

    if not edited:
        print("[Agent 4] WARNING: empty output, keeping draft", file=sys.stderr)
        edited = draft

    # Count remaining issues
    em_dashes = edited.count("—") + edited.count("–")
    wc = len(edited.split())

    if em_dashes > 0:
        print(f"[Agent 4] WARNING: {em_dashes} em/en dashes still present")

    print(f"[Agent 4] Done: {wc} words, {em_dashes} dashes remaining")

    research_data["final_mdx"] = edited
    research_data["final_word_count"] = wc
    return research_data


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    result = run(data)
    out = {k: v for k, v in result.items() if k not in ("competitor_analysis", "draft_mdx")}
    print(json.dumps(out, ensure_ascii=False, indent=2))
