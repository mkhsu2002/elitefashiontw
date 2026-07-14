# Elite TW momo Daily Brand Article Automation Runbook

建立日期：2026-07-14

本文件供 Codex app cron automation 執行 Elite Fashion TW 的 momo 聯盟品牌每日推薦文章流程。它是內部操作文件；不得把本文件的治理字眼、排程邏輯、品牌池語言或模型流程寫進任何公開 HTML。

## 目標

- 每天最多產出並發布 1 篇 momo 聯盟品牌推薦文章。
- 每篇只聚焦 `automation/reports/elite-tw-momo-top-100-brand-daily-post-queue-2026-07-14.csv` 中 1 家 `tracking_status = planned` 的品牌。
- 每篇文章必須符合 `automation/seo-content-execution-rules.md`、`automation/editorial-style-guide.md`、`automation/editorial-review-checklist.md`、`automation/momo-affiliate-content-architecture.md` 與專案 `AGENTS.md`。
- 每週執行一次內容集群治理，避免每日新增文章破壞既有 SEO / GEO / AEO 架構。

## 每日發布前防呆

每日 automation 在建立文章檔前必須完成以下檢查；任一項失敗即停止，不得發布：

1. 確認工作目錄為 `/Users/mkhsu/Documents/FlyPigAI/elitefashiontw`。
2. 讀取專案 `AGENTS.md`、本 runbook、100 天 CSV 佇列、`automation/momo-brand-recommendation-tracker.csv` 與 `automation/momo-affiliate-content-architecture.md`。
3. 從 CSV 佇列選出最前面一筆 `tracking_status = planned` 的品牌；若沒有 planned，記錄 no-op 並結束。
4. 用 `merchant_id` 與品牌名稱回查 tracker：
   - `coverage_status` 必須是 `live`。
   - `recommendation_grade` 必須是 `A+`、`A` 或 `B`。
   - `brand_role` 必須是 `主角候選`、`主推候選` 或 `推薦店家`。
   - `promo_link` 或 `store_link` 至少一個可用。
   - 若 `risk_notes` 指出需查證、暫緩、醫療療效或商品線不明，先暫停該品牌並改處理下一筆 planned。
5. 檢查近 30 天新增文章與 `data/articles-index.json`，不得產出與既有文章高度重疊的搜尋意圖、標題或 FAQ。
6. 檢查所屬分類必須符合既有分類，不新增大分類：
   - `outdoor-mobile-living` -> `outdoor-escapes`
   - `mobile-wardrobe-accessories` -> `casual-chic`
   - `wellness-recovery-support` -> `wellness-movement`
   - `home-ritual-lifestyle`、`daily-food-drink-ritual`、`pet-lifestyle-future`、`family-parenting-future` -> `lifestyle-culture`
   - `creator-work-gear` -> `ai-innovation`
7. 檢查導購文風險：
   - 不得承諾療效、減重、醫療、保健或抗老效果。
   - 不得捏造價格、庫存、折扣、評測、品牌官方說法或實測結果。
   - 不得使用誇張促銷、倒數壓迫、保證成效或網紅式語氣。

## 每日文章生成要求

每篇文章需具備：

- 作者名義為「編輯團隊」。
- 前台標題可加品牌前綴時使用 `Elite Fashion｜`，不得使用 `Elite Fashion TW｜`。
- 開頭先建立讀者問題與判斷框架，再自然進入品牌與商品。
- 至少 2,200 個中文內容字元。
- 至少一段具體的編輯判斷，可是選購順序、台灣情境、常見錯誤、使用頻率或取捨比較。
- FAQ、CTA、導購揭露、重要內鏈與商品資訊必須存在於初始 HTML 可見內容。
- 所有導購連結必須含 `rel="sponsored nofollow"`。
- 文末固定放置可見導購揭露。
- 不得在前台出現「主角品牌、配角品牌、SEO、GEO、AEO、品牌池、矩陣、覆蓋率、批次、排程、prompt、模型、AI 生成流程」等內部語言。
- 使用 Codex 圖片生成功能產生新的封面與 OG/Twitter 圖，尺寸 1200 x 630，保存於 `images/optimized/article-covers/`；圖中不得出現 logo、商標、可讀品牌字樣、水印、簽名、包裝字樣、條碼、QR code 或 UI 文字。

## 每日發布驗證

文章完成後，發布前必須通過：

1. 站內索引、分類頁、搜尋索引、sitemap、feed 與 publish log 已更新。
2. 文章 HTML 有 H1、導言、正文、FAQ、CTA、導購揭露、canonical、OG/Twitter meta、Article schema、BreadcrumbList schema；若有 FAQ，需有 FAQPage schema 且由可見內容支撐。
3. `og:image`、`twitter:image` 與 `Article.image` 指向同一張 1200 x 630 圖。
4. 不得出現 `nosnippet`、`data-nosnippet` 或阻擋摘要的 robots meta。
5. 執行並通過：
   - `python3 scripts/content_pipeline.py sync`
   - `python3 scripts/content_pipeline.py verify`
   - `python3 scripts/content_authenticity_audit.py --latest`
   - `python3 scripts/article_cover_tools.py strict-audit`
6. 發布後需回填：
   - 100 天 CSV 佇列該列 `tracking_status`。
   - `automation/momo-brand-recommendation-tracker.csv` 的文章 slug、live URL、提及次數與最後提及日期。
   - `automation/latest-run.json` 與 `automation/publish-log.json`。
   - Google Sheets `Taiwan` 文章紀錄表，僅在文章已產生 publish log 後同步。

## 每週內容集群治理

每週治理 automation 不直接新增文章，僅做治理、修正與報告：

1. 找出過去 7 天新增或更新的 momo 品牌推薦文章。
2. 按分類、主題群、讀者意圖與品牌角色歸檔。
3. 檢查本週文章彼此，以及與既有文章是否 cannibalize 同一搜尋問題。
4. 檢查 hub / 分類頁 / 延伸閱讀是否需要補內鏈或重排；不得無限制新增 core article。
5. 抽查正式 HTML 的 canonical、OG、Article schema、BreadcrumbList schema、FAQPage schema、圖片 alt、導購揭露與 `rel="sponsored nofollow"`。
6. 必要時更新 `automation/reports/elite-tw-momo-weekly-content-cluster-governance.md`，記錄本週文章、cluster、重疊風險、內鏈調整、下週內容缺口與暫緩品牌。
7. 治理若需修改公開 HTML 或資料檔，必須重跑每日發布驗證中相關命令；檢查失敗不得 commit 或 push。

## 發布與停止條件

- 使用者已要求建立每日自動化生成流程；每日 automation 在所有防呆與驗證通過後，可將本次文章相關檔案 commit 並 push 到 `main`。
- 嚴禁 destructive git 指令、hard push、覆蓋使用者未確認的無關變更或提交 secret。
- 若遇到 merge conflict、測試失敗、疑似 secret、Google Sheets 同步失敗、圖片生成失敗、導購連結失效、文章品質不達標或正式後端/資料契約不同步，必須停止並回報阻塞原因。
