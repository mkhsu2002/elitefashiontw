#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-five-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B05"

base.COVER_SOURCES = {
    "home-cooking-pan-tableware-storage-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379ddbe740819b9cea6ecc4ffa9443.png",
    "rental-small-appliance-kitchen-desk-cleaning-seasonal": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379e2b5710819b96ba7cb7f3eb3ba7.png",
    "travel-shoes-light-bag-crossbody-rain-backup-system": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379e7a8328819b924746cc05b29ae1.png",
    "living-room-work-corner-lighting-scent-storage-system": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379ecc0508819b90016ef008906558.png",
    "ai-workflow-laptop-monitor-cable-protection-backup": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379f21a9b8819bab404f0fce304a01.png",
}

ROW_OVERRIDES = {
    "home-cooking-pan-tableware-storage-order": {
        "elite_judgment": "先看一週真正會開火幾次，再決定鍋、盤、收納與茶食的順序。",
        "answer_summary": "居家餐桌應先處理開火頻率與收納，再買鍋具、餐具與茶食。",
        "risk_guardrail": "鍋具材質、餐具尺寸、食品成分與保存方式請以商品頁與包裝標示為準。",
    },
    "rental-small-appliance-kitchen-desk-cleaning-seasonal": {
        "elite_judgment": "租屋小家電要先看插座、清潔與收納，不要把暫住空間買成倉庫。",
        "answer_summary": "租屋小家電要按使用頻率、插座與收納順序逐步補齊。",
        "risk_guardrail": "電器規格、耗電、保固、安全限制與適用空間請以商品頁和官方標示為準。",
    },
    "travel-shoes-light-bag-crossbody-rain-backup-system": {
        "elite_judgment": "旅行鞋包的重點是走得到、拿得到、濕了有地方放，而不是照片最完整。",
        "answer_summary": "旅行鞋包配置應先看步行距離、拿取頻率與雨天備案。",
        "risk_guardrail": "鞋款尺寸、包款承重、防水或防潑資訊請以商品頁公告為準。",
    },
    "living-room-work-corner-lighting-scent-storage-system": {
        "elite_judgment": "光線先替空間分工，香氛和收納只負責讓轉場更安靜。",
        "answer_summary": "客廳與工作角落照明要先分工，再搭配香氛與收納。",
        "risk_guardrail": "燈具規格、香氛成分、電器限制與收納承重請以商品頁標示為準。",
    },
    "ai-workflow-laptop-monitor-cable-protection-backup": {
        "elite_judgment": "AI 工作流先看視窗、線材與備份，不要只把筆電規格當成效率。",
        "answer_summary": "AI 工作流周邊應先處理螢幕動線、線材相容與備份。",
        "risk_guardrail": "筆電、螢幕、線材、保護貼與備份設備的相容性、保固與規格請以商品頁為準。",
    },
}

base.TOPIC_HUBS = {
    "home-cooking-pan-tableware-storage-order": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
    "rental-small-appliance-kitchen-desk-cleaning-seasonal": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
    "travel-shoes-light-bag-crossbody-rain-backup-system": {
        "topicCategory": "bags-shoes-accessories",
        "topicCategoryLabel": "鞋包與配件",
        "primaryHub": {"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"},
        "secondaryHubs": [{"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}],
    },
    "living-room-work-corner-lighting-scent-storage-system": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "ai-work-reset-45", "title": "AI 工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"}],
    },
    "ai-workflow-laptop-monitor-cable-protection-backup": {
        "topicCategory": "ai-workflow",
        "topicCategoryLabel": "AI 工作流",
        "primaryHub": {"key": "ai-work-reset-45", "title": "AI 工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
}

base.BLUEPRINTS = {
    "home-cooking-pan-tableware-storage-order": {
        "heroAlt": "陽光木質餐桌上有無品牌黑色鐵鍋、陶瓷杯盤、茶壺、餐具收納盒、布巾與玻璃罐",
        "audience": "想建立居家餐桌、週末煮食與日常茶食秩序的讀者",
        "excerpt": "居家餐桌不是先買最漂亮的鍋或杯盤，而是先看一週真正開火幾次、如何收納、誰會一起使用。",
        "tags": ["居家餐桌", "鍋具", "餐具", "收納工具"],
        "intro": "居家餐桌的購物順序，常被一張漂亮照片帶偏：先買鍋、先買杯盤、先買茶食禮盒，最後卻發現櫃子放不下、鍋子太重、餐具不常用。真正成熟的順序，是從一週開火次數、用餐人數與收納位置開始，再讓鍋具、餐具與茶食進入日常。",
        "editorialAngle": "先看開火頻率與收納，再讓鍋具和杯盤進入清單。",
        "sections": [
            ("先算一週會開火幾次", "每週只煮一到兩次的人，不需要先買完整鍋具線；每天煮食的人，才更需要看鍋型、重量與清潔方式。", "廚藝日本鍋具館、鐵本舖台灣鐵鍋與 Home & Ceramics 可放在鍋具與陶瓷器物裡比較；材質和使用限制要回商品頁確認。"),
            ("杯盤要看餐桌尺寸，不只看照片", "兩人桌、吧台和大餐桌需要的杯盤比例不同。餐具太大會讓餐桌變擠，太多套會讓櫃子先失守。", "大正餐具批發零售適合放在杯盤補齊情境中看；尺寸、耐熱與清潔方式以商品頁為準。"),
            ("收納工具應該在購買前就存在", "如果鍋蓋、碗盤、筷匙與茶具沒有位置，再好的餐桌選物都會變成檯面負擔。先留出停靠點，才不會一直買收納補救。", "Elite Fashion 編輯團隊的判斷是：餐桌質感不是物件多，而是每一次用完都能回復。"),
            ("茶食與伴手禮要看保存與共享", "暮朝食粹與 Teavoya 這類茶食可以讓餐桌更完整，但食品與茶品要看保存期限、成分、開封方式與是否適合共享。", "本文不承諾食品、茶品或餐具帶來任何健康效果，所有資訊以商品頁與包裝標示為準。"),
            ("下單前四件事", "量櫃子、量桌面、想清楚開火頻率、確認誰會清洗。這四件事比一次買齊更能保住餐桌秩序。", "價格、規格、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("居家餐桌應先買鍋還是杯盤？", "先看開火頻率。如果常煮，鍋具優先；若多半外食，杯盤與收納可能更先影響日常。"),
            ("餐具要一次買整套嗎？", "不一定。先依用餐人數和桌面尺寸補齊基本款，再慢慢增加。"),
            ("茶食可以當成健康推薦嗎？", "不可以。本文只討論餐桌情境，成分與保存方式請以商品頁和包裝標示為準。"),
        ],
    },
    "rental-small-appliance-kitchen-desk-cleaning-seasonal": {
        "heroAlt": "明亮租屋套房裡有無品牌小電鍋、快煮壺、小風扇、桌燈、清潔刷具、毛巾與收納推車",
        "audience": "租屋、短期居住或小坪數生活中，需要逐步補齊小家電的人",
        "excerpt": "租屋小家電不要一次買滿，先看插座、收納、清潔與季節需求，再決定廚房、桌面與清潔電器。",
        "tags": ["租屋小家電", "小宅生活", "季節電器", "清潔工具"],
        "intro": "租屋最容易把小家電買成一種安心感：快煮壺、小電鍋、電風扇、桌燈、清潔機具都想一次補齊。但租屋空間的限制很直接，插座、檯面、收納、清潔與搬家成本，會比商品功能更快決定它是否留下。",
        "editorialAngle": "租屋小家電要先看插座、清潔與收納，不要一次買滿。",
        "sections": [
            ("先盤點插座和檯面", "廚房小家電最常卡在插座不足、檯面太小和清潔不順。買之前先畫出固定位置，沒有固定位置的電器通常很快會被收起來。", "KINYO、Airmate 與心科技生活家電館可作為廚房和季節電器比較入口；耗電、保固和安全限制請回商品頁確認。"),
            ("桌面電器要服務工作，不是佔據工作", "桌燈、小風扇、充電座和收納推車都可能改善租屋生活，但如果讓桌面更擠，就會削弱工作效率。", "燈后與 SENGLI 適合放在照明與質感小家電中參考；尺寸、亮度、供電方式要看商品頁。"),
            ("清潔用品要和收納一起買", "小吸塵、刷具或拖把若沒有晾乾和收納位置，只會變成另一個佔空間的物件。", "真蓁嚴選清潔生活館可作為掃除工具補充；本文不宣稱任何抗菌、除菌或安全效果。"),
            ("季節電器先租屋測試，再升級", "夏季風扇、冬季保暖、雨季除濕或照明都和房間條件有關。住滿兩週後再補齊，通常比入住第一天買滿更準。", "Elite Fashion 編輯團隊的判斷是：租屋採買要讓下一次搬家仍然輕。"),
            ("下單前檢查", "插座、清潔、收納、搬家重量、保固。五件事都能回答，再看外型與活動。", "價格、規格、活動、庫存、適用空間與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("租屋小家電可以一次買齊嗎？", "不建議。先住一段時間，確認插座、檯面和收納，再分批補。"),
            ("季節電器什麼時候買？", "等確定房間日照、通風和濕度後再買，會比入住當天更準。"),
            ("清潔工具要怎麼選？", "先看晾乾位置和收納方式，再比較功能與價格。"),
        ],
    },
    "travel-shoes-light-bag-crossbody-rain-backup-system": {
        "heroAlt": "飯店床邊擺放無品牌白色好走鞋、深藍輕量包、米色貼身小包、折傘、收納袋與旅行衣物",
        "audience": "需要在城市旅行、短程出國或週末移動中整理鞋包系統的人",
        "excerpt": "旅行鞋包配置要先看步行距離、拿取頻率與雨天備案，再決定好走鞋、輕量包與貼身小包。",
        "tags": ["旅行鞋", "輕量包", "貼身小包", "雨天備案"],
        "intro": "旅行鞋包不是越多越安心。真正影響旅程的是一天走多少路、哪些物品要隨手拿、雨天濕物放哪裡，以及回程是否還有空間。好走鞋、輕量包、貼身小包和雨具要像一組系統，而不是各買各的。",
        "editorialAngle": "走得到、拿得到、濕了有地方放，才是旅行鞋包的核心。",
        "sections": [
            ("先估一天步行距離", "如果一整天都在城市移動，鞋款比包款更早決定疲勞感。鞋底、重量、鞋口和穿脫便利度，都要比造型照片更早看。", "95 SNEAKER、UD LAB 與 S′AIME東京企劃可放在鞋款、輕量包和小包裡比較；尺寸與材質以商品頁為準。"),
            ("貼身小包負責高頻拿取", "護照、手機、票卡、房卡和少量現金不應一直埋在大包深處。貼身小包的價值，是讓高頻物品有自己的位置。", "PPBOX 與 Heine 海恩後背包可作為包款補充參考；承重、防潑或隔層資訊要回商品頁確認。"),
            ("雨天備案不要放在最底層", "折傘、雨罩或濕物袋若放在包底，下雨時整個包都會被翻亂。雨具要能快速拿到，也要有用後收納位置。", "FULTON 富爾頓皇家晴雨傘可放在旅行雨具情境中比較；本文不保證任何天候適用。"),
            ("常見錯誤：一雙鞋走全程", "一雙鞋能否走完全程，不只看舒適，也看衣著場合、下雨、晚餐場景與腳部狀態。若行程跨度大，鞋款策略要更保守。", "Elite Fashion 編輯團隊的判斷是：旅行風格不是少帶，而是每件都知道自己的任務。"),
            ("出發前排一次包內動線", "先放貼身小包，再放雨具，最後放衣物與備品。能在十秒內拿到手機、房卡與傘，旅行就會安靜很多。", "價格、規格、尺寸、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("旅行一定要帶貼身小包嗎？", "若有高頻拿取的證件、票卡或手機，貼身小包會讓動線更穩。"),
            ("好走鞋怎麼選？", "先看步行距離、鞋底、重量和穿脫便利度，再看造型。"),
            ("雨具應該放哪裡？", "放在外層或獨立袋，避免下雨時翻亂整個包。"),
        ],
    },
    "living-room-work-corner-lighting-scent-storage-system": {
        "heroAlt": "夜晚客廳工作角落有黑色桌燈、暖色層架燈、無標籤香氛瓶、收納盒、植物與無品牌筆電",
        "audience": "需要在客廳兼工作角落中安排照明、香氛與收納的人",
        "excerpt": "客廳與工作角落照明要先讓空間分工，再搭配香氛與收納，不要只靠一盞燈解決所有情境。",
        "tags": ["客廳照明", "工作角落", "香氛", "收納"],
        "intro": "客廳兼工作角落最怕光線沒有分工：看書、開會、休息、收納都用同一種亮度，空間自然很難切換。吸頂燈、桌燈、香氛和收納不是裝飾清單，而是讓一個角落能從工作轉回生活的節奏設計。",
        "editorialAngle": "光線先替空間分工，香氛和收納讓轉場更安靜。",
        "sections": [
            ("先分工作光和休息光", "工作需要清楚、穩定、不刺眼；休息需要低亮度和柔和陰影。若兩者都靠同一盞燈，客廳很容易一直停在工作狀態。", "燈后、灰調與 SENGLI 可作為照明、香氛和小家電參考；規格、色溫與用電限制請看商品頁。"),
            ("香氛應放在清潔與通風之後", "香氛不是整理工具。先讓桌面、線材、紙本和收納回到位置，通風後再使用香氛，氣味才不會變成掩蓋混亂。", "au fait 無非與 Hysure 海說可作為香氛和居家設備情境補充；本文不宣稱助眠、療癒或淨化效果。"),
            ("收納盒要收掉轉場物品", "客廳工作角落最容易堆的是筆記本、充電器、文件、遙控器和杯子。收納盒或層架的任務，是讓工作結束後能快速收尾。", "完美主義可放在收納家具情境中比較；尺寸、承重和材質仍以商品頁為準。"),
            ("常見錯誤：只買漂亮桌燈", "桌燈很重要，但如果吸頂光太刺、線材太亂、香氛太近，工作角落仍然不安靜。要先處理光線層次，再看單品。", "Elite Fashion 編輯團隊的判斷是：好的角落讓你知道現在該工作，什麼時候可以停下來。"),
            ("下單前的三層光線檢查", "主燈、任務燈、情境燈三層是否各有任務。若一盞燈被要求做所有事，就該先調整配置。", "價格、規格、活動、庫存、香味描述與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("客廳工作角落先買桌燈嗎？", "先看主燈和工作需求。如果主燈太刺或太暗，再補桌燈會更準。"),
            ("香氛能改善睡眠或情緒嗎？", "本文不宣稱助眠、療癒或健康效果，只討論空間轉場與使用情境。"),
            ("收納盒要放哪裡？", "放在工作結束後最容易堆東西的位置，讓線材、文件和小物能快速歸位。"),
        ],
    },
    "ai-workflow-laptop-monitor-cable-protection-backup": {
        "heroAlt": "石墨色工作桌上有無品牌筆電、外接螢幕、USB-C 線材、透明保護貼、備份硬碟與空白筆記本",
        "audience": "需要建立 AI 工作流程、外接螢幕與資料備份配置的知識工作者",
        "excerpt": "AI 工作流周邊不是只買更強筆電，而是先處理螢幕動線、線材相容、保護與備份。",
        "tags": ["AI 工作流", "外接螢幕", "筆電周邊", "資料備份"],
        "intro": "AI 工作流會讓視窗變多、檔案變多、輸入輸出變快；如果周邊沒有跟上，效率會卡在線材、螢幕切換和資料備份。筆電、外接螢幕、線材、保護貼與備份設備應該一起規劃，而不是看到規格升級就下單。",
        "editorialAngle": "先看視窗、線材與備份，不要只把筆電規格當成效率。",
        "sections": [
            ("先數你的工作視窗", "AI 工具、文件、資料表、瀏覽器、通訊軟體和素材資料夾會同時打開。外接螢幕是否值得買，取決於你每天切換多少視窗。", "華克電腦、REAICE 與日本橋3C 可作為筆電、螢幕和周邊比較入口；本文不假裝實測效能。"),
            ("線材相容比想像中更關鍵", "外接螢幕、充電、硬碟和轉接器都可能卡在接口與線材規格。若線材沒有先確認，桌面會看起來完整，實際上不能順利工作。", "Momax Taiwan 與聯威電腦可作為線材與周邊補充；相容性、速度和供電以商品頁標示為準。"),
            ("保護貼和備份不是最後的小配件", "筆電保護、螢幕保護和資料備份都在降低中斷成本。當 AI 工作流開始累積大量素材和版本，備份就不該等到出事後才做。", "EZstick 3C商品保護賣場可放在保護貼與周邊維護情境中看；備份設備容量、速度和保固需回商品頁確認。"),
            ("常見錯誤：讓規格掩蓋流程", "更大的螢幕、更快的線材和更強筆電，不會自動整理工作流程。若檔案命名、資料夾和備份規則混亂，規格只會讓混亂更快發生。", "Elite Fashion 編輯團隊的判斷是：AI 工作桌的價值是降低切換成本，不是堆滿設備。"),
            ("下單前的工作桌檢查", "視窗數量、接口、供電、線長、備份位置、保護方式。六件事確認後，再比較品牌與價格。", "價格、規格、活動、庫存、保固、相容性與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("AI 工作流一定需要外接螢幕嗎？", "不一定。若每天有大量視窗切換，外接螢幕才更有價值。"),
            ("線材可以到貨後再補嗎？", "可以，但更容易延誤使用。建議下單前先確認接口、供電和線長。"),
            ("備份設備應該什麼時候買？", "當你開始累積素材、版本和客戶檔案時，備份就應該和工作流程一起規劃。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[20:25]:
        copied = dict(row)
        copied.update(ROW_OVERRIDES[copied["slug"]])
        selected.append(copied)
    return selected


def update_tracker(articles: list[dict[str, Any]], tracker_rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    by_merchant = {row["merchant_id"]: row for row in tracker_rows}
    mentions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in articles:
        for product in [*article.get("mainProducts", []), *article.get("sidebarProducts", [])]:
            mentions[product["merchantId"]].append(article)
    for merchant_id, hits in mentions.items():
        row = by_merchant[merchant_id]
        row["coverage_status"] = "live"
        row["article_created"] = "true"
        row["link_status"] = "usable"
        row["risk_notes"] = row.get("risk_notes") or "不使用誇大推薦語氣，商品規格以 momo 商品頁為準"
        slugs = [item for item in row.get("article_slug", "").split(";") if item]
        urls = [item for item in row.get("live_url", "").split(";") if item]
        increment = 0
        for article in hits:
            if article["slug"] not in slugs:
                slugs.append(article["slug"])
                increment += 1
            if article["url"] not in urls:
                urls.append(article["url"])
        row["article_slug"] = ";".join(slugs)
        row["live_url"] = ";".join(urls)
        try:
            existing_mentions = int(row.get("mention_count") or 0)
        except ValueError:
            existing_mentions = 0
        row["mention_count"] = str(existing_mentions + increment)
        row["last_mentioned_at"] = base.TODAY
        note = "2026-06-21 momo 收益型內容第五組 5 篇已置入。"
        if note not in row.get("notes", ""):
            row["notes"] = (row.get("notes", "").rstrip() + (" " if row.get("notes", "").strip() else "") + note).strip()
    with base.TRACKER_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(tracker_rows)


def update_latest_run(config: dict[str, Any], articles: list[dict[str, Any]]) -> None:
    base.pipeline.write_json(
        base.ROOT / config["paths"]["latestRunJson"],
        {
            "version": 1,
            "updatedAt": base.pipeline.now_iso(),
            "status": "generated",
            "triggerType": base.TRIGGER_TYPE,
            "queueId": base.QUEUE_ID,
            "newsletter": "not_sent_manual_codex_publish",
            "articleIds": [article["id"] for article in articles],
            "articleSlugs": [article["slug"] for article in articles],
            "notes": "Codex 手動生成 momo 收益型內容第五組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
