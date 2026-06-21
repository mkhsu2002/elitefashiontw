#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-eight-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B08"
ORIGINAL_MERCHANT_CARD = base.merchant_card
ORIGINAL_LOAD_TRACKER = base.load_tracker
TEXT_REPLACEMENTS = {
    "模型": "拼裝選物",
    "動漫": "角色收藏",
    "玩家": "收藏族群",
}


def merchant_card(row: dict[str, str], slug: str) -> dict[str, str]:
    card = ORIGINAL_MERCHANT_CARD(row, slug)
    for field in ("selectionReason", "riskNote"):
        for source, target in TEXT_REPLACEMENTS.items():
            card[field] = card[field].replace(source, target)
    return card


base.merchant_card = merchant_card


def load_tracker() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], list[str]]:
    rows, rows_by_merchant, fieldnames = ORIGINAL_LOAD_TRACKER()
    for row in rows:
        for field in ("content_angles", "main_products"):
            for source, target in TEXT_REPLACEMENTS.items():
                row[field] = row.get(field, "").replace(source, target)
    return rows, {row["merchant_id"]: row for row in rows}, fieldnames


base.load_tracker = load_tracker

base.COVER_SOURCES = {
    "office-drink-cabinet-plant-milk-tea-coffee-sparkling": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37b79a3f94819b81cea963af00c418.png",
    "road-scooter-dashcam-reflective-rain-charging-kit": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37b7fa31dc819b9c2d3ea3fc4d9df6.png",
    "family-gift-blocks-board-games-puzzles-books": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37b867fbc4819bb2e983596e4bfacb.png",
    "sun-rain-gear-entryway-commute-bag-scooter-storage": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37b8de33e4819bb26337db769dc5d2.png",
    "cold-brew-tea-gift-box-afternoon-decision": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0dff854c67f09b75016a37b95c2bcc819bb70a1536e27a0f47.png",
}

ROW_OVERRIDES = {
    "office-drink-cabinet-plant-milk-tea-coffee-sparkling": {
        "elite_judgment": "飲品櫃先分日常、共享、來客與加班，不把包裝標語當採買理由。",
        "answer_summary": "辦公室飲品櫃要先看保存、咖啡因、糖度與共享便利性，再補植物奶、茶、咖啡與氣泡飲。",
        "risk_guardrail": "飲品與食品不宣稱保健、代謝、減重或醫療效果；成分、咖啡因、保存方式與過敏原請以商品頁及包裝為準。",
    },
    "road-scooter-dashcam-reflective-rain-charging-kit": {
        "elite_judgment": "移動備案先處理可見、可記錄、可充電與可乾收，不把配件當安全保證。",
        "answer_summary": "自駕與機車備案要先看路線、天氣、安裝與充電，再比較行車紀錄、反光、雨具與電力。",
        "risk_guardrail": "行車紀錄、反光配件、雨具與充電用品不保證行車安全；安裝、法規、規格與使用限制請以商品頁及官方規定為準。",
    },
    "family-gift-blocks-board-games-puzzles-books": {
        "elite_judgment": "家庭禮物先看共同使用的時間與收納，而不是把益智二字當成購買理由。",
        "answer_summary": "家庭禮物與益智玩具要先看年齡、共同使用、收納與安全標示，再選積木、桌遊、拼圖與書。",
        "risk_guardrail": "玩具與書籍不承諾學習、發展或能力效果；年齡限制、材質、警語與零件風險請以商品頁及包裝為準。",
    },
    "sun-rain-gear-entryway-commute-bag-scooter-storage": {
        "elite_judgment": "防曬雨具要分成出門前、路上與回家後三個位置，濕物不能只靠記憶處理。",
        "answer_summary": "防曬與雨具收納要先分玄關、通勤包與車廂，並安排乾濕分流。",
        "risk_guardrail": "防曬、防潑、抗風、耐候與收納規格請以商品頁標示為準，不自行延伸保護效果。",
    },
    "cold-brew-tea-gift-box-afternoon-decision": {
        "elite_judgment": "冷泡茶與茶禮盒先看喝的人、喝的時段與保存方式，不只看包裝體面。",
        "answer_summary": "冷泡茶與茶禮盒要先分日常飲用、送禮與下午茶，再看茶種、保存與份量。",
        "risk_guardrail": "茶飲與食品不宣稱保健、助眠、代謝或醫療效果；成分、保存期限、咖啡因與適用限制請以商品頁及包裝為準。",
    },
}

base.TOPIC_HUBS = {
    "office-drink-cabinet-plant-milk-tea-coffee-sparkling": {
        "topicCategory": "food-nutrition",
        "topicCategoryLabel": "飲食與補給",
        "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "road-scooter-dashcam-reflective-rain-charging-kit": {
        "topicCategory": "outdoor-gear",
        "topicCategoryLabel": "戶外裝備",
        "primaryHub": {"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"},
        "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}],
    },
    "family-gift-blocks-board-games-puzzles-books": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
    "sun-rain-gear-entryway-commute-bag-scooter-storage": {
        "topicCategory": "wardrobe-style",
        "topicCategoryLabel": "衣櫥與穿搭",
        "primaryHub": {"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"},
        "secondaryHubs": [{"key": "outdoor-travel-reset", "title": "旅行與戶外移動準備指南", "file": "outdoor-travel-reset.html", "url": "/outdoor-travel-reset", "category": "outdoor-escapes"}],
    },
    "cold-brew-tea-gift-box-afternoon-decision": {
        "topicCategory": "food-nutrition",
        "topicCategoryLabel": "飲食與補給",
        "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
}

base.BLUEPRINTS = {
    "office-drink-cabinet-plant-milk-tea-coffee-sparkling": {
        "heroAlt": "明亮辦公室茶水間層架上有空白紙盒飲品、茶罐、咖啡豆、透明氣泡水瓶與杯具",
        "audience": "想替辦公室茶水間、共享櫃或工作午後補給建立採買順序的讀者",
        "excerpt": "辦公室飲品櫃要先看保存、咖啡因、糖度與共享便利性，再補植物奶、茶、咖啡與氣泡飲。",
        "tags": ["辦公室飲品", "植物奶", "茶包", "咖啡氣泡飲"],
        "intro": "辦公室飲品櫃最容易被包裝和口味帶走，但真正決定使用率的，是保存、開封後放哪裡、誰會喝、多久喝完。植物奶、茶包、咖啡、氣泡飲和草本飲都能替午後留下停頓，只是它們不該被放進同一個籃子裡補貨。若沒有先分日常、共享、來客與加班，茶水間很快會出現重複、過期和沒人敢開封的品項。",
        "editorialAngle": "先按保存與共享情境分格，再看口味和品牌。",
        "sections": [
            ("先分日常、共享、來客與加班", "日常飲品要穩定、保存簡單；共享飲品要份量清楚；來客飲品看體面與沖泡門檻；加班備品則要容易拿取。四種情境分開後，補貨才不會只看當下心情。", "KKM 健康飲食專賣、Teavoya 嘉柏茶業與 Xinto Coffee 可分別放在植物奶、茶與咖啡情境中比較；本文不宣稱保健或個人飲食效果。"),
            ("糖度、咖啡因和保存方式要比包裝先看", "共享櫃最怕的是有人不能喝、有人不想開、有人開了卻不知道該冷藏。茶包、瓶裝、紙盒飲和咖啡豆的保存條件不同，補貨前要先把未開封、已開封和個人用品分層。", "PV女性微甜草本飲、恩亞生活與 Zymoide 可作為不同風味補充，成分、咖啡因與保存方式仍以商品頁和包裝為準。"),
            ("植物奶和咖啡要一起看使用時刻", "植物奶若常被加進咖啡或茶裡，應和咖啡豆、濾掛、杯具、冰箱位置一起規劃。只買飲品不安排杯具和開封保存，最後會變成茶水間的壓力。", "若公司冰箱空間有限，單瓶容量、開封後期限和是否容易分次使用，比一次買大量更重要。"),
            ("常見錯誤：把飲品寫成健康捷徑", "無糖、草本、酵素、植物奶等字眼都容易被過度想像。辦公室飲品可以讓午後有節奏，但不應被看成替代正餐、休息或個人飲食管理的方法。", "Elite Fashion 編輯團隊的判斷是：成熟的飲品櫃不是品項很多，而是每一格都知道誰會喝、何時喝完、開封後放哪裡。"),
            ("補貨前的三格清點", "先清點未開封、已開封、快到期三格，再決定新增。若快到期品項仍很多，先暫停補貨，比追求完整口味更務實。", "價格、活動、庫存、成分、保存方式與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("辦公室飲品櫃要先買哪一類？", "先補每天會喝、保存簡單且共享門檻低的品項，再補來客與加班備用。"),
            ("草本飲、酵素飲或植物奶可以當成健康建議嗎？", "不可以。本文只談補給與收納順序，成分與適用限制請以商品頁及包裝為準。"),
            ("怎麼避免飲品越買越多？", "固定清點未開封、已開封和快到期三格，再設定兩週到一個月的補貨量。"),
        ],
    },
    "road-scooter-dashcam-reflective-rain-charging-kit": {
        "heroAlt": "深色車庫工作桌上有無品牌行車紀錄器、反光配件、雨衣、折傘、充電線與行動電源，旁邊停著沒有標誌的機車",
        "audience": "需要整理自駕、機車通勤與短途移動備案的人",
        "excerpt": "自駕與機車備案要先看路線、天氣、安裝與充電，再比較行車紀錄、反光、雨具與電力。",
        "tags": ["機車通勤", "行車紀錄器", "反光配件", "雨具充電"],
        "intro": "自駕與機車移動的備案，不能只靠臨時想起來。行車紀錄器、反光配件、雨衣、充電線與行動電源都各有角色，但它們不能被寫成安全保證。比較成熟的做法，是先看你的路線、天氣、停車位置、安裝方式和充電習慣，再決定哪些用品應該固定在車上，哪些只適合放在包裡。",
        "editorialAngle": "把可記錄、可看見、可乾收與可充電分開規劃。",
        "sections": [
            ("先分車上固定與包內備案", "行車紀錄、雨具、反光配件、充電線和行動電源有些適合固定在車上，有些適合跟著人走。若全部放在車廂，遇到不同交通方式時反而拿不到。", "安鈦科技行車記錄器、反光屋 FKW 與 OMBRA 可分別放在記錄、可見度與雨具情境裡比較；安裝與法規仍須回商品頁和官方規定確認。"),
            ("雨具要先看濕物收納", "雨衣和折傘的問題通常不是有沒有帶，而是濕了以後放哪裡。車廂、包內與玄關都要有暫放位置，才不會讓下一段行程變得混亂。", "LFM 機車精品網路旗艦店、FULTON 與相關雨具品牌可作為不同移動情境補充，尺寸與材質請以商品頁為準。"),
            ("電力備案要看接口和固定位置", "行動電源、線材、車用充電與手機架若沒有一起看，很容易出現有電源卻沒有線、有線卻不方便導航的情況。", "Momax Taiwan 可作為電力配件參考；相容性、容量、輸出與使用限制請以下單前商品頁公告為準。"),
            ("常見錯誤：把配件當成安心感", "行車紀錄、反光與雨具都是備案，不是讓人忽略路況、規定和天候的理由。真正值得保留的配件，是在需要時拿得到、裝得上、收得回。", "Elite Fashion 編輯團隊的判斷是：移動備案的價值，在於降低臨時慌亂，而不是製造更多車廂雜物。"),
            ("出門前的四點檢查", "路線、天氣、電力、濕物袋。四點確認後，再看是否需要反光配件、備用雨具或額外線材。", "價格、規格、活動、庫存、配送、安裝與適用限制請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("行車紀錄器要怎麼先判斷？", "先看安裝位置、電源方式、畫面角度與法規限制，再比較規格。"),
            ("反光配件可以保證移動安全嗎？", "不可以。本文只把它視為備案配件，實際移動仍需遵守交通規定並注意路況。"),
            ("雨衣和傘要不要都放車上？", "先看交通方式與濕物收納。若車廂潮濕或空間不足，部分雨具可改放通勤包。"),
        ],
    },
    "family-gift-blocks-board-games-puzzles-books": {
        "heroAlt": "陽光客廳木桌上有無品牌積木、桌遊棋盤、拼圖、空白書本、彩色鉛筆與禮盒",
        "audience": "想挑家庭共享禮物、週末桌面活動與書店選物的人",
        "excerpt": "家庭禮物與益智玩具要先看年齡、共同使用、收納與安全標示，再選積木、桌遊、拼圖與書。",
        "tags": ["家庭禮物", "積木桌遊", "拼圖", "書店選物"],
        "intro": "家庭禮物最常被兩種期待拉扯：一邊希望有趣，一邊又希望看起來有意義。積木、桌遊、拼圖和書都適合放進家庭時間，但它們不應被包裝成保證成長或能力改變的工具。更好的挑法，是先看誰會一起玩、玩多久、收在哪裡、是否符合年齡和材質標示，再決定禮物形式。",
        "editorialAngle": "共同使用和收納位置，比禮物看起來多聰明更重要。",
        "sections": [
            ("先看誰會一起使用", "一份好禮物不是只讓收禮者打開，而是能讓家庭裡有人願意一起開始。若需要大人陪同，時間和耐心也要算進選購條件。", "888便利購兒童玩具專賣店、磚星球樂高專賣店與 WA-GU-MI 可作為積木與拼裝選物比較入口；年齡與零件限制請以商品頁和包裝為準。"),
            ("桌遊和拼圖要看收尾難度", "桌遊規則、拼圖片數、收納盒大小與完成後是否能暫放，會直接影響使用率。若每次都要清空餐桌，禮物很快會被收進櫃子。", "墊腳石書店可作為書籍、文具與家庭選物參考；不同品項的適用年齡和警語需分別確認。"),
            ("送給有孩子的家庭，要把安全標示放前面", "材質、年齡限制、小零件、清潔方式與是否需要陪同，都比包裝照片更重要。禮物越靠近入口或手作，越需要保守查看標示。", "寶寶共和國與 SUSS Living 可作為親子用品與生活選物補充；本文不承諾學習、發展或能力效果。"),
            ("常見錯誤：只買看起來高級的盒子", "禮盒漂亮不代表會被使用。若規則太複雜、片數太多、收納太麻煩，家庭時間很容易變成整理壓力。", "Elite Fashion 編輯團隊的判斷是：好的家庭禮物要能在週末午後自然展開，也能在晚餐前快速收起。"),
            ("送禮前的四個問題", "誰一起玩、玩多久、收哪裡、是否符合標示。四個答案清楚後，再比較品牌、預算與包裝。", "價格、規格、材質、年齡限制、警語、活動與庫存請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("家庭禮物要選積木、桌遊還是書？", "先看收禮者年齡、是否有人陪同、可使用時間與收納位置，再決定形式。"),
            ("益智玩具可以寫成能力改變嗎？", "不可以。本文只討論家庭時間與選購順序，年齡限制與警語以商品頁及包裝為準。"),
            ("拼圖片數怎麼抓？", "先看可使用桌面、暫放空間和共同完成時間，不要只看圖案漂亮。"),
        ],
    },
    "sun-rain-gear-entryway-commute-bag-scooter-storage": {
        "heroAlt": "明亮玄關長椅旁有素色防曬外套、折傘、雨傘、通勤包、無品牌安全帽與機車車廂",
        "audience": "想把防曬、雨具、通勤包與機車車廂整理成固定備案的人",
        "excerpt": "防曬與雨具收納要先分玄關、通勤包與車廂，並安排乾濕分流。",
        "tags": ["防曬雨具", "玄關收納", "通勤包", "機車車廂"],
        "intro": "台灣的日曬和午後雨，常讓出門前的判斷變得匆忙。防曬外套、折傘、雨衣、帽子、通勤包和車廂備品如果沒有固定位置，很容易出現出門忘記、下雨翻包、回家濕物亂放的循環。這篇不把任何防護效果寫成保證，而是把玄關、通勤包與車廂分成三個位置，讓出門和回家都更有秩序。",
        "editorialAngle": "用品要分出門前、路上與回家後三段，而不是全部塞在同一處。",
        "sections": [
            ("玄關負責出門前最後檢查", "玄關適合放常用外套、傘、帽子和濕物暫放籃。它不是收納倉庫，而是讓你在關門前看見今天的天氣備案。", "UV100、FULTON 與 OMBRA 可分別放在防曬服飾、晴雨傘與雨衣雨鞋情境中比較；相關規格請以商品頁標示為準。"),
            ("通勤包只放會跟著人走的備案", "包內備案應少而精：折傘、薄袋、紙巾、小外套或雨天收納袋。太多備品會讓包變重，也會讓真正要用的物品沉到底部。", "左都雨傘官方旗艦店與 UD LAB 可作為傘具和包款參考；尺寸、重量、材質與收納方式要回商品頁確認。"),
            ("車廂要留給濕物與路上變化", "機車車廂適合放雨衣、濕物袋或不想放進通勤包的備品，但要避免長期堆放潮濕物。車廂不是萬用抽屜，定期清空才可靠。", "LFM 機車精品網路旗艦店可作為機車周邊補充，適用車型與安裝方式請以下單前資訊為準。"),
            ("常見錯誤：買很多雨具卻沒有濕物位置", "雨具真正麻煩的時刻通常在使用後。若沒有回家後的吊掛、擦拭和暫放位置，再好的雨具也會變成玄關壓力。", "Elite Fashion 編輯團隊的判斷是：防曬雨具採買的成熟度，要看回家後能不能快速復原。"),
            ("下單前做三段式清單", "出門前放玄關、路上放包內、使用後放濕物區。每件用品都要知道自己屬於哪一段。", "價格、規格、活動、庫存、防曬、防潑、抗風與耐候資訊請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("防曬外套和傘要放哪裡？", "常用外套可放玄關，折傘可放包內；若騎車，雨衣和濕物袋可另放車廂。"),
            ("商品標示的防曬、防潑或抗風怎麼看？", "請回商品頁與包裝確認，本文不自行延伸保護效果。"),
            ("車廂可以長期放雨具嗎？", "要看車廂狀態與濕物處理。使用後仍建議晾乾、清空並確認是否影響其他物品。"),
        ],
    },
    "cold-brew-tea-gift-box-afternoon-decision": {
        "heroAlt": "窗邊餐桌上有玻璃冷泡茶壺、無字茶包、素色茶禮盒、小點心、茶杯與綠色緞帶",
        "audience": "想在日常冷泡、下午茶與茶禮盒之間做選擇的人",
        "excerpt": "冷泡茶與茶禮盒要先分日常飲用、送禮與下午茶，再看茶種、保存與份量。",
        "tags": ["冷泡茶", "茶禮盒", "下午茶", "送禮選物"],
        "intro": "茶很容易被包裝成一種體面的禮物，但真正合適的茶，仍要回到誰會喝、在哪裡喝、一次喝多少、是否方便保存。冷泡茶適合日常節奏，茶禮盒適合心意表達，下午茶則更重視搭配與份量。把三種情境分開，才不會只因盒子漂亮就下單。",
        "editorialAngle": "先分喝的人與喝的時段，再看包裝和價格。",
        "sections": [
            ("日常冷泡先看保存和份量", "冷泡茶要看茶包尺寸、壺具容量、冰箱位置和預計喝完時間。若一次泡太多，反而容易造成保存壓力。", "Teavoya 嘉柏茶業、嘉嶼 CATTEA 與 ACE TEA 蒔宇茶可放在冷泡、茶包與茶葉情境中比較；咖啡因與保存方式請以商品頁及包裝為準。"),
            ("送禮茶盒要看對方是否會泡", "禮盒體面不等於適合。若收禮者沒有壺具、沒有保存空間或少喝茶，單份包裝、簡單沖泡和明確保存期限會比華麗盒型更實際。", "暮朝食粹與 LamiFans 可作為伴手禮和生活選物補充，仍要看成分、份量與保存資訊。"),
            ("下午茶重點是搭配，不是茶越多越好", "下午茶通常會搭配點心、工作休息或來客招待。茶種、濃淡、份量和杯具要一起看，避免買了很多茶，卻沒有適合的飲用場景。", "若商品含特殊成分或限制，請回商品頁確認，不自行延伸身體狀態或飲用好處。"),
            ("常見錯誤：只看包裝漂亮", "茶禮盒若太大、保存太短或沖泡太麻煩，很可能成為櫃子裡的壓力。真正好送的茶，應該讓對方容易打開、容易泡、容易喝完。", "Elite Fashion 編輯團隊的判斷是：茶禮盒的質感不在盒子多華麗，而在收禮者是否能自然使用。"),
            ("下單前的三個判斷", "日常飲用看保存；送禮看使用門檻；下午茶看搭配。三種答案不同，適合的茶也會不同。", "價格、活動、庫存、成分、保存期限、咖啡因與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("冷泡茶適合送禮嗎？", "可以作為選項，但要看對方是否有冷藏空間、壺具和飲用習慣。"),
            ("茶可以寫成身體狀態建議嗎？", "不可以。本文不宣稱助眠、保健、代謝或醫療用途，請以商品頁及包裝資訊為準。"),
            ("茶禮盒怎麼避免送了不用？", "先看收禮者是否會泡、多久能喝完、保存是否簡單，再看包裝。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[35:40]:
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
        note = "2026-06-21 momo 收益型內容第八組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第八組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
