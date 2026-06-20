"""
Orchestrator — daily pipeline runner
Cron: 0 9 * * * cd /home/ubuntu/celestial-cluster && python _SEO/agents/orchestrator.py

Usage:
  python orchestrator.py          # run full pipeline (1-2 articles)
  python orchestrator.py --dry-run  # show which keyword would be picked, no writing
  python orchestrator.py --single   # force exactly 1 article
"""
import json
import os
import random
import sys
from pathlib import Path

# Load .env if present
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# Add agents dir to path
sys.path.insert(0, str(Path(__file__).parent))

from config import ARTICLES_PER_DAY_MIN, ARTICLES_PER_DAY_MAX, TELEGRAM_BOT_TOKEN

import importlib
agent1 = importlib.import_module("01_research")
agent2 = importlib.import_module("02_competitor")
agent3 = importlib.import_module("03_writer")
agent4 = importlib.import_module("04_editor")
from telegram_bot import send_article_sync


def run_pipeline(dry_run=False) -> bool:
    print("=" * 60)
    print("[Orchestrator] Starting article pipeline")

    # Agent 1: Pick keyword + get SERP data
    research = agent1.run()
    print(f"[Orchestrator] Keyword: {research['keyword']}")

    if dry_run:
        print("[Orchestrator] DRY RUN — stopping here")
        print(json.dumps(research, ensure_ascii=False, indent=2))
        return True

    # Agent 2: Scrape competitors
    research = agent2.run(research)

    # Agent 3: Write article
    research = agent3.run(research)

    # Agent 4: Edit + humanize
    research = agent4.run(research)

    # Mark keyword as published in CSV
    agent1.mark_as_published(research["csv_path"], research["csv_keyword"])

    # Send to Telegram for approval
    if TELEGRAM_BOT_TOKEN:
        print("[Orchestrator] Sending to Telegram for approval...")
        send_article_sync(research)
        print("[Orchestrator] Sent! Check Telegram.")
    else:
        # No Telegram — save MDX directly
        from config import CONTENT_DIR
        out_dir = CONTENT_DIR / research["content_dir"]
        out_dir.mkdir(parents=True, exist_ok=True)
        mdx_path = out_dir / f"{research['slug']}.mdx"
        mdx_path.write_text(research["final_mdx"], encoding="utf-8")
        print(f"[Orchestrator] No Telegram configured. Article saved to: {mdx_path}")

    print("[Orchestrator] Pipeline complete")
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    single = "--single" in sys.argv

    if single:
        count = 1
    else:
        count = random.randint(ARTICLES_PER_DAY_MIN, ARTICLES_PER_DAY_MAX)

    print(f"[Orchestrator] Will write {count} article(s) today")

    success = 0
    for i in range(count):
        print(f"\n[Orchestrator] Article {i+1}/{count}")
        try:
            ok = run_pipeline(dry_run=dry_run)
            if ok:
                success += 1
        except SystemExit as e:
            print(f"[Orchestrator] Pipeline exited: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[Orchestrator] ERROR: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()

    print(f"\n[Orchestrator] Done: {success}/{count} articles completed")


if __name__ == "__main__":
    main()
