"""
Agent 2 — Competitor scraper
Fetches competitor article content from URLs found in research data.
"""
import json
import sys
import time
import re

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BorchaniBot/1.0; +https://borchani.com)",
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = 15


def clean_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(lines)


def extract_headings(soup: BeautifulSoup) -> list[str]:
    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text:
            headings.append(f"{tag.name.upper()}: {text}")
    return headings[:30]


def extract_faq(soup: BeautifulSoup) -> list[str]:
    questions = []
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(strip=True)
        if "?" in text and len(text) < 150:
            questions.append(text)
    return questions[:10]


def scrape_url(url: str) -> dict:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        body_text = clean_text(soup)
        word_count = len(body_text.split())

        headings = extract_headings(soup)
        faq_questions = extract_faq(soup)

        # trim body to ~2000 words to avoid huge context
        words = body_text.split()
        trimmed = " ".join(words[:2000])

        return {
            "url": url,
            "title": title,
            "word_count": word_count,
            "headings": headings,
            "faq_questions": faq_questions,
            "body_excerpt": trimmed,
            "scraped": True,
        }
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "scraped": False,
        }


def run(research_data: dict) -> dict:
    competitors = research_data.get("competitors", [])
    scraped = []

    for i, comp in enumerate(competitors[:3]):
        url = comp.get("url", "")
        if not url:
            continue
        print(f"[Agent 2] Scraping {i+1}/3: {url}")
        result = scrape_url(url)
        # merge original snippet/title
        result["original_title"] = comp.get("title", "")
        result["original_snippet"] = comp.get("snippet", "")
        scraped.append(result)
        if i < 2:
            time.sleep(2)  # polite delay

    research_data["competitor_analysis"] = scraped
    print(f"[Agent 2] Scraped {len([s for s in scraped if s.get('scraped')])} competitor articles")
    return research_data


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    result = run(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
