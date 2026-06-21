#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-twelve-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B12"

base.COVER_SOURCES = {
    "office-snack-cabinet-nuts-dessert-tea-coffee-layers": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37d2417f0881938bbb2202ff61a2a5.png",
    "family-weekend-table-frozen-food-cookware-tableware-tea": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37d29e4d6881939d9925f56812a4ad.png",
    "breakfast-freezer-buns-sweet-potato-chicken-drinks": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37d3027f94819395795efc9b343b95.png",
    "solo-living-tableware-cookware-coffee-tea-cleaning-storage": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37d364a6c88193a28780026dd9a7d1.png",
    "entryway-shoe-cabinet-umbrella-bag-cleaning-tools": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37d3d247308193961221b46d097726.png",
}

ROW_OVERRIDES = {
    "office-snack-cabinet-nuts-dessert-tea-coffee-layers": {
        "elite_judgment": "辦公室點心櫃先分共享、個人、來客與加班四層，不把點心櫃變成過期品暫存區。",
        "answer_summary": "辦公室點心櫃要先看保存、份量、咖啡因與共享便利性，再分堅果、甜點、茶飲與咖啡。",
        "risk_guardrail": "堅果、甜點、茶、咖啡與植物奶不作身體狀態或飲食結果承諾；成分、咖啡因、過敏原、保存與規格請以商品頁及包裝為準。",
    },
    "family-weekend-table-frozen-food-cookware-tableware-tea": {
        "elite_judgment": "家庭餐桌週末補貨先看誰下廚、誰收拾、冰箱還有多少空間，不只看餐桌照片。",
        "answer_summary": "家庭餐桌週末補貨要先看冷凍保存、鍋具容量、餐具數量與茶點時段，再比較品牌。",
        "risk_guardrail": "冷凍食品、鍋具、餐具與茶點不作身體狀態或料理結果承諾；成分、保存、加熱、材質與規格請以商品頁及包裝為準。",
    },
    "breakfast-freezer-buns-sweet-potato-chicken-drinks": {
        "elite_judgment": "早餐冷凍補貨先看平日時間、冷凍空間與實際吃完速度，不把補貨寫成飲食管理答案。",
        "answer_summary": "早餐與冷凍麵食補貨要先看冷凍容量、加熱方式、份量與飲品保存，再比較饅頭、地瓜、雞胸與沖泡飲。",
        "risk_guardrail": "早餐、冷凍食品、沖泡飲與低碳食品不作身體狀態或飲食結果承諾；成分、保存、加熱、咖啡因與限制請以商品頁及包裝為準。",
    },
    "solo-living-tableware-cookware-coffee-tea-cleaning-storage": {
        "elite_judgment": "一人生活餐具先看一週使用頻率與清洗動線，少而準比成套更重要。",
        "answer_summary": "一人生活餐具清單要先看杯盤數量、鍋具尺寸、咖啡茶習慣與清潔收納，再比較品牌。",
        "risk_guardrail": "餐具、鍋具、茶咖啡與清潔用品的材質、尺寸、保存、清潔與使用限制請以商品頁及包裝為準。",
    },
    "entryway-shoe-cabinet-umbrella-bag-cleaning-tools": {
        "elite_judgment": "玄關先分出門、回家、濕物與清潔四件事，不要讓鞋櫃、傘架、包款和工具互相搶位置。",
        "answer_summary": "玄關分工要先看鞋櫃容量、傘具濕物、外出包暫放與清潔工具位置，再比較家具與收納品。",
        "risk_guardrail": "鞋櫃、傘架、家具、包款與清潔工具的尺寸、材質、承重、保養與使用限制請以商品頁及包裝為準。",
    },
}

base.TOPIC_HUBS = {
    "office-snack-cabinet-nuts-dessert-tea-coffee-layers": {"topicCategory": "food-nutrition", "topicCategoryLabel": "飲食與補給", "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}, "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}]},
    "family-weekend-table-frozen-food-cookware-tableware-tea": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
    "breakfast-freezer-buns-sweet-potato-chicken-drinks": {"topicCategory": "food-nutrition", "topicCategoryLabel": "飲食與補給", "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}, "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}]},
    "solo-living-tableware-cookware-coffee-tea-cleaning-storage": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
    "entryway-shoe-cabinet-umbrella-bag-cleaning-tools": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}]},
}

base.BLUEPRINTS = {
    "office-snack-cabinet-nuts-dessert-tea-coffee-layers": {
        "heroAlt": "明亮辦公室點心櫃有透明堅果罐、甜點盤、無字茶罐、咖啡豆、空白植物奶紙盒與收納籃",
        "audience": "想整理辦公室共享點心櫃、茶水間與下午補給的人",
        "excerpt": "辦公室點心櫃要先看保存、份量、咖啡因與共享便利性，再分堅果、甜點、茶飲與咖啡。",
        "tags": ["辦公室點心", "堅果甜點", "茶飲咖啡", "茶水間收納"],
        "intro": "辦公室點心櫃真正難的不是買什麼，而是誰會吃、多久吃完、開封後放哪裡。堅果、甜點、茶、咖啡和植物奶都有不同保存條件；如果只用口味補貨，很快會出現重複、過期和沒人願意開封的品項。尤其台灣辦公室常有冰箱空間小、午後會議多、共享區人流不固定的情況，分層比買齊更重要。",
        "editorialAngle": "先分共享與保存，再看口味。",
        "sections": [
            ("先分共享、個人、來客與加班", "共享品要份量清楚，個人品要有標準位置，來客品要好拿，加班品要保存簡單。", "囍素堅果、食材玩家與 Teavoya 可放在堅果、甜點和茶飲情境中比較。"),
            ("咖啡和植物奶要看開封後安排", "咖啡豆、濾掛或植物奶若沒有保存位置，會讓茶水間變得混亂。", "Xinto Coffee、馬克老爹與 KKM 可作為咖啡和飲品補充。"),
            ("甜點不要壓過日常補給", "甜點適合來客或週五，而不是每天佔滿最容易拿的位置。", "成分、咖啡因、過敏原與保存方式請以商品頁及包裝為準。"),
            ("常見錯誤：快到期品項看不見", "透明罐、低前高後和開封日比漂亮盒子更重要。", "Elite Fashion 編輯團隊的判斷是：好的點心櫃會提醒你少買，而不是一直加購。"),
            ("補貨前的三格清點", "未開封、已開封、快到期。三格看完再補貨；若快到期品項已經超過一層，就先暫停甜點和飲品新品，只補真正會被消耗的堅果、咖啡或茶。", "價格、規格、活動、庫存與配送請以下單前商品頁公告為準。點心櫃的成熟度不在品項多，而在每一格都知道誰會拿、多久會完食、開封後放哪裡。"),
        ],
        "faq": [("辦公室點心櫃先買哪類？", "先補保存簡單、共享門檻低的品項。"), ("咖啡和茶要分開放嗎？", "建議分開，因為保存和使用時刻不同。"), ("怎麼避免買太多？", "固定清點未開封、已開封和快到期三格。")],
    },
    "family-weekend-table-frozen-food-cookware-tableware-tea": {
        "heroAlt": "週末家庭廚房島台有無品牌鍋具、餐具、冷凍食材盒、地瓜蔬菜、茶壺與茶點",
        "audience": "想替週末家庭餐桌補貨但不想堆滿冰箱的人",
        "excerpt": "家庭餐桌週末補貨要先看冷凍保存、鍋具容量、餐具數量與茶點時段，再比較品牌。",
        "tags": ["家庭餐桌", "冷凍食品", "鍋具餐具", "茶點補貨"],
        "intro": "週末餐桌看起來像放鬆，其實最考驗冰箱、鍋具和收拾動線。冷凍食品、鍋具、餐具、茶點如果沒有先分主餐、配菜、收尾與來客，很容易買得很豐盛，做起來很疲憊。好的補貨清單應該讓週六午餐、週日晚餐和臨時來客都能各自成立，而不是把所有責任丟給一只鍋。",
        "editorialAngle": "先看誰下廚和誰收拾，再補貨。",
        "sections": [
            ("先看冰箱和冷凍容量", "冷凍食品再方便，也要看保存空間、加熱方式和吃完速度。", "田食原可放在冷凍食材情境中比較。"),
            ("鍋具和餐具要看人數", "鍋具容量、爐台尺寸、餐具數量與洗碗空間要一起看。", "廚藝日本鍋具館、Home & Ceramics 與大正餐具可放在鍋具餐具情境中比較。"),
            ("茶點是收尾，不是主餐壓力", "茶、米餅或伴手禮要看時段和份量。", "暮朝食粹與 Teavoya 可作為茶點補充。"),
            ("常見錯誤：只買主角食材", "沒有配菜、餐具和收洗動線，週末餐桌很快變成家務。", "Elite Fashion 編輯團隊的判斷是：好的週末補貨會讓餐後也輕鬆。"),
            ("下單前排一餐流程", "取出、加熱、擺盤、用餐、收洗、保存剩餘。流程跑得通再補。", "價格、成分、保存、加熱方式與庫存請以商品頁及包裝為準。"),
        ],
        "faq": [("週末餐桌先補冷凍食品嗎？", "先看冷凍容量和加熱方式，再補主餐或配菜。"), ("鍋具要怎麼選？", "看人數、爐台、收納和清洗方式。"), ("茶點需要買很多嗎？", "不需要。看來客與午後時段即可。")],
    },
    "breakfast-freezer-buns-sweet-potato-chicken-drinks": {
        "heroAlt": "晨光廚房有蒸籠饅頭、地瓜、雞胸蔬菜餐盒、空白沖泡飲罐、冷凍抽屜與早餐杯碗",
        "audience": "想用冷凍補貨讓平日早餐更穩定的人",
        "excerpt": "早餐與冷凍麵食補貨要先看冷凍容量、加熱方式、份量與飲品保存，再比較饅頭、地瓜、雞胸與沖泡飲。",
        "tags": ["早餐補貨", "冷凍麵食", "地瓜雞胸", "沖泡飲"],
        "intro": "早餐補貨最怕的是以為冰箱會自動解決一切。饅頭、地瓜、雞胸、冷凍蔬菜和沖泡飲都能節省早晨判斷，但前提是冷凍容量、加熱方式、份量和保存期限都先排好。若家裡早上只有十分鐘，商品選擇就要服務速度、清潔與帶出門，而不是服務想像中的完美早餐。",
        "editorialAngle": "先看早晨時間，再看冷凍品項。",
        "sections": [
            ("先估平日可用時間", "五分鐘、十分鐘和十五分鐘需要的早餐完全不同。", "花漾饅頭屋與田食原可放在冷凍麵食和食材情境中比較。"),
            ("飲品要看保存和咖啡因", "沖泡飲、植物奶或低碳食品都要回到成分、保存與飲用時段。", "本草養生、KKM、GUMi低碳與 D醣一刻可作為飲品補充。"),
            ("冷凍抽屜要分格", "主食、蛋白質、蔬菜、備用飲品分格，早上才不會翻找。", "成分、保存、加熱方式和限制請以商品頁及包裝為準。"),
            ("常見錯誤：買得像一個月計畫", "如果兩週吃不完，就先縮小補貨量。", "Elite Fashion 編輯團隊的判斷是：早餐補貨要服務下一週，不是展示意志力。"),
            ("下單前做七天表", "把七個早晨排出主食、飲品和備案，再決定補貨量。", "價格、規格、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [("早餐冷凍補貨先買什麼？", "先看早晨時間和冷凍容量，再決定主食與飲品。"), ("沖泡飲怎麼放？", "看保存方式、咖啡因和使用頻率。"), ("怎麼避免補太多？", "用七天表決定，不要用一個月想像決定。")],
    },
    "solo-living-tableware-cookware-coffee-tea-cleaning-storage": {
        "heroAlt": "小宅餐桌上有兩只杯盤、小鍋平底鍋、咖啡濾杯、茶壺、清潔刷、擦拭布與收納籃",
        "audience": "想替一人生活建立剛好的杯盤鍋具與清潔收納的人",
        "excerpt": "一人生活餐具清單要先看杯盤數量、鍋具尺寸、咖啡茶習慣與清潔收納，再比較品牌。",
        "tags": ["一人生活", "餐具清單", "咖啡茶", "清潔收納"],
        "intro": "一人生活的餐具不需要像展間。真正舒服的是拿得到、洗得完、收得下。杯盤、鍋具、咖啡、茶與清潔工具要按一週使用頻率決定，而不是一次買完整套。小宅尤其需要把清潔和收納放進購物順序，否則漂亮杯盤很快會變成水槽壓力。若平日多外食、週末才下廚，購物清單就應偏向少量高頻；若每天沖咖啡或泡茶，杯具與清洗工具就比來客餐盤更優先。",
        "editorialAngle": "少而準，比成套更有質感。",
        "sections": [
            ("杯盤數量先看一週頻率", "每天用的留在外層，來客備品收進高處。", "Home & Ceramics 可放在杯盤情境中比較。"),
            ("鍋具要看爐台和洗槽", "小鍋、平底鍋和鍋蓋若洗不順，就不會常用。", "廚藝日本鍋具館可作為鍋具參考。"),
            ("咖啡茶不要佔滿櫃子", "茶、咖啡和濾具要看日常時段，不必把所有風味帶回家。", "Teavoya 與馬克老爹可作為茶咖啡補充。"),
            ("常見錯誤：清潔工具最後才買", "清潔刷、擦拭布和收納籃決定一人廚房能不能維持。", "真蓁嚴選與 Desire & Passion 可放在清潔用品情境中比較。"),
            ("下單前做一週洗碗表", "看一週會用幾個杯、幾個盤、幾次鍋。答案會比套組照片誠實；如果一週只煮兩次，就先買真正會用的小鍋和兩組杯盤，不必被完整餐具組牽著走。", "價格、材質、尺寸、活動與庫存請以下單前商品頁公告為準。Elite Fashion 編輯團隊的判斷是：一人生活最有質感的清單，是讓水槽不堆積、櫃子不爆滿、每天仍願意替自己擺一只好用的杯。"),
        ],
        "faq": [("一人生活餐具要買幾人份？", "先看一週使用頻率和來客頻率，不必先買大套組。"), ("小鍋和平底鍋都需要嗎？", "看爐台、洗槽和料理習慣。"), ("清潔用品要一起規劃嗎？", "需要，否則餐具越買越難維持。")],
    },
    "entryway-shoe-cabinet-umbrella-bag-cleaning-tools": {
        "heroAlt": "現代玄關有鞋櫃、傘架、無品牌外出包、清潔工具收納架、掛鉤、鏡子與植栽",
        "audience": "想讓玄關從暫放區變成出入門系統的人",
        "excerpt": "玄關分工要先看鞋櫃容量、傘具濕物、外出包暫放與清潔工具位置，再比較家具與收納品。",
        "tags": ["玄關收納", "鞋櫃傘架", "外出包", "清潔工具"],
        "intro": "玄關最容易從過渡空間變成倉庫。鞋櫃、傘架、外出包、清潔工具和家具若沒有分工，每天出門與回家都會被同一堆東西攔住。玄關要先處理四件事：出門、回家、濕物、清潔。台灣雨季和通勤節奏讓玄關很容易累積傘、鞋、包與地面灰塵，所以分工比容量更重要。真正好用的玄關，不是把所有東西藏起來，而是讓今天會用的物件留在手邊，其他物件退到櫃內或下一層。",
        "editorialAngle": "玄關不是倉庫，而是出入門系統。",
        "sections": [
            ("鞋櫃先看容量和換鞋動線", "鞋櫃不是只收鞋，也要讓出門前能順手換鞋。", "完美主義、悅家傢具城與 RED HOUSE 可放在家具收納裡比較。"),
            ("傘架要處理濕物", "傘具若沒有滴水和晾乾位置，玄關很快會潮濕混亂。", "FULTON 可作為晴雨傘備案參考。"),
            ("包款只放今日外出", "S′AIME 可作為外出包參考，但玄關不該堆放所有包。", "包款尺寸、材質與收納方式請以商品頁為準。"),
            ("常見錯誤：清潔工具沒有家", "掃把、拖把、擦拭布若放在視線外，回家後的小髒污就會被拖延。", "真蓁嚴選可作為清潔工具參考。"),
            ("下單前畫四區", "鞋、傘、包、清潔。每區只能放最常用的物件；如果同一區超過三種用途，就代表需要分層、移位或減少品項。", "價格、尺寸、材質、承重與庫存請以下單前商品頁公告為準。Elite Fashion 編輯團隊的判斷是：玄關的轉單價值在於讓讀者看見缺的是鞋櫃、傘架、包款暫放還是清潔工具，而不是一次買滿家具。"),
        ],
        "faq": [("玄關第一步整理什麼？", "先分鞋、傘、包、清潔四區。"), ("鞋櫃越大越好嗎？", "不一定，要看換鞋動線和常穿鞋數量。"), ("清潔工具可以藏起來嗎？", "可以，但要拿得到，否則很難維持。")],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[55:60]:
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
        note = "2026-06-21 momo 收益型內容第十二組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第十二組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
