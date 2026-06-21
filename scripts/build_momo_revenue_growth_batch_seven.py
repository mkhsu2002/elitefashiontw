#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-seven-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B07"

base.COVER_SOURCES = {
    "scalp-haircare-shampoo-color-styling-brush-choice": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37aace4fe4819b8078e255f76b8b49.png",
    "home-stretch-yoga-mat-props-light-scent-corner": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37ab4b5588819bacef0098c5cd8606.png",
    "weekend-city-outdoor-sun-jacket-shorts-small-bag": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37abc462a8819bad9c6fa09afa0110.png",
    "cat-living-litter-toys-food-cleaning-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37ac3db3ac819bad1709d1d05851d8.png",
    "parent-child-outing-tableware-oral-care-maternity-bag-kit": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37ad370e4c819ba83f53c9032aa7d7.png",
}

ROW_OVERRIDES = {
    "scalp-haircare-shampoo-color-styling-brush-choice": {
        "elite_judgment": "髮品整理先分洗、護、染、造型與工具，不把浴室檯面當展示架。",
        "answer_summary": "頭皮與髮品整理要先看使用頻率、清潔與保存，再比較洗髮、染護、造型與按摩梳。",
        "risk_guardrail": "髮品與頭皮用品不宣稱生髮、治療、修復或醫療效果；成分、使用限制與標示請以商品頁及包裝為準。",
    },
    "home-stretch-yoga-mat-props-light-scent-corner": {
        "elite_judgment": "伸展角落的重點是降低開始門檻，不是把家裡做成健身房。",
        "answer_summary": "居家伸展角落要先安排地面、收納與光線，再補瑜珈墊、輔具與香氛。",
        "risk_guardrail": "瑜珈與伸展用品不宣稱處理身體不適、矯正或醫療效果；身體不適應先尋求專業協助。",
    },
    "weekend-city-outdoor-sun-jacket-shorts-small-bag": {
        "elite_judgment": "週末輕戶外穿搭要能從咖啡店走到河濱，不在城市與戶外之間失去秩序。",
        "answer_summary": "週末輕戶外穿搭要先看行程距離、遮蔽、鞋包容量與回程收納。",
        "risk_guardrail": "服飾防曬、防潑、耐候與尺寸資訊請以商品頁標示為準，不自行延伸效果。",
    },
    "cat-living-litter-toys-food-cleaning-order": {
        "elite_judgment": "貓咪採買先處理砂盆、清潔與固定飲食，再讓玩具成為生活變化。",
        "answer_summary": "貓咪生活用品要先分砂盆、食品、玩具與清潔，並保守看待成分與使用限制。",
        "risk_guardrail": "貓用品、食品與清潔品不宣稱醫療、保健、驅蟲或安全保證；成分與使用限制請以商品頁及獸醫建議為準。",
    },
    "parent-child-outing-tableware-oral-care-maternity-bag-kit": {
        "elite_judgment": "親子外出小物要先讓照顧者拿得到、收得回，再談風格與完整度。",
        "answer_summary": "親子外出小物要先分餐具、口腔清潔、孕產穿搭與外出包位置。",
        "risk_guardrail": "嬰幼兒、口腔與孕產用品不宣稱醫療、安全或適用所有情境；材質、年齡限制與使用方式請以商品頁及包裝為準。",
    },
}

base.TOPIC_HUBS = {
    "scalp-haircare-shampoo-color-styling-brush-choice": {
        "topicCategory": "beauty-grooming",
        "topicCategoryLabel": "妝髮與身體照護",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}],
    },
    "home-stretch-yoga-mat-props-light-scent-corner": {
        "topicCategory": "movement-fitness",
        "topicCategoryLabel": "運動與體態",
        "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "weekend-city-outdoor-sun-jacket-shorts-small-bag": {
        "topicCategory": "wardrobe-style",
        "topicCategoryLabel": "衣櫥與穿搭",
        "primaryHub": {"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"},
        "secondaryHubs": [{"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}],
    },
    "cat-living-litter-toys-food-cleaning-order": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
    "parent-child-outing-tableware-oral-care-maternity-bag-kit": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}],
    },
}

base.BLUEPRINTS = {
    "scalp-haircare-shampoo-color-styling-brush-choice": {
        "heroAlt": "晨光浴室檯面上有無品牌洗髮瓶、髮巾、木質頭皮梳、造型梳與陶瓷托盤",
        "audience": "想整理浴室髮品、染護用品、造型工具與頭皮梳的讀者",
        "excerpt": "頭皮與髮品整理要先分洗、護、染、造型與工具，避免浴室檯面被瓶罐佔滿。",
        "tags": ["頭皮髮品", "洗髮", "染護", "造型工具"],
        "intro": "髮品最容易從一瓶洗髮精長成一整排瓶罐：染護、造型、補色、頭皮梳、化妝箱周邊都各有理由。真正該先做的不是補貨，而是把使用頻率、保存位置和清潔方式分清楚。台灣浴室常有濕氣與檯面不足問題，若沒有先分區，再貴的髮品也很容易被放到過期或用不完。",
        "editorialAngle": "先分使用頻率與工具清潔，再看品牌和品項。",
        "sections": [
            ("先分每天用和每週用", "每天用的洗護品要放在最容易拿的位置，染護或造型用品則可退到第二層。", "Apode、CLOEE 與卡雅仕 KYOGOKU 可放在洗護與染護情境裡比較；本文不宣稱修復、生髮或醫療效果。"),
            ("工具要比瓶罐更重視清潔", "按摩梳、造型梳和化妝箱若沒有清潔節奏，很容易成為浴室裡被忽略的物件。", "MPB巴黎小姐、SANSUI 山水與 GINGER MAKE UP 可作為工具與收納補充參考。"),
            ("染護用品要看使用限制", "補色、染護或造型用品應看成分、停留時間、使用頻率和保存方式，不要只看色感照片。", "成分、使用限制、過敏提醒與保存方式請以商品頁和包裝為準。"),
            ("常見錯誤：先買新品再整理舊品", "先把已開封、很少用和不確定用途的用品分出來，再決定是否補貨。", "Elite Fashion 編輯團隊的判斷是：浴室檯面越清楚，髮品越容易真的被用完。"),
            ("下單前清點四格", "洗、護、染、工具四格都填完，再看哪一格真的缺少。", "價格、規格、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("頭皮梳需要每天用嗎？", "不一定。要看個人習慣、工具清潔方式和商品標示。"),
            ("染護用品需要看哪些資訊？", "本文不宣稱修復、生髮、治療或醫療效果，成分、限制與保存方式以商品頁為準。"),
            ("髮品怎麼避免越買越多？", "先把每天、每週和很少使用的品項分開，再補真正缺口。"),
        ],
    },
    "home-stretch-yoga-mat-props-light-scent-corner": {
        "heroAlt": "安靜公寓角落有素色瑜珈墊、瑜珈磚、伸展帶、抱枕、暖光落地燈與無標籤香氛器",
        "audience": "想在家建立低壓伸展角落，讓開始變容易的人",
        "excerpt": "居家伸展角落要先安排地面、收納與光線，再補瑜珈墊、輔具與香氛。",
        "tags": ["居家伸展", "瑜珈墊", "輔具", "燈光香氛"],
        "intro": "居家伸展角落不是把家裡做成健身房，而是讓開始變得低壓。瑜珈墊、輔具、燈光、香氛與收納的順序，應該服務於你是否願意把墊子打開，而不是服務於照片是否完整。",
        "editorialAngle": "降低開始門檻，比買滿器材更重要。",
        "sections": [
            ("先留出一張墊子的空間", "地面是否平整、是否容易收起、是否會擋到動線，比墊子花色更早決定使用率。", "Juan瑜珈、完美主義與燈后可作為墊子、收納和照明參考。"),
            ("輔具是降低門檻，不是增加難度", "瑜珈磚、伸展帶和抱枕應該讓動作更容易開始，不要變成另一組需要收納的壓力。", "本文不宣稱處理身體不適、矯正或醫療效果；不適時應先尋求專業協助。"),
            ("香氛和光線放在最後", "THANN、灰調與 au fait 無非可作為氣味與情境參考，但香氛不應取代通風、清潔和收納。", "本文不宣稱助眠、療癒或健康效果。"),
            ("常見錯誤：器材比空間多", "如果每次伸展前都要搬開一堆物品，角落很快會停用。", "Elite Fashion 編輯團隊的判斷是：好的伸展角落看起來普通，但每天都能開始。"),
            ("下單前先試七天", "先用現有毛巾或墊子試七天，確認時段與位置，再補正式器材。", "價格、規格、材質、活動與庫存請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("居家伸展一定要買很多輔具嗎？", "不一定。先留出空間和固定時段，再看是否需要輔具。"),
            ("香氛可以幫助睡眠嗎？", "本文不宣稱助眠或健康效果，只討論空間情境。"),
            ("身體不舒服時怎麼判斷？", "若有疼痛、麻木或不確定狀況，應先尋求專業協助。"),
        ],
    },
    "weekend-city-outdoor-sun-jacket-shorts-small-bag": {
        "heroAlt": "城市公園長椅上有無品牌輕薄外套、短褲、小包、白色休閒鞋、水瓶與素色帽子",
        "audience": "週末從城市咖啡店走到河濱、公園或輕戶外行程的人",
        "excerpt": "週末輕戶外穿搭要先看行程距離、遮蔽、鞋包容量與回程收納，再談風格。",
        "tags": ["週末穿搭", "輕戶外", "防曬外套", "小包"],
        "intro": "週末輕戶外最迷人的地方，是可以從城市走到自然。但穿搭若只看戶外感，很容易進咖啡店時太狼狽；若只看城市感，走到河濱又不夠自在。外套、短褲、鞋和小包要一起看。",
        "editorialAngle": "城市和戶外之間，重點是轉場秩序。",
        "sections": [
            ("先看今天會走多遠", "距離決定鞋，天氣決定外套，拿取頻率決定小包。順序不要反過來。", "Litume 意都美、UV100 與 UD LAB 可放在外套、機能服飾與小包中比較；本文不自行延伸防曬或耐候效果。"),
            ("短褲要看坐下與移動", "週末行程常有搭車、坐咖啡店、走戶外步道，短褲長度和材質要能跨場景。", "Be yourself、PPBOX 與 95 SNEAKER 可作為穿搭與鞋包補充。"),
            ("小包要收得下雨天備案", "手機、錢包、紙巾、薄外套或折疊袋要有位置，否則手上很快多出第二袋。", "尺寸、背帶、材質與防潑資訊請以商品頁為準。"),
            ("常見錯誤：只追求戶外感", "太多口袋、太厚材質或過度裝備感，反而讓城市段變得笨重。", "Elite Fashion 編輯團隊的判斷是：輕戶外穿搭應該從回程仍然清爽來判斷。"),
            ("下單前做一張行程卡", "城市、戶外、用餐、回程四段都能成立，再看品牌和預算。", "價格、規格、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("週末輕戶外小包要多大？", "先放手機、錢包、紙巾、雨天備案和水瓶需求，再決定容量。"),
            ("防曬外套能保證遮蔽效果嗎？", "本文不保證防曬或 UPF 表現，規格請回商品頁確認。"),
            ("鞋款怎麼選？", "先看步行距離、路面和回程疲勞，再看造型。"),
        ],
    },
    "cat-living-litter-toys-food-cleaning-order": {
        "heroAlt": "明亮貓咪生活角落，有乾淨砂盆、陶瓷碗、空白食品袋、貓玩具、清潔瓶、收納籃與安靜坐著的貓",
        "audience": "準備貓咪用品補貨，想把砂盆、食物、玩具和清潔分清楚的人",
        "excerpt": "貓咪生活用品要先處理砂盆、食品、玩具與清潔分工，並保守看待成分與使用限制。",
        "tags": ["貓咪用品", "貓砂", "貓玩具", "居家清潔"],
        "intro": "貓咪採買最容易被可愛玩具帶走，但真正影響日常的，通常是砂盆位置、食品保存、清潔動線和收納。玩具可以讓生活有變化，但不應該先於基礎秩序。尤其小宅或多貓家庭，若沒有先安排補貨、倒砂、清洗和暫放位置，用品再多也只會讓照顧流程更亂。",
        "editorialAngle": "先處理砂盆與清潔，再讓玩具成為變化。",
        "sections": [
            ("砂盆和清潔是第一順位", "砂盆位置、清潔頻率和耗材收納會決定家裡是否穩定。砂鏟、備用袋、清潔布與補砂位置最好在同一個動線裡，避免每次清理都要跨區尋找。", "愛貓聯盟、愛貓聯萌與尾巴丘毛孩選物可作為貓砂、食品與用品比較入口。"),
            ("食品要看保存和標示", "食品、零食或補給要看成分、保存方式、份量和貓咪實際狀況，不要只看包裝。", "Mommywant、寵物用品品牌與有喵病可作為用品補充；本文不宣稱醫療、保健或改善效果。"),
            ("玩具要輪替，不要堆滿", "玩具一次太多，反而容易被忽略。少量輪替比一次買滿更容易維持新鮮感。", "淨淨 Clean Clean 可放在清潔用品補充情境中看；清潔品使用限制需回商品頁確認。"),
            ("常見錯誤：把除味當清潔", "味道來源要先找砂盆、布品、地板或垃圾，不要只用香味覆蓋。", "Elite Fashion 編輯團隊的判斷是：貓咪生活採買的成熟感，來自人和貓都少一點混亂。"),
            ("下單前分四格", "砂盆、食品、玩具、清潔四格先分清楚，再看缺口。", "商品成分、使用限制、價格、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("貓咪用品第一步買什麼？", "先處理砂盆、食品保存和清潔動線，再補玩具。"),
            ("寵物食品可以寫保健效果嗎？", "本文不宣稱醫療、保健或改善效果，成分與限制以商品頁為準。"),
            ("除味用品可以取代清潔嗎？", "不可以。先找味道來源，再處理砂盆、布品與地板。"),
        ],
    },
    "parent-child-outing-tableware-oral-care-maternity-bag-kit": {
        "heroAlt": "明亮玄關桌上有無品牌幼兒餐具、口腔清潔小包、柔軟孕產外套、外出托特包、水瓶與空白濕巾袋",
        "audience": "需要整理親子短程外出、孕產穿搭與照顧者包內動線的人",
        "excerpt": "親子外出小物要先分餐具、口腔清潔、孕產穿搭與外出包位置，讓照顧者拿得到、收得回。",
        "tags": ["親子外出", "幼兒餐具", "口腔清潔", "外出包"],
        "intro": "親子外出最怕的是東西都有帶，但真正要用時拿不到。餐具、口腔清潔、孕產穿搭、外出包和小物收納，需要按使用時刻排序，而不是按商品類別塞進包裡。短程出門也會遇到用餐、清潔、溫差、濕物與臨時找物的壓力，包內順序比品項數量更能決定照顧者是否從容。",
        "editorialAngle": "照顧者拿得到、收得回，比買滿更重要。",
        "sections": [
            ("先排使用時刻", "上車前、用餐時、餐後清潔、換衣或回程，每個時刻需要的小物不同。", "2angels、牙齒寶寶與 Babyshare 可分別放在餐具、口腔清潔與孕產穿搭裡比較；材質和限制要回商品頁確認。"),
            ("外出包要有乾濕分區", "餐具、濕巾、衣物、口腔清潔和個人物品若混放，回家後整理會更累。乾物靠近內層，濕物和餐後用品要有獨立袋，才不會讓下一次出門重新整理整包。", "MiffyBaby、寶寶共和國與 S′AIME東京企劃可作為婦幼用品和包款補充。"),
            ("口腔與嬰幼兒用品要更保守", "涉及入口、年齡限制、材質和清潔方式的商品，都要回到包裝標示，不憑想像延伸。", "本文不宣稱醫療、安全或適用所有情境。"),
            ("常見錯誤：全部放進同一袋", "短程外出也需要分層，否則餐後、濕物和備品會互相干擾。", "Elite Fashion 編輯團隊的判斷是：親子外出包的價值，在於回家後也能快速復原。"),
            ("出門前十秒檢查", "餐具、清潔、替換、濕物袋、水瓶。五件事確認後，再看是否需要玩具或備用衣。", "價格、材質、年齡限制、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("親子外出包要放哪些小物？", "先放用餐、清潔、替換和濕物分區，再依行程長度補充。"),
            ("口腔清潔用品可以共用嗎？", "不建議用想像判斷，應看年齡、材質、清潔方式與商品標示。"),
            ("孕產穿搭要怎麼放進外出包？", "先看外出時間、溫差與替換需求，再決定是否需要薄外套或披巾。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[30:35]:
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
        note = "2026-06-21 momo 收益型內容第七組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第七組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
