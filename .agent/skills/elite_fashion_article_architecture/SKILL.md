---
name: elite_fashion_article_architecture
description: Audit or modify Elite Fashion TW article hub assignments, stable topic categories, breadcrumbs, related reading, category pages, and SEO information architecture.
---

# Elite Fashion 文章資訊架構 Skill

## 使用時機

- 使用者要求檢查文章是否掛在適當分類、hub、breadcrumb 或延伸閱讀。
- 需要調整 `primaryHub`、`secondaryHubs`、`topicCategory`、category hub 或 cornerstone hub。
- 需要避免分類膨脹、孤兒文章、hub 核心文章過多或 schema breadcrumb 不一致。

## 核心規則

- 每篇文章只能有 1 個 `primaryHub`。
- 每篇文章可有 0 到 2 個 `secondaryHubs`。
- Article breadcrumb 使用 `primaryHub`：首頁 → primary hub → article。
- `secondaryHubs` 只在文章頁延伸閱讀顯示，不要寫進 breadcrumb。
- 每個 hub 頁只顯示 8 到 12 篇 cornerstone / cluster 核心文章。
- 站內穩定細分類維持 16 到 24 個，由 `scripts/article_taxonomy.py` 管理。
- 不因新文章或舊目錄名稱新增臨時分類；舊目錄要映射到穩定分類。

## 操作順序

1. 讀 `scripts/article_taxonomy.py`，確認 hub 與 stable topic category 的單一來源。
2. 讀 `automation/site-config.json`，確認大分類仍是正式站點分類。
3. 若修改規則，同步更新：
   - `scripts/article_taxonomy.py`
   - `scripts/content_pipeline.py`
   - `scripts/seo_site_maintenance.py`
   - 必要時更新 `.agent/skills/create_elite_article/SKILL.md`
4. 執行 `python3 scripts/content_pipeline.py sync` 重新產生索引與頁面。
5. 驗證文章索引：
   - 每篇有有效 `primaryHub`
   - `secondaryHubs` 數量不超過 2
   - `topicCategory` 在穩定分類清單內
   - 每個 hub 核心文章數為 8 到 12
6. 驗證 sitemap、feed、schema 與測試。

## 前台文字限制

前台可使用「主題策展」「延伸主題」「相關文章」「分類總覽」。不要在前台使用 `primaryHub`、`secondaryHubs`、`cluster`、`taxonomy`、`SEO`、`矩陣`、`批次` 等內部語言。
