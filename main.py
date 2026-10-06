import os
import sys
from datetime import datetime
from config import OUTPUT_DIR, MAX_TOTAL_ITEMS_TO_SUMMARIZE
from collector import fetch_articles
from summarizer import summarize_articles
from exporter import export_markdown, export_json, export_html

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

def run_pipeline():
    print("=" * 60)
    print("🚀 AI ニュースまとめ配信パイプライン 開始")
    print("=" * 60)
    
    # 1. ニュース記事収集
    print("\n[ステップ 1/3] ニュースソースから最新記事を取得中...")
    articles = fetch_articles()
    print(f"-> 有効な記事を {len(articles)} 件取得しました。")

    if not articles:
        print("記事が見つかりませんでした。終了します。")
        return

    # 上位件数に絞り込み
    selected_articles = articles[:MAX_TOTAL_ITEMS_TO_SUMMARIZE]
    print(f"-> 今回のダイジェスト対象: 上位 {len(selected_articles)} 件")

    # 2. 要約生成
    print("\n[ステップ 2/3] AIによる要約・カテゴリ分類を実行中...")
    summarized = summarize_articles(selected_articles)

    # 3. エクスポート
    print("\n[ステップ 3/3] 各種フォーマットで出力中...")
    today_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    md_file = os.path.join(OUTPUT_DIR, f"digest_{today_str}.md")
    json_file = os.path.join(OUTPUT_DIR, f"digest_{today_str}.json")
    html_file = os.path.join(OUTPUT_DIR, "index.html")

    export_markdown(summarized, md_file, today_str)
    export_json(summarized, json_file, today_str)
    export_html(summarized, html_file, today_str)

    print("\n" + "=" * 60)
    print("🎉 処理が完了しました！")
    print(f"- Markdown: {md_file}")
    print(f"- JSON:     {json_file}")
    print(f"- HTML:     {html_file} (ブラウザで開けます)")
    print("=" * 60)

    # コンソール上でのプレビュー表示
    print("\n【本日のおすすめダイジェスト プレビュー】")
    for i, a in enumerate(summarized, 1):
        print(f"\n[{i}] {a.get('title_ja', a['title'])}")
        print(f"    カテゴリ: {a.get('category')} | ソース: {a['source']}")
        for pt in a.get('points', []):
            print(f"    - {pt}")

if __name__ == "__main__":
    run_pipeline()
