#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-six-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B06"

base.COVER_SOURCES = {
    "home-comfort-massage-device-brace-care-supplies-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37a2cfc560819b8e69ede903ac6d67.png",
    "freezer-meal-prep-chicken-sweet-potato-vegetables-pack": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37a3387810819b9e3df4c0e235737a.png",
    "pet-friendly-home-cleaning-floor-laundry-storage-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37a39986c4819b95a62de640cf01f4.png",
    "japanese-camping-style-table-stove-cup-storage-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37a522a154819bbe3bb9c26ebcbacf.png",
    "daily-skincare-essence-mask-body-sunscreen-order-2": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37a460842c819baf4dc1334d805a6e.png",
}

ROW_OVERRIDES = {
    "home-comfort-massage-device-brace-care-supplies-order": {
        "elite_judgment": "先看家人是否適合使用，再看尺寸、力道、清潔與收納，不把設備當成照護答案。",
        "answer_summary": "居家舒壓設備要先確認使用限制、空間與清潔，再比較按摩椅、按摩槍與護具。",
        "risk_guardrail": "按摩與護具用品不取代專業診斷或治療；使用限制、禁忌與規格請以商品頁及專業建議為準。",
    },
    "freezer-meal-prep-chicken-sweet-potato-vegetables-pack": {
        "elite_judgment": "冷凍庫不是越滿越有效率，而是每一包都知道何時會被吃掉。",
        "answer_summary": "冷凍備餐要先看保存期限、份量與烹調動線，再補雞胸、地瓜、蔬菜與料理包。",
        "risk_guardrail": "食品成分、保存期限、過敏原、加熱方式與營養標示請以商品頁及包裝為準，不作健康或減重承諾。",
    },
    "pet-friendly-home-cleaning-floor-laundry-storage-order": {
        "elite_judgment": "寵物友善清潔先分地板、布品與收納，產品不應直接接觸毛孩或取代照護判斷。",
        "answer_summary": "寵物友善居家清潔要按地板、洗衣、除味與收納分工，並保守看待成分與使用限制。",
        "risk_guardrail": "寵物用品與清潔品不宣稱除菌、驅蟲、治療或安全保證；成分與使用限制請以商品頁及獸醫建議為準。",
    },
    "japanese-camping-style-table-stove-cup-storage-order": {
        "elite_judgment": "露營風格先從坐得穩、煮得順、收得回來開始，而不是先買整套美照。",
        "answer_summary": "日系露營入門要先看桌椅穩定、爐具使用條件、杯具與收納，再談風格完整度。",
        "risk_guardrail": "戶外爐具、燈具與收納用品的安全限制、適用場地與規格請以商品頁及場地規定為準。",
    },
    "daily-skincare-essence-mask-body-sunscreen-order-2": {
        "elite_judgment": "保養清單要先分早晚與使用頻率，少而穩比一口氣堆滿更接近日常。",
        "answer_summary": "日常保養應先分早晚、頻率與肌膚耐受，再看精華、面膜、身體保養與防曬。",
        "risk_guardrail": "保養品與防曬不宣稱美白、抗老、治療或醫療效果；成分、使用限制與標示請以商品頁及包裝為準。",
    },
}

base.TOPIC_HUBS = {
    "home-comfort-massage-device-brace-care-supplies-order": {
        "topicCategory": "care-support",
        "topicCategoryLabel": "照護與輔具",
        "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "freezer-meal-prep-chicken-sweet-potato-vegetables-pack": {
        "topicCategory": "food-nutrition",
        "topicCategoryLabel": "飲食與補給",
        "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "pet-friendly-home-cleaning-floor-laundry-storage-order": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
    "japanese-camping-style-table-stove-cup-storage-order": {
        "topicCategory": "outdoor-gear",
        "topicCategoryLabel": "戶外裝備",
        "primaryHub": {"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "daily-skincare-essence-mask-body-sunscreen-order-2": {
        "topicCategory": "beauty-grooming",
        "topicCategoryLabel": "妝髮與身體照護",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}],
    },
}

base.BLUEPRINTS = {
    "home-comfort-massage-device-brace-care-supplies-order": {
        "heroAlt": "暖光客廳裡有無品牌按摩椅、按摩槍、護具、毛毯、收納籃與水杯，呈現安靜居家照護角落",
        "audience": "替家人安排居家放鬆設備、支撐用品與日常照護收納的人",
        "excerpt": "居家舒壓設備要先確認是否適合使用，再看尺寸、力道、清潔與收納，不把設備當成照護答案。",
        "tags": ["居家舒壓", "按摩設備", "護具", "照護用品"],
        "intro": "替家人買按摩椅、按摩槍或護具，最容易被『看起來很體貼』推著走。但身體狀況、使用限制、收納空間和清潔方式，才是這類用品能否長期留下的關鍵。本文以保守順序整理，讓設備回到日常協助，而不是被期待成為照護答案。",
        "editorialAngle": "先確認使用限制與空間，再比較設備種類。",
        "sections": [
            ("先看是否適合使用", "若家人有疼痛、麻木、特殊病史或不確定狀況，應先尋求專業建議，不要用購物代替判斷。", "輝葉良品、一然健康與安里嚴選可作為按摩設備比較入口；本文不承諾治療、止痛或醫療效果。"),
            ("尺寸、力道與清潔比外型更重要", "按摩椅需要空間，按摩槍需要握持與力道控制，護具需要尺寸和清潔。這些都比照片裡的質感更直接。", "BELEX、Jasper 大來護具 Mo+ 與 COZZY嚴選可作為支撐用品與生活設備補充參考。"),
            ("常見錯誤：把設備放到不會用的位置", "如果設備被放在太遠、太重或需要每次搬動的位置，再好的功能也會被閒置。", "Elite Fashion 編輯團隊的判斷是：照護用品要讓照顧者和使用者都少一點負擔。"),
            ("下單前五問", "誰會用、多久用、誰清潔、放哪裡、不適合時怎麼退場。五個答案清楚，再看品牌與預算。", "商品規格、使用禁忌、活動、保固、庫存與配送請以下單前商品頁公告為準。"),
            ("使用後要留複查時間", "設備進家後先觀察兩週：使用者是否真的願意用、清潔是否麻煩、擺放是否造成動線壓力。", "若答案不理想，先調整位置與使用時段，不急著再買下一件。"),
        ],
        "faq": [
            ("按摩椅或按摩槍能處理疼痛問題嗎？", "本文不宣稱治療、止痛或醫療效果；有不適應先尋求專業協助。"),
            ("護具要怎麼選？", "先看尺寸、使用時刻、清潔方式與是否適合個人狀況。"),
            ("送給家人前要注意什麼？", "確認對方是否適合使用、家中是否有空間，以及設備是否容易清潔和收納。"),
        ],
    },
    "freezer-meal-prep-chicken-sweet-potato-vegetables-pack": {
        "heroAlt": "打開的冷凍庫與廚房檯面上有分裝雞胸、地瓜、冷凍蔬菜、空白料理包與透明保鮮盒",
        "audience": "想用冷凍庫建立平日備餐節奏，但不想把冰箱塞滿的人",
        "excerpt": "冷凍備餐不是越滿越有效率，而是每一包都知道何時會被吃掉、怎麼加熱、如何輪替。",
        "tags": ["冷凍備餐", "雞胸", "地瓜", "冷凍蔬菜"],
        "intro": "冷凍庫備餐看似理性，實際上最怕買成庫存壓力。舒肥雞胸、地瓜、冷凍蔬菜和料理包都能省時間，但如果份量、保存期限和加熱方式沒有安排好，很快就會變成忘在冷凍庫深處的負擔。",
        "editorialAngle": "先看保存期限、份量和加熱動線，再補食材。",
        "sections": [
            ("先決定一週吃幾次", "備餐不是囤貨。先估一週需要幾餐、哪幾餐最容易失控，再決定雞胸、地瓜、蔬菜和料理包的比例。", "田食原、小嚼士與老饕廚房可作為冷凍食材與料理包比較入口；食品資訊以商品頁和包裝為準。"),
            ("份量要比口味更早決定", "同一口味買太多容易疲乏，份量太大則會讓解凍變麻煩。單餐份量、加熱時間和容器尺寸要先看。", "呷什麵、KKM 與 GUMi低碳可作為主食、飲品或補給參考；本文不作健康、減重或營養效果承諾。"),
            ("冷凍庫要有先進先出規則", "把最早到期的放前面，未開封和已開封分開，才不會讓備餐變成考古。", "Elite Fashion 編輯團隊的判斷是：備餐的價值不是冰滿，而是疲憊時也能快速做出選擇。"),
            ("下單前看標示", "保存期限、成分、過敏原、加熱方式、份量和配送溫層。這些比包裝照更重要。", "價格、活動、庫存、配送與保存條件請以下單前商品頁公告為準。"),
            ("每週留一餐清庫存", "備餐系統需要固定回收。每週留一餐把快到期或剩餘份量處理掉，冷凍庫才不會越補越滿。", "如果某種口味連續兩週沒有被吃掉，下次就降低補貨量。"),
        ],
        "faq": [
            ("冷凍備餐能當成減重建議嗎？", "本文不作減重、控糖或健康效果承諾，只討論備餐秩序與保存。"),
            ("雞胸、地瓜、蔬菜要怎麼分配？", "先看一週用餐次數與口味輪替，再決定比例。"),
            ("料理包要注意什麼？", "看成分、過敏原、加熱方式、保存期限與配送溫層。"),
        ],
    },
    "pet-friendly-home-cleaning-floor-laundry-storage-order": {
        "heroAlt": "明亮寵物友善居家洗衣玄關區，有空白清潔瓶、拖把、洗衣籃、收納盒、地板與安靜休息的貓狗",
        "audience": "與犬貓同住、需要整理地板、洗衣、除味與收納清潔動線的人",
        "excerpt": "寵物友善清潔要先分地板、布品、除味與收納，並保守看待成分與使用限制。",
        "tags": ["寵物友善清潔", "地板清潔", "洗衣收納", "除味"],
        "intro": "和毛孩同住，清潔不是把香味變重，也不是把用品堆滿。地板、布品、廁所周邊、外出用品和收納位置都要分開看，並且所有清潔品都要保守看待成分和使用限制。",
        "editorialAngle": "產品不應直接接觸毛孩或取代照護判斷。",
        "sections": [
            ("先分地板和布品", "地板清潔、寵物墊、毛巾和人用衣物的清潔邏輯不同。混在一起只會讓家務更模糊。", "艾寵聯萌、酷狗地板與淨淨 Clean Clean 可放在寵物清潔、地板與居家清潔情境中比較。"),
            ("除味不是用香味蓋過去", "味道來源可能來自地板、布品、垃圾或收納不通風。先找來源，再看清潔品。", "JINKO 淨科、寵物王國與真蓁嚴選可作為清潔和收納補充；本文不宣稱除菌、驅蟲、治療或安全保證。"),
            ("清潔品要有固定存放位置", "清潔瓶、拖把、毛巾和替換耗材若沒有位置，會增加毛孩誤碰風險。", "Elite Fashion 編輯團隊的判斷是：寵物友善清潔的核心是降低混亂，而不是追求香味。"),
            ("下單前看成分與使用限制", "確認是否需要稀釋、是否能用於地板或布品、是否要避開寵物活動區。", "商品成分、使用限制、活動、庫存與配送請以下單前商品頁公告為準；特殊狀況請諮詢獸醫。"),
            ("使用後先看毛孩動線", "清潔完成後，觀察毛孩常走、常躺、常磨蹭的位置，確認用品有收好、地面已乾、布品已分區。", "這比一次買更多清潔品更接近寵物友善的日常。"),
        ],
        "faq": [
            ("寵物友善清潔品一定安全嗎？", "不應這樣理解。仍需看成分、使用限制和實際環境，必要時諮詢獸醫。"),
            ("除味用品可以取代清潔嗎？", "不可以。先找味道來源，再處理地板、布品與收納。"),
            ("清潔用品要放哪裡？", "放在寵物不易接觸、通風且容易取用的位置。"),
        ],
    },
    "japanese-camping-style-table-stove-cup-storage-order": {
        "heroAlt": "森林湖畔金色光線下，無品牌低桌、折疊椅、未點火爐具、琺瑯杯、木箱與素色收納布安靜排列",
        "audience": "想入門日系露營風格，但不想一次買滿整套裝備的人",
        "excerpt": "日系露營入門先從桌椅穩定、爐具條件、杯具與收納開始，再談風格完整度。",
        "tags": ["日系露營", "露營桌椅", "露營爐具", "戶外收納"],
        "intro": "日系露營風格迷人，但新手最容易買成一套照片：桌椅、爐具、杯具、燈和木箱都想一次到位。真正應該先處理的是坐得穩、煮得順、收得回來，風格才會留得久。",
        "editorialAngle": "露營風格先從使用順序開始，不從完整美照開始。",
        "sections": [
            ("桌椅先決定營位節奏", "桌高、椅高、收納體積和車內空間會決定露營是否順。桌椅不穩，再漂亮的杯具也只是擺設。", "Snow Peak Taiwan、campingflying 想露飛飛與江大露營裝備可作為桌椅與風格裝備比較入口。"),
            ("爐具要看場地與安全限制", "爐具不是只看外型，還要看使用場地、燃料、通風、收納和清潔。", "ANPING 安平、未來戶外城市與 Litume 意都美可作為戶外用品補充；安全限制以商品頁與場地規定為準。"),
            ("杯具和收納負責收尾", "杯具、餐具和木箱讓風格完整，但也會增加清洗與搬運。先確定會用，再慢慢補。", "Elite Fashion 編輯團隊的判斷是：日系露營不是買滿，而是讓每一件用品都有安靜的位置。"),
            ("下單前做一次車內排位", "把桌椅、箱子、爐具和杯具的體積想像成回程狀態。回程收得回來，才是真正可持續。", "價格、活動、庫存、尺寸、重量與適用限制請以下單前商品頁公告為準。"),
            ("第一次出門要少帶一點", "新手第一次露營不需要把風格買滿。少帶一些，才看得出哪些物件是真的被使用，哪些只是照片需要。", "回家後依照清洗、收納和搬運感受，再決定下一輪補什麼。"),
        ],
        "faq": [
            ("日系露營新手先買什麼？", "先買桌椅和基本收納，再看爐具、杯具與風格小物。"),
            ("爐具可以只看外型嗎？", "不行。要看場地規定、通風、燃料、清潔與收納限制。"),
            ("露營收納為什麼重要？", "因為回程能否快速收回車內，會決定裝備是否真的常用。"),
        ],
    },
    "daily-skincare-essence-mask-body-sunscreen-order-2": {
        "heroAlt": "晨光浴室檯面上有無品牌精華瓶、空白面膜包、身體乳瓶、防曬管、陶瓷托盤與淡紫毛巾",
        "audience": "想把保養品減量、分早晚與頻率，避免浴室檯面堆太滿的人",
        "excerpt": "日常保養應先分早晚、頻率與肌膚耐受，再看精華、面膜、身體保養與防曬。",
        "tags": ["日常保養", "精華", "面膜", "防曬"],
        "intro": "保養品最容易越買越多，尤其是精華、面膜、身體保養與防曬都各有說法。真正能留下來的，不是最多瓶，而是能放進早晚節奏、不造成使用負擔、也能清楚知道何時暫停的那幾件。",
        "editorialAngle": "少而穩比一口氣堆滿更接近日常。",
        "sections": [
            ("先分早上和晚上", "早上重點是清爽與後續妝髮穿搭，晚上重點是清潔後的穩定使用。兩者混在一起，最容易過度疊擦。", "Cell Secret、AYSWE 與唯詩生醫可作為精華與保養品比較入口；本文不宣稱美白、抗老或醫療效果。"),
            ("面膜和身體保養看頻率", "面膜不一定每天用，身體保養則要看洗澡後是否真的會擦。頻率不清楚，囤貨就會變成浴室壓力。", "雪亞緹、THANN 與 Bioyona 可作為身體保養與香氛保養參考；成分與使用限制以商品頁和包裝為準。"),
            ("防曬要回到使用情境", "通勤、戶外、室內辦公和旅行需要的使用感不同。本文不自行延伸防曬表現，規格請回商品頁確認。", "Elite Fashion 編輯團隊的判斷是：保養不是堆滿檯面，而是讓每一步都有明確理由。"),
            ("下單前先做浴室清點", "把現有用品分成每天用、每週用、很少用、已不確定四類。先消耗，再補缺口。", "價格、規格、成分、活動、庫存、保存期限與配送請以下單前商品頁公告為準。"),
            ("新用品一次只加入一種", "保養品同時換太多，很難判斷哪一件適合、哪一件造成負擔。一次只加入一種，並保留觀察時間。", "若有不適或疑慮，應停止使用並依個人狀況尋求專業建議。"),
        ],
        "faq": [
            ("精華和面膜可以每天疊很多嗎？", "不建議只用數量判斷。應看肌膚耐受、產品標示與使用頻率。"),
            ("文章會推薦美白或抗老訴求嗎？", "不會。本文不宣稱美白、抗老、治療或醫療效果。"),
            ("防曬怎麼排進日常？", "回到通勤、戶外或旅行情境，再看商品頁標示與使用感。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[25:30]:
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
        note = "2026-06-21 momo 收益型內容第六組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第六組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
