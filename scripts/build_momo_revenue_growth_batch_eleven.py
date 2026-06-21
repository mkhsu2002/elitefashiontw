#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-eleven-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B11"

base.COVER_SOURCES = {
    "night-mobility-reflective-dashcam-rain-earplug-kit": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37ca0b0d8c8193a0f3178d5dd9d1f0.png",
    "family-weekend-outing-sun-tableware-toys-rain-storage": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37ca6bf8a48193b36138a0bf8c5a04.png",
    "first-pet-shopping-food-toy-cleaning-outing-order-2": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37cad4f54881939a44d55fdcd2e5ed.png",
    "aquarium-reptile-small-pet-food-cleaning-habitat-storage": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37cb27aaa48193a76a8c99108d4152.png",
    "pet-birthday-gift-cake-snack-toy-cleaning": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37cb86e29c8193914cf0070bf16b36.png",
}

ROW_OVERRIDES = {
    "night-mobility-reflective-dashcam-rain-earplug-kit": {
        "elite_judgment": "夜間移動清單先分路上、車上、雨天與住宿四段，不把配件寫成安全或睡眠答案。",
        "answer_summary": "夜間移動清單要先看路線、天氣、記錄、可見度、電力與住宿環境，再比較配件。",
        "risk_guardrail": "反光配件、行車紀錄、雨具、耳塞、護具與充電用品不作行車、身體休息或使用結果承諾；規格、安裝、材質與限制請以商品頁及官方規定為準。",
    },
    "family-weekend-outing-sun-tableware-toys-rain-storage": {
        "elite_judgment": "親子週末清單先按出門、用餐、玩耍、雨天與回家後收納排序，不把所有小物塞進同一袋。",
        "answer_summary": "親子週末出門要先看日曬、用餐、玩具、雨具與乾濕收納，再補防曬服飾、餐具與小包。",
        "risk_guardrail": "防曬、嬰幼餐具、玩具、雨具與包款不作安全或能力承諾；材質、年齡限制、警語與規格請以商品頁及包裝為準。",
    },
    "first-pet-shopping-food-toy-cleaning-outing-order-2": {
        "elite_judgment": "第一次養寵物先處理食品、飲水、清潔與外出，再讓玩具成為日常變化。",
        "answer_summary": "第一次養寵物購物要先看食品保存、清潔動線、玩具輪替與外出用品，再比較品牌。",
        "risk_guardrail": "寵物食品、特殊補給品、玩具、清潔與外出用品不作身體狀態或使用結果承諾；成分、適用限制與獸醫建議請以商品頁、包裝與專業意見為準。",
    },
    "aquarium-reptile-small-pet-food-cleaning-habitat-storage": {
        "elite_judgment": "水族與小寵補貨先看飼料保存、棲地穩定、清潔工具與耗材收納，不把補貨變成堆貨。",
        "answer_summary": "水族與小寵補貨要先分飼料、清潔、棲地與收納，再比較水族、寵物與清潔用品。",
        "risk_guardrail": "水族、小寵、飼料、清潔與棲地用品不作身體狀態或環境結果承諾；成分、材質、使用限制與專業建議請以商品頁及包裝為準。",
    },
    "pet-birthday-gift-cake-snack-toy-cleaning": {
        "elite_judgment": "寵物生日禮物先看食品限制、份量、玩具材質與清潔備案，儀式感不能蓋過日常秩序。",
        "answer_summary": "寵物生日禮物要先看蛋糕、零食、玩具與清潔備案，再比較造型和品牌。",
        "risk_guardrail": "寵物蛋糕、零食、食品、玩具與清潔品不作身體狀態、營養或使用結果承諾；成分、保存、份量與適用限制請以商品頁、包裝與獸醫建議為準。",
    },
}

base.TOPIC_HUBS = {
    "night-mobility-reflective-dashcam-rain-earplug-kit": {
        "topicCategory": "outdoor-gear",
        "topicCategoryLabel": "戶外裝備",
        "primaryHub": {"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
    "family-weekend-outing-sun-tableware-toys-rain-storage": {
        "topicCategory": "outdoor-gear",
        "topicCategoryLabel": "戶外裝備",
        "primaryHub": {"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "first-pet-shopping-food-toy-cleaning-outing-order-2": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
    "aquarium-reptile-small-pet-food-cleaning-habitat-storage": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
    "pet-birthday-gift-cake-snack-toy-cleaning": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
}

base.BLUEPRINTS = {
    "night-mobility-reflective-dashcam-rain-earplug-kit": {
        "heroAlt": "夜間玄關車庫桌面上有無品牌反光配件、行車紀錄器、雨衣、耳塞盒、充電線與行動電源",
        "audience": "需要整理夜間通勤、自駕、機車與住宿備案的人",
        "excerpt": "夜間移動清單要先看路線、天氣、記錄、可見度、電力與住宿環境，再比較配件。",
        "tags": ["夜間移動", "反光配件", "行車紀錄", "雨具耳塞"],
        "intro": "夜間移動的清單，不是讓人把所有配件都帶上，而是把路上、車上、雨天與住宿四段分清楚。反光配件、行車紀錄、雨具、耳塞、護具和充電用品各有位置，但都不應被寫成安全或睡眠答案。真正值得下單的，是在需要時拿得到、用得上、收得回的備案。",
        "editorialAngle": "把移動拆成四段，配件才有清楚位置。",
        "sections": [
            ("路上先看可見度與雨天備案", "夜間步行、騎車或停車場移動，最先要看路線和天氣。反光配件與雨具要放在容易拿的位置，不要埋進包底。", "反光屋 FKW、OMBRA 與 Momax Taiwan 可放在反光、雨具和電力備案裡比較。"),
            ("車上用品要看安裝與法規", "行車紀錄器、車用充電和固定配件都要看安裝、線路、視角和規定。", "安鈦科技行車記錄器可作為行車紀錄參考；安裝與使用限制請回商品頁和官方規定確認。"),
            ("住宿或長途移動用品只談環境", "耳塞、護具或休息小物可放進備案袋，但不寫成身體承諾。", "耳根清靜與 BELEX 可作為用品比較入口；材質、尺寸與使用限制請以商品頁為準。"),
            ("常見錯誤：把備案當答案", "配件是降低慌亂，不是取代路況判斷、交通規定或身體狀態評估。", "Elite Fashion 編輯團隊的判斷是：夜間移動的成熟感，在於備品少而準。"),
            ("出門前四點確認", "路線、天氣、電力、濕物袋。四點清楚後，再看反光、紀錄、耳塞和雨具。", "價格、規格、活動、庫存、材質與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("夜間移動用品第一步買什麼？", "先看路線和天氣，再補反光、雨具或電力備案。"),
            ("耳塞可以寫成睡眠建議嗎？", "不可以。本文只談住宿或移動環境的小物安排。"),
            ("行車紀錄器要注意什麼？", "安裝位置、電源、視角和法規限制都要確認。"),
        ],
    },
    "family-weekend-outing-sun-tableware-toys-rain-storage": {
        "heroAlt": "陽光公園野餐桌上有無品牌防曬外套、嬰幼餐具、木質玩具、折傘、小包與乾濕收納袋",
        "audience": "想把親子週末外出用品整理成固定包內順序的人",
        "excerpt": "親子週末出門要先看日曬、用餐、玩具、雨具與乾濕收納，再補防曬服飾、餐具與小包。",
        "tags": ["親子外出", "防曬餐具", "玩具雨具", "收納袋"],
        "intro": "親子週末出門最怕的是每樣都帶了，真正要用時卻翻不到。防曬外套、餐具、玩具、雨具、小包和乾濕袋應按使用時刻排序：出門前、用餐時、玩耍時、下雨時、回家後。順序清楚，包才不會越帶越重。",
        "editorialAngle": "按使用時刻排包，比品項數量更重要。",
        "sections": [
            ("出門前先看日曬和雨天", "戶外活動要先看遮蔽、路線和回程天氣。防曬服飾與傘具應放在包內外層。", "UV100 與 FULTON 可作為防曬與晴雨傘備案參考；規格請以商品頁為準。"),
            ("用餐用品要好拿也好收", "餐具、濕物袋和替換袋要靠近包口。餐後清潔比餐前準備更容易被忽略。", "2angels 可放在嬰幼餐具情境中比較；材質和年齡限制請以包裝為準。"),
            ("玩具少量輪替即可", "888便利購、SUSS Living 與 S′AIME 可放在玩具、生活小物和包款裡比較。外出玩具不必多，重點是能收回。", "玩具年齡限制、警語與材質請以商品頁為準。"),
            ("常見錯誤：乾濕混放", "雨具、餐具和濕紙巾若和衣物、文件混放，回家後會很累。乾濕分層是親子包的核心。", "Elite Fashion 編輯團隊的判斷是：親子週末清單要讓回家後也能快速復原。"),
            ("下單前做包內分層", "日曬、用餐、玩具、雨具、濕物五層先排好，再看缺哪一格。", "價格、規格、活動、庫存、材質與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("親子週末包要放幾種玩具？", "少量輪替即可，重點是能收回且符合年齡限制。"),
            ("餐具要怎麼收？", "用餐用品和餐後濕物要分袋，避免和衣物混放。"),
            ("防曬和雨具可以放同一層嗎？", "可放在外層，但濕物使用後要另外收。"),
        ],
    },
    "first-pet-shopping-food-toy-cleaning-outing-order-2": {
        "heroAlt": "溫暖居家角落有空白寵物食品袋、陶瓷碗、玩具、牽繩、外出包、清潔瓶、收納籃與安靜貓狗",
        "audience": "第一次養寵物，需要建立食品、玩具、清潔與外出購物順序的人",
        "excerpt": "第一次養寵物購物要先看食品保存、清潔動線、玩具輪替與外出用品，再比較品牌。",
        "tags": ["第一次養寵物", "寵物食品", "清潔玩具", "外出用品"],
        "intro": "第一次養寵物很容易先被玩具和可愛用品吸引，但真正讓日常穩定的是食品保存、飲水、清潔、外出和收納。玩具可以慢慢補，基礎動線要先成立。食品、玩具、清潔和外出用品都要回到成分、適用限制與專業建議。",
        "editorialAngle": "先建立日常照顧動線，再補儀式感用品。",
        "sections": [
            ("食品和飲水先固定位置", "食品、碗、飲水和保存容器要先有位置，補貨才不會散落。", "HeroMama、Tails Life 與寵物王國可放在食品和用品情境中比較。"),
            ("清潔用品比玩具更早進清單", "地板、碗具、外出包和掉毛清潔都需要固定工具。", "淨淨 Clean Clean 與尾巴丘毛孩選物可作為清潔和生活用品補充。"),
            ("特殊用品要更保守", "petit 沛蒂等品牌若涉及特殊需求，應回到包裝、成分和專業建議。", "本文只討論採買順序與使用限制。"),
            ("常見錯誤：玩具一次買太多", "玩具要輪替，不要堆滿。太多玩具會讓清潔和收納變難。", "Elite Fashion 編輯團隊的判斷是：新手採買成熟度，來自能每天重複執行。"),
            ("下單前分四格", "食品、清潔、玩具、外出。四格先滿足基本需求，再看造型。", "價格、成分、規格、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("第一次養寵物先買玩具嗎？", "不建議。先處理食品、飲水、清潔和外出，再補玩具。"),
            ("寵物食品怎麼判斷？", "看成分、保存、份量和適用限制，必要時詢問專業意見。"),
            ("清潔用品要買哪些？", "先看地板、碗具、外出包和毛髮清潔，再補細項。"),
        ],
    },
    "aquarium-reptile-small-pet-food-cleaning-habitat-storage": {
        "heroAlt": "明亮居家水族櫃旁有水草魚缸、小型棲地、空白飼料罐、清潔刷、虹吸管、收納盒與擦拭布",
        "audience": "需要替水族、小寵、棲地與清潔耗材建立補貨順序的人",
        "excerpt": "水族與小寵補貨要先分飼料、清潔、棲地與收納，再比較水族、寵物與清潔用品。",
        "tags": ["水族補貨", "小寵用品", "棲地清潔", "收納耗材"],
        "intro": "水族與小寵補貨最怕的是看到缺什麼就買什麼，結果飼料、清潔工具、棲地材料和收納耗材都散在不同地方。水族和小寵的日常，需要穩定而保守的清單：先看飼料保存，再看清潔工具，最後才補裝飾與備品。",
        "editorialAngle": "補貨是維持日常，不是把櫃子填滿。",
        "sections": [
            ("飼料先看保存和份量", "飼料或補給品要看保存期限、容器密封和使用頻率，不要一次買到看不見底。", "Aqua Corner、寵物王國與尾巴丘毛孩選物可放在水族與小寵用品中比較。"),
            ("清潔工具要放在同一區", "刷具、虹吸管、擦拭布和清潔用品最好固定收在棲地旁，不要每次清理都找工具。", "淨淨 Clean Clean、JINKO 淨科與真蓁嚴選可作為清潔用品參考。"),
            ("棲地用品要看限制", "水族、小寵或爬蟲棲地用品都有材質和使用限制，不能只看照片漂亮。", "成分、材質、適用物種與使用限制請以商品頁、包裝和專業建議為準。"),
            ("常見錯誤：補貨沒有日期", "沒有開封日和補貨量，飼料與耗材很容易重複。", "Elite Fashion 編輯團隊的判斷是：水族與小寵清單越安靜，日常越穩。"),
            ("下單前盤點四格", "飼料、清潔、棲地、收納。每格只補真正缺口。", "價格、規格、活動、庫存、成分與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("水族與小寵補貨先補什麼？", "先看飼料保存和清潔工具，再看棲地與收納。"),
            ("清潔品可以混用嗎？", "不要用想像判斷，應看材質、使用限制和商品說明。"),
            ("怎麼避免補貨過量？", "記錄開封日、使用頻率和下一次補貨時間。"),
        ],
    },
    "pet-birthday-gift-cake-snack-toy-cleaning": {
        "heroAlt": "明亮居家慶祝角落有無字寵物蛋糕、空白零食罐、玩具、清潔布、無標籤清潔瓶、收納籃與安靜貓狗",
        "audience": "想替寵物生日準備蛋糕、零食、玩具與清潔備案的人",
        "excerpt": "寵物生日禮物要先看蛋糕、零食、玩具與清潔備案，再比較造型和品牌。",
        "tags": ["寵物生日", "寵物蛋糕", "零食玩具", "清潔備案"],
        "intro": "寵物生日可以有儀式感，但不應讓儀式感蓋過日常限制。蛋糕、零食、玩具和清潔備案都要先看成分、份量、保存、材質和收拾方式。對寵物來說，生日不是把所有好看的東西放上桌，而是讓人和寵物都能輕鬆收尾。",
        "editorialAngle": "先看份量與收拾，再談生日畫面。",
        "sections": [
            ("蛋糕和零食先看成分與份量", "寵物蛋糕和零食要看成分、保存、份量與適用限制，不要只看照片可愛。", "NiNiJA 妮妮家、Tails Life 與 HeroMama 可放在蛋糕、零食與食品情境中比較。"),
            ("玩具要看材質與收納", "玩具適合當生日變化，但要看尺寸、材質和是否容易清潔。", "寵物王國與尾巴丘毛孩選物可作為玩具和用品補充。"),
            ("清潔備案不能省略", "生日當天會有食物、毛髮、包裝和玩具碎屑，清潔布、收納袋和清潔用品要先準備。", "淨淨 Clean Clean 可放在清潔備案裡比較；使用限制請回商品頁確認。"),
            ("常見錯誤：只準備拍照畫面", "蛋糕太大、零食太多或玩具太複雜，都可能讓後續收拾變麻煩。", "Elite Fashion 編輯團隊的判斷是：好的寵物生日禮物，要在慶祝後仍能回到穩定日常。"),
            ("下單前做生日四格", "蛋糕、零食、玩具、清潔。四格都保守確認，再看包裝和預算。", "價格、成分、保存、規格、活動與庫存請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("寵物生日一定要買蛋糕嗎？", "不一定。先看成分、份量、保存和寵物狀況，再決定是否需要。"),
            ("零食和玩具要怎麼搭？", "零食少量、玩具可輪替，並保留清潔備案。"),
            ("生日用品可以寫成身體狀態建議嗎？", "不可以。本文只討論送禮和使用順序，成分與限制請以商品頁為準。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[50:55]:
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
        note = "2026-06-21 momo 收益型內容第十一組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第十一組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
