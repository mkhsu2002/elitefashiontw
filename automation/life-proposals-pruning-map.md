# `life-proposals` 103 篇整理清單

> 這是第一輪 stop-loss 盤點，依目前站內索引、標題品質、分類邏輯與 2026 春夏策略整理。
>
> 本清單不代表立刻刪文；其中標記為 `刪除` 的頁面，正式執行前仍應再交叉確認 Search Console、GA4、反向連結與外部引用狀況。

## 動作定義
- `保留`：意圖清楚、仍符合站點方向，建議直接改標題、補 FAQ、補內鏈後繼續保留。
- `合併`：題目有價值，但應與其他近似頁整併，改由較清楚的 owner page 承接。
- `降權`：短期不建議再主推，應自首頁 / 類別策展中退場，必要時考慮 `noindex` 或移出 sitemap。
- `刪除`：意圖弱、過度抽象或重複度太高，若無實際流量與外鏈支撐，建議退場。

## 總覽
- `保留`：42 篇
- `合併`：40 篇
- `降權`：17 篇
- `刪除`：4 篇

## 已執行
- 2026-05-07：先對 4 篇標記為 `刪除` 的低價值頁加入 `noindex, follow`，並更新同步與 sitemap 產生邏輯，使 noindex 頁不再進入 `data/articles-index.json`、`data/search-index.json`、`all-articles.html` 與 `sitemap.xml`。
- 2026-05-07：`high-performance.html` 與 `high-performance/` 3 篇舊專題改為 `noindex, follow`，頁面保留站內可讀性與 follow link，並導回 `ai-innovation`、`wellness-movement`、`mature-life-reset.html` 三個較符合現行定位的 owner。
- 2026-05-07：第一批 owner-linked legacy 文章完成標題、首屏與 CTA 文案降噪，先處理健康恢復、春夏衣櫥與趨勢轉譯相關高曝光頁。
- 本次沒有刪除檔案，也沒有設定 301；若後續 Search Console / GA4 / 外鏈檢查確認無殘值，再決定是否正式刪除或 redirect。

## AI 與職涯重整

| ID | 頁面 | 動作 | 目標群 | 原因 |
| --- | --- | --- | --- | --- |
| 001 | `ai-career-navigation-for-managers`｜團隊開始談 AI，你卻不知道從哪裡跟上？ | 合併 | AI 導入給 45+ 管理者（`ai-innovation`） | FlyPig lead 型頁，與 AI 採用題重疊。 |
| 002 | `ai-second-curve-for-career-pivot`｜不會寫程式，也該開始看懂 AI | 合併 | AI 第二曲線入門（`ai-innovation`） | 與 043、058、069、094 同群。 |
| 003 | `ai-side-hustle-for-experts`｜想做副業，卻怕 AI 讓努力白費？ | 合併 | AI 副業與知識變現（`ai-innovation`） | 與副業／第二曲線重疊。 |
| 043 | `career-pivot-start-over`｜中年轉職：45歲是最棒的重新開機時刻？ | 保留 | 中年轉職與重啟（`lifestyle-culture`） | 搜尋意圖明確，可做 owner page。 |
| 058 | `entrepreneurship-after-40`｜40歲後創業：利用智慧紅利 | 合併 | 熟齡副業與第二曲線（`lifestyle-culture`） | 與創業、接案、副業題可整併。 |
| 069 | `gig-economy-second-act`｜零工經濟浪潮：40+女性如何靠接案開啟第二人生？ | 合併 | 接案與第二人生（`lifestyle-culture`） | 與 058、094 屬同一決策群。 |
| 083 | `networking-for-introverts`｜內向者也能建立高品質職場人脈 | 保留 | 內向者人脈與職場關係（`lifestyle-culture`） | 問題清楚，與熟齡工作者高度相關。 |
| 091 | `resume-refresh-modern`｜履歷健檢：40+如何凸顯領導力與軟實力？ | 保留 | 履歷健檢（`lifestyle-culture`） | 具體、高實用，適合保留。 |
| 092 | `salary-negotiation-value`｜40+職場女性的薪資談判全攻略 | 保留 | 薪資談判（`lifestyle-culture`） | 強意圖題，轉換與內鏈價值高。 |
| 094 | `side-hustles-midlife`｜適合中年女性的 5 種優雅副業 | 保留 | 副業選項總覽（`lifestyle-culture`） | 與第二曲線強相關，可做主力 evergreen。 |
| 103 | `workplace-mentorship-fulfillment`｜如何從競爭者變成引路人？ | 保留 | Mentor 與職場傳承（`lifestyle-culture`） | 差異化高，符合熟齡職涯視角。 |

## 關係、家庭與人生重整

| ID | 頁面 | 動作 | 目標群 | 原因 |
| --- | --- | --- | --- | --- |
| 005 | `finding-yourself-after-40`｜自我重構權威與熟齡女性存有資產管理 | 合併 | 中年自我重整（`lifestyle-culture`） | 核心意圖可留，但標題公式化。 |
| 006 | `grandparenting-joy-no-stress`｜隔代喜悅與家族文化資產管理 | 降權 | 家庭角色轉換（`lifestyle-culture`） | 題目較窄，非春夏主擴張線。 |
| 007 | `gray-divorce-new-chapter`｜離婚主權協議與身分重塑管理 | 合併 | 離婚後生活重整（`lifestyle-culture`） | 題目重要，但要改成讀者語言。 |
| 011 | `let-go-control-kids`｜控制釋放與意識邊界管理 | 合併 | 成年子女邊界（`lifestyle-culture`） | 與 015 可整併。 |
| 012 | `long-distance-family-bonds`｜跨海家族連結與數位親密 | 降權 | 跨海家庭關係（`lifestyle-culture`） | 非本站當前主力意圖。 |
| 013 | `marriage-reset-empty-nest`｜空巢浪漫與伴侶情感資產管理 | 合併 | 空巢後伴侶關係重整（`lifestyle-culture`） | 題意可用，但公式化。 |
| 014 | `one-hour-useless-time`｜無用美學與意識效率管理 | 刪除 | - | 概念抽象，缺少搜尋與服務導向。 |
| 015 | `parenting-adult-children-consultant`｜家長角色轉型與顧問式教養 | 合併 | 成年子女關係再定位（`lifestyle-culture`） | 與 011 屬同群。 |
| 016 | `please-yourself-not-world`｜悅己權威與自尊資產管理 | 降權 | 悅己與自我價值（`lifestyle-culture`） | 過度口號化，意圖太寬。 |
| 017 | `solitude-in-marriage-hobbies`｜婚姻中的分開興趣與空間管理 | 合併 | 伴侶共處與保留自己的空間（`lifestyle-culture`） | 與伴侶邊界群相容。 |
| 018 | `solitude-is-enjoyment`｜孤獨主權與心理空間管理 | 降權 | 獨處能力（`lifestyle-culture`） | 抽象度高，與 017、090 重疊。 |
| 022 | `healing-mother-daughter-wounds`｜母女關係創傷修復 | 合併 | 母女關係修復（`lifestyle-culture`） | 主題有價值，但應避免權威口吻。 |
| 031 | `housewife-worth-not-clean-floor`｜主婦價值不只在乾淨地板 | 保留 | 家務角色覺醒（`lifestyle-culture`） | 受眾清楚，情緒張力與服務感兼具。 |
| 037 | `art-of-apology-repair`｜道歉與關係修復的金繕美學 | 保留 | 關係修復與道歉（`lifestyle-culture`） | 角度有辨識度，可保留但要去掉舊公式感。 |
| 044 | `change-is-never-too-late`｜現在改變永遠不晚 | 合併 | 後悔與人生再啟動（`lifestyle-culture`） | 主題可留，但標題太泛。 |
| 046 | `dating-at-40-plus`｜40+ 的約會市場 | 合併 | 中年約會與再社交（`lifestyle-culture`） | 可做系列，但不應孤立成單薄頁。 |
| 052 | `elegant-refusal-relationship-detox`｜優雅拒絕與人際斷捨離 | 保留 | 人際邊界（`lifestyle-culture`） | 問題導向清楚，可直接保留。 |
| 055 | `emotional-first-aid-kit`｜情緒急救箱 | 保留 | 情緒急救（`lifestyle-culture`） | 與站點人生提案角色相符。 |
| 056 | `emotional-labor-awakening`｜主婦的情緒勞動覺醒 | 保留 | 情緒勞動與看不見的付出（`lifestyle-culture`） | 讀者痛點明確。 |
| 057 | `empty-nest-freedom-year`｜空巢期不是分離，而是自由元年 | 保留 | 空巢期重整（`lifestyle-culture`） | 與目標受眾高度吻合。 |
| 061 | `fear-of-being-forgotten-aging`｜我們恐懼的不是皺紋，而是被遺忘 | 合併 | 面對衰老與存在焦慮（`lifestyle-culture`） | 題目太抽象，應整併到身份重整群。 |
| 066 | `finding-your-tribe-midlife`｜40+ 女性如何建立高品質社交圈？ | 保留 | 中年找新朋友（`lifestyle-culture`） | 搜尋意圖與讀者需求都清楚。 |
| 067 | `forgive-imperfect-past-self`｜與過去和解 | 合併 | 與過去和解（`lifestyle-culture`） | 主題可留，但不需再分出太多薄頁。 |
| 068 | `friendship-audit-outgrow`｜朋友也要斷捨離 | 保留 | 友情邊界與社交圈整理（`lifestyle-culture`） | 近期方向很對，可保留。 |
| 071 | `in-law-boundaries`｜婆媳/岳婿關係的邊界感 | 保留 | 姻親邊界（`lifestyle-culture`） | 典型熟齡問題解法題。 |
| 077 | `love-languages-update`｜40歲後最想要的愛的語言 | 合併 | 熟齡伴侶溝通（`lifestyle-culture`） | 題意可用，但與 013、089 重疊。 |
| 079 | `midlife-anxiety-opportunity`｜中年焦慮如何化為轉機？ | 合併 | 中年焦慮與重整（`lifestyle-culture`） | 可用，但應避免太空泛。 |
| 085 | `perfect-wife-trap-60-percent`｜別讓完美賢妻的標籤困住妳 | 保留 | 婚姻中的自我邊界（`lifestyle-culture`） | 與受眾高度貼合。 |
| 086 | `pet-companionship-healing`｜毛小孩如何療癒空巢期與孤獨？ | 合併 | 寵物陪伴與熟齡生活（`lifestyle-culture` / 品牌專案） | 主題有潛力，但應與寵物企劃整併。 |
| 089 | `redefining-partnership-sacrifice-to-support`｜與伴侶重新定義後半生的關係 | 保留 | 伴侶關係再定義（`lifestyle-culture`） | 方向正確，可保留。 |
| 090 | `rediscovering-worth-beyond-motherhood`｜當孩子不需要妳時，妳是誰？ | 保留 | 母職之外的自我價值（`lifestyle-culture`） | 與本站核心受眾高度吻合。 |
| 093 | `sandwich-generation-care`｜三明治世代的生存之道 | 保留 | 照護壓力與自我照顧（`lifestyle-culture`） | 明確高價值 evergreen。 |
| 096 | `sisterhood-female-support`｜女性互助網絡是中年最堅強後盾 | 合併 | 女性互助與支持網絡（`lifestyle-culture`） | 與 066、068 可形成社交 owner cluster。 |
| 098 | `social-energy-management`｜社交能量管理 | 保留 | 社交能量與內向者節奏（`lifestyle-culture`） | 問題具體，可保留。 |
| 099 | `stop-comparing-with-youth`｜別再拿現在的自己跟20歲比 | 合併 | 接受變化與熟齡自我觀（`lifestyle-culture`） | 可收進身份重整群，不需單獨擴張。 |
| 101 | `toxic-relationships-goodbye`｜拒絕任何有毒關係 | 保留 | 關係斷捨離（`lifestyle-culture`） | 受眾痛點強，適合保留。 |

## 健康恢復與身體節奏

| ID | 頁面 | 動作 | 目標群 | 原因 |
| --- | --- | --- | --- | --- |
| 010 | `joint-health-travel`｜關節主權與移動資產管理 | 保留 | 旅行體力與關節行動力（`wellness-movement` / `outdoor-escapes`） | 與春夏移動生活高度相符。 |
| 021 | `health-check-list-40plus`｜40+ 健康檢查清單 | 保留 | 健康檢查與預防（`wellness-movement`） | 搜尋意圖明確，可做 evergreen。 |
| 023 | `posture-correction-youth`｜骨架對齊與體態革命 | 合併 | 姿勢與體態穩定（`wellness-movement`） | 方向可用，但需去醫美式口吻。 |
| 024 | `self-massage-lymphatic`｜淋巴流動力與身心淨化 | 降權 | 恢復習慣（`wellness-movement`） | 醫療化風險高，應降權。 |
| 025 | `sugar-detox-impact`｜糖分權威與血糖革命 | 合併 | 血糖與飲食穩定（`wellness-movement`） | 主題可用，但標題過度聳動。 |
| 026 | `gut-health-second-brain`｜腸道權威與第二大腦革命 | 降權 | 腸道與情緒（`wellness-movement`） | 醫療化與概念化雙重過高。 |
| 027 | `water-hydration-anti-aging`｜水分主權與細胞水合 | 保留 | 春夏補水與疲勞恢復（`wellness-movement`） | 有季節性價值，適合重寫保留。 |
| 028 | `tcm-woman-40`｜漢方權威與經絡革命 | 降權 | 氣血與恢復（`wellness-movement`） | 醫療可信度要求高，不宜自動擴張。 |
| 032 | `eye-care-presbyopia`｜視能主權與熟齡視力革命 | 降權 | 老花與視力自我照護（`wellness-movement`） | YMYL 風險偏高。 |
| 033 | `hot-flashes-diet`｜更年期燥熱與飲食調整 | 保留 | 更年期熱感與飲食節奏（`wellness-movement`） | 春夏強相關，可直接保留。 |
| 034 | `sleep-well-menopause`｜更年期好眠革命 | 保留 | 更年期夜間恢復（`wellness-movement`） | 高需求 evergreen，可做 owner page。 |
| 035 | `bone-health-anti-aging`｜骨骼權威與存骨本美學 | 合併 | 骨質與中年行動力（`wellness-movement`） | 題目有價值，但應從審美語氣抽離。 |
| 038 | `aromatherapy-hormones`｜嗅覺權威與荷爾蒙共振 | 降權 | 芳香放鬆習慣（`wellness-movement`） | 醫療暗示過重，證據風險高。 |
| 039 | `40-body-revolution`｜40 歲身體革命 | 刪除 | - | 太空泛、重複度高，缺少明確 owner intent。 |
| 040 | `10-min-micro-exercise`｜10 分鐘微運動 | 保留 | 微運動與日常體力（`wellness-movement`） | 實用性強，容易與新企劃串連。 |
| 042 | `breathing-for-anxiety`｜腹式呼吸法 | 保留 | 焦慮緩解與呼吸（`wellness-movement`） | 問題清楚、低風險、可操作。 |
| 050 | `digital-detox-eye-brain`｜數位排毒，修復大腦與眼睛疲勞 | 合併 | 數位排毒與專注恢復（`wellness-movement`） | 題目可用，但可與視力／專注群整併。 |
| 054 | `emotional-eating-truth`｜情緒性進食的真相 | 保留 | 情緒性進食（`wellness-movement`） | 典型問題解法型。 |
| 078 | `menopause-is-second-youth`｜更年期是第二青春的開始 | 合併 | 更年期重新理解（`wellness-movement`） | 與 033、034 同 cluster。 |
| 080 | `mindfulness-in-chores`｜把家事變成正念修煉 | 刪除 | - | 概念化過高，搜尋與服務路徑弱。 |
| 097 | `smile-makeover-dental`｜牙齒美白與矯正找回自信笑容 | 降權 | 熟齡儀容照護（`casual-chic` / `wellness-movement`） | 牙科 YMYL 風險高，不宜主推。 |

## 風格、外型與春夏衣櫥

| ID | 頁面 | 動作 | 目標群 | 原因 |
| --- | --- | --- | --- | --- |
| 004 | `makeup-for-mature-skin`｜熟齡彩妝革命 | 合併 | 熟齡彩妝與減法保養（`casual-chic`） | 意圖有價值，但舊公式太重。 |
| 008 | `grey-hair-revolution`｜銀髮革命與原生美學 | 合併 | 白髮與自然造型（`casual-chic`） | 題目方向好，但要改寫。 |
| 009 | `hairstyle-frames-your-face`｜熟齡臉龐輪廓與髮型 | 合併 | 熟齡髮型與臉型平衡（`casual-chic`） | 可收成較強 owner page。 |
| 019 | `hand-neck-care-secrets`｜手頸次級區域美學 | 降權 | 熟齡細節保養（`casual-chic`） | 題目過碎，不宜繼續擴張。 |
| 020 | `manicure-magic-nails`｜指尖主權與手部資產管理 | 降權 | 指甲與手部保養（`casual-chic`） | 題目過窄、商業價值有限。 |
| 029 | `skincare-glow-not-anti-aging`｜熟齡護膚革命 | 合併 | 減法保養與肌膚光澤（`casual-chic`） | 可併入保養 owner page。 |
| 030 | `hair-loss-scalp-care`｜熟齡養髮革命 | 合併 | 頭皮與髮量照護（`casual-chic`） | 題意可保留，但口吻需收斂。 |
| 036 | `art-of-scarves`｜絲綢主權與纖維敘事美學 | 刪除 | - | 秋冬傾向強、概念感過重。 |
| 041 | `capsule-wardrobe-basics`｜40+ 女性膠囊衣櫥 | 保留 | 春夏膠囊衣櫥（`casual-chic`） | 與春夏策略高度一致。 |
| 045 | `comfortable-stylish-shoes`｜好走又時髦的美鞋 | 保留 | 久走鞋款選擇（`casual-chic`） | 強實用題，可保留。 |
| 048 | `declutter-closet-let-go`｜衣櫥斷捨離 | 保留 | 衣櫥整理與減法購物（`casual-chic`） | 與膠囊衣櫥可互相支撐。 |
| 051 | `dressing-for-body-type-curves`｜身型修飾完全指南 | 保留 | 身型修飾穿搭（`casual-chic`） | 搜尋意圖強，適合保留。 |
| 060 | `fabric-matters-cashmere-silk`｜投資羊絨與真絲 | 降權 | 材質判斷（`casual-chic`） | 春夏優先度低，且偏秋冬。 |
| 065 | `finding-your-style-at-40`｜找到妳的風格關鍵字 | 保留 | 熟齡個人風格（`casual-chic`） | owner page 潛力高。 |
| 070 | `glasses-chic-accessory`｜老花眼鏡也可以很時尚 | 合併 | 老花眼鏡作為配件（`casual-chic`） | 題目可用，但應併到配件 cluster。 |
| 074 | `jewelry-statement-pieces`｜Statement Pieces 點亮秋冬穿搭 | 降權 | 配件點綴（`casual-chic`） | 季節性偏秋冬，現階段不主推。 |
| 076 | `lingerie-internal-confidence`｜適合 40+ 身型的內在美 | 降權 | 基礎內著與舒適支撐（`casual-chic`） | 主題偏窄，暫不作擴張核心。 |
| 081 | `minimalism-skincare`｜熟齡肌膚的減法保養 | 保留 | 減法保養（`casual-chic`） | 方向成熟，與品牌語氣一致。 |
| 095 | `signature-scent-fragrance`｜尋找人生下半場的本命香 | 合併 | 香氣與個人風格（`casual-chic`） | 可留，但不需大量擴張。 |
| 102 | `vintage-sustainable-fashion`｜40+ 女性的古著入門 | 合併 | 古著與永續風格（`casual-chic`） | 題目有辨識度，但屬次要延伸題。 |

## 財務與長期安全

| ID | 頁面 | 動作 | 目標群 | 原因 |
| --- | --- | --- | --- | --- |
| 047 | `debt-be-gone-strategies`｜退休前必做的債務清零計畫 | 保留 | 中年前後的債務整理（`lifestyle-culture`） | 問題清楚、讀者價值高。 |
| 049 | `designing-dream-retirement`｜設計夢想退休生活 | 合併 | 退休生活與目的感（`lifestyle-culture`） | 與 075 可整併。 |
| 053 | `emergency-fund-peace`｜緊急預備金 | 保留 | 緊急預備金（`lifestyle-culture`） | 核心 evergreen 題。 |
| 059 | `estate-planning-legacy`｜遺產規劃是對家人最後的愛 | 合併 | 遺產規劃與家人溝通（`lifestyle-culture`） | 有價值，但應放在財務安全 cluster。 |
| 062 | `financial-independence-options`｜40+ 的財富自由其實是 Say No 的權利 | 保留 | 財務自主與選擇權（`lifestyle-culture`） | 可留，但後續標題應更務實。 |
| 063 | `financial-infidelity-partners`｜財務不忠比肉體出軌更可怕？ | 保留 | 伴侶金錢溝通（`lifestyle-culture`） | 與熟齡伴侶決策高度相關。 |
| 064 | `financial-literacy-kids`｜給孩子的財商教育 | 降權 | 親子金錢教育（`lifestyle-culture`） | 與本站主要受眾略有偏移。 |
| 072 | `insurance-audit-protection`｜40+ 必做的保單健檢 | 保留 | 保單風險盤點（`lifestyle-culture`） | 高實用、可留。 |
| 073 | `investment-101-fearless`｜理財新手的 ETF 與指數化投資 | 保留 | 投資入門（`lifestyle-culture`） | 意圖清楚，但需保守風險聲明。 |
| 075 | `late-starter-retirement`｜晚鳥理財族的退休追趕策略 | 合併 | 晚起步退休準備（`lifestyle-culture`） | 與 049 群組接近。 |
| 082 | `money-minimalism-abundance`｜金錢極簡主義 | 合併 | 花費與價值排序（`lifestyle-culture`） | 題目可用，但太觀念化。 |
| 084 | `passive-income-reality`｜破解被動收入迷思 | 保留 | 被動收入迷思拆解（`lifestyle-culture`） | 適合保留成反迷思題。 |
| 087 | `psychology-of-money-abundance`｜擺脫匱乏心態 | 合併 | 金錢焦慮與匱乏心態（`lifestyle-culture`） | 與 082、062 同群。 |
| 088 | `real-estate-investing-retirement`｜買房當包租婆還是退休的好主意嗎？ | 降權 | 不動產與退休現金流（`lifestyle-culture`） | 投資風險高，且非本站核心強項。 |
| 100 | `timeless-bag-investment`｜投資一個經典款包包 | 合併 | 經典包與消費決策（`casual-chic`） | 題意可留，但屬風格消費題，不必單獨做財務論述。 |

## 執行順序建議
1. 先做 `降權`
- 把 `life-proposals` 從首頁與分類策展的主力位置退下來。
- 暫停任何同類題型自動擴張。

2. 再做 `合併`
- 先建立或改寫 owner page，再把近似題導回去。
- 優先順序：
- 離婚 / 空巢 / 社交邊界
- 更年期睡眠 / 熱感 / 恢復
- 膠囊衣櫥 / 旅行穿搭 / 鞋包舒適度
- 第二曲線 / 副業 / AI 工作採用

3. 最後處理 `刪除`
- 先看流量、外鏈、是否已有站內引用。
- 若確定無殘值，再刪除或 301 到對應 owner page。
