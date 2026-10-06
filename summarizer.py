import json
import time
import re
import sys
import truststore
truststore.inject_into_ssl()

from config import GEMINI_API_KEY, OPENAI_API_KEY

CANDIDATE_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-flash-latest"
]

def summarize_with_gemini(articles: list[dict]) -> list[dict]:
    """Summarize articles using Google Gemini API with model fallback."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""あなたはAI専門のキュレーター兼リサーチャーです。
以下の{len(articles)}件のAI関連ニュースを読み、日本の読者がサッと理解できるように、魅力的な日本語ダイジェストを作成してください。

【重要な要件】:
1. 英語の記事（TechCrunch, The Vergeなど）は、**必ず自然で分かりやすい日本語のタイトルに翻訳**してください。
2. 要約の3行箇条書き（points）は以下のように構成してください：
   - 1行目: 何が発表・発生したか（ファクト）
   - 2行目: 技術的・ビジネス的な特徴や背景
   - 3行目: 今後の影響、読者が注目すべきポイント
3. カテゴリは内容に応じて適切に分類してください（"海外トレンド・速報", "開発・技術", "ビジネス・導入", "セキュリティ・倫理", "LLM・生成AI" 等）。
4. 重要度（importance）は 1〜5 の整数で評価してください。

出力形式は必ず有効なJSON配列形式（```json ... ``` または純粋なJSON配列）にしてください。
各要素のキー:
- "index": 入力の番号(0始まりの整数)
- "title_ja": 日本語タイトル
- "points": [要約の箇条書き3行]
- "category": カテゴリ名
- "importance": 1〜5の整数

【記事一覧】:
"""
    for i, a in enumerate(articles):
        prompt += f"\n--- 記事 {i} ---\nタイトル: {a['title']}\n情報元: {a['source']} (初期カテゴリ: {a.get('category')})\n概要: {a['summary_raw'][:400]}\n"

    for model_name in CANDIDATE_MODELS:
        try:
            print(f"🤖 モデル [{model_name}] を呼び出し中...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            content_text = response.text.strip()
            # Clean markdown codeblocks if wrapped
            if content_text.startswith("```json"):
                content_text = content_text[7:]
            if content_text.startswith("```"):
                content_text = content_text[3:]
            if content_text.endswith("```"):
                content_text = content_text[:-3]
            content_text = content_text.strip()

            data = json.loads(content_text)
            
            # Merge back into articles
            for item in data:
                idx = item.get("index")
                if idx is not None and 0 <= idx < len(articles):
                    articles[idx]["title_ja"] = item.get("title_ja", articles[idx]["title"])
                    articles[idx]["points"] = item.get("points", [])
                    articles[idx]["category"] = item.get("category", articles[idx]["category"])
                    articles[idx]["importance"] = item.get("importance", 3)
            print(f"✨ Gemini [{model_name}] による要約が正常に完了しました！")
            return articles
        except Exception as e:
            print(f"モデル [{model_name}] でのエラー: {e}")
            time.sleep(1)

    print("すべてのGeminiモデル呼び出しが失敗したため、デモモードに切り替えます。")
    return mock_summarize(articles)

def mock_summarize(articles: list[dict]) -> list[dict]:
    """Fallback mock summarizer when API call fails."""
    print("💡 [デモモード] デモ要約エンジンを使用します。")
    
    for a in articles:
        is_english = any(ord(c) < 128 for c in a["title"][:20]) and not any(ord(c) > 0x3000 for c in a["title"])
        if is_english:
            a["title_ja"] = f"【海外速報】{a['title']}"
            a["points"] = [
                f"海外メディア「{a['source']}」が報じた最新トピック。",
                "最新のモデル動向やグローバルなAIサービス展開に関するニュースです。",
                "日本国内のAIエコシステムや開発環境にも波及する可能性があり注目されます。"
            ]
        else:
            a["title_ja"] = a["title"]
            a["points"] = [
                f"「{a['title']}」に関する最新ニュース。",
                f"{a['source']} より配信。記事本文よりトピックを抽出しています。",
                "AIの最新トレンドや実用化動向として要注目のトピックです。"
            ]
        a["importance"] = 4
        
    return articles

def summarize_articles(articles: list[dict]) -> list[dict]:
    """Entry point for summarization. Routes to Gemini if configured, else mock."""
    if not articles:
        return []
        
    if GEMINI_API_KEY:
        print("🤖 Gemini APIを使用してニュースを要約中...")
        return summarize_with_gemini(articles)
    else:
        return mock_summarize(articles)
