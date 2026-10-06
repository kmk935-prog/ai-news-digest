import html
import truststore
truststore.inject_into_ssl()

import requests
import feedparser
from bs4 import BeautifulSoup
from config import RSS_FEEDS

def clean_html(raw_html: str) -> str:
    """Remove HTML tags, decode entities, and clean up whitespace."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    text = html.unescape(text)
    return " ".join(text.split())

def fetch_articles() -> list[dict]:
    """Fetch articles from enabled RSS feeds, deduplicate, and return as a list."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-News-Digest-Collector/1.0"
    }
    
    seen_urls = set()
    seen_titles = set()
    articles = []

    for feed_info in RSS_FEEDS:
        if not feed_info.get("enabled", True):
            continue

        name = feed_info["name"]
        url = feed_info["url"]
        category = feed_info.get("category", "AI全般")
        max_items = feed_info.get("max_items", 3)
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            parsed = feedparser.parse(resp.content)
            
            count = 0
            for entry in parsed.entries:
                if count >= max_items:
                    break
                
                title = clean_html(entry.get("title", ""))
                link = entry.get("link", "").strip()
                published = entry.get("published", entry.get("updated", ""))
                summary = clean_html(entry.get("summary", entry.get("description", "")))
                
                # Deduplication check
                if not title or not link:
                    continue
                if link in seen_urls or title in seen_titles:
                    continue
                
                seen_urls.add(link)
                seen_titles.add(title)
                
                articles.append({
                    "title": title,
                    "url": link,
                    "published": published,
                    "source": name,
                    "summary_raw": summary,
                    "category": category
                })
                count += 1
                
        except Exception as e:
            print(f"[{name}] 取得エラー: {e}")

    return articles

if __name__ == "__main__":
    arts = fetch_articles()
    print(f"合計 {len(arts)} 件の記事を取得しました。")
    for a in arts[:5]:
        print(f"- [{a['category']}] [{a['source']}] {a['title']}")
