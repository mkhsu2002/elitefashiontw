#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-nine-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B09"

base.COVER_SOURCES = {
    "remote-work-bag-charging-audio-presentation-storage": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37bd8e7fbc819396f32c89f054de69.png",
    "desk-cable-charger-monitor-protection-backup-organizer": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37bdcebfd881939d71a114ab73a7e4.png",
    "summer-low-pressure-sun-sleep-drink-light-food": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37be591d5c8193ae60476f214a74f4.png",
    "home-care-bathing-transfer-storage-safety-flow": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37be9ad55881939b9eff765896df23.png",
    "scent-bodycare-gift-essential-oil-towel-goods": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_02dd0d2c5ed5c541016a37bee27658819399ebb25659801aa8.png",
}

ROW_OVERRIDES = {
    "remote-work-bag-charging-audio-presentation-storage": {
        "elite_judgment": "遠距工作包先分簡報、通話、充電與收納四格，不把包塞滿當成準備充分。",
        "answer_summary": "遠距工作包清單要先看會議、移動距離、電力與線材，再補耳機、簡報轉接與收納。",
        "risk_guardrail": "3C 商品相容性、規格、保固、活動與庫存請以商品頁及官方說明為準，不自行延伸效率或穩定性承諾。",
    },
    "desk-cable-charger-monitor-protection-backup-organizer": {
        "elite_judgment": "桌面線材整理先把正在使用、偶爾使用與備份小物分層，線不該靠抽屜消失。",
        "answer_summary": "桌面線材要先看設備數量、接口、充電位置與備份流程，再買收納和保護周邊。",
        "risk_guardrail": "充電、保護貼、螢幕與備份周邊的相容性、規格、保固、活動與庫存請以商品頁及官方說明為準。",
    },
    "summer-low-pressure-sun-sleep-drink-light-food": {
        "elite_judgment": "夏季低負擔日常先處理日曬、噪音、飲品保存與輕食補給，不把單一商品寫成身體答案。",
        "answer_summary": "夏季日常要先看日曬、休息環境、飲品保存與輕食份量，再比較防曬、耳塞與補給品。",
        "risk_guardrail": "服飾、耳塞、飲品與食品不作醫療、保健、睡眠或身形承諾；成分、咖啡因、保存與規格請以商品頁及包裝為準。",
    },
    "home-care-bathing-transfer-storage-safety-flow": {
        "elite_judgment": "居家照護動線先看浴室入口、移位路徑、濕物收納與照顧者拿取位置，不把用品當萬用解方。",
        "answer_summary": "居家照護動線要先看沐浴、移位、收納與照顧者流程，再比較輔具、濾淨、按摩與收納品。",
        "risk_guardrail": "照護、沐浴、移位、按摩、濾淨與收納用品不能取代動線評估或專業判斷；使用限制、承重、安裝與專業建議請以商品頁及專業人員說明為準。",
    },
    "scent-bodycare-gift-essential-oil-towel-goods": {
        "elite_judgment": "香氛與身體保養送禮先看收禮者習慣、空間大小、氣味接受度與耗材保存，不只看包裝漂亮。",
        "answer_summary": "香氛與身體保養送禮要先分氣味、布品、身體清潔與生活小物，再看品牌和預算。",
        "risk_guardrail": "香氛、精油、蠟燭、毛巾與身體保養品不作療效、空間狀態、睡眠或氣味承諾；成分、材質、保存與使用限制請以商品頁及包裝為準。",
    },
}

base.TOPIC_HUBS = {
    "remote-work-bag-charging-audio-presentation-storage": {
        "topicCategory": "smart-living-tech",
        "topicCategoryLabel": "智慧生活科技",
        "primaryHub": {"key": "ai-work-reset-45", "title": "AI 工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"},
        "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}],
    },
    "desk-cable-charger-monitor-protection-backup-organizer": {
        "topicCategory": "smart-living-tech",
        "topicCategoryLabel": "智慧生活科技",
        "primaryHub": {"key": "ai-work-reset-45", "title": "AI 工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "summer-low-pressure-sun-sleep-drink-light-food": {
        "topicCategory": "food-nutrition",
        "topicCategoryLabel": "飲食與補給",
        "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"},
        "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}],
    },
    "home-care-bathing-transfer-storage-safety-flow": {
        "topicCategory": "home-rituals",
        "topicCategoryLabel": "居家儀式",
        "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"},
        "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}],
    },
    "scent-bodycare-gift-essential-oil-towel-goods": {
        "topicCategory": "beauty-grooming",
        "topicCategoryLabel": "妝髮與身體照護",
        "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"},
        "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}],
    },
}

base.BLUEPRINTS = {
    "remote-work-bag-charging-audio-presentation-storage": {
        "heroAlt": "機場貴賓室大理石桌面上有無品牌工作包、筆電、充電線、耳機盒、簡報轉接器與收納包",
        "audience": "需要在咖啡店、客戶辦公室、旅館與移動途中穩定工作的讀者",
        "excerpt": "遠距工作包清單要先看會議、移動距離、電力與線材，再補耳機、簡報轉接與收納。",
        "tags": ["遠距工作", "工作包", "充電線材", "簡報收納"],
        "intro": "遠距工作包不是把所有 3C 配件都塞進去，而是讓下一場會議、下一段移動和下一次簡報不被小物拖住。真正該先盤點的是：你在哪些地方工作、每次離開插座多久、會不會需要投影、通話是否常被環境干擾。當使用時刻先排出來，充電、耳機、簡報線材和收納包才會各就各位。",
        "editorialAngle": "先排工作時刻，再決定哪些配件進包。",
        "sections": [
            ("先分會議、移動與簡報三格", "會議需要耳機和穩定電力，移動需要輕量收納，簡報需要轉接與備線。三格分清楚後，工作包會變薄也更可靠。", "Momax Taiwan、DTAudio 聆翔與 REAICE 可分別放在電力、音訊與螢幕線材情境中比較；規格仍需回商品頁確認。"),
            ("線材要成組，不要散放", "充電頭、線、轉接器和備用小物若分散在不同夾層，很容易臨場找不到。每一組線材最好對應一個任務。", "LamiFans、華克電腦與 UD LAB 可作為生活小物、筆電和包款收納補充。"),
            ("耳機和簡報線材要看場地限制", "客戶辦公室、共享空間和旅館會議室設備不同，轉接器和音訊配件要按常見場地準備，不要只看自己桌上的配置。", "相容性、接口、保固與適用限制請以商品頁與官方說明為準。"),
            ("常見錯誤：為了安心帶太多", "備品越多不一定越穩，反而可能讓包變重、翻找變慢。連續三次沒用到的配件，可以降級為行李箱備案。", "Elite Fashion 編輯團隊的判斷是：成熟的遠距工作包，應該讓你少翻包，而不是帶著一座抽屜出門。"),
            ("下單前做一次包內演練", "從開電腦、接電、開會、簡報、收線到離開，照順序摸一次包內位置。卡住的地方，才是真正需要補的物件。", "價格、規格、活動、庫存、保固與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("遠距工作包最先補什麼？", "先補電力、通話與簡報轉接的缺口，再看收納包和外型。"),
            ("線材要不要每一條都備份？", "不一定。常用接口可備一組，低頻線材可放在固定備用包裡。"),
            ("耳機怎麼選？", "先看通話場景、配戴時間、設備相容性與攜帶方式，再比較規格。"),
        ],
    },
    "desk-cable-charger-monitor-protection-backup-organizer": {
        "heroAlt": "灰色升降桌上有無品牌外接螢幕、充電器、螢幕線、保護貼套、備份硬碟與分格收納盒",
        "audience": "想整理工作桌線材、充電與備份流程的人",
        "excerpt": "桌面線材要先看設備數量、接口、充電位置與備份流程，再買收納和保護周邊。",
        "tags": ["桌面線材", "充電器", "螢幕線", "備份收納"],
        "intro": "桌面線材整理不能只靠收納盒。真正混亂的原因通常是設備數量變多、接口不一致、充電位置太遠、備份小物沒有固定位置。若沒有先分正在使用、偶爾使用和只在備份時才拿出的線，整理完的桌面很快又會回到原狀。",
        "editorialAngle": "先釐清線材任務，再決定收納方式。",
        "sections": [
            ("先列出桌上每天會接的設備", "筆電、外接螢幕、手機、平板、耳機、硬碟各需要不同線材。先列設備，再看接口和插座，會比先買集線器更穩。", "Momax Taiwan、REAICE 與 EZstick 可放在充電、螢幕線材與保護周邊裡比較。"),
            ("線材分三層：常用、低頻、備份", "常用線留在桌上，低頻線進抽屜，備份線放標準收納袋。若所有線都躺在桌上，桌面永遠不會真的乾淨。", "手些小子3C、muni 3C 與日本橋3C 可作為手機平板與 3C 周邊補充。"),
            ("保護貼和備份小物要有固定位置", "保護貼、擦拭布、備份硬碟和讀卡小物若散放，會在需要時失蹤。它們不必出現在桌面，但要固定在同一層抽屜。", "材質、尺寸、相容性與保固資訊請以商品頁為準。"),
            ("常見錯誤：把線藏起來就算整理", "線藏進盒子但沒有標準路徑，下一次拔插會更麻煩。整理的目標是讓每條線知道自己去哪，而不是消失在視線外。", "Elite Fashion 編輯團隊的判斷是：好的桌面整理要能支撐每天重複使用，而不是只為拍照。"),
            ("下單前先畫桌面線路", "螢幕線往哪走、充電器插哪、硬碟放哪、抽屜能不能打開。先畫路線，再看是否需要收納盒、線夾或轉接器。", "價格、規格、活動、庫存、保固與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("桌面線材整理第一步是什麼？", "先列出每天會接的設備和接口，再分常用、低頻與備份線。"),
            ("收納盒越多越好嗎？", "不一定。若沒有先分任務，收納盒只會把混亂藏起來。"),
            ("備份硬碟要放桌上嗎？", "不一定。重點是固定位置與固定流程，而不是一定要露出在桌面。"),
        ],
    },
    "summer-low-pressure-sun-sleep-drink-light-food": {
        "heroAlt": "夏日明亮臥室與陽台旁有素色防曬外套、耳塞盒、冰飲、空白植物奶紙盒與輕食盤",
        "audience": "想用更低壓方式整理夏季出門、休息、飲品與輕食的人",
        "excerpt": "夏季日常要先看日曬、休息環境、飲品保存與輕食份量，再比較防曬、耳塞與補給品。",
        "tags": ["夏季日常", "防曬外套", "耳塞", "輕食飲品"],
        "intro": "夏天的低負擔，不是把所有東西都換成清爽版本，而是讓日曬、噪音、飲品與輕食各有位置。防曬服飾、耳塞、草本飲、植物奶和輕食補給都可以進入生活，但它們不該被寫成身體答案。更實際的順序，是先看一天中最容易失控的時刻，再決定需要哪些小物協助。",
        "editorialAngle": "用一天的時段拆解需求，不把單一商品當答案。",
        "sections": [
            ("早上先處理日曬和通勤", "出門前先看會不會曝曬、是否需要外套、帽子或包內備品。防曬服飾要按行程、收納和清洗方式來看。", "UV100 可放在防曬服飾情境中比較；相關標示與規格請以商品頁為準。"),
            ("午后飲品要看保存與糖度", "草本飲、植物奶、果乾或輕食都要看成分、咖啡因、糖度、保存和份量，不要只看包裝或口味。", "PV女性微甜草本飲、KKM 健康飲食、GUMi低碳與 Zymoide 可作為飲品與輕食補給參考。"),
            ("夜間用品只談環境，不談承諾", "耳塞、薄毯和床邊水杯可以幫助空間更安靜有序，但不應被寫成身體狀態保證。", "耳根清靜可作為耳塞用品參考；配戴感、材質與限制請回商品頁確認。"),
            ("常見錯誤：低負擔變成低營養或少休息", "低負擔不是少吃、少喝或硬撐，而是把保存、份量和使用時刻看清楚。夏天越忙，越不能只靠臨時購買。", "Elite Fashion 編輯團隊的判斷是：夏季清爽感來自規律補位，不是把每件商品都賦予過多期待。"),
            ("下單前的四個問題", "會不會曬、會不會吵、飲品能不能保存、輕食多久吃完。四個答案清楚後，再看品牌和預算。", "價格、成分、咖啡因、保存方式、規格、活動與庫存請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("夏季低負擔日常先買什麼？", "先看最常卡住的是通勤日曬、午后飲品、夜間環境或輕食保存，再補對應物品。"),
            ("耳塞可以寫成身體狀態建議嗎？", "不可以。本文只討論環境與收納，配戴限制請以商品頁為準。"),
            ("飲品和輕食怎麼避免買太多？", "先看保存期限與兩週內使用量，再決定補貨。"),
        ],
    },
    "home-care-bathing-transfer-storage-safety-flow": {
        "heroAlt": "明亮無障礙浴室裡有無品牌沐浴椅、扶手、移位板、止滑墊、毛巾與開放式收納架",
        "audience": "需要替家中照護、沐浴、移位與收納流程建立基本順序的人",
        "excerpt": "居家照護動線要先看沐浴、移位、收納與照顧者流程，再比較輔具、濾淨、按摩與收納品。",
        "tags": ["居家照護", "沐浴動線", "移位收納", "照顧者流程"],
        "intro": "居家照護用品最不能只看單一商品照片。沐浴、移位、擦乾、暫放衣物、收納耗材，每一步都牽涉空間、照顧者、使用者和濕滑環境。用品可以補位，但不能取代專業評估；真正該先建立的是動線，而不是先把浴室塞滿。",
        "editorialAngle": "先看每一步如何發生，再看用品是否真的能放進家裡。",
        "sections": [
            ("先畫出浴室入口到沐浴點", "門寬、轉身空間、地面高低差、毛巾位置和換洗衣物暫放點，都要先看。若路徑不清楚，用品會變成障礙。", "TWyzy新世代、一然健康與 EVERPOLL 可放在沐浴、照護與濾淨情境裡比較；使用限制與安裝條件要回商品頁確認。"),
            ("移位用品要看承重與照顧者動作", "移位板、沐浴椅或扶手都不是只看尺寸。承重、材質、固定方式、地面狀況和照顧者姿勢都需要被確認。", "必要時應先詢問專業人員，不用商品文案替代評估。"),
            ("收納要靠近使用點", "毛巾、清潔品、備用衣物、濕物袋和照護耗材最好按使用順序放置。拿不到的用品，在照護當下等於不存在。", "完美主義可作為收納補充；安里嚴選與 COZZY 嚴選可作為按摩或生活用品參考。"),
            ("常見錯誤：只買大件，忽略小動線", "浴室裡最常出問題的不是只有大件用品，也可能是毛巾放太遠、地墊太厚、瓶罐太多或暫放區不足。", "Elite Fashion 編輯團隊的判斷是：居家照護的質感來自每一步少一點慌亂，而不是用品數量。"),
            ("下單前的四項確認", "尺寸、承重、安裝、清潔。四項都確認後，再看是否需要濾淨、按摩或收納補充。", "價格、規格、活動、庫存、承重、安裝與使用限制請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("居家照護用品第一步買什麼？", "先看浴室入口、移位路徑和照顧者動作，再決定是否補沐浴椅、移位板或收納。"),
            ("商品可以保證使用安全嗎？", "不可以。承重、安裝、使用方式與專業建議都需要分別確認。"),
            ("按摩或濾淨用品要放進照護清單嗎？", "可以作為補充，但不能取代動線評估與專業建議。"),
        ],
    },
    "scent-bodycare-gift-essential-oil-towel-goods": {
        "heroAlt": "深色梳妝台上有空白琥珀精油瓶、無品牌陶瓷蠟燭、折疊毛巾、無字香皂、禮盒與木質小物",
        "audience": "想挑香氛、精油、蠟燭、毛巾與身體保養送禮的人",
        "excerpt": "香氛與身體保養送禮要先分氣味、布品、身體清潔與生活小物，再看品牌和預算。",
        "tags": ["香氛送禮", "精油蠟燭", "毛巾浴巾", "身體保養"],
        "intro": "香氛與身體保養送禮很容易被包裝牽著走，但氣味、布品、蠟燭、精油和身體清潔用品都很私密。送得體面不等於適合使用；比較好的順序，是先看收禮者是否使用香味、空間大小、是否在意材質、是否容易保存，再決定禮盒內容。",
        "editorialAngle": "先看收禮者習慣，再讓包裝成為收尾。",
        "sections": [
            ("香氛先看接受度，不先看濃度", "精油、蠟燭或木質香氛都可能很有質感，但如果對方不使用香味，再漂亮也會變成負擔。", "THANN、au fait 無非與大檜仁心可放在香氛與木質小物情境中比較；氣味描述與成分請以商品頁為準。"),
            ("布品要看觸感與清洗", "毛巾、浴巾和襪類送禮比想像中實用，但尺寸、材質、清洗方式與收納空間要先看。", "MORINO 摩力諾生活館與 Awayuki 淡雪可作為布品和日製小物參考；材質與保存請以商品頁為準。"),
            ("蠟燭和精油要附上使用邊界", "香氛用品最怕的是收禮者不知道怎麼用或放在哪裡。送禮時可搭配托盤、收納袋或簡單使用提醒，但不要寫成身體或空間承諾。", "蒔柒可作為香氛生活選品補充；本文不作療效、空間狀態、睡眠或氣味承諾。"),
            ("常見錯誤：只看禮盒漂亮", "禮盒越大不一定越好。若收禮者住小宅、對氣味敏感或不常使用身體保養，少量高使用率比大盒更成熟。", "Elite Fashion 編輯團隊的判斷是：好的香氛送禮，是讓對方能自然打開，不需要重新安排生活。"),
            ("下單前的四個問題", "對方用不用香味、空間夠不夠、材質是否合適、多久能用完。四個答案清楚後，再比較品牌和預算。", "價格、成分、材質、香味描述、活動、庫存與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("香氛送禮最怕什麼？", "最怕只看包裝，忽略對方是否使用香味、是否有保存空間。"),
            ("精油或蠟燭可以寫成身體或空間效果嗎？", "不可以。本文只討論送禮與使用情境，成分與限制請以商品頁為準。"),
            ("毛巾浴巾適合當禮物嗎？", "適合實用型送禮，但要看材質、尺寸、清洗方式與對方收納空間。"),
        ],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[40:45]:
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
        note = "2026-06-21 momo 收益型內容第九組 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第九組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
