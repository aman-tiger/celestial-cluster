"""
Agent 1 — Research
Picks an unused keyword from CSV files, returns research context JSON.
"""
import csv
import json
import random
import re
import sys
from datetime import date
from pathlib import Path

from config import KEYWORDS_DIR, QUEUE_FILE, CATEGORY_DIR_MAP


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text)


def load_queue() -> list:
    if QUEUE_FILE.exists():
        return json.loads(QUEUE_FILE.read_text())
    return []


def pick_keyword() -> dict | None:
    """Pick a random unused keyword weighted by priority and volume."""
    candidates = []

    for category_folder in sorted(KEYWORDS_DIR.iterdir()):
        if not category_folder.is_dir():
            continue
        category = category_folder.name

        own_csv = category_folder / "own.csv"
        if not own_csv.exists():
            continue

        with open(own_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                keyword = row.get("keyword", "").strip()
                if not keyword:
                    continue
                if row.get("published", "").strip():
                    continue  # already used

                try:
                    priority = int(row.get("priority", 5) or 5)
                except ValueError:
                    priority = 5
                try:
                    volume = int(row.get("volume", 0) or 0)
                except ValueError:
                    volume = 0

                # collect competitor data already in CSV
                competitors = []
                for i in range(1, 4):
                    url_key = f"Ссылка конкурента {i}"
                    title_key = f"Заголовок конкурента {i}"
                    snippet_key = f"Сниппет конкурента {i}"
                    url = row.get(url_key, "").strip()
                    if url:
                        competitors.append({
                            "url": url,
                            "title": row.get(title_key, "").strip(),
                            "snippet": row.get(snippet_key, "").strip(),
                        })

                candidates.append({
                    "keyword": keyword,
                    "category": category,
                    "content_dir": CATEGORY_DIR_MAP.get(category, "blog"),
                    "slug": slugify(keyword),
                    "volume": volume,
                    "priority": priority,
                    "kd": row.get("kd", ""),
                    "intent": row.get("intent", ""),
                    "seed": row.get("seed", ""),
                    "competitors": competitors,
                    "csv_path": str(own_csv),
                    "csv_keyword": keyword,
                })

    if not candidates:
        return None

    # weight = priority (lower = more important) inverted * log(volume+1)
    import math
    weights = []
    for c in candidates:
        w = (10 - c["priority"]) * math.log(c["volume"] + 2)
        weights.append(max(w, 0.1))

    chosen = random.choices(candidates, weights=weights, k=1)[0]
    return chosen


def mark_as_published(csv_path: str, keyword: str) -> None:
    """Write today's date into the 'published' column for this keyword."""
    today = date.today().isoformat()
    rows = []
    fieldnames = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            if row.get("keyword", "").strip() == keyword:
                row["published"] = today
            rows.append(row)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pick_keyword_from_topic(topic: str) -> dict | None:
    """Pick a random unused keyword from a specific topic folder."""
    import math
    category_folder = KEYWORDS_DIR / topic
    own_csv = category_folder / "own.csv"
    if not own_csv.exists():
        return None

    candidates = []
    with open(own_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            keyword = row.get("keyword", "").strip()
            if not keyword or row.get("published", "").strip():
                continue
            try:
                priority = int(row.get("priority", 5) or 5)
            except ValueError:
                priority = 5
            try:
                volume = int(row.get("volume", 0) or 0)
            except ValueError:
                volume = 0

            competitors = []
            for i in range(1, 4):
                url = row.get(f"Ссылка конкурента {i}", "").strip()
                if url:
                    competitors.append({
                        "url": url,
                        "title": row.get(f"Заголовок конкурента {i}", "").strip(),
                        "snippet": row.get(f"Сниппет конкурента {i}", "").strip(),
                    })

            candidates.append({
                "keyword": keyword,
                "category": topic,
                "content_dir": CATEGORY_DIR_MAP.get(topic, "blog"),
                "slug": slugify(keyword),
                "volume": volume,
                "priority": priority,
                "kd": row.get("kd", ""),
                "intent": row.get("intent", ""),
                "seed": row.get("seed", ""),
                "competitors": competitors,
                "csv_path": str(own_csv),
                "csv_keyword": keyword,
            })

    if not candidates:
        return None

    weights = [max((10 - c["priority"]) * math.log(c["volume"] + 2), 0.1) for c in candidates]
    return random.choices(candidates, weights=weights, k=1)[0]


def run_for_topic(topic: str) -> dict | None:
    """Run research for a specific topic folder."""
    result = pick_keyword_from_topic(topic)
    if not result:
        return None
    return _enrich(result)


def run() -> dict:
    result = pick_keyword()
    if not result:
        print("No unused keywords found.", file=sys.stderr)
        sys.exit(1)

    return _enrich(result)


def _enrich(result: dict) -> dict:
    """Add LSI keywords and date to a keyword dict."""
    questions_csv = Path(result["csv_path"]).parent / "questions.csv"
    lsi_keywords = []
    if questions_csv.exists():
        with open(questions_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 20:
                    break
                q = row.get("keyword", row.get("question", "")).strip()
                if q:
                    lsi_keywords.append(q)

    result["lsi_keywords"] = lsi_keywords[:15]
    result["today"] = date.today().isoformat()
    result["utm_campaign"] = result.get("slug", "borchani")

    print(f"[Agent 1] Picked: {result['keyword']} (category: {result['category']}, vol: {result['volume']})")
    return result


if __name__ == "__main__":
    data = run()
    print(json.dumps(data, ensure_ascii=False, indent=2))
