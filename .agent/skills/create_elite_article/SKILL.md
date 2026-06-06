---
name: create_elite_article
description: Create, edit, or review Elite Fashion TW articles with the project's Traditional Chinese editorial voice, article taxonomy, hub assignments, affiliate disclosure, and SEO/schema requirements.
---

# Elite Fashion 文章產製 Skill

## 使用時機

- 新增、改寫、審核或批次產生 Elite Fashion TW 文章。
- 調整文章分類、hub 歸屬、內鏈、FAQ、導購揭露、封面或 schema。
- 檢查文章是否符合專案 AGENTS 與 `automation/seo-content-execution-rules.md`。

## 必讀檔案

先讀這些專案檔，避免寫出與現行流程衝突的內容：

- `AGENTS.md`
- `automation/seo-content-execution-rules.md`
- `automation/editorial-style-guide.md`
- `automation/momo-affiliate-content-architecture.md`（只有 momo 聯盟文章需要）
- `automation/momo-brand-recommendation-tracker.csv`（只有 momo 聯盟文章需要）
- `scripts/article_taxonomy.py`

## 文章資訊架構

- 每篇文章必須有且只能有 1 個 `primaryHub`。
- 每篇文章可有 0 到 2 個 `secondaryHubs`，不可與 `primaryHub` 重複。
- 文章 breadcrumb 使用 `primaryHub`，不是只使用大分類。
- `secondaryHubs` 只作為延伸主題閱讀，不要在前台使用「secondaryHub」這種內部字。
- 每個 cornerstone hub 頁只顯示 8 到 12 篇核心文章；核心清單由 `scripts/article_taxonomy.py` 的 `CORE_HUB_LINKS` 管理。
- 穩定細分類使用 `topicCategory` / `topicCategoryLabel`，數量維持 16 到 24 個；不要因單篇文章新增臨時分類。
- 大分類仍沿用 `automation/site-config.json` 的既有分類；除非使用者明確要求，不新增大分類頁。

## 內容規則

- 全文繁體中文，語氣像雜誌編輯團隊，不暴露 AI、prompt、SEO、批次、品牌池、矩陣、導流等內部語言。
- 文章需先有雜誌式引言與讀者問題框架，再進入商品、品牌或工具。
- 每篇文章需有具體判斷段落，例如台灣情境、使用頻率、取捨順序、常見錯誤或選購順序。
- FAQ、CTA、重要內鏈與導購揭露必須存在於初始 HTML，不可只靠 JavaScript 載入。
- 涉及健康、睡眠、食品、護具、照護、美容成分或身體不適時，不承諾療效、減重、保健或抗老效果。
- 若含導購連結，正文最末端必須有可見導購揭露，連結使用 `rel="sponsored nofollow"`。

## 產出與驗證

完成文章或分類/hub 調整後，至少執行：

```bash
python3 scripts/content_pipeline.py sync
python3 -m py_compile scripts/content_pipeline.py scripts/seo_site_maintenance.py scripts/article_taxonomy.py generate_sitemap.py
python3 -m unittest discover tests
```

若變更 sitemap/feed/schema，再檢查 `sitemap.xml`、`feed.xml`、`rss.xml` 可被 XML parser 解析。

不要自動 commit / push；只有使用者明確要求發布或推送時才執行。
