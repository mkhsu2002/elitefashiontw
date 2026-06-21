#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-four-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B04"

base.COVER_SOURCES = {
    "spring-summer-commute-sun-umbrella-light-bag-outfit": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a3799ed0464819bbfb1063d3fe69162.png",
    "faceless-content-rig-light-filter-audio-buying-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379b35d648819ba23b2e6a9cbb53a7.png",
    "quality-gifting-coffee-tea-massage-umbrella-custom-goods": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379a73d2d0819b85f5614de0c4c337.png",
    "bathroom-kitchen-cleaning-scale-grease-odor-tool-storage": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379ab3a7d0819bb102cc73497c288e.png",
    "beginner-hiking-shirt-rainwear-knee-support-storage-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a379af2b0ec819b8a9a38429d6b0081.png",
}

base.TOPIC_HUBS = {
    "spring-summer-commute-sun-umbrella-light-bag-outfit": {
        "topicCategory": "wardrobe-style",
        "topicCategoryLabel": "衣櫥與穿搭",
        "primaryHub": {
            "key": "commute-style-reset",
            "title": "通勤衣櫥與鞋包選物指南",
            "file": "commute-style-reset.html",
            "url": "/commute-style-reset",
            "category": "casual-chic",
        },
        "secondaryHubs": [
            {
                "key": "outdoor-travel-reset",
                "title": "旅行與戶外移動準備指南",
                "file": "outdoor-travel-reset.html",
                "url": "/outdoor-travel-reset",
                "category": "outdoor-escapes",
            }
        ],
    },
    "faceless-content-rig-light-filter-audio-buying-order": {
        "topicCategory": "creator-tools",
        "topicCategoryLabel": "創作工具",
        "primaryHub": {
            "key": "ai-work-reset-45",
            "title": "AI 工作重整與第二曲線",
            "file": "ai-work-reset-45.html",
            "url": "/ai-work-reset-45",
            "category": "ai-innovation",
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
    "quality-gifting-coffee-tea-massage-umbrella-custom-goods": {
        "topicCategory": "bags-shoes-accessories",
        "topicCategoryLabel": "鞋包與配件",
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
    "bathroom-kitchen-cleaning-scale-grease-odor-tool-storage": {
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
    "beginner-hiking-shirt-rainwear-knee-support-storage-order": {
        "topicCategory": "outdoor-gear",
        "topicCategoryLabel": "戶外裝備",
        "primaryHub": {
            "key": "outdoor-travel-reset",
            "title": "旅行與戶外移動準備指南",
            "file": "outdoor-travel-reset.html",
            "url": "/outdoor-travel-reset",
            "category": "outdoor-escapes",
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
}

base.BLUEPRINTS = {
    "spring-summer-commute-sun-umbrella-light-bag-outfit": {
        "heroAlt": "春夏晴朗通勤天橋長椅上，淡綠防曬外套、淺色小包、折傘、樂福鞋與水瓶形成清爽穿搭配置",
        "audience": "需要在捷運、機車移動與會議室之間維持正式感的春夏通勤讀者",
        "excerpt": "春夏通勤防曬要同時處理遮蔽、收納與正式感，不能只靠一件外套或一把傘。",
        "tags": ["春夏通勤", "防曬外套", "抗風傘", "輕量包"],
        "intro": "春夏通勤最難的地方，不是單純怕曬，而是早上在戶外需要遮蔽，進捷運或辦公室又不能狼狽。外套、抗風傘、輕量包和鞋款必須一起看，才不會出現手上拿太多、包裡塞太滿、進會議室又顯得不俐落的狀況。",
        "editorialAngle": "防曬穿搭要能從捷運、機車到會議室銜接。",
        "sections": [
            ("先決定主要移動方式", "捷運通勤重點是收納與折疊，機車通勤重點是遮蔽和固定，步行通勤則要看鞋款與手持物。移動方式不同，防曬外套、傘和包的優先順序也不同。", "UV100、FULTON 富爾頓皇家晴雨傘與 S′AIME東京企劃可分別放在外套、雨傘和小包位置比較；本文不宣稱防曬效果或 UPF 表現。"),
            ("傘與外套不是互相取代", "傘負責短時間戶外移動，外套負責雙手需要空出來的時刻。若你常騎車、拎咖啡或拿文件，只靠傘會讓通勤變得很忙。", "OMBRA、左都雨傘與 UD LAB 可作為雨具與包款備案參考；抗風、防潑、材質與尺寸要回商品頁確認。"),
            ("輕量包要能收進雨天與冷氣備案", "春夏通勤包看似可以變小，但實際上要放折傘、薄外套、文件、手機與補水用品。太小的包會讓手上多出第二袋，正式感反而下降。", "下單前先把每日物品排在桌上，確認包款開口、背帶寬度和濕物隔離方式。"),
            ("進會議室前要能快速收尾", "好的通勤穿搭不是路上看起來完整而已，也要能在進辦公室前十秒完成整理：傘收進袋、外套摺好、包背帶不扭、鞋面不狼狽。", "這是 Elite Fashion 編輯團隊最重視的判斷：通勤不是造型照，而是一連串轉場。"),
            ("下單前四問", "這件外套收起來多大？這把傘濕了放哪？這個包能否放下文件？這雙鞋走到會議室是否仍得體？四個問題都回答得出來，再看品牌與預算。", "價格、活動、規格、尺寸、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("防曬外套可以取代傘嗎？", "不一定。要看移動方式、雙手是否需要空出來，以及傘濕了後能否收納。"),
            ("文章會推薦特定防曬係數嗎？", "不會。本文不宣稱防曬效果或 UPF，規格請回商品頁確認。"),
            ("輕量包要怎麼選？", "先確認折傘、薄外套、文件與手機是否能分層放入，再看外型。"),
        ],
    },
    "faceless-content-rig-light-filter-audio-buying-order": {
        "heroAlt": "暗色創作者桌面上有無品牌攝影固定架、LED 面板燈、桌上麥克風、濾鏡片與線材收納包",
        "audience": "製作不露臉短影音、產品拍攝或知識內容，需要按順序採買設備的人",
        "excerpt": "不露臉內容的設備順序是固定、光線、聲音先穩，再補濾鏡、風格與其他周邊。",
        "tags": ["不露臉內容", "拍攝設備", "LED 燈", "收音"],
        "intro": "不露臉內容不是少一張臉就能少一半設備。鏡頭不穩、光線亂、聲音悶，會比是否露臉更快讓觀眾離開。支架、燈光、濾鏡與收音應該按問題排序，而不是看到哪個配件漂亮就先買哪個。",
        "editorialAngle": "先把固定、光線與聲音三件事穩住，再談濾鏡和風格。",
        "sections": [
            ("第一件事是固定，不是濾鏡", "桌拍、手部示範、商品開箱或講解畫面，都需要穩定的拍攝位置。支架高度、夾具角度和桌面重量，會直接影響拍攝是否能重複。", "GoRig、Haida 與 DTAudio 可放在固定、濾鏡和聲音情境中比較；本文不假裝實測，也不承諾畫質或收音改善。"),
            ("光線決定畫面是否乾淨", "燈光的價值不是把畫面打亮而已，而是讓主體、桌面和背景分開。若只靠房間天花板燈，商品邊緣和手部動作很容易糊成一片。", "燈后、SANSUI 山水與 Momax Taiwan 可作為照明、影音和周邊參考；亮度、色溫、供電和相容性以商品頁為準。"),
            ("收音比很多人想得更早", "不露臉內容常靠聲音建立信任。即使畫面很乾淨，背景噪音、桌面震動或過遠收音都會削弱專業感。", "購買前先確認拍攝距離、連接方式、是否需要轉接與錄音環境，不要只看商品照片。"),
            ("濾鏡是風格工具，不是救命工具", "濾鏡、色片和背景布可以讓畫面更有風格，但它們解決不了晃動、暗光與噪音。若前三件事還不穩，濾鏡只會讓問題更漂亮地出現。", "這是 Elite Fashion 編輯團隊的採買順序：先穩定，再乾淨，最後才是風格。"),
            ("下單前做一次假拍攝", "把手機或相機放在預計位置，錄三十秒，檢查畫面是否晃、光是否亂、聲音是否空。問題在哪裡，就先買哪一類設備。", "價格、規格、活動、庫存、保固、相容性與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("不露臉內容第一個設備要買什麼？", "通常先看固定與支架，因為畫面不穩會影響所有後續設備的價值。"),
            ("濾鏡可以讓畫質變好嗎？", "本文不承諾畫質改善。濾鏡更適合作為風格工具，實際表現需看設備與環境。"),
            ("收音要很早規劃嗎？", "建議要。知識型或產品講解內容很依賴聲音清楚度。"),
        ],
    },
    "quality-gifting-coffee-tea-massage-umbrella-custom-goods": {
        "heroAlt": "木桌上有無字禮盒、陶瓷茶具、玻璃罐咖啡豆、黑色折傘、無品牌按摩設備與木質小物",
        "audience": "想替同事、家人、合作夥伴或節日場合挑選不過度用力禮物的人",
        "excerpt": "質感送禮的關鍵是使用頻率與對方能否自然收下，不是價格、包裝或聲量。",
        "tags": ["質感送禮", "咖啡茶禮", "雨傘", "客製小物"],
        "intro": "送禮最怕用力。咖啡、茶、按摩設備、雨傘和客製小物都能很體面，但真正好的禮物，是對方能在自己的生活裡自然使用，而不是收下後還要找地方供著。本文用使用頻率、保存門檻和關係距離，重新整理一份不過度表演的送禮順序。",
        "editorialAngle": "送禮先看對方生活節奏，不要只看價格或包裝。",
        "sections": [
            ("先判斷對方會不會真的使用", "喜歡咖啡的人未必需要器材，喝茶的人也未必想要大禮盒。送禮前先想對方的一天如何開始、在辦公室停留多久、家裡是否有收納空間。", "Teavoya、馬克老爹專賣好咖啡與大檜仁心可作為茶、咖啡與木質小物情境參考；口味與材質仍以商品頁為準。"),
            ("按摩設備要更保守", "按摩設備看起來體貼，但涉及身體感受、使用禁忌和收納空間，不適合所有關係。若不確定，寧可選擇更低壓力的茶、咖啡或雨傘。", "LamiFans 與輝葉良品可放在生活設備和按摩用品裡比較；本文不承諾按摩、舒緩或健康效果。"),
            ("雨傘是務實禮，但要看風格距離", "一把好傘有使用頻率，也不會太私人；但顏色、尺寸、重量與收納方式會影響對方是否真的帶出門。", "FULTON 富爾頓皇家晴雨傘適合放在通勤與送禮情境中看；抗風、防潑與耐用資訊請回商品頁確認。"),
            ("客製小物要克制", "客製化容易顯得用心，也容易過度靠近。除非很了解對方，建議選低個人化、可放在桌面或包內的小物，不要把名字、紀念日或私密語句做得太醒目。", "Elite Fashion 編輯團隊的判斷是：禮物要替對方減少負擔，不是增加解釋。"),
            ("下單前的送禮三問", "對方會在哪裡用、多久用一次、收納是否麻煩。三個答案都清楚，才進入價格、包裝和配送時間。", "價格、活動、規格、庫存、保存期限、材質和配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("質感送禮要先看價格嗎？", "不用。先看對方生活節奏、使用頻率和收納負擔，再看預算。"),
            ("按摩設備適合送禮嗎？", "要保守判斷。本文不承諾按摩或健康效果，且應確認對方是否適合使用。"),
            ("客製小物要怎麼不尷尬？", "降低個人化強度，選擇可自然使用的小物，不把私密訊息做得太醒目。"),
        ],
    },
    "bathroom-kitchen-cleaning-scale-grease-odor-tool-storage": {
        "heroAlt": "明亮浴室與廚房交界檯面上，空白清潔噴瓶、刷具、抹布、刮水器、小水桶與綠植整齊分工",
        "audience": "需要替浴室、廚房和清潔工具建立分工，不想讓家務變成大工程的人",
        "excerpt": "浴室與廚房清潔要先分污垢來源，再分工具與收納；香味不是清潔完成的證明。",
        "tags": ["浴室清潔", "廚房清潔", "水垢油污", "清潔工具收納"],
        "intro": "清潔用品最容易被買成一整排，但真正有效的不是瓶數，而是分工。浴室的水垢、廚房的油污、排水處的氣味和工具收納各自有不同問題；如果用一瓶想解決全屋，最後常會變成更混亂的收納和更模糊的責任。",
        "editorialAngle": "先分污垢來源，再分清潔工具；香味不是清潔完成的證明。",
        "sections": [
            ("先分水垢、油污、氣味和日常擦拭", "浴室常見的是水垢、皂垢與潮濕，廚房常見的是油污、食物殘留與檯面擦拭。先分來源，才知道清潔劑和工具如何配置。", "美利購、天森無患與 JINKO 淨科可放在不同清潔用品情境中比較；抗菌、除菌或安全無毒等描述，必須以商品頁支持為準。"),
            ("工具比香味更能證明清潔完成", "香味會讓人覺得乾淨，但它不是清潔完成的證據。刷具、抹布、刮水器、手套和晾乾位置，往往比味道更能影響日常維護。", "淨淨 Clean Clean、真蓁嚴選清潔生活館與 MORINO 可作為清潔用品、掃除工具與毛巾備品參考。"),
            ("浴室工具要能晾乾", "浴室清潔工具若沒有晾乾位置，很快就會成為另一個需要清潔的物件。刷子、抹布和刮水器要有固定掛點或通風位置。", "購買前先看尺寸、掛放方式、替換耗材和是否適合現有浴室，不要只看照片。"),
            ("廚房工具要避免交叉使用", "擦油污的布、擦餐桌的布和擦水槽的刷具不應混用。用顏色或位置分區，能減少家務中的猶豫。", "這是 Elite Fashion 編輯團隊的具體判斷：清潔分工不是潔癖，而是讓每次家務少一次決定。"),
            ("下單前的清潔櫃盤點", "把現有清潔品拿出來，分成浴室、廚房、地板、備品四類。重複功能的先消耗完，再補真正缺少的工具。", "價格、成分、規格、活動、庫存、使用限制與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("浴室和廚房清潔用品可以共用嗎？", "部分工具可共用，但油污、水垢和氣味來源不同，建議依功能分區。"),
            ("香味可以代表清潔完成嗎？", "不可以。香味只是感受，不能取代實際清潔與沖洗。"),
            ("文章會宣稱抗菌或除菌嗎？", "不會。除非商品頁有明確支持，本文不宣稱抗菌、除菌或安全無毒。"),
        ],
    },
    "beginner-hiking-shirt-rainwear-knee-support-storage-order": {
        "heroAlt": "霧氣山徑旁木桌上有排汗衣、灰色雨衣褲、護膝、輕量收納袋、水瓶與橘色反光配件",
        "audience": "準備開始輕登山、郊山步道或週末戶外行程，需要建立基礎裝備順序的人",
        "excerpt": "新手登山裝備要先處理天氣、支撐與收納，再談品牌完整度和風格小物。",
        "tags": ["新手登山", "排汗衣", "雨衣褲", "護膝"],
        "intro": "新手登山最容易把購物清單寫得太滿：外套、鞋、包、帽子、配件都想一次到位。但真正第一輪該買的，是能應對天氣、路線變化和身體負擔的東西。排汗衣、雨衣褲、護膝和輕量收納應該按風險排序，而不是按照片完整度排序。",
        "editorialAngle": "先買能應對氣候與路線風險的東西，再買風格小物。",
        "sections": [
            ("天氣是第一順位", "郊山也可能遇到悶熱、午後雨、風口和濕滑路面。排汗衣與雨衣褲的順序應早於造型配件，因為它們處理的是路線中的基本不確定。", "Litume 意都美、北方狼與 ANPING 安平可放在登山服飾、雨具與戶外用品裡比較；本文不承諾安全保證。"),
            ("護膝護腰要保守看待", "護膝、護腰或其他支撐用品可以放進裝備選項，但不應被當成醫療防護或免除訓練的捷徑。若已有疼痛、麻木或活動受限，應先尋求專業協助。", "BELEX 與 Jasper 大來護具 Mo+ 可作為支撐用品參考；本文不宣稱治療、止痛或醫療效果。"),
            ("輕量收納讓雨具和濕物有位置", "雨衣褲、濕毛巾、備用襪和小垃圾都需要位置。沒有收納袋，回程很容易把乾濕物混在一起。", "反光屋 FKW 可放在夜間可視與反光配件情境中比較；夜間或低能見度活動仍需依路線和官方資訊評估。"),
            ("不要用品牌完整度取代路線判斷", "同一套裝備不會適合所有路線。新手應先看步道長度、海拔、天氣、撤退點和同行者，再決定是否需要加買。", "Elite Fashion 編輯團隊的判斷是：第一套登山裝備應該能讓你更穩地完成簡單路線，而不是看起來最像資深玩家。"),
            ("出門前的四項確認", "天氣預報、路線時間、雨具位置、身體狀態。這四件事確認後，再看包內是否有水、行動電源、簡易補給和必要個人物品。", "價格、規格、活動、尺寸、庫存、適用條件與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("新手登山第一件該買什麼？", "先看天氣和路線需求，通常排汗衣、雨具和基本收納會比風格配件更早。"),
            ("護膝可以保證登山安全嗎？", "不可以。本文不承諾安全保證或醫療防護，身體不適應先尋求專業協助。"),
            ("反光配件一定要帶嗎？", "若可能遇到低能見度、傍晚回程或車道旁移動，可納入備案，但仍要依路線規劃。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[15:20]


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
        note = "2026-06-21 momo 收益型內容第四組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第四組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
