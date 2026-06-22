#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-fourteen-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B14"

base.COVER_SOURCES = {
    "patio-balcony-shade-outdoor-chair-storage-plant-care": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a382966a6dc81989d2336a3b1c0256f.png",
    "swimming-outdoor-class-goggles-sun-towel-storage-bag": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a3829b1fb7481989abb21194f0cb86c.png",
    "city-weekend-photo-kit-phone-rig-cpl-filter-sun-jacket": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a382ace93f08198a731f796e11cdda6.png",
    "car-phone-setup-mount-charger-cable-dashcam-rain": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a382b1d051c81988b88eac442f827cf.png",
    "presentation-day-remote-gear-headset-mic-monitor-light": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a382a81766c8198b535fd269ef87639.png",
}

ROW_OVERRIDES = {
    "patio-balcony-shade-outdoor-chair-storage-plant-care": {
        "elite_judgment": "小陽台先分遮陽、坐下、澆水與收納四件事，不要把戶外家具買成另一個雜物角落。",
        "answer_summary": "小陽台與庭院用品要先看日照、雨水、椅子尺度、植物照顧頻率與收納位置，再比較戶外用品。",
        "risk_guardrail": "遮陽、戶外椅、植物用品與收納家具的尺寸、材質、耐候、承重與安裝限制請以商品頁及現場條件為準。",
    },
    "swimming-outdoor-class-goggles-sun-towel-storage-bag": {
        "elite_judgment": "游泳與戶外課前準備先看濕物回收和日曬時間，泳鏡、防曬、毛巾與收納袋才會真的用得到。",
        "answer_summary": "游泳與戶外課前準備要先分泳池用品、防曬、毛巾乾濕分離與回家清洗，再比較品牌與商品。",
        "risk_guardrail": "泳鏡、防曬、毛巾、收納袋與戶外用品不作防護保證；尺寸、材質、標示、使用限制與清洗方式請以商品頁及包裝為準。",
    },
    "city-weekend-photo-kit-phone-rig-cpl-filter-sun-jacket": {
        "elite_judgment": "城市週末拍攝包先看拍攝路線、光線與拿取頻率，手機支架、濾鏡和防曬外套才不會只是重量。",
        "answer_summary": "城市週末拍攝包要先看手機固定、濾鏡收納、日照與步行時間，再比較支架、濾鏡、防曬外套與雨天備案。",
        "risk_guardrail": "手機支架、濾鏡、外套、配件與雨具的相容性、尺寸、材質、防護描述與使用限制請以商品頁為準。",
    },
    "car-phone-setup-mount-charger-cable-dashcam-rain": {
        "elite_judgment": "車用手機配置先把視線、線材、電力與雨天拿取分開，不要讓手機架和充電線影響駕駛動線。",
        "answer_summary": "車用手機配置要先看固定位置、充電線路、行車紀錄與雨天備案，再比較手機架、車充、線材與配件。",
        "risk_guardrail": "車用手機架、車充、線材、行車紀錄器與雨具的安裝、安全、相容性、法規與使用限制請以商品頁、車輛手冊與道路規範為準。",
    },
    "presentation-day-remote-gear-headset-mic-monitor-light": {
        "elite_judgment": "簡報日設備先看聲音、畫面、光線與備援，不要只升級螢幕或麥克風其中一項。",
        "answer_summary": "遠距簡報設備要先看耳機收音、麥克風距離、螢幕視線、桌面光線與備用線材，再比較設備。",
        "risk_guardrail": "耳機、麥克風、螢幕、燈具與線材的相容性、規格、保固、用電與使用限制請以商品頁及官方說明為準。",
    },
}

base.TOPIC_HUBS = {
    "patio-balcony-shade-outdoor-chair-storage-plant-care": {"topicCategory": "outdoor-gear", "topicCategoryLabel": "戶外裝備", "primaryHub": {"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}, "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}]},
    "swimming-outdoor-class-goggles-sun-towel-storage-bag": {"topicCategory": "outdoor-gear", "topicCategoryLabel": "戶外裝備", "primaryHub": {"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
    "city-weekend-photo-kit-phone-rig-cpl-filter-sun-jacket": {"topicCategory": "smart-living-tech", "topicCategoryLabel": "智慧生活科技", "primaryHub": {"key": "ai-work-reset-45", "title": "工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"}, "secondaryHubs": [{"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}]},
    "car-phone-setup-mount-charger-cable-dashcam-rain": {"topicCategory": "smart-living-tech", "topicCategoryLabel": "智慧生活科技", "primaryHub": {"key": "ai-work-reset-45", "title": "工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"}, "secondaryHubs": [{"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}]},
    "presentation-day-remote-gear-headset-mic-monitor-light": {"topicCategory": "smart-living-tech", "topicCategoryLabel": "智慧生活科技", "primaryHub": {"key": "ai-work-reset-45", "title": "工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"}, "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}]},
}

base.BLUEPRINTS = {
    "patio-balcony-shade-outdoor-chair-storage-plant-care": {
        "heroAlt": "陽光小陽台有遮陽布、藤編戶外椅、植栽、澆水壺與收納長凳",
        "audience": "想把小陽台或庭院角落整理成可坐、可照顧植物、也好收納的人",
        "excerpt": "小陽台先分遮陽、坐下、澆水與收納四件事，再決定戶外椅、遮陽用品和植物工具要買到哪裡。",
        "tags": ["小陽台", "戶外椅", "遮陽", "植物照顧"],
        "intro": "小陽台最容易被當成額外收納區，直到想坐下喝杯茶時，才發現椅子、植物、清潔工具與晒衣用品互相搶位置。真正好用的陽台不一定大，而是日照、雨水、坐下尺度、澆水路線與收納位置都先排清楚。若只因為一張戶外椅照片心動，很可能買回家後沒有地方伸腳，也沒有地方收墊子。",
        "editorialAngle": "先處理日照和雨水，再放入椅子與植物。",
        "sections": [
            ("先看日照，不要先看椅子", "陽台日照會決定遮陽、植物和坐下時間。西曬強的空間需要先想遮蔭，日照少的空間則要避免過度堆植物。", "把早上、下午和雨天各看一次，比只看尺寸更可靠。"),
            ("戶外椅要留腳和轉身空間", "小陽台的椅子不是越舒服越好，而是坐下後還能開門、拿水、澆花和收東西。", "購買前先用膠帶在地面貼出椅子尺度。"),
            ("植物照顧要有工具位置", "澆水壺、剪刀、土鏟和肥料如果沒有固定位置，最後會和室內雜物混在一起。", "植物用品要遠離高頻通道，也要考慮滴水與清潔。"),
            ("常見錯誤：把收納箱放到最順手的位置", "收納箱若佔了最佳坐位，陽台就失去生活功能。收納應服務使用，不是取代使用。", "只保留戶外真正會用到的物品。"),
            ("下單前的四區檢查", "遮陽、坐下、植物、收納。每一區都要有明確位置，再比較品牌與預算。", "Elite Fashion 編輯團隊的判斷是：小陽台的價值不是塞滿戶外感，而是讓一個平日傍晚真的能被使用。"),
        ],
        "faq": [("小陽台先買戶外椅嗎？", "不一定。先看日照、雨水和門片開合，確定坐下後不影響動線。"), ("植物用品要放室內還室外？", "看濕氣、日曬和拿取頻率；常用工具可以放室外，但要避免受潮。"), ("遮陽用品要怎麼選？", "先看安裝限制、租屋規範、風勢和日照方向，再看材質。")],
    },
    "swimming-outdoor-class-goggles-sun-towel-storage-bag": {
        "heroAlt": "泳池旁木桌有無標誌泳鏡、藍色毛巾、白色防曬瓶、網袋、水瓶與帽子",
        "audience": "需要替游泳課、戶外課或夏季活動整理包內順序的人",
        "excerpt": "游泳與戶外課準備要先分乾濕、日曬、回家清洗與補水，再決定泳鏡、防曬、毛巾和收納袋。",
        "tags": ["游泳課", "泳鏡", "防曬", "乾濕分離"],
        "intro": "游泳與戶外課最容易漏掉的不是大件物品，而是使用後的回收路線。泳鏡、防曬、毛巾、濕衣物、收納袋和回家後清洗，如果沒有先分乾濕，很快會讓整個包都潮濕。好的準備不是把用品買多，而是讓上課前、課中、課後各自有順序。",
        "editorialAngle": "先分乾濕與日曬，再放入泳鏡和毛巾。",
        "sections": [
            ("泳鏡先看臉型與收納盒", "泳鏡不是只看顏色，還要看貼合、調整方式和是否有固定收納盒。沒有盒子時，鏡面很容易和其他物品摩擦。", "配戴感和視野請以商品頁與實際使用為準。"),
            ("防曬用品要放在課前會拿的位置", "防曬若放在包底，常常到現場才想起來。它應該和毛巾、帽子或外套一起放在第一層。", "防曬標示、使用方式與補擦條件請以包裝為準。"),
            ("毛巾和濕物要分開", "乾毛巾、濕泳衣、拖鞋和水瓶不應全部放在同一層。網袋、夾鏈袋或乾濕分離袋能減少回家後的整理壓力。", "材質是否防水或透氣，請回商品頁確認。"),
            ("常見錯誤：只準備去程，沒準備回程", "活動結束後才是真正考驗。濕物、汗味、瓶罐和垃圾都需要位置。", "回程動線順，下一次才不會抗拒準備。"),
            ("出門前的五件確認", "泳鏡、毛巾、防曬、水瓶、濕物袋。五件都在固定位置，再補其他小物。", "Elite Fashion 編輯團隊的判斷是：游泳與戶外課的購物價值，來自讓回家後更好收，而不是讓包看起來更專業。"),
        ],
        "faq": [("游泳包要買乾濕分離嗎？", "若常有濕衣物或濕毛巾，乾濕分離會更好整理；仍要看包款材質和容量。"), ("防曬能保證戶外不曬傷嗎？", "不能保證。請依商品標示使用，並搭配衣物、帽子與補擦。"), ("泳鏡需要收納盒嗎？", "建議有固定收納，能降低鏡面被刮傷的機率。")],
    },
    "city-weekend-photo-kit-phone-rig-cpl-filter-sun-jacket": {
        "heroAlt": "城市屋頂夕陽下有無標誌手機支架、空白濾鏡盒、圓形濾鏡、防曬外套、小包與墨鏡",
        "audience": "想用手機拍攝週末城市散步、短影音或旅行紀錄的人",
        "excerpt": "城市週末拍攝包要先看路線、光線、手持穩定與拿取頻率，再決定手機支架、濾鏡、防曬外套和雨天備案。",
        "tags": ["手機拍攝", "城市週末", "CPL濾鏡", "防曬外套"],
        "intro": "城市週末拍攝包最容易被器材清單帶著走：支架、濾鏡、補光、外套、雨具、小包，每一樣都看起來合理，最後卻變成一整天的重量。真正該先想的，是路線會遇到什麼光、要拍多少次、器材是否能快速拿取，以及太陽或雨天會不會讓拍攝中斷。",
        "editorialAngle": "先看路線光線，再決定器材重量。",
        "sections": [
            ("手機支架要服務拍攝姿勢", "如果多半是街角、咖啡桌或屋頂定點拍攝，迷你腳架會比大型設備更實際。若是一邊走一邊拍，重量和收納速度更重要。", "相容性、承重和夾具尺寸請回商品頁確認。"),
            ("濾鏡不要帶到忘記使用", "CPL、黑柔或其他濾鏡應該對應明確場景，例如玻璃反光、水面、強日照或夜晚燈光。沒有場景就先少帶。", "濾鏡尺寸、轉接環和手機鏡頭位置要先確認。"),
            ("防曬外套是行程穩定器", "城市拍攝常在日照最強的時段移動。薄外套、帽子或雨具不只是防曬，也能讓行程不被天氣打斷。", "防護描述與材質標示請以商品頁為準。"),
            ("常見錯誤：把所有器材放在最深處", "拍攝小物若拿取麻煩，就會被放棄使用。濾鏡盒、支架和手機線材應放在同一側，避免每次停下來都翻包。", "小包內的層次比器材數量更重要。"),
            ("出門前的三格包法", "手機固定、光線控制、天氣備案。三格都成立，再加入水瓶或個人物品。", "Elite Fashion 編輯團隊的判斷是：好的城市拍攝包不是帶最多，而是讓你在光線出現時能立刻拿得到。"),
        ],
        "faq": [("手機拍攝一定需要濾鏡嗎？", "不一定。若沒有明確反光、強光或夜景需求，先從支架與收納開始。"), ("防曬外套要放拍攝包嗎？", "如果行程多在戶外或午後，建議納入備案。"), ("器材包怎麼避免太重？", "把器材分成必拍、可能用、備案三類，只帶前兩類。")],
    },
    "car-phone-setup-mount-charger-cable-dashcam-rain": {
        "heroAlt": "雨天停車中的車內副駕座，有空白手機架、車充、線材、小型行車紀錄器、折傘與擦拭布",
        "audience": "想整理車內手機架、充電線、行車紀錄與雨天備案的人",
        "excerpt": "車用手機配置要先看視線、線材、電力與雨天拿取，再決定手機架、車充、線材和行車紀錄器的位置。",
        "tags": ["車用手機架", "車充線材", "行車紀錄器", "雨天備案"],
        "intro": "車內配件不是買齊就好，尤其手機架、車充、線材與行車紀錄器都和視線、電力和安全動線有關。若手機架擋住視野、線材跨過排檔、雨傘和擦拭布放在拿不到的位置，再好的配件都會變成干擾。整理車用手機配置，應該先把視線、線路、電力和雨天備案分開。",
        "editorialAngle": "先保留視線與駕駛動線，再整理電力。",
        "sections": [
            ("手機架先看視線，不看造型", "手機架應避免遮擋前方視野、出風口關鍵操作或安全氣囊區域。不同車款條件不同，下單前要回到實車位置測量。", "安裝與道路規範請依車輛手冊和當地規定。"),
            ("充電線要走最短且不干擾的路", "線材太長會纏住杯架和排檔，太短又會拉扯接口。線路應先畫出來，再決定車充和線長。", "功率、接口和相容性請回商品頁確認。"),
            ("行車紀錄器要和手機功能分工", "行車紀錄器負責記錄，手機負責導航或聯絡。兩者都需要電力和固定位置，不能互相搶插座。", "錄影規格、安裝角度和記憶卡條件請以官方說明為準。"),
            ("雨天備案要放在下車前拿得到的位置", "折傘、擦拭布、雨衣或小袋如果放到後車廂，下車瞬間就來不及。副駕或門邊應有固定位置。", "濕物也要有回收袋，避免弄濕座椅。"),
            ("出發前的一分鐘檢查", "手機固定、線材不纏、電力正常、鏡頭視角清楚、雨具可拿。五件完成再出發。", "Elite Fashion 編輯團隊的判斷是：車用配置的好買點，是讓駕駛更少分心，而不是讓中控台更滿。"),
        ],
        "faq": [("手機架可以裝在任何位置嗎？", "不建議。要避開視線遮擋、安全氣囊與操作干擾，並依車款條件判斷。"), ("車充要看瓦數嗎？", "要看裝置需求、接口與線材相容性，但仍以商品頁和裝置規格為準。"), ("雨具放後車廂可以嗎？", "備用可以，但常用雨具建議放在下車前拿得到的位置。")],
    },
    "presentation-day-remote-gear-headset-mic-monitor-light": {
        "heroAlt": "專業居家工作桌有無標誌耳機、麥克風、黑屏外接螢幕、桌燈、筆電與空白筆記本",
        "audience": "需要在簡報、遠距會議或線上提案前整理桌面設備的人",
        "excerpt": "簡報日設備要先看聲音、畫面、光線與備援，再比較耳機、麥克風、螢幕、桌燈和線材。",
        "tags": ["遠距簡報", "耳機麥克風", "外接螢幕", "桌面光線"],
        "intro": "簡報日最怕的是前十分鐘才發現聲音不穩、鏡頭畫面太暗、螢幕切換不順或線材不見。耳機、麥克風、外接螢幕和桌燈都能改善呈現，但順序要先從失敗風險開始：聲音是否清楚、畫面是否可讀、光線是否穩定、備援是否存在。這比單純升級某一件設備更重要。",
        "editorialAngle": "先降低簡報失敗風險，再升級設備。",
        "sections": [
            ("聲音永遠比畫面更早檢查", "遠距簡報中，聲音斷續比畫面普通更影響理解。耳機、麥克風和環境噪音要先測，位置也要固定。", "收音表現與相容性請以商品頁和實際軟體測試為準。"),
            ("螢幕要服務資料切換", "外接螢幕不是越大越好，而是能不能同時看簡報、備註、通訊與資料。桌深與視距也要一起看。", "尺寸、接口、解析度和支架高度都要確認。"),
            ("光線要穩，不要只追求好看", "桌燈或補光要避免反光、臉部陰影和螢幕眩光。若窗邊光線變化大，簡報前要先測試。", "燈具亮度、色溫與用電安全請回商品頁確認。"),
            ("備援線材和備用耳機要固定位置", "簡報日不應臨時找轉接頭。備援配件放在同一個小袋，並在前一天確認。", "線材相容性要依設備和會議平台確認。"),
            ("前一天的設備彩排", "開會軟體、麥克風、耳機、螢幕分享、燈光、充電器。六件一次測完，隔天才不慌。", "Elite Fashion 編輯團隊的判斷是：簡報日設備的價值不是桌面看起來專業，而是讓你少一個失控點。"),
        ],
        "faq": [("遠距簡報先買麥克風還是耳機？", "先測目前聲音問題。若環境吵，耳機和收音位置通常要一起看。"), ("外接螢幕一定需要嗎？", "若常要看備註、資料與簡報畫面，外接螢幕會更有幫助；仍要看桌深和接口。"), ("桌燈可以取代補光嗎？", "要看角度、亮度和反光情況。簡報前應實際測試畫面。")],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[65:70]:
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
        note = "2026-06-21 momo 收益型內容第十四組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第十四組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
