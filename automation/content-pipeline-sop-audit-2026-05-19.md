# Elite Fashion TW 文章撰寫與生成機制盤點

盤點日期：2026-05-19

本文記錄目前 `elitefashiontw` 網站的文章撰寫、生成、排程、發布、驗證與後續紀錄 SOP，方便後續追蹤與研讀。

## 一、網站內容產線總覽

這個網站目前不是單純手寫 HTML，而是「靜態站 + 內容自動化流水線」。

文章可以透過三種方式產出：

1. 人工撰寫或人工介入修改 HTML。
2. 自然語言指令觸發單篇或系列規劃。
3. GitHub Actions 排程自動消化 queue，或 queue 為空時從 fallback 題庫選題。

產文完成後，系統會同步更新文章檔、索引、前台列表、搜尋資料、發文紀錄、sitemap、Google Sheets、正式站可讀狀態與電子報寄送。

正式部署鏈路目前記錄為：

```text
GitHub main -> GitHub Pages -> Cloudflare 自訂網域代理 -> https://tw.elitefasion.com
```

## 二、核心 SOP

### 1. 策略與選題

主要依據：

- `automation/content-strategy.md`
- `automation/topic-selection-mechanism.md`
- `automation/editorial-review-checklist.md`
- `automation/topic-backlog.json`
- `automation/life-proposals-pruning-map.md`

網站核心受眾是 40+ 熟齡女性，主軸包含：

- 熟齡人生重整
- 健康恢復與身體節奏
- 日常穿搭與移動衣櫥
- 生活品味與工具化生活
- 戶外與移動場景
- AI 與未來工作
- 時尚與設計趨勢轉譯

目前內容治理方向：

- `lifestyle-culture` 是主核心分類。
- `wellness-movement` 前台定位為「健康恢復」。
- `casual-chic` 聚焦日常穿搭與移動衣櫥。
- `outdoor-escapes` 聚焦熟齡獨旅、輕戶外與長途移動。
- `ai-innovation` 聚焦 45+ 工作者與第二曲線的 AI 採用。
- `runway-trends` 與 `designer-perspective` 採低頻高品質策略。
- `life-proposals` 停止作為新文章分類擴張。
- `high-performance` 不再作獨立新增分類。

### 2. 兩種自然語言入口

使用者或 GitHub Actions 可透過以下格式控制內容系統。

加入主題序列：

```text
加入主題序列：主題，篇數：N，補充：補充方向
```

用途：先規劃一組系列文章，寫入 queue，後續依排程逐篇生成。

直接生成主題：

```text
直接生成主題：主題
```

用途：立即產出單篇文章，不進 queue。

### 3. 主腳本執行

核心腳本：

```text
scripts/content_pipeline.py
```

常用 CLI：

```bash
python3 scripts/content_pipeline.py enqueue --topic "主題" --count 6 --direction "補充方向"
python3 scripts/content_pipeline.py generate-now --topic "單篇主題"
python3 scripts/content_pipeline.py scheduled-run
python3 scripts/content_pipeline.py sync
python3 scripts/content_pipeline.py verify --article-id <article-id>
python3 scripts/content_pipeline.py wait-for-live --article-url <url> --article-title "標題"
python3 scripts/content_pipeline.py send-notification --article-title "標題" --article-url <url>
python3 scripts/content_pipeline.py send-newsletter
```

### 4. 模型與 prompt

系列規劃 prompt：

```text
automation/prompts/series-planner.md
```

文章撰寫 prompt：

```text
automation/prompts/article-writer.md
```

模型設定由 `automation/site-config.json` 與 GitHub Actions 環境變數共同決定。

支援路徑：

- OpenAI Responses API
  - endpoint: `https://api.openai.com/v1/responses`
  - default writer model: `gpt-5-mini`
  - default planner model: `gpt-5-mini`
- NVIDIA chat completions
  - endpoint: `https://integrate.api.nvidia.com/v1/chat/completions`
  - README 記錄正式曾用 `deepseek-ai/deepseek-v4-pro`

若缺少模型 API key，腳本目前會改走內建 fallback template。這有助於本地測試，但正式排程若無意間缺 key，可能產出模板感較重的文章，屬於需注意風險。

## 三、每篇文章生成後會寫入的檔案

每次產文通常會更新：

- 實際文章 HTML，例如 `ai-innovation/xxx.html`
- `automation/articles/*.json`
- `automation/articles/*.md`
- `data/articles-index.json`
- `data/front-listing.json`
- `data/search-index.json`
- `automation/publish-log.json`
- `automation/publish-log.md`
- `automation/topic-queue.json`
- `automation/topic-queue.md`
- `automation/latest-run.json`
- `all-articles.html`
- `search.html`
- `index.html`
- 對應分類頁，例如 `lifestyle-culture.html`
- `sitemap.xml`

文章資料契約在 `automation/site-config.json` 的 `articleContract.requiredFields` 中定義，必要欄位包含：

- `id`
- `title`
- `slug`
- `excerpt`
- `tags`
- `metaTitle`
- `metaDescription`
- `category`
- `series`
- `readTimeMinutes`
- `listingTitle`
- `listingExcerpt`
- `markdownBody`
- `faq`
- `extendedReading`
- `cta`
- `publishedAt`
- `url`
- `file`

## 四、GitHub Actions 發布流程

主要 workflow：

- `.github/workflows/content-scheduler.yml`
- `.github/workflows/content-command.yml`

### 固定排程

`content-scheduler.yml` 會定期執行：

```bash
python3 scripts/content_pipeline.py scheduled-run
```

目前 README 記錄常態排程為每週 4 次：

- `35 19 * * 6`
- `50 19 * * 6`
- `15 2 * * 3`
- `15 2 * * 5`

以溫哥華夏令時間換算：

- 週六 12:35pm
- 週六 12:50pm
- 週二 7:15pm
- 週四 7:15pm

以台灣時間換算：

- 週日 03:35
- 週日 03:50
- 週三 10:15
- 週五 10:15

注意：workflow 裡仍保留 `2026-04-25` 壓測用的日月 cron，但 GitHub cron 不含年份，因此理論上每年 4/25、4/26 仍可能再觸發。

### 手動自然語言指令

`content-command.yml` 透過 `workflow_dispatch` 接收：

- `instruction`
- `fixture`

可用來手動加入 queue 或直接生成文章。

### 發布順序

兩條主要 workflow 大致流程一致：

1. checkout repo。
2. setup Python。
3. install `gspread`。
4. 解析模型 provider。
5. 執行內容生成或指令。
6. 檢查 git diff。
7. 若有變更，commit。
8. push 到 `main`。
9. 等正式站可讀。
10. 寄 Resend 上線通知。
11. 同步 Google Sheets。
12. 發送 newsletter broadcast。

## 五、queue 與 fallback 運作

queue 檔案：

```text
automation/topic-queue.json
automation/topic-queue.md
```

排程執行時：

1. 先讀取 queue。
2. 若有 `planned` item，優先產出該 item。
3. 發布後更新 item 狀態為 `published`。
4. 若整個 series 都完成，series 狀態改為 `completed`。
5. 若 queue 沒有可用 item，才讀 `automation/topic-backlog.json` 做 fallback 選題。

fallback 選題會考量：

- 與既有標題是否重複。
- 是否命中舊公式標題，如「主權協議 / 權威 / 革命」。
- 分類缺口。
- 春夏季節適配度。
- 商業與內連價值。
- evergreen 程度。
- 近期關鍵字是否過度重複。

## 六、驗證機制

`scripts/content_pipeline.py verify` 會檢查：

- 必要檔案是否存在。
- article id 是否重複。
- article url 是否重複。
- article file 是否重複。
- 文章檔是否存在。
- 指定文章是否出現在 `front-listing`。
- 指定文章是否出現在 `search-index`。
- 指定文章是否出現在 `publish-log`。
- `all-articles.html` 是否有最新文章連結。
- 對應分類頁是否有最新文章連結。
- 首頁最新文章區是否有最新文章連結。

`wait-for-live` 會輪詢正式站 URL，確認 HTTP 200 且頁面內容包含文章標題，才視為正式可讀。

## 七、Google Sheets 與電子報

Google Sheets 同步腳本：

```text
scripts/log_article_to_google_sheets.py
```

主要 workflow 目前在發文成功後使用：

```bash
python3 scripts/log_article_to_google_sheets.py --all-site-articles
```

同步欄位包含：

- `article_id`
- `slug`
- `title`
- `live_url`
- `path`
- `category`
- `series`
- `published_at`
- `queue_id`
- `trigger_type`
- `provider`
- `model`
- `site_name`
- `site_url`
- `status`
- `notes`
- `cover_image_url`

重複保護以 `article_id` 去重。

電子報與通知使用 Resend。相關功能集中在 `scripts/content_pipeline.py`：

- `send-notification`
- `subscribe-newsletter`
- `send-newsletter`
- `check-resend-email`

Cloudflare Worker：

- `workers/contact.js`
- `wrangler.toml`

正式 route：

```text
tw.elitefasion.com/api/*
```

## 八、圖片與 SEO 補強機制

文章封面工具：

```text
scripts/article_cover_tools.py
```

用途：

- 統一文章封面輸出到 `images/optimized/article-covers/*.jpg`
- 確保尺寸為 1200 x 630
- 檢查 og:image 與實際 cover 是否一致
- 檢查缺圖、外部圖、重複圖、hash 重複
- 更新文章 HTML、索引、列表卡片與 publish log 的 cover URL

GitHub Actions：

```text
.github/workflows/article-cover-audit.yml
```

會在 push main 或 PR 時跑：

```bash
python scripts/article_cover_tools.py strict-audit
```

重要排除規則：

```text
outdoor-escapes/horizon-x-space-travel-neck-pillow.html
```

這類特殊前導頁、品牌頁、產品頁或結構明顯不同的一頁式內容，不應被一般文章封面重複圖片批次替換。

SEO 與圖片優化補強腳本：

```text
scripts/seo_media_optimize.py
```

用途包含：

- social image 產生。
- local image 轉 webp 或壓縮。
- canonical 補強。
- og / twitter meta 補強。
- Article / CollectionPage / WebPage / Breadcrumb JSON-LD 補強。
- missing local image refs 稽核。

## 九、目前盤點驗證結果

本次在本機執行：

```bash
python3 scripts/content_pipeline.py verify
```

結果：

```json
{
  "status": "ok",
  "articlesCount": 239,
  "queueSeries": 12,
  "verifiedArticleId": null
}
```

執行文章封面稽核：

```bash
/Users/mkhsu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/article_cover_tools.py audit
```

結果摘要：

```json
{
  "total": 239,
  "sameOgCover": 239,
  "mismatch": 0,
  "external": 0,
  "missingImages": 0,
  "wrongSizeImages": 0,
  "duplicateGroups": 0,
  "duplicateArticles": 0,
  "duplicateHashGroups": 0,
  "duplicateHashArticles": 0
}
```

目前分類文章數：

```text
ai-innovation: 18
casual-chic: 19
designer-perspective: 11
life-proposals: 99
lifestyle-culture: 31
outdoor-escapes: 16
runway-trends: 17
special-features: 12
wellness-movement: 16
```

目前 queue 摘要：

```text
queue updatedAt: 2026-05-13T06:01:11Z
nextQueueSequence: 13
series: 12
```

近期 queue 狀態：

```text
Q-0005 completed 中年未婚高知識女性如何學會一個人生活
Q-0006 in_progress 中年未婚海歸返台女性如何學會一個人生活
Q-0007 planned 中年未婚創業女性如何學會一個人生活
Q-0008 planned 中年未婚大型企業高管女性如何學會一個人生活
Q-0009 planned 中年喪偶高知識女性如何學會一個人生活
Q-0010 planned 中年喪偶海歸返台女性如何學會一個人生活
Q-0011 planned 中年喪偶創業女性如何學會一個人生活
Q-0012 planned 中年喪偶大型企業高管女性如何學會一個人生活
```

## 十、目前風險與建議

### 1. 正式排程缺模型 key 時不應 silently fallback

目前若缺少模型 API key，`content_pipeline.py` 會使用 fallback template。這對本地測試友善，但正式 GitHub Actions 若 secret 遺失，可能仍產生模板文並發布。

建議：增加 CI strict mode，例如在 GitHub Actions 中設定 `CI_STRICT_MODEL=true`，正式排程缺 key 就 fail。

### 2. 壓測 cron 應清理或加註

`content-scheduler.yml` 中保留多筆 4/25、4/26 cron。README 說是 2026-04-25 一次性壓測，但 cron 本身沒有年份。

建議：若已不需要，移除這些壓測 cron；若要保留，需在 workflow 明確加條件避免每年重跑。

### 3. 內容品質 guardrail 可再強化

目前資料鏈驗證完整，但內容品質主要依 prompt 與 checklist。建議後續可加入自動 guardrail，阻擋：

- 內部策略文字外洩。
- 過度公式化標題。
- 不支援的醫療、投資、法律承諾。
- 缺 FAQ、延伸閱讀或 CTA。
- 外部導購連結缺 disclosure 或 rel 屬性。

### 4. 圖片批次替換需維持特殊頁排除

`outdoor-escapes/horizon-x-space-travel-neck-pillow.html` 已在 `scripts/article_cover_tools.py` 排除。後續任何封面替換或 AI 生圖批次，需延續此規則，避免破壞特殊頁面。

### 5. 新增前端文案時不可暴露內部生成思路

專案規則明確要求：撰寫前端文字內容時，不可將內部思考過程、文案策略構思或模型提示外露到前台。

後續任何產文 prompt、文章模板、CTA、電子報模板，都需持續檢查這點。

## 十一、快速維運清單

產文前：

- 確認目標分類合理。
- 確認主題沒有重複既有文章。
- 高風險題材需保守表述。
- 品牌、導購、合作文需 disclosure。

產文後：

- 跑 `python3 scripts/content_pipeline.py verify`。
- 跑文章封面 audit。
- 確認 `automation/latest-run.json`。
- 確認 `automation/publish-log.json`。
- 確認首頁、分類頁、all articles、search index 有更新。

發布後：

- 確認已 push 到 `main`。
- 確認正式 URL 可讀。
- 確認 Google Sheets 有紀錄。
- 確認通知信或電子報狀態。

若涉及後端或 API：

- 不可只更新前端。
- 必須交叉確認 deployed code、deployed schema 與 live behavior。
- 若涉及點數、付款、訂單、配額、帳本、佇列、狀態同步，需同步檢查 log / audit / retry / fallback 流程。
