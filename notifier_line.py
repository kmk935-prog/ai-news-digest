import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_USER_ID = os.getenv("LINE_USER_ID", "")

def send_line_notification(articles: list[dict], date_str: str) -> bool:
    """Send summary notification to LINE using LINE Messaging API."""
    if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_USER_ID:
        print("ℹ️ [LINE通知] LINE_CHANNEL_ACCESS_TOKEN または LINE_USER_ID が未設定のためスキップします。")
        return False

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }

    # Top 3 or 5 articles for preview
    top_articles = articles[:3]
    article_lines = []
    for i, a in enumerate(top_articles, 1):
        title = a.get("title_ja", a.get("title", ""))
        cat = a.get("category", "")
        article_lines.append(f"{i}. [{cat}] {title}")

    message_text = f"""🤖 本日のAIニュース速報 ({date_str})

【本日の注目ピックアップ】
{chr(10).join(article_lines)}

▼ 全{len(articles)}件の要約と詳細はこちら！
https://kmk935-prog.github.io/ai-news-digest/
"""

    payload = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message_text.strip()
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print("📱 [LINE通知] 送信に成功しました！")
            return True
        else:
            print(f"⚠️ [LINE通知] 送信失敗 (Status: {response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ [LINE通知] エラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    test_articles = [
        {"title_ja": "OpenAI、次世代推論モデルを発表", "category": "LLM・生成AI"},
        {"title_ja": "Google、Pixelに新AI機能を搭載", "category": "国内テック・話題"},
        {"title_ja": "行政DXでの生成AI活用事例", "category": "ビジネス・導入"}
    ]
    send_line_notification(test_articles, "2026-10-07")
