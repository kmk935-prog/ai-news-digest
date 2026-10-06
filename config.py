import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# RSS Feeds configuration
# enabled: True/False で個別にオン/オフ切り替え可能
RSS_FEEDS = [
    # --- 🌍 海外最新AIトレンド（英語 -> 日本語要約） ---
    {
        "name": "TechCrunch AI",
        "category": "海外トレンド・速報",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "enabled": True,
        "max_items": 3
    },
    {
        "name": "The Verge AI",
        "category": "海外トレンド・速報",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "enabled": True,
        "max_items": 3
    },

    # --- 🛠️ 開発・技術・エンジニアリング ---
    {
        "name": "Zenn (AIトピック)",
        "category": "開発・技術",
        "url": "https://zenn.dev/topics/ai/feed",
        "enabled": True,
        "max_items": 3
    },
    {
        "name": "Qiita (AIタグ)",
        "category": "開発・技術",
        "url": "https://qiita.com/tags/ai/feed",
        "enabled": True,
        "max_items": 2
    },
    {
        "name": "はてなブックマーク (AI関連人気)",
        "category": "開発・技術",
        "url": "https://b.hatena.ne.jp/q/AI?mode=rss&sort=recent",
        "enabled": True,
        "max_items": 3
    },

    # --- 💼 国内ビジネス・導入事例・プレスリリース ---
    {
        "name": "ITmedia AI+",
        "category": "ビジネス・導入",
        "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
        "enabled": True,
        "max_items": 3
    },
    {
        "name": "PR TIMES (生成AIプレスリリース)",
        "category": "ビジネス・導入",
        "url": "https://news.google.com/rss/search?q=%E7%94%9F%E6%88%90AI+site:prtimes.jp&hl=ja&gl=JP&ceid=JP:ja",
        "enabled": True,
        "max_items": 3
    },

    # --- 🌐 総合トレンド ---
    {
        "name": "Google News (AI総合)",
        "category": "総合トレンド",
        "url": "https://news.google.com/rss/search?q=%E7%94%9F%E6%88%90AI+OR+%E4%BA%BA%E5%B7%A5%E7%9F%A5%E8%83%BD&hl=ja&gl=JP&ceid=JP:ja",
        "enabled": True,
        "max_items": 3
    }
]

# ダイジェストに含める合計最大記事数（重要記事に厳選）
MAX_TOTAL_ITEMS_TO_SUMMARIZE = 8

# 出力先ディレクトリ
OUTPUT_DIR = "data"
