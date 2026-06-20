import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
KEYWORDS_DIR = BASE_DIR / "keywords"
PROMPTS_DIR = BASE_DIR / "prompts"
STATE_DIR = BASE_DIR / "state"
CONTENT_DIR = BASE_DIR.parent.parent / "src" / "data" / "post"

QUEUE_FILE = STATE_DIR / "queue.json"
LOG_FILE = STATE_DIR / "log.json"
MASTER_PROMPT_FILE = PROMPTS_DIR / "master_prompt.md"

# Telegram (required for approval flow)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# How many articles per day (1 or 2, chosen randomly by orchestrator)
ARTICLES_PER_DAY_MIN = 1
ARTICLES_PER_DAY_MAX = 2

# Claude CLI command (uses subscription auth, no API key needed)
CLAUDE_CMD = "claude"

# Category → content subdirectory mapping
CATEGORY_DIR_MAP = {
    "01_alternatives": "alternatives",
    "02_vs":           "vs",
    "03_solutions":    "solutions",
    "04_build":        "build",
    "05_for":          "for",
    "06_use-cases":    "solutions",
    "07_guides":       "build",
    "08_templates":    "build",
    "09_prompts":      "build",
    "10_blog":         "blog",
    "11_faq":          "blog",
    "12_dictionary":   "blog",
    "14_tools":        "blog",
    "16_paywall":      "blog",
    "17_landing":      "blog",
    "18_pricing":      "blog",
    "19_auth":         "build",
    "21_affiliate":    "blog",
}
