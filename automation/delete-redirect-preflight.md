# 刪除 / 301 前置檢查

更新日期：2026-05-07

## 原則

正式刪除或 301 前，先確認 Search Console、GA4、外鏈與站內引用。若任一頁面仍有有效曝光、流量、轉換、反向連結、社群引用或合作方入口，先維持 `noindex, follow`，不要直接刪檔。

## 目前 noindex 頁面

| 頁面 | 目前狀態 | 初步處理 |
| --- | --- | --- |
| `high-performance.html` | `noindex, follow` | 保留舊專題入口，導回 AI、健康恢復與人生重整 owner。 |
| `high-performance/marketing-engine.html` | `noindex, follow` | 先不刪，待外部殘值確認。 |
| `high-performance/sleep-optimization.html` | `noindex, follow` | 先不刪，待外部殘值確認。 |
| `high-performance/financial-stack.html` | `noindex, follow` | 先不刪，待外部殘值確認。 |
| `life-proposals/one-hour-useless-time.html` | `noindex, follow` | 刪除候選，可能導回 `mature-life-reset.html`。 |
| `life-proposals/40-body-revolution.html` | `noindex, follow` | 刪除候選，可能導回 `body-rhythm-reset.html`。 |
| `life-proposals/mindfulness-in-chores.html` | `noindex, follow` | 刪除候選，可能導回 `mature-life-reset.html` 或健康恢復相關 owner。 |
| `life-proposals/art-of-scarves.html` | `noindex, follow` | 刪除候選，可能導回 `spring-summer-capsule-wardrobe.html` 或 `casual-chic.html`。 |

## 本地站內引用檢查

仍有站內連結指向 4 個刪除候選頁，正式刪除前必須先改內鏈：

- `lifestyle-culture.html` 仍連到 `one-hour-useless-time.html`、`mindfulness-in-chores.html`、`40-body-revolution.html`、`art-of-scarves.html`。
- 多篇 `life-proposals/` 文章的推薦閱讀仍連到上述 4 頁，包括 `housewife-worth-not-clean-floor.html`、`joint-health-travel.html`、`marriage-reset-empty-nest.html`、`money-minimalism-abundance.html`、`signature-scent-fragrance.html`、`social-energy-management.html`、`vintage-sustainable-fashion.html` 等。
- `high-performance.html` 仍連到三篇 high-performance 子頁；這是舊專題內部保留路徑，若未來要刪子頁，需同步改 hub 卡片。

## 外部資料待查

刪除或 301 前，逐頁確認：

- Search Console：近 16 個月 clicks、impressions、queries、平均排名。
- GA4：landing sessions、engagement、事件、轉換或 assisted conversion。
- 外鏈：Google Search Console links、Ahrefs / Semrush / 其他 backlink 工具、社群與合作方引用。
- 伺服器 / CDN：是否仍有 referral、舊廣告、電子報、社群貼文導流。

## 暫定結論

目前只完成本地 preflight，尚未取得 Search Console / GA4 / 外鏈資料，因此不執行正式刪除、301 或 canonical 變更。下一步先清理上述站內舊連結，再進入外部資料交叉確認。
