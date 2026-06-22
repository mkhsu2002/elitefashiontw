#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-sixteen-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B16"

base.COVER_SOURCES = {
    "family-bathroom-restock-towel-cleaning-oral-care-storage": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0b443cf65105518e016a3885845ee4819b93cc019e2a0043a0.png",
    "coffee-tea-gift-table-tableware-snack-scent-custom": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0b443cf65105518e016a3883d7b6c0819b8d8d250c651cf905.png",
    "weekend-home-reset-cleaning-laundry-bedding-restock-bag": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0b443cf65105518e016a3885f31420819baf65970bcee9b487.png",
    "desk-afternoon-ritual-coffee-cup-tea-snack-scent-lamp": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0b443cf65105518e016a388658c860819b8c84084ce7173525.png",
    "night-before-travel-luggage-rain-charging-sleep-brace-check": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0a93ec7fad90bf60016a38871105948199bec618d0d215ed56.png",
}

ROW_OVERRIDES = {
    "family-bathroom-restock-towel-cleaning-oral-care-storage": {
        "elite_judgment": "家庭浴室補貨先看使用人數、乾濕分區與回收路線，毛巾、清潔和口腔用品才不會互相佔位。",
        "answer_summary": "家庭浴室補貨要先看毛巾輪替、清潔用品、口腔用品與收納高度，再比較品牌與商品。",
        "risk_guardrail": "毛巾、清潔用品、口腔用品與收納品的尺寸、材質、成分、使用限制與保存方式請以商品頁及包裝為準。",
    },
    "coffee-tea-gift-table-tableware-snack-scent-custom": {
        "elite_judgment": "咖啡茶與伴手禮桌先看對方會不會使用，再決定杯盤、茶點、香氛與客製小物的份量。",
        "answer_summary": "咖啡茶與伴手禮桌要先看使用門檻、保存期限、杯盤數量、香氛偏好與客製需求，再比較選物。",
        "risk_guardrail": "咖啡、茶、點心、香氛、杯盤與客製小物的成分、香味、材質、保存、規格與交期請以商品頁及包裝為準。",
    },
    "weekend-home-reset-cleaning-laundry-bedding-restock-bag": {
        "elite_judgment": "週末家務重整先排清潔、洗衣、床寢、補貨與出門包的順序，不要把週末變成無止境採買。",
        "answer_summary": "週末家務重整要先看清潔動線、洗衣輪次、床寢替換、補貨清單與出門包，再比較用品。",
        "risk_guardrail": "清潔、洗衣、床寢、補貨與包款用品的尺寸、材質、成分、清洗與使用限制請以商品頁及包裝為準。",
    },
    "desk-afternoon-ritual-coffee-cup-tea-snack-scent-lamp": {
        "elite_judgment": "桌面下午茶儀式先控制份量、光線與收尾，不要讓咖啡杯、茶包、點心和香氛變成新的桌面雜物。",
        "answer_summary": "桌面下午茶儀式要先看杯具、茶咖啡保存、點心份量、香氛位置與閱讀燈，再比較選物。",
        "risk_guardrail": "咖啡、茶、點心、香氛、燈具與杯盤不作健康、保健、助眠或療效承諾；成分、咖啡因、香味、亮度與規格請以商品頁及包裝為準。",
    },
    "night-before-travel-luggage-rain-charging-sleep-brace-check": {
        "elite_judgment": "旅行前一晚先分明天早上要拿、路上會用、抵達後才用三層，行李箱、雨具、充電和睡眠備品才不會混亂。",
        "answer_summary": "旅行前一晚採買檢查要先看行李箱、雨具、充電、睡眠小物與護具位置，再比較旅行用品。",
        "risk_guardrail": "行李箱、雨具、充電用品、耳塞與護具不作安全、健康或恢復效果承諾；尺寸、材質、相容性、交通限制與使用方式請以商品頁及官方規範為準。",
    },
}

base.TOPIC_HUBS = {
    "family-bathroom-restock-towel-cleaning-oral-care-storage": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
    "coffee-tea-gift-table-tableware-snack-scent-custom": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
    "weekend-home-reset-cleaning-laundry-bedding-restock-bag": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}]},
    "desk-afternoon-ritual-coffee-cup-tea-snack-scent-lamp": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
    "night-before-travel-luggage-rain-charging-sleep-brace-check": {"topicCategory": "outdoor-gear", "topicCategoryLabel": "戶外裝備", "primaryHub": {"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
}

base.BLUEPRINTS = {
    "family-bathroom-restock-towel-cleaning-oral-care-storage": {
        "heroAlt": "明亮家庭浴室層架有毛巾、牙刷杯、棉花棒、收納籃、清潔布與綠植",
        "audience": "想整理家庭浴室補貨、乾濕分區與口腔用品位置的人",
        "excerpt": "家庭浴室補貨要先看使用人數、乾濕分區、毛巾輪替與口腔用品高度，再決定要補什麼。",
        "tags": ["浴室補貨", "毛巾", "口腔用品", "浴室收納"],
        "intro": "浴室補貨很容易一次買很多，卻仍然每天找不到乾毛巾、牙刷杯或清潔布。家庭浴室的問題不是物品不足，而是乾濕分區、拿取高度和回收路線沒有先定義。毛巾、清潔、口腔用品與收納應該各自有一層，不要全部堆在同一個櫃子裡。",
        "editorialAngle": "先分乾濕與拿取高度，再補貨。",
        "sections": [
            ("毛巾先看輪替，不看顏色", "每人使用量、洗衣頻率和晾乾時間，會決定毛巾數量。顏色整齊很好，但輪替順序更重要。", "若常常找不到乾毛巾，先補位置，不一定先補數量。"),
            ("口腔用品要依身高分層", "牙刷、杯子、牙線或漱口用品要放在使用者拿得到的位置。家庭共用區尤其要避免混放。", "成分與使用方式請以包裝為準。"),
            ("清潔布和清潔用品要獨立", "清潔布、刷具和補充品不應和毛巾混在一起。濕物要能晾乾，補充品要能看見餘量。", "清潔用品保存需依商品標示。"),
            ("常見錯誤：把所有備品塞進同一籃", "同一籃看似整齊，實際上會讓快用完的物品看不見。按用途分小籃更穩。", "高頻物在外層，囤貨退到後方。"),
            ("週末補貨前的三格檢查", "正在用、備用品、快用完。三格看完再下單。", "Elite Fashion 編輯團隊的判斷是：好的浴室補貨會讓早晨少一次翻找，而不是讓櫃子看起來更滿。"),
        ],
        "faq": [("浴室毛巾要準備幾條？", "先看人數、洗衣頻率和晾乾條件，再決定數量。"), ("口腔用品可以共用收納嗎？", "可以，但建議依使用者或用途分杯分格。"), ("清潔用品要放浴室嗎？", "常用可放近，但要避免和毛巾混放並依標示保存。")],
    },
    "coffee-tea-gift-table-tableware-snack-scent-custom": {
        "heroAlt": "花園窗邊餐桌上有咖啡杯、茶壺、點心、陶瓷香氛、空白禮物標籤與小布袋",
        "audience": "想準備咖啡茶、伴手禮桌與小型待客禮的人",
        "excerpt": "咖啡茶與伴手禮桌要先看對方會不會使用，再決定杯盤、茶點、香氛與客製小物。",
        "tags": ["咖啡茶", "伴手禮", "杯盤", "香氛小物"],
        "intro": "伴手禮最容易被包裝感帶著走。咖啡、茶、杯盤、點心、香氛和客製小物都可以很體面，但若對方沒有沖泡習慣、保存空間或香味偏好，再漂亮也可能變成負擔。好的禮桌不是堆滿，而是讓每一件物品都有使用情境。",
        "editorialAngle": "先看使用門檻，再看禮感。",
        "sections": [
            ("咖啡茶要看對方習慣", "有些人喝咖啡，有些人偏茶，也有人不常沖泡。先看使用門檻，再決定豆、濾掛、茶包或即飲形式。", "咖啡因、成分與保存請以包裝為準。"),
            ("杯盤數量不要壓過餐桌", "杯盤適合當禮物，但收納空間和使用頻率要一起看。單件質感比大套組更容易被用到。", "材質、尺寸和清潔方式請回商品頁確認。"),
            ("香氛要保守，不要替對方決定氣味", "香氛禮物需要更克制。若不確定偏好，選擇小容量或更中性的形式。", "不宣稱療癒、助眠或淨化效果。"),
            ("常見錯誤：客製小物只重形式", "客製要有實際用途，例如收納袋、杯墊或小托盤，而不只是寫名字。", "交期、材質和退換限制要先確認。"),
            ("送禮前的三句判斷", "對方會用嗎、放得下嗎、保存簡單嗎。三句通過，再談美感。", "Elite Fashion 編輯團隊的判斷是：有質感的禮，不是把品項堆滿，而是讓對方不用勉強收下。"),
        ],
        "faq": [("咖啡茶禮盒怎麼選？", "先看對方沖泡習慣、咖啡因接受度和保存空間。"), ("香氛適合送禮嗎？", "適合但要保守，避免太強烈或太私人化的味道。"), ("客製小物要注意什麼？", "看實用性、交期、材質和退換限制。")],
    },
    "weekend-home-reset-cleaning-laundry-bedding-restock-bag": {
        "heroAlt": "週末晨光中木桌上有床寢、洗衣籃、清潔布、補貨籃、外出包與牛仔外套",
        "audience": "想把週末家務、補貨與出門準備排成一個順序的人",
        "excerpt": "週末家務重整先排清潔、洗衣、床寢、補貨與出門包的順序，才不會把週末變成無止境採買。",
        "tags": ["週末家務", "清潔洗衣", "床寢補貨", "出門包"],
        "intro": "週末家務最怕沒有邊界：清潔做到一半想到洗衣，洗衣做到一半又補貨，最後出門包還沒整理。真正有效的週末重整，是先把清潔、洗衣、床寢、補貨和出門包排成順序，讓每一件事有開始也有收尾。",
        "editorialAngle": "先排順序，再補用品。",
        "sections": [
            ("清潔先處理會擋路的地方", "玄關、桌面和浴室若先清出空間，後面的洗衣與補貨才有地方暫放。", "清潔用品不必多，先讓工具好拿。"),
            ("洗衣和床寢要一起看", "床單、毛巾和外出衣物會競爭洗衣機與晾曬空間。週末先排輪次，避免全部堆到晚上。", "材質與清洗方式請依商品標示。"),
            ("補貨不要在疲勞時決定", "家務做到累時最容易亂買。先看庫存，再補清潔、毛巾、床寢或包內小物。", "不要把補貨清單當成犒賞清單。"),
            ("出門包是週末收尾", "把下週會用的包款、雨具、充電和小物放回固定位置，週一早上會輕很多。", "包款材質和尺寸請回商品頁確認。"),
            ("兩小時版本的重整法", "30 分鐘清潔、40 分鐘洗衣、20 分鐘床寢、20 分鐘補貨、10 分鐘出門包。", "Elite Fashion 編輯團隊的判斷是：週末重整的價值，不是把家變完美，而是讓下週少一個混亂開頭。"),
        ],
        "faq": [("週末家務先做清潔還是洗衣？", "若空間混亂，先清出桌面和地面，再排洗衣輪次。"), ("補貨要一次買齊嗎？", "不建議。先看快用完和真的缺的品項。"), ("出門包為什麼放在最後？", "因為它承接下週工作日，放在最後能避免週一早上翻找。")],
    },
    "desk-afternoon-ritual-coffee-cup-tea-snack-scent-lamp": {
        "heroAlt": "午後木質工作桌有咖啡杯、空白茶包、點心盤、香氛陶器、黃銅閱讀燈與空白筆記本",
        "audience": "想把桌面下午茶變成短暫休息而不是桌面雜物的人",
        "excerpt": "桌面下午茶儀式要控制杯具、茶包、點心、香氛和閱讀燈的份量與收尾。",
        "tags": ["下午茶", "桌面儀式", "咖啡杯", "閱讀燈"],
        "intro": "桌面下午茶可以是一天裡最小的暫停，也可能變成杯子、茶包、點心袋和香氛瓶的堆積。真正有質感的儀式不是買更多，而是決定什麼時候開始、放哪裡、何時收掉。杯具、茶咖啡、點心、香氛與閱讀燈各自有角色，不能全都留在桌面中央。",
        "editorialAngle": "先控制份量，再談儀式感。",
        "sections": [
            ("杯具只留一只高頻杯", "桌面最容易被杯子佔滿。工作桌建議只留一只高頻杯，其他杯盤回到餐櫃。", "材質和清潔方式請回商品頁確認。"),
            ("茶包和點心要有收尾", "茶包、點心和堅果若沒有固定小盒，會在桌上越堆越多。份量小比種類多更重要。", "成分、咖啡因和保存請以包裝為準。"),
            ("香氛不要壓過工作", "香氛適合放在桌角或窗邊，不適合和杯具、文件混在一起。氣味也不應太強。", "不宣稱健康、助眠或情緒效果。"),
            ("閱讀燈要服務紙本和休息", "若下午會讀紙本或手寫，閱讀燈可以固定角度；若只用螢幕，就先看反光。", "亮度、色溫與用電條件請確認。"),
            ("五分鐘收尾", "杯子進水槽、茶包丟棄、點心收盒、香氛歸位、燈關閉。儀式能收尾，才不會變成雜物。", "Elite Fashion 編輯團隊的判斷是：好的下午茶桌面，是讓你回到工作時更清楚，而不是更分心。"),
        ],
        "faq": [("桌面下午茶需要香氛嗎？", "不一定。先讓杯具和點心有位置，再考慮香氛。"), ("茶包和點心怎麼避免堆積？", "用小盒控制份量，並設定收尾時間。"), ("閱讀燈要放工作桌嗎？", "若常讀紙本或手寫可以；只用螢幕則先看反光。")],
    },
    "night-before-travel-luggage-rain-charging-sleep-brace-check": {
        "heroAlt": "旅行前一晚臥室長椅上有無標誌軟行李包、雨衣、折傘、行動電源、線材、耳塞盒與護具束帶",
        "audience": "出發前一晚想快速確認行李、雨具、充電、睡眠小物與護具的人",
        "excerpt": "旅行前一晚採買檢查要分明天早上要拿、路上會用、抵達後才用三層。",
        "tags": ["旅行前檢查", "行李箱", "雨具", "充電備品"],
        "intro": "旅行前一晚不適合重新規劃整趟行程，只適合做最後分層：明天早上會拿、路上會用、抵達後才用。行李箱、雨具、充電、耳塞、護具和睡眠小物如果全部混在一起，隔天最容易在玄關或車站翻找。好的檢查清單，是讓物品回到正確層級。",
        "editorialAngle": "先分三層，再補最後缺口。",
        "sections": [
            ("明天早上要拿的放最外層", "雨具、外套、手機、充電線和證件類物品不要放進深層。若一早會下雨，雨具應比衣服更靠近出口。", "實際交通與安檢限制仍要確認。"),
            ("路上會用的放隨身包", "耳塞、充電、支撐小物、水杯和薄外套，應該在座位上拿得到。", "耳塞與護具不作效果承諾，材質與配戴感請自行判斷。"),
            ("抵達後才用的退到行李內層", "換洗衣物、備用鞋、較大型清潔用品和非立即用品，可以放進行李深層，避免干擾轉乘。", "行李箱尺寸與重量限制請看交通規範。"),
            ("常見錯誤：出發前又開始採買", "前一晚只補真正缺口，不應重開整張購物清單。若缺的是雨具或充電，可以補；若只是想升級外型，留到下次。", "時間越晚，決策越要保守。"),
            ("睡前最後五件", "行李關好、雨具在外、電力充滿、耳塞就位、護具可拿。完成就停止整理。", "Elite Fashion 編輯團隊的判斷是：旅行前一晚的好清單，是讓你能準時睡，而不是把所有不安都拿去購物。"),
        ],
        "faq": [("旅行前一晚還需要採買嗎？", "只補真正缺口，例如雨具、充電線或必要小物，不建議重新擴大清單。"), ("耳塞和護具要放哪裡？", "若路上會用，放隨身包；抵達後才用則放行李內層。"), ("雨具要放行李箱嗎？", "若出發當天可能下雨，應放在最外層或玄關可拿處。")],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[75:80]:
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
        note = "2026-06-21 momo 收益型內容第十六組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第十六組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
