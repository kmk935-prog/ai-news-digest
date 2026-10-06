import os
import json
import html
from datetime import datetime

CATEGORY_COLORS = {
    "海外トレンド・速報": {
        "badge_bg": "bg-purple-100 dark:bg-purple-900/50",
        "badge_text": "text-purple-700 dark:text-purple-300",
        "border": "border-purple-200 dark:border-purple-800/50"
    },
    "開発・技術": {
        "badge_bg": "bg-emerald-100 dark:bg-emerald-900/50",
        "badge_text": "text-emerald-700 dark:text-emerald-300",
        "border": "border-emerald-200 dark:border-emerald-800/50"
    },
    "ビジネス・導入": {
        "badge_bg": "bg-blue-100 dark:bg-blue-900/50",
        "badge_text": "text-blue-700 dark:text-blue-300",
        "border": "border-blue-200 dark:border-blue-800/50"
    },
    "セキュリティ・倫理": {
        "badge_bg": "bg-rose-100 dark:bg-rose-900/50",
        "badge_text": "text-rose-700 dark:text-rose-300",
        "border": "border-rose-200 dark:border-rose-800/50"
    },
    "LLM・生成AI": {
        "badge_bg": "bg-indigo-100 dark:bg-indigo-900/50",
        "badge_text": "text-indigo-700 dark:text-indigo-300",
        "border": "border-indigo-200 dark:border-indigo-800/50"
    },
    "総合トレンド": {
        "badge_bg": "bg-amber-100 dark:bg-amber-900/50",
        "badge_text": "text-amber-700 dark:text-amber-300",
        "border": "border-amber-200 dark:border-amber-800/50"
    }
}

DEFAULT_COLOR = {
    "badge_bg": "bg-slate-100 dark:bg-slate-800",
    "badge_text": "text-slate-700 dark:text-slate-300",
    "border": "border-slate-200 dark:border-slate-700"
}

def export_markdown(articles: list[dict], output_path: str, date_str: str) -> None:
    """Export summarized articles to a clean Markdown file."""
    lines = [
        f"# 🤖 AI ニュース・トピック デイリーダイジェスト",
        f"**日付**: {date_str}  |  **記事数**: {len(articles)}件\n",
        "---",
        ""
    ]

    for i, a in enumerate(articles, 1):
        stars = "★" * a.get("importance", 3) + "☆" * (5 - a.get("importance", 3))
        lines.append(f"## {i}. {a.get('title_ja', a['title'])}")
        lines.append(f"- **カテゴリ**: `{a.get('category', 'AI')}` | **情報元**: [{a['source']}]({a['url']}) | **重要度**: {stars}")
        lines.append(f"- **配信日時**: {a.get('published', 'N/A')}\n")
        lines.append("**【要約ポイント】**")
        for pt in a.get("points", []):
            lines.append(f"- {pt}")
        lines.append(f"\n🔗 [元記事を読む]({a['url']})\n")
        lines.append("---")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[Markdown] 出力完了: {output_path}")

def export_json(articles: list[dict], output_path: str, date_str: str) -> None:
    """Export summarized articles to JSON for web frontends."""
    data = {
        "date": date_str,
        "updated_at": datetime.now().isoformat(),
        "total_count": len(articles),
        "articles": articles
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[JSON] 出力完了: {output_path}")

def export_html(articles: list[dict], output_path: str, date_str: str) -> None:
    """Export to an ultra-modern, fully responsive (Mobile + PC) web dashboard."""
    
    # Extract unique categories for filter tabs
    categories = sorted(list(set(a.get("category", "その他") for a in articles)))
    
    cards_html = ""
    for i, a in enumerate(articles, 1):
        cat = a.get("category", "総合トレンド")
        theme = CATEGORY_COLORS.get(cat, DEFAULT_COLOR)
        importance = a.get("importance", 3)
        stars_html = "".join([f"<span class='text-amber-400'>★</span>" for _ in range(importance)]) + \
                     "".join([f"<span class='text-slate-300 dark:text-slate-600'>★</span>" for _ in range(5 - importance)])
        
        points = a.get("points", [])
        points_html = ""
        for idx, pt in enumerate(points):
            points_html += f"""
            <li class="flex items-start text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                <span class="inline-flex items-center justify-center w-5 h-5 mr-2.5 mt-0.5 rounded-full bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 text-xs font-bold shrink-0">
                    {idx + 1}
                </span>
                <span>{html.escape(pt)}</span>
            </li>
            """

        title_ja = html.escape(a.get('title_ja', a['title']))
        source = html.escape(a.get('source', 'Web'))
        pub_date = html.escape(a.get('published', '')[:25])
        article_url = a.get('url', '#')

        cards_html += f"""
        <article class="article-card group bg-white dark:bg-slate-800/90 rounded-2xl p-5 sm:p-6 shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-200/80 dark:border-slate-700/80 flex flex-col justify-between"
                 data-category="{html.escape(cat)}"
                 data-title="{title_ja.lower()}"
                 data-content="{' '.join(html.escape(p).lower() for p in points)}">
            <div>
                <!-- Top metadata row -->
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold tracking-wide {theme['badge_bg']} {theme['badge_text']}">
                        {html.escape(cat)}
                    </span>
                    <div class="flex items-center gap-1.5 text-xs bg-slate-50 dark:bg-slate-900/50 px-2.5 py-1 rounded-full border border-slate-200/50 dark:border-slate-700/50">
                        <span class="text-slate-500 dark:text-slate-400 font-medium">注目度</span>
                        <div class="flex tracking-tight text-xs">{stars_html}</div>
                    </div>
                </div>

                <!-- Title -->
                <h3 class="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-snug mb-3 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    <a href="{article_url}" target="_blank" rel="noopener noreferrer">
                        {title_ja}
                    </a>
                </h3>

                <!-- Source & Date -->
                <div class="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-4 pb-3 border-b border-slate-100 dark:border-slate-700/50">
                    <span class="inline-flex items-center font-medium px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700/60 text-slate-700 dark:text-slate-300">
                        {source}
                    </span>
                    <span class="truncate">{pub_date}</span>
                </div>

                <!-- 3-point summary box -->
                <div class="bg-slate-50/80 dark:bg-slate-900/60 rounded-xl p-3.5 sm:p-4 mb-4 border border-slate-100 dark:border-slate-800">
                    <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2.5 flex items-center gap-1.5">
                        <svg class="w-3.5 h-3.5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                        3行要約ダイジェスト
                    </div>
                    <ul class="space-y-2">
                        {points_html}
                    </ul>
                </div>
            </div>

            <!-- Footer actions -->
            <div class="pt-2 flex items-center justify-between border-t border-slate-100 dark:border-slate-700/40 mt-auto">
                <a href="{article_url}" target="_blank" rel="noopener noreferrer" 
                   class="inline-flex items-center gap-1.5 text-xs sm:text-sm font-semibold text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 transition group-hover:translate-x-0.5 transform">
                    元記事を読む
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                </a>
                <button onclick="copyArticle(this, '{title_ja}', '{article_url}')"
                        class="inline-flex items-center gap-1 text-xs text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 px-2 py-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700/60 transition"
                        title="タイトルとURLをコピー">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                    <span>コピー</span>
                </button>
            </div>
        </article>
        """

    # Category pills
    cat_pills = f"""
    <button onclick="filterCategory('all', this)" class="cat-pill active px-3.5 py-1.5 rounded-full text-xs sm:text-sm font-bold transition whitespace-nowrap bg-blue-600 text-white shadow-sm">
        すべて ({len(articles)})
    </button>
    """
    for cat in categories:
        count = sum(1 for a in articles if a.get("category") == cat)
        cat_pills += f"""
        <button onclick="filterCategory('{html.escape(cat)}', this)" class="cat-pill px-3.5 py-1.5 rounded-full text-xs sm:text-sm font-medium transition whitespace-nowrap bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:border-blue-500 dark:hover:border-blue-400">
            {html.escape(cat)} ({count})
        </button>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="ja" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>AI Daily Digest | {date_str}</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Hiragino Sans"', '"Meiryo"', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>
    <style>
        /* Smooth touch scrolling on mobile */
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 min-h-screen flex flex-col antialiased transition-colors duration-200 selection:bg-blue-500 selection:text-white">

    <!-- Top Sticky Header -->
    <header class="sticky top-0 z-40 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
            
            <!-- Logo & Brand -->
            <div class="flex items-center gap-3 shrink-0">
                <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
                    <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                </div>
                <div>
                    <h1 class="text-base sm:text-lg font-black tracking-tight leading-none text-slate-900 dark:text-white">
                        AI Daily Digest
                    </h1>
                    <span class="text-[10px] sm:text-xs text-slate-500 dark:text-slate-400 font-medium">毎日朝の自動キュレーション</span>
                </div>
            </div>

            <!-- Controls (Search + Theme toggle) -->
            <div class="flex items-center gap-2 sm:gap-3">
                <!-- Search input (Desktop) -->
                <div class="relative hidden sm:block w-48 md:w-64">
                    <input type="text" id="searchInputDesktop" oninput="handleSearch(this.value)" placeholder="キーワード検索..." 
                           class="w-full pl-8 pr-3 py-1.5 text-xs rounded-full bg-slate-100 dark:bg-slate-800 border border-transparent focus:border-blue-500 dark:focus:border-blue-400 focus:bg-white dark:focus:bg-slate-900 outline-none transition text-slate-900 dark:text-white">
                    <svg class="w-4 h-4 text-slate-400 absolute left-2.5 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>

                <!-- Theme Toggle Button -->
                <button onclick="toggleDarkMode()" id="themeBtn" aria-label="テーマ切り替え"
                        class="w-9 h-9 rounded-xl flex items-center justify-center bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition text-slate-600 dark:text-slate-300">
                    <!-- Sun / Moon icons handled by JS -->
                    <span id="themeIcon">🌙</span>
                </button>
            </div>
        </div>

        <!-- Search input (Mobile only) -->
        <div class="sm:hidden px-4 pb-3 pt-1">
            <div class="relative w-full">
                <input type="text" id="searchInputMobile" oninput="handleSearch(this.value)" placeholder="キーワードで記事を検索..." 
                       class="w-full pl-8 pr-3 py-1.5 text-xs rounded-xl bg-slate-100 dark:bg-slate-800 border border-transparent focus:border-blue-500 focus:bg-white dark:focus:bg-slate-900 outline-none text-slate-900 dark:text-white">
                <svg class="w-4 h-4 text-slate-400 absolute left-2.5 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 flex-1 w-full">
        
        <!-- Hero Header -->
        <div class="mb-6 sm:mb-8 text-center sm:text-left flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-slate-200/80 dark:border-slate-800 pb-6">
            <div>
                <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200/60 dark:border-emerald-800/60 text-emerald-700 dark:text-emerald-300 text-xs font-bold mb-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
                    本日の最新AIニュース
                </div>
                <h2 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
                    {date_str} ダイジェスト
                </h2>
                <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
                    世界のAIトレンド・論文・ビジネス導入動向をGeminiが毎朝3行で要約
                </p>
            </div>

            <!-- Stats Badge -->
            <div class="flex items-center justify-center sm:justify-end gap-2 text-xs">
                <span class="px-3 py-1.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 font-semibold shadow-sm">
                    厳選 <strong class="text-blue-600 dark:text-blue-400 font-extrabold text-sm">{len(articles)}</strong> 件
                </span>
                <span class="px-3 py-1.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 shadow-sm">
                    更新: {datetime.now().strftime('%H:%M')}
                </span>
            </div>
        </div>

        <!-- Filter Pills (Horizontal Scroll on Mobile) -->
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-3 mb-6 -mx-4 px-4 sm:mx-0 sm:px-0">
            {cat_pills}
        </div>

        <!-- Zero results message -->
        <div id="noResults" class="hidden text-center py-16">
            <p class="text-4xl mb-3">🔍</p>
            <p class="text-base font-bold text-slate-700 dark:text-slate-300">該当する記事が見つかりませんでした</p>
            <p class="text-xs text-slate-500 mt-1">検索キーワードを変更するか、フィルターをリセットしてください</p>
            <button onclick="resetFilters()" class="mt-4 px-4 py-2 rounded-xl bg-blue-600 text-white text-xs font-bold shadow hover:bg-blue-700 transition">
                フィルターをクリア
            </button>
        </div>

        <!-- Article Grid (Responsive: 1 col on mobile, 2 cols on tablet, 3 cols on large PC) -->
        <div id="articlesGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
            {cards_html}
        </div>
    </main>

    <!-- Scroll to Top Floating Button -->
    <button onclick="window.scrollTo({{ top: 0, behavior: 'smooth' }})" id="scrollTopBtn"
            class="fixed bottom-6 right-6 w-11 h-11 rounded-full bg-blue-600 hover:bg-blue-700 text-white shadow-lg flex items-center justify-center opacity-0 pointer-events-none transition-all duration-300 z-30">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18"></path></svg>
    </button>

    <!-- Footer -->
    <footer class="bg-white dark:bg-slate-900 border-t border-slate-200/80 dark:border-slate-800 py-8 px-4 text-center text-xs text-slate-500 dark:text-slate-400">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <p>© {date_str[:4]} AI Daily Pulse. Automated with Google Gemini & Python.</p>
            <div class="flex items-center gap-4 text-slate-400">
                <span>ITmedia</span>
                <span>•</span>
                <span>Zenn</span>
                <span>•</span>
                <span>TechCrunch</span>
                <span>•</span>
                <span>The Verge</span>
            </div>
        </div>
    </footer>

    <!-- Interactive Scripts -->
    <script>
        // Dark Mode Logic
        function initTheme() {{
            const saved = localStorage.getItem('theme');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (saved === 'dark' || (!saved && prefersDark)) {{
                document.documentElement.classList.add('dark');
                document.getElementById('themeIcon').textContent = '☀️';
            }} else {{
                document.documentElement.classList.remove('dark');
                document.getElementById('themeIcon').textContent = '🌙';
            }}
        }}

        function toggleDarkMode() {{
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            document.getElementById('themeIcon').textContent = isDark ? '☀️' : '🌙';
        }}

        initTheme();

        // Filter and Search Logic
        let currentCategory = 'all';
        let searchQuery = '';

        function filterCategory(cat, btn) {{
            currentCategory = cat;
            
            // Update button styles
            document.querySelectorAll('.cat-pill').forEach(b => {{
                b.classList.remove('active', 'bg-blue-600', 'text-white', 'shadow-sm');
                b.classList.add('bg-white', 'dark:bg-slate-800', 'text-slate-600', 'dark:text-slate-300', 'border');
            }});
            btn.classList.add('active', 'bg-blue-600', 'text-white', 'shadow-sm');
            btn.classList.remove('bg-white', 'dark:bg-slate-800', 'text-slate-600', 'dark:text-slate-300', 'border');

            applyFilters();
        }}

        function handleSearch(query) {{
            searchQuery = query.toLowerCase().trim();
            // Sync desktop and mobile search inputs
            const dInput = document.getElementById('searchInputDesktop');
            const mInput = document.getElementById('searchInputMobile');
            if (dInput && dInput.value !== query) dInput.value = query;
            if (mInput && mInput.value !== query) mInput.value = query;
            applyFilters();
        }}

        function applyFilters() {{
            const cards = document.querySelectorAll('.article-card');
            let visibleCount = 0;

            cards.forEach(card => {{
                const cardCat = card.getAttribute('data-category');
                const cardTitle = card.getAttribute('data-title');
                const cardContent = card.getAttribute('data-content');

                const matchesCat = (currentCategory === 'all' || cardCat === currentCategory);
                const matchesSearch = !searchQuery || cardTitle.includes(searchQuery) || cardContent.includes(searchQuery);

                if (matchesCat && matchesSearch) {{
                    card.classList.remove('hidden');
                    visibleCount++;
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            const noRes = document.getElementById('noResults');
            if (visibleCount === 0) {{
                noRes.classList.remove('hidden');
            }} else {{
                noRes.classList.add('hidden');
            }}
        }}

        function resetFilters() {{
            searchQuery = '';
            const dInput = document.getElementById('searchInputDesktop');
            const mInput = document.getElementById('searchInputMobile');
            if (dInput) dInput.value = '';
            if (mInput) mInput.value = '';
            const allBtn = document.querySelector('.cat-pill');
            if (allBtn) filterCategory('all', allBtn);
        }}

        // Copy Article Link
        function copyArticle(btn, title, url) {{
            const text = `${{title}}\\n${{url}}`;
            navigator.clipboard.writeText(text).then(() => {{
                const span = btn.querySelector('span');
                const original = span.textContent;
                span.textContent = '完了!';
                btn.classList.add('text-emerald-600', 'dark:text-emerald-400');
                setTimeout(() => {{
                    span.textContent = original;
                    btn.classList.remove('text-emerald-600', 'dark:text-emerald-400');
                }}, 2000);
            }});
        }}

        // Scroll to Top visibility
        window.addEventListener('scroll', () => {{
            const btn = document.getElementById('scrollTopBtn');
            if (window.scrollY > 300) {{
                btn.classList.remove('opacity-0', 'pointer-events-none');
                btn.classList.add('opacity-100');
            }} else {{
                btn.classList.add('opacity-0', 'pointer-events-none');
                btn.classList.remove('opacity-100');
            }}
        }});
    </script>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[HTML] レスポンシブHTML出力完了: {output_path}")
