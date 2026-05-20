# momo 聯盟店家分批推薦文章規劃

建立日期：2026-05-20  
來源資料：`automation/momo-brand-recommendation-tracker.csv`、`automation/momo-affiliate-content-architecture.md`

本文件是內部批次規劃，用來安排後續 momo 聯盟店家如何分批進入 Elite Fashion 文章系統。前台文章不可出現本文件中的內部規劃語言，例如批次、覆蓋率、主推/配角、SEO、品牌池、矩陣、分潤等。

## 一、目前狀態

- tracker 目前共有 393 個店家。
- 已 live 覆蓋約 32 個店家，主要集中在 `outdoor-mobile-living`、`mobile-wardrobe-accessories` 與少量 `wellness-recovery-support`、`daily-food-drink-ritual`。
- 尚未充分展開的高潛力主題包括：
  - 居家儀式、照明、收納、清潔。
  - 辦公室咖啡茶、冷凍庫補給、送禮。
  - AI 工作角落、創作者拍攝、遠距會議裝備。
  - 身體恢復、睡眠、護具、按摩與居家伸展。
  - 美妝髮品、香氛與自我整理。
  - 寵物、家庭、親子禮物等低頻但可補長尾情境的內容。

## 二、後續批次原則

1. 每批以 5 篇為單位，方便撰寫、上傳、驗證與 Google Sheets 回填。
2. 每篇文章控制在 2 到 4 個主推店家、3 到 6 個補充店家，不寫成店家堆疊。
3. 已在近三批多次出現的品牌，後續只在非它不可的文章中出現；新批次優先拉高 pending A / B 店家的曝光。
4. 食品、草本飲、護具、按摩、睡眠、長照、美妝保養、寵物保健一律使用保守語氣，不承諾療效、保健效果、減重、抗老、醫療結果或安全保證。
5. 實體店家或在地服務相關店家，不得虛構 Google Business Profile、地址、營業時間或服務範圍。
6. 每篇都要符合 `automation/seo-content-execution-rules.md`：初始 HTML 可爬取、導言可產生摘要、圖片有描述性 alt、FAQ/schema 有可見內容支撐。

## 三、優先執行批次

### Batch 04：居家儀式與小宅生活升級

目標：補足目前覆蓋不足但與 Elite Fashion 調性高度相符的居家、香氛、燈光、收納與清潔主題。  
主分類：`lifestyle-culture`，部分可交叉 `wellness-movement`。

| 順序 | 暫定標題 | 分類 | 主推店家 | 補充店家 | 注意事項 |
|---|---|---|---|---|---|
| 04-01 | 下班後的安定感：香氛、燈光與收納的居家升級順序 | `lifestyle-culture` | THANN 官方直營、大檜仁心、燈后 | au fait 無非、蒔柒、灰調、完美主義 | 不寫療癒功效，改寫氣味、光線與收納節奏。 |
| 04-02 | 睡前 30 分鐘的低壓居家儀式：耳塞、枕頭、香氛與燈光怎麼搭 | `wellness-movement` | 耳根清靜、BETENSH、大檜仁心 | 紳娜多家居、禾肯居家、THANN、燈后 | 不承諾改善失眠；用環境整理與個人舒適度表述。 |
| 04-03 | 小宅收納不是買更多盒子：玄關、衣櫃、書桌與清潔工具的配置 | `lifestyle-culture` | 完美主義、真蓁嚴選、壹品輕奢家居館 | TZUMii、SUSS Living、多彩家居、Awayuki 淡雪 | 強調動線與物品分類，避免純收納盒清單。 |
| 04-04 | 質感清潔用品怎麼選：浴室水垢、廚房油污、除臭與天然清潔 | `lifestyle-culture` | 美利購清潔劑、Desire & Passion 天森無患、JINKO 淨科 | 淨淨 Clean Clean、GW 水玻璃、真蓁嚴選 | 不宣稱抗菌、除菌效果，除非商品頁明確且可支持。 |
| 04-05 | 客廳與工作角落的照明改造：吸頂燈、桌面燈、香氛與收納 | `lifestyle-culture` | 燈后、灰調、SENGLI | 職人椅YA、Hysure、完美主義、au fait 無非 | 可連到 AI 工作角落系列，但文章主軸仍是居家光線。 |

### Batch 05：AI 工作角落與創作者裝備

目標：把 3C 店家轉譯成白領工作者、創作者、顧問與遠距會議的日常配置，不寫成規格站。  
主分類：`ai-innovation`。

| 順序 | 暫定標題 | 分類 | 主推店家 | 補充店家 | 注意事項 |
|---|---|---|---|---|---|
| 05-01 | 高效率工作者的第二螢幕：外接螢幕、筆電與桌面配置怎麼選 | `ai-innovation` | REAICE、華克電腦、SENGLI | 日本橋3C、聯威電腦、Momax | 不承諾效能提升；聚焦視窗、會議、文件與收納。 |
| 05-02 | 不想露臉也能做內容：手機拍攝支架、濾鏡、燈光與收音入門 | `ai-innovation` | GoRig、Haida 台灣總代理、DTAudio | 燈后、SANSUI 山水、Momax | 不假裝實測；以入門拍攝配置與常見錯誤為主。 |
| 05-03 | 顧問與講師的遠距工作包：充電、耳機、簡報與移動收納 | `ai-innovation` | Momax、DTAudio、REAICE | LamiFans、華克電腦、曜暘音響、UD LAB | 可少量帶包款，但避免與既有通勤包文重複。 |
| 05-04 | AI 工作流需要什麼筆電：規格、保固、外接螢幕與資料備份的判斷 | `ai-innovation` | 華克電腦、凱銓科技、REAICE | 聯威電腦、日本橋3C、EZstick | 不能捏造效能測試；用規格判斷框架。 |
| 05-05 | 手機攝影怎麼升級：CPL、黑柔濾鏡、支架與戶外拍攝配件 | `ai-innovation` | Haida 台灣總代理、GoRig、Momax | Cliff Top、Litume 意都美、UV100 | 可連到戶外/旅行，但主軸是內容拍攝。 |

### Batch 06：辦公室飲食、咖啡茶與送禮

目標：把食品飲品店家轉為辦公室補給、冷凍庫、下午茶、送禮與輕戶外餐食內容。  
主分類：`lifestyle-culture`，部分可交叉 `wellness-movement`、`outdoor-escapes`。

| 順序 | 暫定標題 | 分類 | 主推店家 | 補充店家 | 注意事項 |
|---|---|---|---|---|---|
| 06-01 | 忙碌日常的辦公室咖啡補給：咖啡豆、濾掛與掛耳包怎麼選 | `lifestyle-culture` | 歐力咖啡、Xinto Coffee、馬克老爹 | LEOBUNA、BINCOO | Xinto/馬克/LEOBUNA 已出現，本文應補歐力主視角。 |
| 06-02 | 冷泡茶與茶禮盒怎麼選：日常飲用、送禮與下午茶的不同判斷 | `lifestyle-culture` | Teavoya、嘉嶼 CATTEA、ACE TEA | 暮朝食粹、台酒旗艦店 | 不寫健康功效；寫風味、保存、送禮情境。 |
| 06-03 | 不想每天煮飯的冷凍庫清單：舒肥雞胸、地瓜、冷凍蔬菜與料理包 | `wellness-movement` | 田食原、小嚼士、老饕廚房 | 呷什麵、KKM、GUMi 低碳、D 醣一刻 | 不寫減重、控糖療效；用時間管理與備餐便利性。 |
| 06-04 | 辦公室飲品清單：氣泡飲、植物奶、茶包與咖啡怎麼搭 | `lifestyle-culture` | PV 女性微甜草本飲、KKM、Teavoya | Zymoïde、恩亞生活、Xinto Coffee | 草本、酵素只寫口味與日常搭配，不寫功效。 |
| 06-05 | 質感送禮怎麼選：咖啡、茶、按摩設備、雨傘與客製小物 | `lifestyle-culture` | LamiFans、Teavoya、輝葉良品 | 馬克老爹、FULTON、Mister 手作皮件、大檜仁心 | 可做節慶 evergreen，不綁單一節日。 |

### Batch 07：身體恢復、護具與低壓伸展

目標：補足健康恢復主軸，但全程避免醫療、療效、保健與安全保證。  
主分類：`wellness-movement`。

| 順序 | 暫定標題 | 分類 | 主推店家 | 補充店家 | 注意事項 |
|---|---|---|---|---|---|
| 07-01 | 久站久坐的膝蓋與腰背支撐：護膝、護腰與鞋包重量怎麼看 | `wellness-movement` | BELEX、Jasper 大來護具、安里嚴選 | Sports Support、Cool Sport Support、UD LAB | 不承諾矯正或治療；提醒不適需諮詢專業。 |
| 07-02 | 給家人的居家舒壓設備：按摩椅、按摩槍、護具與照護用品怎麼看 | `wellness-movement` | 輝葉良品、一然健康、安里嚴選 | COZZY、BELEX、Jasper | 高風險，需重點檢查用語。 |
| 07-03 | 居家伸展角落怎麼打造：瑜珈墊、輔具、燈光與香氛的低壓配置 | `wellness-movement` | Juan 瑜珈、燈后、THANN | 完美主義、灰調、au fait 無非 | 回到每日可維持的環境，不寫運動效果保證。 |
| 07-04 | 夏季低負擔日常：涼感、防曬、睡眠降噪與飲食補給 | `wellness-movement` | UV100、耳根清靜、PV 女性微甜草本飲 | KKM、GUMi、D 醣一刻、Zymoïde | 已曝光品牌可少量使用，重點補飲食類 pending 店家。 |
| 07-05 | 家中照護動線怎麼整理：沐浴、移位、收納與安全提醒 | `wellness-movement` | TWyzy、一然健康、EVERPOLL | 安里嚴選、COZZY、完美主義 | 高風險文章，需人工查證商品頁後才可寫；若資料不足則暫緩。 |

### Batch 08：保養、髮品與自我整理

目標：將美妝保養店家導入「日常整理」與「低負擔保養」角度，不寫醫美或效果承諾。  
主分類：`lifestyle-culture`，部分可歸 `casual-chic`。

| 順序 | 暫定標題 | 分類 | 主推店家 | 補充店家 | 注意事項 |
|---|---|---|---|---|---|
| 08-01 | 日常保養別堆太多：精華、面膜、身體保養與防曬的整理順序 | `lifestyle-culture` | Cell Secret、AYSWE、唯詩生醫 | 雪亞緹、Bioyona、THANN | 不寫外泌體/PDRN 功效；只寫保養流程與使用情境。 |
| 08-02 | 頭皮與髮品怎麼整理：洗髮餅、染護、造型與按摩梳的選擇 | `lifestyle-culture` | Apode、CLOEE、KYOGOKU | MPB 巴黎小姐、SANSUI 山水 | 避免生髮、改善頭皮疾病等宣稱。 |
| 08-03 | 居家美甲與彩妝工具：新手友善材料、刷具與收納怎麼買 | `casual-chic` | 女王美學、GINGER MAKE UP、BAYBEYLA | ART64、玖伍 jewelry、Mister | 可連到穿搭配件；不做專業美甲技術承諾。 |
| 08-04 | 香氛與身體保養送禮：精油、蠟燭、毛巾與生活小物怎麼搭 | `lifestyle-culture` | THANN、au fait 無非、MORINO | 大檜仁心、蒔柒、Awayuki 淡雪 | 可作 evergreen 禮物文章。 |
| 08-05 | 會議前後的儀容整理包：髮品、補妝工具、香氛與小包配置 | `casual-chic` | S′AIME、Apode、GINGER MAKE UP | BAYBEYLA、MORINO、UD LAB | 避免寫成只給女性；以公開工作情境表述。 |

### Batch 09：寵物、家庭與低頻禮物題

目標：低頻補長尾，不讓網站主軸變成親子或寵物站；每批最多 1 到 2 篇進入正式排程。  
主分類：`lifestyle-culture`，少量可歸 `wellness-movement` 或專題。

| 順序 | 暫定標題 | 分類 | 主推店家 | 補充店家 | 注意事項 |
|---|---|---|---|---|---|
| 09-01 | 毛孩日常補貨清單：主食、零食、清潔與外出用品怎麼分工 | `lifestyle-culture` | HeroMama、Tails Life、petit 沛蒂 | DEHpet、寵物王國、尾巴丘 | 寵物保健不得寫功效；需保守。 |
| 09-02 | 貓咪生活整理：貓砂、玩具、食品與居家清潔的採買順序 | `lifestyle-culture` | 愛貓聯盟、愛貓聯萌、有喵病 | 尾巴丘、Mommywant、淨淨 Clean Clean | 注意品牌名稱相近，避免混淆。 |
| 09-03 | 寵物友善居家清潔：除臭、地板、洗衣與收納怎麼看 | `lifestyle-culture` | 艾寵聯萌、酷狗地板、淨淨 Clean Clean | JINKO、寵物王國、真蓁嚴選 | 不宣稱驅蟲、除菌或保健效果。 |
| 09-04 | 家庭禮物與益智玩具：積木、桌遊、拼圖與書店選物怎麼挑 | `lifestyle-culture` | 磚星球、888便利購、WA-GU-MI | 墊腳石書店、寶寶共和國、SUSS Living | 可寫為送禮，不把網站轉成親子教養站。 |
| 09-05 | 親子外出與生活小物：餐具、口腔清潔、孕產穿搭與外出包配置 | `lifestyle-culture` | 2angels、牙齒寶寶、Babyshare | MiffyBaby、寶寶共和國、S′AIME | 題材較窄，建議排在低優先或等相關需求出現。 |

### Batch 10：穿搭、包款與城市移動補強

目標：補足 `mobile-wardrobe-accessories` 尚未使用的 B / C 可用品牌，但避免與既有通勤包文章重複。  
主分類：`casual-chic`，部分交叉 `outdoor-escapes`。

| 順序 | 暫定標題 | 分類 | 主推店家 | 補充店家 | 注意事項 |
|---|---|---|---|---|---|
| 10-01 | 大尺碼穿搭也能俐落：上班、旅行與週末的選款順序 | `casual-chic` | B+ 大尺碼專家、UV100 | VENUSY、Be yourself、S′AIME | 前台不寫年齡；強調比例、舒適與場合。 |
| 10-02 | 雨天上班不失控：雨鞋、雨衣、抗風傘與包款材質的搭配清單 | `casual-chic` | OMBRA、FULTON、UD LAB | 左都雨傘、S′AIME、LFM 機車精品 | 與既有雨天戶外文需換角度，聚焦上班體面。 |
| 10-03 | 週末輕戶外穿搭：城市感、防曬外套、短褲與小包怎麼搭 | `casual-chic` | Litume 意都美、UV100、UD LAB | Be yourself、KANGOL、95 SNEAKER | 不寫成戶外裝備文，重點是城市與週末轉換。 |
| 10-04 | 飾品與皮件送禮：戒指、銀飾、皮夾、小包與日常配件怎麼選 | `casual-chic` | ART64、玖伍 jewelry、Mister 手作皮件 | S′AIME、KANGOL、LamiFans | 可補送禮詞，但避免過度情人節化。 |
| 10-05 | 旅行鞋包配置：好走鞋、輕量包、貼身小包與雨天備案 | `casual-chic` | UD LAB、S′AIME、鞋掌櫃 | 95 SNEAKER、Heine、FULTON | 需避免與城市旅行斜背包文章 cannibalization。 |

## 四、建議執行順序

優先順序建議：

1. **先做 Batch 04**：居家香氛、照明、收納、清潔與睡前儀式最符合網站調性，也能快速補目前最大缺口。
2. **再做 Batch 05**：AI 工作角落與創作者裝備能連回既有 AI/工作效率定位，且高價值 3C 店家仍大量 pending。
3. **第三做 Batch 06**：食品飲品與送禮能擴充日常內容，但食品/草本需嚴格控宣稱。
4. **Batch 07 視人工查證進度執行**：健康恢復類價值高，但高風險語氣需最嚴。
5. **Batch 08、09、10 作為輪替補量**：美妝、寵物家庭、穿搭補強都可寫，但不宜連續多批，避免網站主軸發散。

## 五、每批開寫前檢查

每批正式撰寫前：

- 先查 tracker 的 `article_slug` 與 `mention_count`，避免同一品牌連續過度曝光。
- 將本批主題對照既有 `data/articles-index.json`，避免標題或搜尋意圖互相競爭。
- 每篇先寫 spec card：搜尋意圖、讀者問題、主推店家、補充店家、不可宣稱事項、內部連結、封面圖方向。
- 文章完成後回填 tracker，更新發布紀錄與 Google Sheets。
- 每 5 篇為一個 commit/push 單位，跑 `content_pipeline.py verify`、`article_cover_tools.py strict-audit`、公開 URL spot check。
