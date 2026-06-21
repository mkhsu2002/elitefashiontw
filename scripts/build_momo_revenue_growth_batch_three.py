#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-three-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B03"

base.COVER_SOURCES = {
    "meeting-grooming-hair-makeup-scent-small-bag-kit": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a37958aa90c81909f8718321f6aafaf.png",
    "travel-luggage-front-open-carry-on-packing-system-2": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a3795d246648190a485863cb327a6ae.png",
    "small-home-entry-closet-desk-cleaning-storage-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a379621c7fc81908b8bfd008c92014e.png",
    "workday-knee-back-support-cushion-bag-weight-guide": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a379680d0c8819099730c52bf3db7aa.png",
    "office-snack-cabinet-low-sugar-nuts-vegetarian-drinks": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a3796e3e9808190b86cacff052312e5.png",
}

base.TOPIC_HUBS = {
    "meeting-grooming-hair-makeup-scent-small-bag-kit": {
        "topicCategory": "beauty-grooming",
        "topicCategoryLabel": "妝髮與身體照護",
        "primaryHub": {
            "key": "commute-style-reset",
            "title": "通勤衣櫥與鞋包選物指南",
            "file": "commute-style-reset.html",
            "url": "/commute-style-reset",
            "category": "casual-chic",
        },
        "secondaryHubs": [
            {
                "key": "mature-life-reset",
                "title": "人生重整與一人生活秩序",
                "file": "mature-life-reset.html",
                "url": "/mature-life-reset",
                "category": "lifestyle-culture",
            }
        ],
    },
    "travel-luggage-front-open-carry-on-packing-system-2": {
        "topicCategory": "travel-planning",
        "topicCategoryLabel": "旅行準備",
        "primaryHub": {
            "key": "outdoor-travel-reset",
            "title": "旅行與戶外移動準備指南",
            "file": "outdoor-travel-reset.html",
            "url": "/outdoor-travel-reset",
            "category": "outdoor-escapes",
        },
        "secondaryHubs": [
            {
                "key": "commute-style-reset",
                "title": "通勤衣櫥與鞋包選物指南",
                "file": "commute-style-reset.html",
                "url": "/commute-style-reset",
                "category": "casual-chic",
            }
        ],
    },
    "small-home-entry-closet-desk-cleaning-storage-order": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {
            "key": "mature-life-reset",
            "title": "人生重整與一人生活秩序",
            "file": "mature-life-reset.html",
            "url": "/mature-life-reset",
            "category": "lifestyle-culture",
        },
        "secondaryHubs": [
            {
                "key": "body-rhythm-reset",
                "title": "身體節奏與恢復生活指南",
                "file": "body-rhythm-reset.html",
                "url": "/body-rhythm-reset",
                "category": "wellness-movement",
            }
        ],
    },
    "workday-knee-back-support-cushion-bag-weight-guide": {
        "topicCategory": "care-support",
        "topicCategoryLabel": "照護與輔具",
        "primaryHub": {
            "key": "body-rhythm-reset",
            "title": "身體節奏與恢復生活指南",
            "file": "body-rhythm-reset.html",
            "url": "/body-rhythm-reset",
            "category": "wellness-movement",
        },
        "secondaryHubs": [
            {
                "key": "commute-style-reset",
                "title": "通勤衣櫥與鞋包選物指南",
                "file": "commute-style-reset.html",
                "url": "/commute-style-reset",
                "category": "casual-chic",
            }
        ],
    },
    "office-snack-cabinet-low-sugar-nuts-vegetarian-drinks": {
        "topicCategory": "food-nutrition",
        "topicCategoryLabel": "飲食與補給",
        "primaryHub": {
            "key": "body-rhythm-reset",
            "title": "身體節奏與恢復生活指南",
            "file": "body-rhythm-reset.html",
            "url": "/body-rhythm-reset",
            "category": "wellness-movement",
        },
        "secondaryHubs": [
            {
                "key": "mature-life-reset",
                "title": "人生重整與一人生活秩序",
                "file": "mature-life-reset.html",
                "url": "/mature-life-reset",
                "category": "lifestyle-culture",
            }
        ],
    },
}

base.BLUEPRINTS = {
    "meeting-grooming-hair-makeup-scent-small-bag-kit": {
        "heroAlt": "明亮化妝台上有無品牌米色整理包、黑色手提包、木柄髮刷、補妝刷具、小鏡子與柔軟毛巾",
        "audience": "需要在會議、通勤與晚間行程之間維持清爽儀容的讀者",
        "excerpt": "會議整理包不是把浴室搬進包裡，而是把會議前五分鐘最常用到的髮品、補妝工具與小包位置排清楚。",
        "tags": ["會議整理包", "補妝工具", "小包收納", "通勤儀容"],
        "intro": "真正好用的會議整理包，不是品項最多的那一個，而是你在會議前五分鐘能快速找到的那一個。髮品、補妝、香氛、小毛巾與小包都可能有用，但只要沒有順序，就會變成包內雜訊。本文把整理包拆成儀容摩擦點、拿取頻率、清潔與補貨四個層次，讓通勤包保有空間，也讓會議前後的整理更從容。",
        "editorialAngle": "先補最容易被看見的儀容摩擦點，再決定香氛和備用品是否需要進包。",
        "sections": [
            ("先列會議前五分鐘會用到的東西", "整理包的第一層，只放真正會在會議前五分鐘拿出來的物件：小鏡子、補妝工具、髮夾或小梳、紙巾與必要的清潔小物。不是每一件好看的用品都該進包。", "S′AIME東京企劃、GINGER MAKE UP 與 BAYBEYLA 可以分別放在小包、化妝收納與刷具情境中比較，但妝效、髮品表現與成分限制仍要回商品頁確認。"),
            ("髮品與補妝不要混在同一層", "髮品、刷具、粉餅、唇彩與小毛巾的清潔要求不同。若全部混放，容易讓整理包看起來很滿，真正要拿時卻不好找。", "Apode 歐美專業髮品、MORINO 與 UD LAB 可作為髮品、毛巾與小包補充參考；本文不宣稱任何美妝或髮品效果。"),
            ("香氛是最後一層，不是必要主角", "香氛小物可以讓會議前整理更完整，但它應該放在清潔、儀容和衣物狀態之後。若包內空間有限，香氛應該比補妝工具更容易被刪減。", "選擇氣味用品時，要看容量、保存方式與使用場合，不把個人喜好寫成所有人都適合的推薦。"),
            ("小包的尺寸由最大件工具決定", "很多人先買小包，再勉強把物品塞進去；更穩的做法，是先放入最大件工具，再決定包款深度和開口。", "如果最大件是髮刷或化妝刷，開口就要好拿；如果只是唇彩與小鏡，薄型小包就能降低重量。"),
            ("台灣通勤情境要多看濕熱與移動", "濕熱天氣、機車通勤、捷運擁擠和辦公室冷氣，都會讓整理包的清潔和材質更重要。布面、拉鍊與內袋是否容易擦拭，比漂亮照片更接近日常。", "若商品頁沒有清楚標示材質、清潔方式或尺寸，建議先暫緩，不要只靠想像下單。"),
            ("下單前的整理包清單", "把用品分成每日必帶、會議前使用、雨天備案和晚間行程四類。每一類最多留一到兩件，才不會讓整理包變成負擔。", "價格、規格、活動、庫存、成分與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("會議整理包要放哪些東西？", "先放會議前五分鐘會用到的物品，例如小鏡子、補妝工具、簡易髮夾或清潔小物，再依包內空間增減。"),
            ("髮品和補妝工具可以一起放嗎？", "可以放在同一個整理包，但建議分層或分袋，避免清潔需求不同造成混亂。"),
            ("香氛小物需要必帶嗎？", "不一定。香氛應放在最後一層考量，且需看使用場合、容量與個人習慣。"),
        ],
    },
    "travel-luggage-front-open-carry-on-packing-system-2": {
        "heroAlt": "陽光臥室中，無品牌前開式行李箱、登機箱、收納袋、折傘、旅行小包與衣物整齊排列",
        "audience": "準備出國旅行、短程商務行程或週末移動，需要重新整理箱包系統的讀者",
        "excerpt": "箱包系統要先用旅程天數與拿取頻率決定箱體，再比較前開式行李箱、登機箱與收納袋。",
        "tags": ["前開式行李箱", "登機箱", "旅行收納", "出國準備"],
        "intro": "出國前買行李箱，最容易被外型、容量和照片裡的整齊感帶走。但真正會影響旅程的是：你要走幾天、移動幾次、哪些東西需要在機場或飯店門口快速拿到。前開式行李箱、登機箱、收納袋與隨身小包不是互相取代，而是一套拿取頻率的安排。",
        "editorialAngle": "先用天數決定箱體，再用拿取頻率決定前開、分層與隨身小包。",
        "sections": [
            ("旅程天數決定箱體，不是照片決定", "三天兩夜、五天四夜與十天以上旅行，需要的不是同一種箱體。先估衣物、鞋、盥洗、伴手禮與回程空間，再看是否需要前開或分層。", "ENDUO恩多箱包、DW優選家官方直營店與戶外趣可放在箱體、登機箱與旅行用品裡比較；尺寸與限制仍以航空公司和商品頁公告為準。"),
            ("前開式適合高頻拿取，不是所有人都需要", "前開式行李箱的價值，在於筆電、文件、外套或臨時用品需要快速拿取。若你的行程多在飯店一次展開，傳統箱體加收納袋也可能更簡潔。", "不要只因為前開看起來方便就購買；先想自己會在哪裡、用哪隻手、開幾次箱。"),
            ("收納袋要照使用時機分，不照顏色分", "衣物袋、內衣袋、盥洗袋、電子配件袋與雨具袋應依使用時間排序。第一晚會用到的放上層，回程才用的放底層。", "UD LAB、FULTON 富爾頓皇家晴雨傘與 S′AIME東京企劃可作為小包、雨具與隨身整理補充參考。"),
            ("登機箱要同時看尺寸、重量與輪子", "登機箱不只看容量，還要看空箱重量、輪子滑順度、拉桿穩定與航空限制。若常轉機或搭大眾運輸，輪子和把手比多一點容量更重要。", "航空公司對尺寸、重量、電池和液體等限制可能變動，出發前請以官方公告為準。"),
            ("常見錯誤：把所有備案都放進大箱", "雨具、藥品、充電器、證件影本和第一天會穿的外套若都在大箱深處，遇到延誤或天氣變化就很麻煩。備案要放在能快速拿到的位置。", "箱包系統的成熟感，來自每一件物品都知道自己該在旅程哪一刻被拿出來。"),
            ("出發前的箱包檢查", "先確認航空尺寸與重量，再確認證件、充電、雨具、第一晚衣物和回程空間。最後才是造型與顏色。", "價格、活動、規格、庫存、材質和配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("前開式行李箱適合誰？", "適合需要在機場、車站或飯店外快速拿取文件、筆電、外套或小物的人。"),
            ("登機箱尺寸可以只看商品頁嗎？", "不建議。商品頁是參考，航空公司最新尺寸與重量限制仍要出發前確認。"),
            ("收納袋要買很多嗎？", "不用先追求數量。依使用時機分成衣物、盥洗、電子、雨具與回程五類即可。"),
        ],
    },
    "small-home-entry-closet-desk-cleaning-storage-order": {
        "heroAlt": "小宅玄關、衣櫃、書桌與清潔工具區整齊連成一排，木質家具、綠色布品與收納盒形成清爽生活感",
        "audience": "住在小宅、租屋或需要重新安排玄關衣櫃與工作桌的人",
        "excerpt": "小宅收納的核心不是買更多盒子，而是先替物品安排停靠點，再看玄關、衣櫃、書桌與清潔工具如何接上動線。",
        "tags": ["小宅收納", "玄關整理", "衣櫃收納", "清潔工具"],
        "intro": "小宅收納最常見的誤會，是以為多買盒子就會變整齊。實際上，盒子只會把問題延後：東西沒有固定停靠點，明天還是會回到桌面、椅背和地上。本文從回家後的第一個動作開始，把玄關、衣櫃、書桌與清潔工具區串成一條日常動線。",
        "editorialAngle": "先替物品安排停靠點，再決定容器、層架與清潔工具。",
        "sections": [
            ("玄關是小宅的第一個壓力測試", "包、鞋、鑰匙、口罩、信件和外套都會在玄關交會。若沒有托盤、鞋位和暫放區，小宅很快會從門口開始失控。", "完美主義、真蓁嚴選清潔生活館與壹品輕奢家居館可分別放在收納家具、清潔工具與小宅家居中比較；承重、尺寸與材質仍要看商品頁。"),
            ("衣櫃不要先買盒子，先分穿著頻率", "常穿的衣服要拿得到，季節備品才適合收進盒子。若先買一排收納盒，反而可能把每天要穿的東西藏起來。", "SUSS Living生活良品與 Awayuki淡雪 日本製精品可作為小物與生活用品補充參考，但不保證適合所有坪數或衣櫃深度。"),
            ("書桌收納的標準是能否重新開始工作", "桌面不必空無一物，但要能在三十秒內回到可工作的狀態。文件、筆、充電器、耳機與水杯都要有固定位置。", "灰調 生活家飾選品可放在燈飾、花器或桌面氛圍中參考；照明與香氛不應取代真正的桌面整理。"),
            ("清潔工具要靠近髒污發生處", "掃把、拖把、抹布和替換耗材若藏太遠，清潔就會變成大型任務。把工具放在髒污最常發生的附近，才有機會真的使用。", "購買前先看收納高度、晾乾方式、替換耗材與可否不釘牆，不要只看商品照是否整齊。"),
            ("台灣小宅要預留濕氣與通風", "玄關鞋位、浴室旁清潔工具和衣櫃深處都容易遇到濕氣。收納容器若不通風，反而可能讓日常維護變麻煩。", "本文不宣稱任何商品具備防潮、除味或承重效果；相關資訊請以商品頁與官方標示為準。"),
            ("下單前畫一條回家路線", "從門口到放包、脫鞋、掛外套、洗手、坐下工作，把每一步畫出來。買收納用品前先問：這件東西能讓哪一步少一次彎腰、少一次尋找或少一次堆放？", "價格、尺寸、材質、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("小宅收納第一步該買什麼？", "第一步不是購買，而是畫出回家後的動線，確認包、鞋、鑰匙、衣物與清潔工具的停靠點。"),
            ("收納盒越多越好嗎？", "不一定。收納盒若沒有分類和拿取邏輯，只會把混亂藏起來。"),
            ("清潔工具要怎麼收？", "放在髒污最常發生且容易晾乾的位置，並確認高度、替換耗材與收納方式。"),
        ],
    },
    "workday-knee-back-support-cushion-bag-weight-guide": {
        "heroAlt": "明亮辦公室裡，無品牌人體工學椅、腰靠坐墊、膝部支撐套、灰色工作包與休閒鞋排列在木桌旁",
        "audience": "久坐工作、通勤負重或需要日常支撐用品比較的人",
        "excerpt": "腰背與膝蓋支撐用品只能協助日常配置，選購前要先看疼痛是否需要專業協助，再比較護具、坐墊與鞋包重量。",
        "tags": ["久坐支撐", "護膝護腰", "坐墊", "通勤包重量"],
        "intro": "久坐工作日的不舒服，很容易讓人想立刻買護腰、護膝或坐墊。但日常支撐用品不是診斷，也不是治療；它們更像是把工作椅、桌高、包重與移動方式重新安排。本文用保守的順序看腰背、膝蓋、坐墊與鞋包重量，避免把支撐用品寫成萬能答案。",
        "editorialAngle": "先判斷是否需要專業協助，再看日常用品是否能降低摩擦與負重。",
        "sections": [
            ("先分辨不舒服是否已超出日常調整", "若疼痛、麻木、無力或活動受限持續出現，應先尋求專業協助，不應用購物清單自行處理。日常支撐用品只能放在生活配置與使用舒適度裡討論。", "BELEX、大來護具 Mo+ 與 Sports Support 可作為護具與支撐用品比較入口；本文不承諾矯正、治療、止痛或醫療效果。"),
            ("坐墊與腰靠要和椅子一起看", "坐墊不是放上去就完成。椅面深度、桌高、螢幕位置、雙腳是否能踩穩，都會影響使用感。", "完美主義可作為居家或辦公家具補充參考；尺寸、材質、承重與適用條件仍需回商品頁確認。"),
            ("膝蓋支撐要看使用時刻", "護膝或支撐配件可能出現在通勤、運動、久站或搬重物時，但每種情境的需求不同。把它當成全天候用品前，先確認穿戴時間、透氣與活動限制。", "Cool Sport Support 巴酷運動與 Sports Support 可在運動配件情境中比較；涉及個人身體狀況時，請以專業建議為準。"),
            ("包包重量常是被忽略的支撐問題", "筆電、充電器、水壺、文件和整理包每天累積在同一側肩膀上，比單一護具更容易被忽略。先減重，再談支撐用品，才是更成熟的順序。", "UD LAB 可放在通勤小包與分層情境裡看，但是否適合承重或長時間背負仍要看商品頁。"),
            ("常見錯誤：把護具當成工作流程補丁", "若椅子高度不對、螢幕太低、長時間不休息，護具很容易被期待承擔太多。先調整工作流程，再決定是否需要支撐用品。", "每五十到六十分鐘起身走動、重新放鬆肩頸與調整坐姿，通常比一直加裝用品更可持續。"),
            ("下單前的保守檢查", "確認身體狀況、使用時刻、穿戴時間、清潔方式、尺寸與退換貨條件。任何涉及不適或疼痛的問題，都不要只靠商品描述判斷。", "價格、規格、材質、活動、庫存、適用限制與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("護腰或護膝可以治療疼痛嗎？", "本文不做治療、矯正或止痛承諾。若疼痛、麻木或活動受限持續出現，請先尋求專業協助。"),
            ("坐墊需要搭配椅子看嗎？", "需要。椅面深度、桌高、螢幕位置與腳部支撐都會影響使用感。"),
            ("通勤包重量和腰背有關嗎？", "可能影響日常負重感受。建議先減少不必要物品，再看包款分層與支撐用品。"),
        ],
    },
    "office-snack-cabinet-low-sugar-nuts-vegetarian-drinks": {
        "heroAlt": "辦公室木質零食櫃裡，玻璃罐裝堅果、素食零嘴、無字紙袋與沖泡飲小包整齊分層收納",
        "audience": "想替辦公室、居家工作角落或加班時段建立零食櫃的人",
        "excerpt": "低負擔零食櫃要看份量、保存與口味疲乏，不把低醣、堅果、素食零嘴或沖泡飲寫成健康捷徑。",
        "tags": ["辦公室零食", "低醣點心", "堅果", "沖泡飲"],
        "intro": "零食櫃不是自律象徵，也不是健康標語的展示牆。它更像一個下午與加班時段的備案：你需要知道份量、保存方式、口味是否容易疲乏，以及哪些東西適合共享。本文用更保守的方式整理低醣點心、堅果、素食零嘴與沖泡飲，讓補貨回到生活節奏，而不是口號。",
        "editorialAngle": "用份量、保存方式與共享便利性決定零食櫃，不用健康標語決定。",
        "sections": [
            ("先決定零食櫃服務哪一段時間", "下午三點、加班前、會議間或下班後，零食櫃的內容會完全不同。先定義使用時段，才知道要補單份包、堅果、沖泡飲或較有飽足感的小點。", "D醣一刻、囍素堅果與本草養生 From Nature 可放在不同零食與飲品情境裡比較；本文不宣稱控糖、減重、代謝或保健效果。"),
            ("份量比大包裝更重要", "辦公室零食最容易出現兩種浪費：一種是大包裝開封後沒吃完，另一種是單一口味太多很快膩。單份或小份量更容易控制補貨節奏。", "JAYSUWAN-健素旺、KKM 與 PV女性微甜草本飲可作為素食、飲品與風味補充參考；成分、過敏原與保存方式以商品頁和包裝標示為準。"),
            ("堅果和沖泡飲要分區", "堅果、果乾、沖泡飲與即食零嘴的保存方式不同。若混在同一抽屜，最常發生的是快過期的看不見，已開封的被忘記。", "把櫃子分成未開封、已開封、共享、個人四格，補貨時會清楚很多。"),
            ("低醣或素食不等於適合所有人", "低醣、素食、草本或養生字眼都需要回到個人飲食需求、成分標示與食用限制。不要因為包裝語言舒服，就把它當成所有人的共同答案。", "有特殊飲食限制、過敏或健康需求者，應自行確認標示或諮詢專業意見。"),
            ("常見錯誤：一次買太多口味", "看起來很豐富的零食櫃，若沒有輪替規則，很快就會變成過期庫存。每次補貨保留兩到三種固定款，再加一種新口味試水溫即可。", "若某一款連續兩次沒被拿完，就應該降低補貨量，而不是繼續囤。"),
            ("補貨前的三個問題", "誰會吃、多久吃完、開封後放哪裡。這三個問題能直接排除很多看似划算但不適合辦公室的組合。", "價格、活動、庫存、成分、保存方式、過敏原與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("低醣點心可以當成控糖或減重建議嗎？", "不可以。本文只討論零食櫃配置，不宣稱控糖、減重、代謝或保健效果。"),
            ("辦公室零食櫃要買大包裝嗎？", "不一定。若共享人數不固定，小份量或單份包裝通常更容易管理。"),
            ("堅果、素食零嘴和沖泡飲要怎麼放？", "建議依保存方式與開封狀態分區，並定期檢查期限、成分與剩餘量。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[10:15]


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
        note = "2026-06-21 momo 收益型內容第三組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第三組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
