# 🤖 AI ニュース自動収集・要約 プロトタイプ

最新のAI関連ニュースをRSSから自動取得し、AI（Gemini API）で要約・カテゴリ分類を行い、配信用のMarkdown / JSON / HTMLを自動生成するプロトタイプです。

---

## 📁 ディレクトリ構成

- `main.py` : 収集から要約・出力までを一括実行するメインスクリプト
- `collector.py` : RSSフィード（ITmedia AI+、Zenn、Google News等）から記事を自動収集・重複排除
- `summarizer.py` : Gemini APIによる3行要約とカテゴリ分類（APIキー未設定時はデモモードで動作）
- `exporter.py` : Markdown / JSON / HTML（Webページ）への書き出し
- `config.py` : 取得元RSSや件数の設定
- `data/` : 出力結果（`index.html`、`digest_YYYY-MM-DD.md`、`digest_YYYY-MM-DD.json`）
- `.env.example` : 環境変数サンプル

---

## 🚀 使い方

### 1. 実行方法
以下のコマンドを実行すると、最新のニュースを自動取得して要約ファイルを作成します。

```bash
python main.py
```

### 2. Gemini API で本番AI要約を有効にする場合
1. [Google AI Studio](https://aistudio.google.com/) から無料のAPIキーを取得します。
2. プロジェクト直下に `.env` ファイルを作成し、以下を記述します：
   ```env
   GEMINI_API_KEY=あなたのAPIキー
   ```
3. 再度 `python main.py` を実行すると、Geminiによる高精度な3行要約が自動適用されます。

### 3. 生成される配信ファイル
`data/` フォルダ内に以下が出力されます：
- `index.html` : そのままブラウザで閲覧可能なモダンUIのダイジェストページ
- `digest_YYYY-MM-DD.md` : ブログやGitHubなどに投稿できるMarkdown
- `digest_YYYY-MM-DD.json` : Next.js/AstroなどのWebフロントエンドと連携できるJSONデータ
