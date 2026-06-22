#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-fifteen-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B15"

base.COVER_SOURCES = {
    "efficient-desk-cushion-backrest-monitor-storage-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0835e28e7b9c9065016a387d9c9658819899432dfad0dd1fd6.png",
    "work-corner-sound-headphones-speaker-noise-meeting-audio": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0835e28e7b9c9065016a38805dd3c481989efe7180d0be13a7.png",
    "summer-office-ac-backup-light-jacket-hot-drink-earplug-lamp": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0835e28e7b9c9065016a387e45ff148198a2ab7585bff5d811.png",
    "long-trip-recovery-kit-earplug-brace-luggage-tea-sun": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0835e28e7b9c9065016a387fb0191c81989f370441f8f5cdea.png",
    "elder-reading-care-corner-lamp-glasses-storage-care-supplies": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0835e28e7b9c9065016a3880083990819885c22836e166abde.png",
}

ROW_OVERRIDES = {
    "efficient-desk-cushion-backrest-monitor-storage-order": {
        "elite_judgment": "高效率桌面要先看坐姿、視線、收納與線材，不是把桌子換大就能解決工作阻力。",
        "answer_summary": "高效率桌面要先看椅墊靠枕、螢幕高度、桌面收納與線材位置，再比較家具與設備。",
        "risk_guardrail": "椅墊、靠枕、螢幕、收納與燈具的尺寸、材質、承重、相容性與使用限制請以商品頁及現場條件為準。",
    },
    "work-corner-sound-headphones-speaker-noise-meeting-audio": {
        "elite_judgment": "工作角落的聲音要分會議、專注、播放與備援四種情境，耳機和喇叭才不會互相干擾。",
        "answer_summary": "工作角落聲音整理要先看會議收音、耳機配戴、喇叭位置與噪音來源，再比較音訊設備。",
        "risk_guardrail": "耳機、喇叭、麥克風、耳塞與線材的相容性、材質、音量、安全與使用限制請以商品頁及官方說明為準。",
    },
    "summer-office-ac-backup-light-jacket-hot-drink-earplug-lamp": {
        "elite_judgment": "夏季辦公室冷氣備案先處理溫差、噪音與桌面光線，不要把薄外套或熱飲寫成身體解方。",
        "answer_summary": "夏季辦公室冷氣備案要先看座位風口、薄外套、熱飲、耳塞與桌面燈，再比較日常小物。",
        "risk_guardrail": "薄外套、熱飲、耳塞、燈具與防曬衣物不作健康、助眠或療效承諾；材質、成分、亮度與使用限制請以商品頁及包裝為準。",
    },
    "long-trip-recovery-kit-earplug-brace-luggage-tea-sun": {
        "elite_judgment": "長途移動恢復包先看睡眠干擾、身體支撐、行李拿取與日曬變化，備品才不會只增加重量。",
        "answer_summary": "長途移動恢復包要先看耳塞、護具、行李箱拿取、茶包與防曬層次，再比較旅行用品。",
        "risk_guardrail": "耳塞、護具、行李箱、茶包、防曬與雨具不作健康、保健或恢復效果承諾；材質、尺寸、成分、標示與使用限制請以商品頁及包裝為準。",
    },
    "elder-reading-care-corner-lamp-glasses-storage-care-supplies": {
        "elite_judgment": "閱讀與照護角落先把光線、眼鏡、拿取高度與備品分層，避免讓關心變成家人每天翻找。",
        "answer_summary": "閱讀與照護角落要先看檯燈光線、眼鏡位置、收納高度與照護備品，再比較用品。",
        "risk_guardrail": "檯燈、眼鏡、收納、照護用品與保健相關商品不作醫療、療效或安全保證；規格、標示與使用限制請以商品頁及專業建議為準。",
    },
}

base.TOPIC_HUBS = {
    "efficient-desk-cushion-backrest-monitor-storage-order": {"topicCategory": "smart-living-tech", "topicCategoryLabel": "智慧生活科技", "primaryHub": {"key": "ai-work-reset-45", "title": "工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"}, "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}]},
    "work-corner-sound-headphones-speaker-noise-meeting-audio": {"topicCategory": "smart-living-tech", "topicCategoryLabel": "智慧生活科技", "primaryHub": {"key": "ai-work-reset-45", "title": "工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
    "summer-office-ac-backup-light-jacket-hot-drink-earplug-lamp": {"topicCategory": "recovery-sleep", "topicCategoryLabel": "睡眠與恢復", "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}, "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}]},
    "long-trip-recovery-kit-earplug-brace-luggage-tea-sun": {"topicCategory": "recovery-sleep", "topicCategoryLabel": "睡眠與恢復", "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}, "secondaryHubs": [{"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}]},
    "elder-reading-care-corner-lamp-glasses-storage-care-supplies": {"topicCategory": "recovery-sleep", "topicCategoryLabel": "睡眠與恢復", "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}, "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}]},
}

base.BLUEPRINTS = {
    "efficient-desk-cushion-backrest-monitor-storage-order": {
        "heroAlt": "明亮工作桌旁有椅墊、靠枕、黑屏外接螢幕、文件收納盤、桌燈與綠植",
        "audience": "想提升工作桌使用效率但不想只靠換大桌的人",
        "excerpt": "桌面效率先看坐姿、視線、收納與線材，再決定椅墊、靠枕、螢幕和收納品。",
        "tags": ["工作桌", "椅墊靠枕", "螢幕配置", "桌面收納"],
        "intro": "很多人以為工作卡住是桌子不夠大，實際上常是椅子坐不住、螢幕高度不對、文件沒有回收位置、線材每天都要重整理。桌面效率不是把桌面清空，而是讓身體、視線和物件都有固定路線。換大桌之前，先檢查坐姿、螢幕和收納，通常更接近問題核心。",
        "editorialAngle": "先修坐姿與視線，再買桌面收納。",
        "sections": [
            ("先看椅子，不要先看桌子", "椅墊和靠枕的存在，是讓坐姿更容易維持，而不是把普通椅子變成萬能設備。高度、深度和桌面距離要一起看。", "如果腳放不穩或手肘懸空，再大的桌面都會累。"),
            ("螢幕高度決定切換成本", "外接螢幕應服務視窗切換與閱讀，不只是增加一片黑色設備。桌深、眼距和筆電位置要一起調整。", "尺寸、接口、支架與相容性請以商品頁為準。"),
            ("收納要處理正在進行的事", "文件盤、抽屜盒和桌上收納應分成待處理、進行中、已完成。沒有狀態分層，收納只是把工作藏起來。", "高頻工具留桌面，低頻物品退到櫃內。"),
            ("常見錯誤：把效率買成裝飾", "桌燈、螢幕架、收納盒都可能讓桌面更漂亮，但若沒有對應使用時刻，就會變成新的障礙物。", "每件物品都要回答自己幫你少做哪一步。"),
            ("下單前的四點檢查", "坐姿、視線、文件、線材。四點都畫出位置，再比較椅墊、螢幕、收納與燈具。", "Elite Fashion 編輯團隊的判斷是：高效率桌面的轉換力，在於讓工作開始更容易，而不是讓桌面看起來更大。"),
        ],
        "faq": [("桌子太小一定要換大桌嗎？", "不一定。先看收納、線材和螢幕位置，很多問題不是桌面尺寸造成。"), ("椅墊和靠枕怎麼選？", "先看椅子深度、高度和坐姿需求，材質與尺寸請回商品頁確認。"), ("外接螢幕需要搭配收納嗎？", "建議一起看，否則桌面容易被線材、文件和配件重新佔滿。")],
    },
    "work-corner-sound-headphones-speaker-noise-meeting-audio": {
        "heroAlt": "深色工作角落有無標誌耳機、麥克風、喇叭、吸音板、理線托盤與綠植",
        "audience": "想整理會議收音、專注聆聽和桌面聲音設備的人",
        "excerpt": "聲音整理要分會議、專注、播放與備援，不要讓耳機、喇叭和麥克風互相搶位置。",
        "tags": ["耳機", "會議收音", "桌面喇叭", "工作角落"],
        "intro": "工作角落的聲音很少只有一種用途。會議需要清楚收音，專注需要降低干擾，播放需要穩定音量，臨時狀況需要備援。若只買一副耳機或一支麥克風，卻沒有看空間噪音、桌面位置和線材，聲音設備很快會變成桌上的另一團線。",
        "editorialAngle": "先分聲音用途，再選耳機與麥克風。",
        "sections": [
            ("會議聲音先測環境", "先在平常開會的位置錄一小段聲音，聽鍵盤、冷氣、窗外與回音。問題來源清楚後，再決定耳機、麥克風或吸音配置。", "不要直接用器材規格推論效果。"),
            ("耳機和喇叭要分工", "耳機適合會議和專注，喇叭適合短暫播放和不需要隱私的內容。兩者都放桌面時，要避免互相擋線與佔位。", "配戴感、音量和相容性請回商品頁確認。"),
            ("麥克風距離比外型重要", "麥克風太遠會收進環境聲，太近又可能擋住視線或鍵盤。支架、線材和桌面位置要一起看。", "若會議不頻繁，可先優化既有設備。"),
            ("常見錯誤：所有聲音設備都插著", "耳機、喇叭、麥克風同時接線，反而讓每天切換更亂。固定主要設備，備援設備收在可拿位置即可。", "線材整理是聲音體驗的一部分。"),
            ("下單前的四種情境", "會議、專注、播放、備援。每一種只指定一個主設備，缺口自然會浮現。", "Elite Fashion 編輯團隊的判斷是：好的工作聲音配置，是讓你少一次重複測試麥克風，而不是堆滿音訊設備。"),
        ],
        "faq": [("會議一定要買獨立麥克風嗎？", "不一定。先測目前收音問題，再決定是否需要。"), ("耳機和喇叭可以都放桌面嗎？", "可以，但要分工並整理線材，不要讓切換更複雜。"), ("吸音板有必要嗎？", "看空間回音和噪音來源，不應只為外型購買。")],
    },
    "summer-office-ac-backup-light-jacket-hot-drink-earplug-lamp": {
        "heroAlt": "冷色辦公桌旁有薄外套、無字熱飲杯、耳塞盒、桌燈、空白筆記本與綠植",
        "audience": "夏天在辦公室常遇到冷氣溫差、噪音與桌面光線不穩的人",
        "excerpt": "夏季辦公室冷氣備案要處理溫差、噪音與光線，薄外套、熱飲、耳塞和桌燈各自有位置。",
        "tags": ["辦公室冷氣", "薄外套", "耳塞", "桌燈"],
        "intro": "夏天辦公室不一定是熱，更多時候是風口太冷、會議室太暗、公共區太吵。薄外套、熱飲、耳塞和桌面燈都可以成為備案，但它們不應被寫成健康答案，而是讓工作日更穩定的小系統。先看座位位置、冷氣風向、噪音來源和光線條件，再決定備品。",
        "editorialAngle": "先看座位風口，再安排冷氣備案。",
        "sections": [
            ("薄外套要看座位，不看季節", "同一間辦公室不同座位差很多。靠風口、靠窗或會議室使用頻率，都會影響外套厚薄與放置位置。", "材質與尺寸請以商品頁為準。"),
            ("熱飲是工作節奏，不是身體承諾", "熱茶、咖啡或沖泡飲可以是午後停頓，但不應被期待有特定健康效果。成分、咖啡因和保存方式要先確認。", "共享飲品也要看保存期限。"),
            ("耳塞適合處理短時噪音", "公共辦公室、午休或交通聲可以用耳塞做短時間備案，但配戴感與材質因人而異。", "不應把耳塞寫成保證安靜。"),
            ("桌面燈要補文件和臉部光線", "如果桌面太暗或視訊會議常逆光，小燈比更換整個座位更實際。要注意反光與用電位置。", "亮度、色溫與插座條件請確認。"),
            ("下班前的備品回收", "外套回椅背或抽屜、杯子清空、耳塞回盒、燈具關閉。備品能回位，隔天才不會變亂。", "Elite Fashion 編輯團隊的判斷是：冷氣備案的價值，是讓你不用每天重新忍耐同一件事。"),
        ],
        "faq": [("辦公室冷氣太冷先買什麼？", "先看座位風口與可放置位置，再決定薄外套、披肩或熱飲備案。"), ("耳塞能解決辦公室噪音嗎？", "只能作為短時備案，不保證隔音效果，材質與配戴感請自行確認。"), ("桌燈會不會影響同事？", "要看照射方向和亮度，建議選擇可調角度並避免直射他人。")],
    },
    "long-trip-recovery-kit-earplug-brace-luggage-tea-sun": {
        "heroAlt": "機場候機區長椅上有無標誌登機箱、耳塞盒、護具束帶、空白茶包、防曬外套與墨鏡",
        "audience": "需要為長途飛行、高鐵或跨城市移動準備舒適備品的人",
        "excerpt": "長途移動恢復包要先看睡眠干擾、身體支撐、行李拿取和日曬變化，再放入耳塞、護具、茶包與防曬。",
        "tags": ["長途旅行", "耳塞", "護具", "行李箱"],
        "intro": "長途移動不是把用品塞進行李箱就結束。真正影響體感的是耳朵是否能休息、身體支撐是否好拿、茶包或飲品是否符合限制、日曬或冷氣是否有備案。這些物品不該被包裝成健康或恢復保證，而是讓移動中少幾個可預見的不適與混亂。",
        "editorialAngle": "先看旅途中會被打斷的時刻。",
        "sections": [
            ("耳塞放在最容易拿的位置", "長途交通中噪音常來得突然，耳塞若放進大行李就失去意義。固定小盒比散放更重要。", "材質、尺寸與配戴感請以商品頁及自身狀況判斷。"),
            ("護具要看坐姿和拿取", "護膝、腰靠或支撐束帶若很難拿出來，就不會在旅途中使用。體積和收納位置要先想好。", "本文不宣稱醫療或恢復效果。"),
            ("行李箱要服務分層拿取", "長途移動最常拿的是證件、外套、耳塞、充電和水。這些不應被放到需要整箱打開的位置。", "箱體尺寸、輪子與登機限制請回商品頁與航空規範確認。"),
            ("茶包與防曬都是情境備案", "茶包、外套、防曬和雨具要看目的地天候與交通限制，不是每趟都帶同一套。", "食品成分、咖啡因與保存請以包裝為準。"),
            ("出發前的分層清單", "身上、隨身包、登機箱、托運。每一件備品都要知道在哪一層。", "Elite Fashion 編輯團隊的判斷是：長途移動包的價值，是讓下一次轉乘不用在行李裡翻找。"),
        ],
        "faq": [("長途移動一定要帶耳塞嗎？", "若容易受環境聲干擾，可列為小體積備案；配戴感需自行確認。"), ("護具可以改善旅途不適嗎？", "本文不作醫療或效果承諾，若有身體狀況應諮詢專業意見。"), ("茶包可以放隨身行李嗎？", "需看目的地與交通規定，食品類物品出境前要確認限制。")],
    },
    "elder-reading-care-corner-lamp-glasses-storage-care-supplies": {
        "heroAlt": "溫暖閱讀角落有檯燈、兩副眼鏡、空白封面書、收納盒、毛毯與無標籤照護備品籃",
        "audience": "想替家人整理閱讀光線、眼鏡拿取與日常照護備品的人",
        "excerpt": "閱讀與照護角落要先把光線、眼鏡、拿取高度與備品分層，讓家人不用每天翻找。",
        "tags": ["閱讀角落", "檯燈", "眼鏡收納", "照護備品"],
        "intro": "閱讀與照護角落的重點不是買很多用品，而是讓需要的人不用開口找東西。檯燈、眼鏡、放大鏡、收納盒、毛毯和照護備品如果分散在不同房間，家人每天都會重複尋找。把光線、視線、拿取高度和備品放在同一個角落，才是體貼真正落地的方式。",
        "editorialAngle": "先讓常用物伸手可及，再談添購。",
        "sections": [
            ("檯燈先看照射位置", "光要落在閱讀區，不是只照亮桌面。燈具高度、角度和開關位置要讓使用者容易操作。", "亮度、色溫與用電條件請以商品頁為準。"),
            ("眼鏡要有固定回家位置", "閱讀眼鏡、太陽眼鏡或備用眼鏡不應散在客廳、臥室和包包。固定托盤或盒位能減少翻找。", "度數與視力相關需求應依專業建議。"),
            ("收納高度比容量重要", "照護備品若放得太高或太深，即使容量很大也不好用。常用物應在坐姿可拿範圍內。", "用品標示和使用限制仍需保留。"),
            ("常見錯誤：把角落做得像醫療區", "家裡的閱讀角落應保留生活感。照護備品可以收在籃中，不必全部攤在視線裡。", "溫暖、尊重和好拿同樣重要。"),
            ("下單前的坐姿測試", "坐下、開燈、拿眼鏡、拿書、拿備品。五個動作都順，再決定是否需要新燈、收納或照護用品。", "Elite Fashion 編輯團隊的判斷是：好的照護角落不是把用品買齊，而是讓家人保持自己的節奏。"),
        ],
        "faq": [("閱讀角落先買檯燈嗎？", "若光線不足，檯燈是優先項；但也要一起看眼鏡和備品位置。"), ("照護用品可以全部放桌上嗎？", "不建議。常用物放近，其他備品分類收納，視線會更舒服。"), ("眼鏡要怎麼收才不容易找不到？", "固定托盤或盒位，並放在坐姿可拿的位置。")],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[70:75]:
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
        note = "2026-06-21 momo 收益型內容第十五組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第十五組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
