# Elite Fashion 內容自動化系統

本專案已加入可持續運作的靜態內容流水線，目標不是只產出單篇文章，而是讓內容從策略、選題、queue 排程、生成、同步、驗證、正式上線到通知，都走同一條可追蹤的資料鏈。

## 正式部署鏈

2026-04-25 已驗證的正式鏈路如下：

`GitHub main -> GitHub Pages -> Cloudflare 自訂網域代理 -> https://tw.elitefasion.com`

補充：
- `CNAME` 指向 `tw.elitefasion.com`
- `https://mkhsu2002.github.io/elitefashiontw/` 會轉址到正式網域
- 正式回應標頭同時出現 GitHub 與 Cloudflare 痕跡，因此不是 Cloudflare Pages

## 系統目標

這套機制的核心原則如下：

- 不是亂數產文，而是策略驅動
- 不是單篇腳本，而是可持續內容流水線
- 不是只生成文字，而是要同步接上前台索引、搜尋、列表與正式部署
- 不是 push 就算完成，而是要等正式站真的可讀後才通知

## 內容選題原則

本網站的自動選題邏輯不是以外部熱門工具名為主，而是回到站點本身的內容身份。

目前的選題基準是：

- 服務熟齡女性的生活決策、工作重整、品味與行動力
- 把 AI、設計、秀場、趨勢翻譯成日常可執行的內容
- 優先產出 evergreen 題，而不是只追短期熱詞
- 避免跟既有標題高度重複
- 避免空泛、誇大或過度工具導向的標題

當 queue 為空時，系統會優先從以下方向選題：

- 45+ 女性職涯重整與 AI 協作
- 熟齡睡眠、恢復、肌力與健康習慣
- 旅行穿搭、舒適鞋包、獨旅與移動中的體面感
- 居家閱讀、日常記錄、生活工具與工作角落
- 把趨勢、秀場與設計轉譯成日常判斷

## 流程總覽

每次產文的標準流程如下：

1. 讀取內容策略與校稿規範
2. 讀取既有文章、主題 backlog 與 queue
3. 若 queue 有待處理項目，優先消化 queue
4. 若 queue 為空，依站點選題邏輯挑出下一個最值得寫的題目
5. 生成完整文章 metadata + Markdown + HTML
6. 同步更新文章索引、前台列表、搜尋索引、發文紀錄、queue 狀態
7. 驗證資料鏈是否完整，避免 id / url / file 重複
8. commit + push 到 `main`
9. 等正式站真的讀得到文章
10. 確認正式上線後，寄送通知 email

## 核心檔案

- `automation/content-strategy.md`：內容策略
- `automation/topic-selection-mechanism.md`：queue 為空時的自動選題機制
- `automation/editorial-review-checklist.md`：人工校稿標準
- `automation/topic-backlog.json`：站點預設備選題庫
- `automation/topic-queue.json`：queue 原始資料
- `automation/topic-queue.md`：queue 人類可讀版
- `automation/publish-log.json`：發文紀錄原始資料
- `automation/publish-log.md`：發文紀錄人類可讀版
- `automation/latest-run.json`：最近一次執行狀態
- `automation/site-config.json`：站點設定、部署鏈、通知設定、資料契約
- `automation/articles/`：自動生成文章的 metadata 與 Markdown
- `data/articles-index.json`：文章主索引
- `data/front-listing.json`：前台列表資料
- `data/search-index.json`：站內搜尋索引
- `scripts/content_pipeline.py`：內容流水線主腳本
- `.github/workflows/content-scheduler.yml`：固定排程產文
- `.github/workflows/content-command.yml`：手動或自然語言指令工作流程

## 自然語言使用指南

你可以直接用兩種指令控制系統。

### 1. 加入主題序列

用途：把主題放進 queue，後續依排程逐篇生成。

指令格式：

```text
加入主題序列：主題，篇數：N，補充：補充方向
```

例子：

```text
加入主題序列：45+ 女性職涯重整與 AI 協作，篇數：6，補充：偏台灣上班族、實務入門、避免太技術
加入主題序列：熟齡睡眠與恢復，篇數：4，補充：偏日常可執行、避免醫療誇大
加入主題序列：旅行穿搭與舒適鞋包，篇數：5，補充：偏熟齡女性、移動情境與體面感
```

系統收到後會先做整組規劃，不會直接亂寫。規劃結果會寫入：

- `automation/topic-queue.json`
- `automation/topic-queue.md`

每個 queue series 會記錄：

- `queueId`
- `topic`
- `direction`
- `plannedCount`
- `status`
- `createdAt`
- 每篇的順序、標題、切角、目標讀者、分類、CTA 提示與發文狀態

### 2. 直接生成主題

用途：立即產出單篇文章，不進 queue。

指令格式：

```text
直接生成主題：主題
```

例子：

```text
直接生成主題：不會寫程式的人，怎麼開始用 AI 重整工作流程
直接生成主題：50+ 女性旅行穿搭，怎麼兼顧舒適與體面
直接生成主題：熟齡女性如何建立不過度用力的晨間恢復習慣
```

### 本地執行範例

```bash
python3 scripts/content_pipeline.py command --instruction "加入主題序列：45+ 女性職涯重整與 AI 協作，篇數：6，補充：偏台灣上班族、實務入門、避免太技術"
python3 scripts/content_pipeline.py command --instruction "直接生成主題：不會寫程式的人，怎麼開始用 AI 重整工作流程"
```

若只是想測資料鏈、不打真模型，可加上 `--fixture`：

```bash
python3 scripts/content_pipeline.py command --instruction "直接生成主題：測試文章" --fixture
```

## CLI 指令一覽

```bash
python3 scripts/content_pipeline.py enqueue --topic "主題" --count 6 --direction "補充方向"
python3 scripts/content_pipeline.py generate-now --topic "單篇主題"
python3 scripts/content_pipeline.py scheduled-run
python3 scripts/content_pipeline.py sync
python3 scripts/content_pipeline.py verify --article-id <article-id>
python3 scripts/content_pipeline.py wait-for-live --article-url <url> --article-title "標題"
python3 scripts/content_pipeline.py send-notification --article-title "標題" --article-url <url>
```

用途說明：

- `enqueue`：直接把一組系列主題加入 queue
- `generate-now`：立即生成單篇
- `scheduled-run`：優先消化 queue，否則走 fallback 選題
- `sync`：重建索引、列表、搜尋、queue 與發文紀錄
- `verify`：驗證資料鏈是否完整
- `wait-for-live`：輪詢正式站，確認文章真的上線
- `send-notification`：寄送上線通知信

## 排程規則

預設排程由 GitHub Actions 執行，不依賴本機常駐。

- 目前每週排程 4 次
- 目前 GitHub Actions cron 為：
  - `35 19 * * 6`
  - `50 19 * * 6`
  - `15 2 * * 3`
  - `15 2 * * 5`
- 以溫哥華夏令時間（PDT）換算，目前對應為：
  - `週六 12:35pm`
  - `週六 12:50pm`
  - `週二 7:15pm`
  - `週四 7:15pm`
- 以台灣時間（UTC+8）換算，目前對應為：
  - `週日 03:35`
  - `週日 03:50`
  - `週三 10:15`
  - `週五 10:15`
- queue 有待處理項目時，優先依序消化 queue
- queue 為空時，才回到站點自動選題機制
- 通過同步與驗證後才會 commit / push
- 只有正式站確認可讀後才寄通知

備註：

- GitHub Actions `schedule` 使用 UTC，所以上述「溫哥華夏令時間」是依目前夏令時間換算。
- 若進入溫哥華冬令時間（PST），`週六 12:35pm` 這筆會自然變成 `週六 11:35am`，`週六 12:50pm` 這筆會自然變成 `週六 11:50am`；若你之後希望冬令時間也固定維持當地時間，需要再調整 cron。

## 每次產文會同步更新哪些檔案

- 實際文章檔案，例如 `ai-innovation/xxx.html`
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
- 受資料驅動的首頁、分類頁、`all-articles.html`、`search.html`

## 驗證機制

正式提交前，系統至少會檢查：

- 文章檔存在
- `articles-index` 已更新
- 前台列表資料已更新
- 搜尋索引已更新
- 發文紀錄已更新
- queue 狀態已更新
- `article id`、`url`、`file` 沒有重複
- 首頁、分類頁與文章列表頁都有讀到新文章
- 正式站網址可讀到最新文章

若驗證失敗，不應視為完成發布。

## Email 通知

目前通知服務使用 Resend，主旨前綴可在 `automation/site-config.json` 設定。

目前格式為：

```text
伊麗時尚 TW｜文章已上線：文章標題
```

信件內容維持極簡，只包含：

- 文章標題
- 正式站網址

## 模型 API 與版本紀錄

### 目前正式使用中

截至 `2026-04-25`，GitHub Actions 目前啟用的模型供應商為：

- Provider：`nvidia`
- Endpoint：`https://integrate.api.nvidia.com/v1/chat/completions`
- API mode：`chat_completions`
- Writer model：`deepseek-ai/deepseek-v4-pro`
- Planner model：`deepseek-ai/deepseek-v4-pro`

目前這套切換機制已實測通過：

- OpenAI 路徑仍可正常呼叫
- NVIDIA 路徑已成功完成正式文章生成、上線與 email 通知

### 保留的回切設定

OpenAI 並沒有被覆蓋，仍完整保留作為 fallback：

- Provider：`openai`
- Endpoint：`https://api.openai.com/v1/responses`
- API mode：`responses`
- Writer model：`gpt-5-mini`
- Planner model：`gpt-5-mini`

### 程式層備註

- `scripts/content_pipeline.py` 會依 `CONTENT_MODEL_PROVIDER` 自動選擇 provider
- OpenAI 走 `responses`
- NVIDIA 走 `chat_completions`
- NVIDIA 路徑目前會使用較小的既有標題上下文，避免長 prompt 導致 `502`
- `automation/site-config.json` 目前 `requestTimeoutSeconds` 已調整為 `300`

## GitHub Secrets / Variables

### Secrets

- `CONTENT_MODEL_API_KEY`
- `NVIDIA_CONTENT_MODEL_API_KEY`
- `RESEND_API_KEY`
- `CONTENT_NOTIFICATION_FROM_EMAIL`
- `CONTENT_NOTIFICATION_TO_EMAIL`

### Variables

- `CONTENT_MODEL_PROVIDER`
- `OPENAI_CONTENT_MODEL`
- `OPENAI_CONTENT_PLANNER_MODEL`
- `NVIDIA_CONTENT_MODEL`
- `NVIDIA_CONTENT_PLANNER_MODEL`

### 目前 GitHub 上的實際角色

- `CONTENT_MODEL_PROVIDER`
  - 決定工作流程目前要走 `openai` 或 `nvidia`
- `CONTENT_MODEL_API_KEY`
  - 保留給 OpenAI 使用
- `NVIDIA_CONTENT_MODEL_API_KEY`
  - 給 NVIDIA 使用
- `OPENAI_CONTENT_MODEL` / `OPENAI_CONTENT_PLANNER_MODEL`
  - OpenAI 路徑的 writer / planner 模型
- `NVIDIA_CONTENT_MODEL` / `NVIDIA_CONTENT_PLANNER_MODEL`
  - NVIDIA 路徑的 writer / planner 模型

### 舊變數備註

以下變數目前仍保留在 repo，但已不是切換機制的主要控制來源：

- `CONTENT_MODEL`
- `CONTENT_PLANNER_MODEL`

它們屬於舊版單供應商配置遺留值。現階段 workflow 會優先依 provider 選用 `OPENAI_*` 或 `NVIDIA_*` 變數。

## 未來切換備忘

### 切到 NVIDIA

1. 確認 secret `NVIDIA_CONTENT_MODEL_API_KEY` 有效
2. 將 variable `CONTENT_MODEL_PROVIDER` 設成 `nvidia`
3. 確認：
   - `NVIDIA_CONTENT_MODEL=deepseek-ai/deepseek-v4-pro`
   - `NVIDIA_CONTENT_PLANNER_MODEL=deepseek-ai/deepseek-v4-pro`
4. 建議先跑最小 smoke test，再跑正式文章

### 切回 OpenAI

1. 不需要重建 secret，只要保留既有 `CONTENT_MODEL_API_KEY`
2. 將 variable `CONTENT_MODEL_PROVIDER` 改回 `openai`
3. 確認：
   - `OPENAI_CONTENT_MODEL=gpt-5-mini`
   - `OPENAI_CONTENT_PLANNER_MODEL=gpt-5-mini`
4. 建議先跑最小 smoke test，再恢復正式排程

### 切換時的注意事項

- 不要用新的 provider 覆蓋另一個 provider 的 secret
- 先切 provider，再跑手動測試，確認成功後再放給固定排程
- 若 NVIDIA 再次出現 `502` 或超時，優先檢查 prompt 大小與 timeout，不要直接假設 key 失效
- 若 OpenAI 或 NVIDIA key 曾在對話、log 或螢幕錄影中曝光，應先旋轉再繼續使用
- 切換 provider 後，最好先觀察一篇正式上線結果，再決定是否讓後續 queue 繼續自動跑

## 維運建議

- 任何生成完成都不應只看本地檔案，要看正式站是否真的可讀
- 若前台資料結構改動，必須同步檢查索引與頁面模板是否一致
- 若更換通知網域或寄件信箱，先驗證 Resend domain status 是否仍為 `verified`
- 若移植到其他網站，優先改 `automation/site-config.json`、內容策略文件與題庫，而不是先改主流程程式
