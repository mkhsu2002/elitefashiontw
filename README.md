# Elite Fashion 內容自動化系統

本專案已加入可持續運作的靜態內容流水線，核心目標是讓文章從主題規劃、queue 排程、生成、同步、驗證、上線到通知都能在同一條資料鏈上完成。

## 正式部署鏈

2026-04-25 已驗證的正式鏈路如下：

`GitHub main -> GitHub Pages -> Cloudflare 自訂網域代理 -> https://tw.elitefasion.com`

補充：
- `CNAME` 指向 `tw.elitefasion.com`
- `https://mkhsu2002.github.io/elitefashiontw/` 會轉址到正式網域
- 正式回應標頭同時出現 GitHub 與 Cloudflare 痕跡，因此不是 Cloudflare Pages

## 核心檔案

- `automation/content-strategy.md`：內容策略
- `automation/topic-selection-mechanism.md`：queue 為空時的自動選題機制
- `automation/editorial-review-checklist.md`：校稿清單
- `automation/topic-queue.json` / `automation/topic-queue.md`：主題 queue
- `automation/publish-log.json` / `automation/publish-log.md`：發文紀錄
- `data/articles-index.json`：文章主索引
- `data/front-listing.json`：前台列表資料
- `data/search-index.json`：站內搜尋索引
- `scripts/content_pipeline.py`：內容流水線主腳本

## 自然語言操作

```bash
python3 scripts/content_pipeline.py command --instruction "加入主題序列：Dify AI，篇數：6，補充：偏台灣中小企業導入與實作"
python3 scripts/content_pipeline.py command --instruction "直接生成主題：AI 代理人怎麼落地到客服部門" --fixture
```

## GitHub Secrets / Variables

- `CONTENT_MODEL_API_KEY`
- `CONTENT_MODEL`
- `CONTENT_PLANNER_MODEL`
- `RESEND_API_KEY`
- `CONTENT_NOTIFICATION_FROM_EMAIL`
- `CONTENT_NOTIFICATION_TO_EMAIL`

排程與手動工作流程會在內容同步與驗證通過後才 commit / push；通知則會等正式站實際讀得到文章才送出。
