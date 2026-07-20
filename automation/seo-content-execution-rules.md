# Elite Fashion SEO 內容執行規範

本文件根據 2026-05-19 使用者提供的四張 SEO 指南截圖整理，作為 Elite Fashion 後續文章、聯盟導購文、專題頁與多媒體頁的發布規範。核心原則是：讓 Googlebot、搜尋使用者與 AI 回應系統都能直接理解頁面主體內容，同時避免用制式 AI 文字稀釋網站可信度。

## 一、截圖重點整理

1. **摘要可產生性**
   - 頁面不應使用 `nosnippet`、`data-nosnippet` 或過度限制 `max-snippet` 等方式封鎖摘要。
   - 文章開頭與每個主要段落應有可被節錄的清楚句子，讓搜尋結果與 AI 摘要能理解本文價值。

2. **內容可被正常爬取**
   - 若大量內容依賴 JavaScript 動態載入，必須確認 Googlebot 實際看得到主體內容。
   - 本站優先維持靜態 HTML、SSR 或預先渲染輸出，不把文章主體、CTA、FAQ、導購揭露、重要內鏈放在只靠前端執行後才出現的位置。

3. **產品與服務資料可被機器理解**
   - 若頁面有商品、品牌、店家、服務項目或影片，應用可見文字與結構化資料協助搜尋系統理解。
   - 有商品導購時，品牌、適用情境、選購理由、限制、替代選項與連結必須是頁面可見內容，不可只藏在資料檔或腳本中。
   - 實體店家或在地服務業才應維護 Google Business Profile；本站不得為了 SEO 虛構所在地服務或店面資訊。

4. **第一手經驗與差異化角度**
   - 不要產出任何人用 AI 都能寫出的通用稿。
   - 動筆前必須問：「這篇文章裡，有哪一段是只有 Elite Fashion 編輯團隊能寫得出來的？」
   - 若回答不出來，就要重新找角度、補研究、補比較、補使用場景或改寫主軸。

5. **圖片與影片理解**
   - 圖片需有具描述性的 `alt`，幫助搜尋與可近用性。
   - 若頁面使用影片，需加入可見摘要或逐字稿，並在可支撐時加上 `VideoObject` schema。
   - 圖片與影片應服務內容理解，不只是裝飾。

## 二、本站新增文章發布規範

### 1. 摘要與前言

- `metaDescription` 必須用自然語言說清楚本文解決什麼問題，不可只堆關鍵字。
- 新文章需遵守 `automation/editorial-style-guide.md`：語氣優雅、精準、克制，帶有編輯判斷與生活品味；不可寫成廣告文案、品牌新聞稿、網紅推薦或制式搜尋拼貼。
- 新文章預設要評估商品置入；除非主題確實不適合，否則需提供 4 到 6 個相關商品或店家，並讓商品資訊存在於初始 HTML 的可見內容中。商品置入應是延伸準備，不可取代文章主體。
- 文章導言必須在前 150 字內完成三件事：
  - 帶出讀者面臨的真實問題。
  - 說明本文會如何幫助判斷、排序或取捨。
  - 提供一個可被搜尋摘要節錄的完整結論句。
- 禁止在公開頁面出現內部字眼，例如 `SEO 策略`、`品牌池`、`覆蓋率`、`批次`、`prompt`、`模型`、`AI 生成流程`。

### 2. 可爬取性

- 新文章必須輸出為靜態 HTML，主文、H1/H2、FAQ、延伸閱讀、CTA、導購揭露與頁尾都要存在於初始 HTML。
- 不得新增會阻擋搜尋摘要或主體爬取的 robots meta、`nosnippet`、`data-nosnippet` 或前端遮罩。
- 導購連結不可只由 JavaScript 注入；正式 HTML 需能直接看到連結文字與 `href`。
- 若未來新增互動工具、篩選器或動態商品模組，必須另備可爬取的靜態摘要、核心清單或 SSR 輸出。

### 3. 商品、品牌與聯盟導購內容

- 每篇導購文必須先建立讀者問題與選購框架，再自然帶入品牌；不可一開始只羅列商品情境。
- 品牌露出必須分工清楚：
  - 主推品牌：說明適合誰、何時值得買、關鍵取捨。
  - 配角品牌：補足價格帶、功能詞、替代選項或情境比較。
  - 低把握品牌：只能弱露出，不可用強推薦語氣。
- 商品或品牌資料必須出現在可見正文、FAQ 或 CTA 中；不得只放在 schema、JSON 或內部紀錄表。
- 聯盟連結需使用 `rel="sponsored nofollow"`，並在文章末端固定放置導購揭露。
- 不得捏造產品規格、價格、庫存、評測結果、店家資訊或官方聲明。

### 4. 第一手與編輯判斷

- 每篇文章至少要有一段「編輯判斷」性內容，但前台不可寫成內部流程說明。可用方式包括：
  - 選購順序：先買什麼、什麼先不要買。
  - 使用頻率：每天、週末、旅行、雨天、會議前後如何不同。
  - 常見錯誤：讀者最容易買錯或想錯的地方。
  - 取捨比較：容量與重量、正式感與舒適度、防曬與收納、儀式感與省事。
  - 台灣情境：梅雨、機車通勤、捷運、辦公室冷氣、週末短途旅行、居家收納。
- 若文章無法寫出上述任一類差異化段落，應暫緩發布並回到選題或研究階段。

### 5. 圖片、alt 與 OG

- 每篇文章需有獨立封面與 OG/Twitter 圖，且全站不得重複。
- 封面與社群預覽圖固定輸出為 `1200 x 630`；文章封面、`og:image`、`twitter:image` 與 `Article.image` 必須指向同一張可公開讀取的圖片。
- 文章 HTML 必須具備完整社群預覽 meta：`og:image`、`og:image:secure_url`、`og:image:type`、`og:image:width`、`og:image:height`、`og:image:alt`、`twitter:card`、`twitter:title`、`twitter:description`、`twitter:image`、`twitter:image:alt`。
- GitHub Actions 自動產文的文字模型與封面圖片模型分離：文章撰寫可維持 `CONTENT_MODEL_PROVIDER=nvidia`，封面圖預設使用 `COVER_IMAGE_PROVIDER=gemini`、`GEMINI_IMAGE_API_KEY` 或 `GEMINI_API_KEY`、`GEMINI_IMAGE_MODEL=imagen-4.0-fast-generate-001`。若 workflow 明確啟用圖片 provider 但缺少金鑰或生成失敗，必須讓流程失敗，不得用舊圖或分類預設圖假裝新封面。
- 圖片 `alt` 不應只重複檔名或空泛標題，應描述畫面與文章主題。例如：「戶外桌面上的手沖咖啡器具、濾掛包與簡易餐食配置」。
- 封面圖應協助理解文章主題；不得只是抽象情緒、模糊背景或與主題無關的裝飾。
- 自動封面生圖 prompt 不得把中文文章標題、摘要或 H2 原文交給圖片模型，也不得使用「magazine cover」「poster」「book cover」等容易誘發文字排版的描述。需改以英文視覺主題描述，並明確禁止任何可讀文字、亂碼、字母、數字、招牌、書脊、包裝字樣、條碼、QR code、UI 文字與類似排版符號。
- 若頁面有多張圖片，裝飾圖可留空 alt；內容圖必須寫清楚畫面內容與使用情境。

### 6. 影片與結構化資料

- 新增影片頁或嵌入影片時，必須同時提供可見的影片摘要或逐字稿重點。
- 只有當頁面確實含影片，且 schema 內容能由可見頁面支撐時，才可加入 `VideoObject`。
- `Article`、`FAQPage`、`Product`、`Review`、`VideoObject` 等 schema 不得超出頁面可見內容；不能為了 SEO 標記不存在的評測、商品或影片。

### 7. 在地服務與 Google Business Profile

- 本站目前是內容媒體與聯盟導購站，不是實體店家或在地服務業，不能建立或宣稱不實的 Google Business Profile。
- 若未來 NorthPath AI 或 Elite Fashion 有真實可驗證的在地服務、地址、電話、營業時間，才可建立或維護 Google Business Profile。
- 在地資訊必須與網站 `about`、`contact`、頁尾與公開商業資料一致。

## 三、發布前必檢

每篇新文章發布前，必須確認：

- 初始 HTML 可看到 H1、導言、正文、FAQ、延伸閱讀、CTA、頁尾。
- 無 `nosnippet`、`data-nosnippet` 或阻擋摘要的 robots meta。
- `metaTitle`、`metaDescription`、canonical、OG/Twitter 圖完整。
- `og:image:width=1200`、`og:image:height=630`，且 `twitter:image` 可直接打開並回傳 200。
- 圖片有描述性 alt；封面與 OG 圖為同一張且不與其他文章重複。
- FAQ 與 schema 有可見內容支撐。
- 聯盟連結有 `sponsored nofollow`，導購揭露在文章末端。
- 新文章內容厚度至少 2,200 個中文內容字元；增加篇幅必須用具體情境、選購順序、常見錯誤、使用限制、取捨比較或維護方式補強，不可用重複段落、空泛形容詞、堆疊 CTA 或重複揭露湊字數。
- 文章至少有一段具體情境、第一手判斷或取捨比較，而不是通用 AI 文字。
- 站內索引、搜尋索引、sitemap、發布紀錄與品牌追蹤表已更新。

## 四、目前專案落地方式

- 文章生成提示詞：`automation/prompts/article-writer.md`
- 人工校稿清單：`automation/editorial-review-checklist.md`
- 自動化渲染與索引：`scripts/content_pipeline.py`
- 封面與 OG 稽核：`scripts/article_cover_tools.py strict-audit`
  - 若本機 Python 尚未安裝 Pillow，先執行 `python3 -m pip install --user --break-system-packages Pillow`
- 品牌覆蓋追蹤：`automation/momo-brand-recommendation-tracker.csv`
- 本規範需由 `AGENTS.md` 強制引用；後續新增內容若違反本文件，視為發布前未完成。
