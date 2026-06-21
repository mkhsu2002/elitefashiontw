#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-ten-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B10"

base.COVER_SOURCES = {
    "home-nail-makeup-tools-brush-storage-beginner": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37c2d0b2988193ba99c6a7095c37e9.png",
    "jewelry-leather-gift-ring-wallet-small-bag": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37c37cb3d08193b1bd8c91e378ab7f.png",
    "mens-commute-shirt-trousers-jacket-shoes-wardrobe": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37c42895348193b09fff6e6e89e533.png",
    "plus-size-work-travel-outfit-jacket-bag-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37c4817f9c8193ab6437d619c31e40.png",
    "camping-coffee-outdoor-meal-prep-cookware-food": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37c4e31c0c819399405d2141463ef0.png",
}

ROW_OVERRIDES = {
    "home-nail-makeup-tools-brush-storage-beginner": {
        "elite_judgment": "居家美甲和彩妝工具先看清潔、收納與練習頻率，不把一次買齊當成新手捷徑。",
        "answer_summary": "居家美甲與彩妝工具要先分材料、刷具、清潔與收納，再比較品牌和組合。",
        "risk_guardrail": "美甲、彩妝、刷具、飾品與皮件不作肌膚、醫療或外觀承諾；成分、材質、尺寸與使用限制請以商品頁及包裝為準。",
    },
    "jewelry-leather-gift-ring-wallet-small-bag": {
        "elite_judgment": "飾品皮件送禮先看對方日常穿搭、尺寸和使用頻率，不只看禮盒照片。",
        "answer_summary": "飾品與皮件送禮要先看尺寸、材質、日常使用率與保養方式，再選銀飾、戒指、皮夾與小包。",
        "risk_guardrail": "銀飾、戒指、皮件與包款的材質、尺寸、保養、活動與庫存請以商品頁公告為準。",
    },
    "mens-commute-shirt-trousers-jacket-shoes-wardrobe": {
        "elite_judgment": "男士通勤衣櫥先排一週場景，再補襯衫、長褲、外套、鞋與包款。",
        "answer_summary": "男士通勤衣櫥要先看辦公室正式度、天氣、步行距離與清洗頻率，再比較單品。",
        "risk_guardrail": "服飾、鞋包與雨具的尺寸、材質、防曬、防潑、耐候與保養資訊請以商品頁標示為準。",
    },
    "plus-size-work-travel-outfit-jacket-bag-order": {
        "elite_judgment": "大尺碼工作與旅行穿搭先看比例、活動量與行李限制，不把遮掩當成唯一答案。",
        "answer_summary": "大尺碼工作與旅行穿搭要先看版型比例、舒適度、外套層次與包款容量，再比較品牌。",
        "risk_guardrail": "服飾與包款不作身形承諾；尺寸、版型、材質、保養與庫存請以商品頁標示為準。",
    },
    "camping-coffee-outdoor-meal-prep-cookware-food": {
        "elite_judgment": "露營咖啡與戶外餐食先看水源、火源、冷藏與收洗動線，不把裝備感當成好吃的保證。",
        "answer_summary": "露營咖啡與戶外餐食要先看手沖流程、鍋具收納、冷凍食材保存與收洗動線。",
        "risk_guardrail": "咖啡、食品、鍋具與戶外用品不保證風味或料理表現；成分、保存、加熱、材質與使用限制請以商品頁及包裝為準。",
    },
}

base.TOPIC_HUBS = {
    "home-nail-makeup-tools-brush-storage-beginner": {
        "topicCategory": "beauty-grooming",
        "topicCategoryLabel": "妝髮與身體照護",
        "primaryHub": {"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "jewelry-leather-gift-ring-wallet-small-bag": {
        "topicCategory": "wardrobe-style",
        "topicCategoryLabel": "衣櫥與穿搭",
        "primaryHub": {"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "mens-commute-shirt-trousers-jacket-shoes-wardrobe": {
        "topicCategory": "wardrobe-style",
        "topicCategoryLabel": "衣櫥與穿搭",
        "primaryHub": {"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"},
        "secondaryHubs": [{"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}],
    },
    "plus-size-work-travel-outfit-jacket-bag-order": {
        "topicCategory": "wardrobe-style",
        "topicCategoryLabel": "衣櫥與穿搭",
        "primaryHub": {"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"},
        "secondaryHubs": [{"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}],
    },
    "camping-coffee-outdoor-meal-prep-cookware-food": {
        "topicCategory": "outdoor-gear",
        "topicCategoryLabel": "戶外裝備",
        "primaryHub": {"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
}

base.BLUEPRINTS = {
    "home-nail-makeup-tools-brush-storage-beginner": {
        "heroAlt": "明亮梳妝台上有無品牌指甲油瓶、美甲工具、彩妝刷具、化妝箱、分格收納盤與銀色飾品",
        "audience": "想從零建立居家美甲和彩妝工具收納的人",
        "excerpt": "居家美甲與彩妝工具要先分材料、刷具、清潔與收納，再比較品牌和組合。",
        "tags": ["居家美甲", "彩妝刷具", "化妝箱", "工具收納"],
        "intro": "居家美甲和彩妝工具最容易一開始就買太多。指甲油、底膠、刷具、化妝箱、清潔用品和飾品搭配都很吸引人，但新手真正需要的是能持續練習、容易清潔、看得見缺口的桌面。先把工具分層，再決定品牌，會比一次買齊更穩。",
        "editorialAngle": "先看練習頻率與清潔路徑，再補材料。",
        "sections": [
            ("先分材料、工具、清潔和收納", "材料負責顏色，工具負責操作，清潔負責維持，收納負責讓下一次願意開始。四格分清楚，桌面才不會越買越亂。", "女王美學美甲材料、GINGER MAKE UP 與 BAYBEYLA 可放在美甲、化妝箱與刷具情境中比較。"),
            ("刷具和美甲工具要看清潔方式", "刷具、銼刀、剪刀或小工具若沒有清潔節奏，很快會失去使用意願。下單前先想好清潔、晾乾和收回的位置。", "成分、材質、使用限制與清潔方式請以商品頁及包裝為準。"),
            ("飾品和皮件只當造型補充", "ART64、玖伍 Jiuwu jewelry 與 Mister 手作皮件可放在完成造型後的配件情境，不要讓配件先於工具秩序。", "尺寸、材質和保養方式仍要回商品頁確認。"),
            ("常見錯誤：把漂亮盒子當成收納", "化妝箱或收納盤若拿取不順，最後只會把工具藏起來。好的收納是常用物能快速拿、低頻物能乾淨退場。", "Elite Fashion 編輯團隊的判斷是：居家美甲的轉單價值，來自讀者知道先買哪一格，而不是被顏色淹沒。"),
            ("下單前的桌面演練", "從拿工具、上色、清潔、等待、收回做一次流程。卡住的步驟，才是該補貨的地方。", "價格、規格、活動、庫存、材質與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("新手居家美甲要先買完整套組嗎？", "不一定。先看練習頻率和清潔方式，再補材料與工具。"),
            ("彩妝刷具怎麼避免堆滿桌面？", "常用刷具放外層，低頻刷具和備品進盒，並固定清潔位置。"),
            ("飾品要一起買嗎？", "可作造型補充，但先把美甲和彩妝工具秩序建立好。"),
        ],
    },
    "jewelry-leather-gift-ring-wallet-small-bag": {
        "heroAlt": "精品禮物桌上有無品牌銀戒、素面皮夾、小型斜背包、空白禮盒、緞帶與柔和窗光",
        "audience": "想挑銀飾、戒指、皮夾與日常小包送禮的人",
        "excerpt": "飾品與皮件送禮要先看尺寸、材質、日常使用率與保養方式，再選銀飾、戒指、皮夾與小包。",
        "tags": ["飾品送禮", "銀飾戒指", "皮件", "日常小包"],
        "intro": "飾品與皮件送禮的難度，不在預算，而在尺寸、材質和對方是否真的會用。銀飾和戒指很私密，皮夾和小包則跟每天的拿取習慣有關。把日常使用率放在禮盒照片前面，送禮才不會只有打開那一刻漂亮。",
        "editorialAngle": "先看對方日常，再看禮盒體面。",
        "sections": [
            ("戒指和銀飾先確認尺寸與風格", "戒指尺寸、銀飾保養和對方平常配戴習慣，都比照片質感更早決定是否適合。", "ART64 與玖伍 Jiuwu jewelry 可放在銀飾與原創飾品情境中比較。"),
            ("皮夾要看卡片數和拿取方式", "皮夾不是越精緻越好，卡片數、零錢習慣、包內位置和厚度都要看。", "Mister 手作皮件可作為皮件送禮參考；材質與保養請以商品頁為準。"),
            ("小包要看對方的日常路線", "S′AIME、PPBOX 與 LamiFans 可放在小包和生活選物裡比較。若對方常通勤或旅行，容量和背帶比裝飾更重要。", "包款尺寸、重量、材質和活動請以下單前商品頁公告為準。"),
            ("常見錯誤：用自己的品味替對方決定", "送禮最常失準，是把自己的審美當成對方需要。先看對方常戴什麼、常用什麼包，再補缺口。", "Elite Fashion 編輯團隊的判斷是：好的飾品皮件禮物，是對方明天就能自然拿出門。"),
            ("下單前的四項確認", "尺寸、材質、保養、退換限制。四項都清楚，再看是否需要禮盒包裝。", "價格、規格、活動、庫存、保固與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("戒指送禮最需要確認什麼？", "尺寸和對方平常配戴習慣。若不確定，選可調整或改送其他飾品更保守。"),
            ("皮夾和小包哪個更適合送禮？", "看對方日常需求。卡片多的人看皮夾，常外出的人可看小包。"),
            ("銀飾需要注意保養嗎？", "需要。材質、保養與保存方式請以商品頁說明為準。"),
        ],
    },
    "mens-commute-shirt-trousers-jacket-shoes-wardrobe": {
        "heroAlt": "現代玄關衣櫥裡有無品牌男士襯衫、長褲、輕外套、素色鞋款、通勤包與折傘",
        "audience": "想建立男士通勤一週衣櫥順序的人",
        "excerpt": "男士通勤衣櫥要先看辦公室正式度、天氣、步行距離與清洗頻率，再比較單品。",
        "tags": ["男士通勤", "襯衫長褲", "外套鞋包", "一週衣櫥"],
        "intro": "男士通勤衣櫥若只靠單件好看，很容易出現每天早上還是沒得穿。襯衫、長褲、外套、鞋、包和雨具應該按一週行程排列：會議日、一般辦公日、客戶拜訪日、雨天和週五輕鬆日。順序排出來，購物清單才會從零散變成系統。",
        "editorialAngle": "先排一週場景，再補單品。",
        "sections": [
            ("先看正式度，不先看流行", "辦公室正式度會決定襯衫、長褲和鞋的基準。基準穩，外套和包款才有變化空間。", "GIBBON 男裝與 NARMES 可放在襯衫、長褲與上衣情境中比較。"),
            ("鞋和包要看步行距離", "95 SNEAKER、PPBOX 與 UD LAB 可放在鞋包選擇裡比較。若每天步行多，鞋底和包重比造型更早決定使用率。", "尺寸、材質和保養方式請以商品頁為準。"),
            ("雨天備案不要最後才想", "FULTON 可作為晴雨傘備案參考。雨具、外套和鞋材若沒有一起看，雨天早上很容易破壞整套衣櫥。", "防潑、耐候與尺寸資訊請以商品頁標示為準。"),
            ("常見錯誤：只買正式單品，沒有轉場單品", "通勤衣櫥需要從辦公室走到餐會、捷運、停車場和雨天。外套和包款的轉場能力很重要。", "Elite Fashion 編輯團隊的判斷是：男士通勤衣櫥要看週五晚上仍然不狼狽。"),
            ("下單前做五天搭配", "把週一到週五排出來，看哪一天缺襯衫、哪一天缺鞋、哪一天缺雨天備案。", "價格、規格、活動、庫存、尺寸與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("男士通勤衣櫥先買襯衫還是鞋？", "先看辦公室正式度和步行距離，再決定哪一格最缺。"),
            ("外套要怎麼選？", "看天氣、通勤方式和能否搭配一週多數褲鞋。"),
            ("雨具需要放進衣櫥規劃嗎？", "需要。雨天會影響外套、鞋和包，最好一起看。"),
        ],
    },
    "plus-size-work-travel-outfit-jacket-bag-order": {
        "heroAlt": "飯店房間衣架上有無品牌大尺碼西裝外套、柔軟上衣、寬褲、旅行托特包、行李箱與舒適鞋",
        "audience": "想整理大尺碼工作與旅行穿搭順序的人",
        "excerpt": "大尺碼工作與旅行穿搭要先看版型比例、舒適度、外套層次與包款容量，再比較品牌。",
        "tags": ["大尺碼穿搭", "工作旅行", "外套包款", "比例舒適"],
        "intro": "大尺碼工作與旅行穿搭不該被縮成遮掩問題。真正成熟的選法，是看比例、活動量、坐站時間、行李限制和包款容量。外套、寬褲、上衣、鞋和包要一起服務行程，而不是讓讀者為衣服忍耐一整天。",
        "editorialAngle": "把舒適和比例放在同一張清單裡。",
        "sections": [
            ("先分工作日和旅行日", "工作日重視正式度和坐站舒適，旅行日重視收納、皺摺和鞋包重量。兩種情境不要用同一套標準。", "B+大尺碼專家、VENUSY 與 Be yourself 可放在版型、上衣與日常穿搭中比較。"),
            ("外套是比例工具，不是遮掩工具", "UV100 或其他外套選擇應看天氣、長度、肩線與收納，而不是只為遮住身體。", "防曬、防潑與尺寸資訊請以商品頁標示為準。"),
            ("包款要看容量和肩背感", "S′AIME 與 UD LAB 可作為包款補充。旅行時包款要能放文件、雨具和小物，工作時則要維持俐落。", "尺寸、背帶、重量與材質請以下單前商品頁公告為準。"),
            ("常見錯誤：只看顯瘦照片", "照片角度不等於真實穿著。坐下、抬手、走路和拉行李時是否自在，才是工作與旅行穿搭的核心。", "Elite Fashion 編輯團隊的判斷是：好的大尺碼穿搭要讓人忘記衣服，而不是一整天調整衣服。"),
            ("下單前做三段測試", "站著、坐著、走路。三段都能成立，再看是否需要外套、包款或第二雙鞋。", "價格、規格、活動、庫存、尺寸與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("大尺碼穿搭要先買外套嗎？", "不一定。先看工作日和旅行日缺口，再決定外套、上衣、褲款或包款。"),
            ("可以只看顯瘦照片選衣服嗎？", "不建議。應看尺寸、版型、坐站活動和材質。"),
            ("旅行包款怎麼選？", "看文件、雨具、小物和行李搭配，肩背感也要一起考慮。"),
        ],
    },
    "camping-coffee-outdoor-meal-prep-cookware-food": {
        "heroAlt": "森林露營桌上有無品牌手沖壺、濾杯、空白咖啡袋、鍋具、琺瑯杯、冷藏餐盒與蔬菜餐食",
        "audience": "想把露營咖啡、手沖、鍋具與戶外餐食流程整理好的人",
        "excerpt": "露營咖啡與戶外餐食要先看手沖流程、鍋具收納、冷凍食材保存與收洗動線。",
        "tags": ["露營咖啡", "戶外餐食", "手沖鍋具", "冷凍食材"],
        "intro": "露營咖啡與戶外餐食的魅力，不只在器材，而在清晨能不能順利煮水、磨豆、沖咖啡、準備餐食、收洗乾淨。手沖、濾掛、鍋具、冷凍食材和麵食都需要被放進同一條流程裡。若只看裝備感，很容易到營地才發現水源、火源、冷藏和垃圾收納都沒安排。",
        "editorialAngle": "先看水火與收洗，再看器材美感。",
        "sections": [
            ("先確認水源、火源和桌面", "手沖咖啡需要水、火、穩定桌面和垃圾收納。四件事缺一件，器材再漂亮都會變麻煩。", "BINCOO、Xinto Coffee 與馬克老爹可放在手沖、咖啡豆與濾掛情境中比較。"),
            ("冷凍食材要看保存和加熱", "田食原、呷什麵與其他食材選物要看保存、份量、加熱方式和營地限制，不要只看照片。", "成分、保存、加熱方式與適用限制請以商品頁及包裝為準。"),
            ("鍋具和咖啡器材要能一起收", "LEOBUNA、BINCOO 或其他咖啡器具若和鍋具、杯具、餐盒不能一起收納，回程會很狼狽。", "材質、尺寸、重量與清潔方式請以下單前商品頁公告為準。"),
            ("常見錯誤：忘記收洗動線", "露營餐食最常崩壞在餐後：油污、咖啡渣、濕布、未吃完食材和垃圾都需要位置。", "Elite Fashion 編輯團隊的判斷是：好看的露營餐桌，要能在餐後十五分鐘內恢復秩序。"),
            ("下單前排一餐流程", "煮水、沖咖啡、加熱主食、分裝、用餐、收洗、回收。流程跑得通，再補器材。", "價格、規格、活動、庫存、保存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("露營咖啡要先買手沖器具嗎？", "先確認水源、火源、桌面和收洗方式，再決定手沖或濾掛。"),
            ("冷凍食材適合露營嗎？", "要看保存條件、加熱方式和營地限制，資訊請以商品頁及包裝為準。"),
            ("鍋具怎麼避免帶太多？", "先排一餐流程，確認每件器材都會使用，再進購物清單。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[45:50]:
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
        note = "2026-06-21 momo 收益型內容第十組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第十組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
