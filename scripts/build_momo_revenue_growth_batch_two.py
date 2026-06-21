#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import content_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[1]
MATRIX_CSV = ROOT / "automation" / "reports" / "momo-affiliate-revenue-growth-matrix-2026-06-21.csv"
TRACKER_CSV = ROOT / "automation" / "momo-brand-recommendation-tracker.csv"
COVER_MANIFEST = ROOT / "automation" / "codex-generated-cover-manifest.json"
TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-two-no-newsletter"
QUEUE_ID = "MOMO-REV-2026-06-21-W01-B02"
TODAY = "2026-06-21"


COVER_SOURCES = {
    "summer-airflow-fan-small-appliance-lighting-system": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a378f6ed63c8190917e6646daa56d74.png",
    "day-trip-bag-sun-charging-earplug-rainwear-checklist": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a378fb4bc2081908f4952f8e4a26f9c.png",
    "after-work-home-scent-light-storage-upgrade-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a37900ef87481909572b45f37204299.png",
    "second-monitor-laptop-stand-backup-work-setup": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a3790668c388190b7783efd1049fd96.png",
    "office-afternoon-drinks-tea-sparkling-pantry-guide": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0385f433edfc8f52016a3790bd7ba08190a4ded45e927abcd1.png",
}


TOPIC_HUBS: dict[str, dict[str, Any]] = {
    "summer-airflow-fan-small-appliance-lighting-system": {
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
    "day-trip-bag-sun-charging-earplug-rainwear-checklist": {
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
                "key": "commute-style-reset",
                "title": "通勤衣櫥與鞋包選物指南",
                "file": "commute-style-reset.html",
                "url": "/commute-style-reset",
                "category": "casual-chic",
            }
        ],
    },
    "after-work-home-scent-light-storage-upgrade-order": {
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
    "second-monitor-laptop-stand-backup-work-setup": {
        "topicCategory": "smart-living-tech",
        "topicCategoryLabel": "智慧生活科技",
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
    "office-afternoon-drinks-tea-sparkling-pantry-guide": {
        "topicCategory": "food-nutrition",
        "topicCategoryLabel": "飲食與補給",
        "primaryHub": {
            "key": "body-rhythm-reset",
            "title": "身體節奏與恢復生活指南",
            "file": "body-rhythm-reset.html",
            "url": "/body-rhythm-reset",
            "category": "wellness-movement",
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
}


BLUEPRINTS: dict[str, dict[str, Any]] = {
    "summer-airflow-fan-small-appliance-lighting-system": {
        "heroAlt": "夏日明亮客廳裡，循環扇、落地燈、小家電與窗邊綠植形成通風動線",
        "audience": "想在夏天前整理居家空氣、桌面電器與光線配置的讀者",
        "excerpt": "夏季小家電不是越多越好，先看風從哪裡進、熱停在哪裡，再決定循環扇、小家電與照明的位置。",
        "tags": ["夏季小家電", "循環扇", "居家照明", "空氣動線"],
        "intro": "夏天前整理家，不只是把循環扇或小家電買齊。真正影響舒適感的，是窗、門、桌面、燈光與收納之間有沒有形成一條清楚的空氣路線。若先買電器再找位置，最後常會出現插座不順、風被家具擋住、燈光讓空間更悶的狀況。本文用空氣入口、熱點、使用位置與收尾收納四個角度，整理出夏季前更不容易買錯的順序。",
        "editorialAngle": "先判斷風從哪裡進、熱停在哪裡，再決定電器與燈光。",
        "sections": [
            ("先找風的入口，不要先找電器", "打開窗後先站在家裡三個位置：玄關、沙發旁、工作桌。哪一處有風、哪一處悶熱、哪一處容易被窗簾或櫃體阻擋，會直接決定循環扇和小家電該放哪裡。", "Airmate、KINYO 與燈后這類品牌可以分別放在空氣循環、小家電和照明位置裡比較，但本文不宣稱任何商品具有降溫、節電或健康效果。"),
            ("熱點通常藏在桌邊、窗邊與電器旁", "夏天的熱不一定平均分布。窗邊日照、桌面螢幕、廚房小家電、燈具位置，都可能讓局部溫度感受變得明顯。先找熱點，比直接加一台電器更能避免重複購買。", "若你在客廳工作，桌燈、延長線與風扇角度要一起看；若是租屋或小宅，插座數量和走線安全比外型更優先。"),
            ("照明不要和風扇搶位置", "小宅很常把風扇、落地燈、收納籃與邊桌擠在同一角落，結果每一樣都用得不順。照明要照到使用區，風扇要讓空氣流動，收納則要留給遙控器、線材與季節用品。", "燈后、心科技生活家電館、SENGLI 或 Hysure 海說適合放在不同家電與居家條件裡做參考；尺寸、噪音、耗電與保固仍要回商品頁確認。"),
            ("常見錯誤：只看風量，沒看收尾", "循環扇或小家電用完後要放哪、線材怎麼收、濾網或表面怎麼清，這些才決定它能不能留在日常裡。若每次使用後都要跨過線或搬來搬去，很快就會被閒置。", "下單前先確認：插座距離、走道寬度、清潔方式、收納位置與使用頻率。這五件事比單看規格更接近真實生活。"),
            ("台灣情境要把濕氣也放進來", "台灣夏季的麻煩不只熱，還有悶與濕。小家電若放在潮濕角落或窗邊日曬處，保存與清潔都要更保守。家裡有木質家具、布品或大量紙本，也要避免把風只吹向單一收納角落。", "若商品涉及除濕、空氣處理或家電安全，請以商品標示與官方說明為準，不自行延伸效果。"),
            ("下單前的四格檢查", "把家裡畫成四格：進風口、熱點、工作區、收納點。每一件小家電都要能回答自己屬於哪一格，才值得進入購物清單。", "如果答案只是看起來會更舒服，先量尺寸、看插座、確認清潔方式，再回到商品頁查看規格、價格、活動與庫存。"),
        ],
        "faq": [
            ("循環扇要放在哪裡？", "先找進風口與悶熱點，再決定角度。不要只依商品照片判斷，還要看插座、走道與家具遮擋。"),
            ("夏季小家電可以改善室內溫度嗎？", "本文不宣稱降溫或節電效果。小家電選購應回到商品標示、使用條件與實際空間。"),
            ("照明和風扇需要一起規劃嗎？", "需要。小宅常會共用同一個角落，若不一起看，容易發生走線混亂或使用動線卡住。"),
        ],
    },
    "day-trip-bag-sun-charging-earplug-rainwear-checklist": {
        "heroAlt": "海邊一日輕旅行長椅上，無品牌小包、防曬用品、行動電源、耳塞盒、雨衣與折傘整齊排列",
        "audience": "需要替一日旅行、城市短程出遊與週末移動整理包內順序的讀者",
        "excerpt": "一日旅行的採買順序是防曬與電力先行，再補睡眠、雨天備案與小包位置，包內不要只靠直覺亂塞。",
        "tags": ["一日旅行", "戶外小包", "防曬", "旅行充電"],
        "intro": "一日輕旅行看似簡單，實際上最容易發生的是小東西太多、真正要用的卻在包底。防曬、充電、耳塞、雨具與小包各自解決不同時刻的麻煩，不能只用『有帶就好』來判斷。本文用拿取頻率、天氣變化與回程疲勞三個角度，整理一個不把包塞滿也能安心出門的清單。",
        "editorialAngle": "用拿取頻率決定包內位置，雨具與充電不要放在最深處。",
        "sections": [
            ("先決定這趟旅程有幾次拿取", "從出門到回家，你會拿幾次手機、補幾次防曬、需要幾次付款或交通卡、雨具會不會中途拿出來。拿取次數越高的物品越要靠近外層，不要被漂亮收納袋藏到最深。", "S′AIME、Momax Taiwan 與耳根清靜分別適合放在小包、電力與安靜休息情境中比較；商品規格與相容性仍需回商品頁確認。"),
            ("防曬和電力先行，因為它們最難臨時補救", "一日旅行遇到日曬或手機沒電，通常比少帶一件小物更麻煩。防曬用品、遮陽外套、行動電源和充電線應該比零食或拍照小物更早被確認。", "UV100、FULTON 與 UD LAB 可作為防曬、雨具與包款備案參考；本文不保證任何商品適合所有天候或交通限制。"),
            ("耳塞不是只為睡覺，也為回程留空間", "短程旅行也可能遇到車廂噪音、午休、展演或人潮。耳塞或安靜小物不一定每次都用，但體積小、影響大，適合放在固定小盒中。", "涉及配戴感、材質與隔音表現，請以商品頁標示和個人感受為準，不寫成保證效果。"),
            ("雨具要能快速拿，不要和電子用品混放", "折傘、雨衣或防水袋若放在包底，下雨時會先把整個包翻亂。雨具應有獨立位置，且避免和行動電源、線材、文件直接混在一起。", "如果包款本身沒有濕物分層，可以另外準備薄袋；但材質、防水、防潑或耐用描述仍要看商品頁。"),
            ("常見錯誤：把一日旅行當成小型搬家", "只要想到可能用到就放進包裡，最後會讓肩膀和動線都變沉。真正成熟的清單，是每件物品都知道它會在什麼時刻被拿出來。", "若同一物品連續三次都沒用到，下一次可以降級成備案，不必固定佔據包內主位。"),
            ("出門前的十秒順序", "先確認手機電量與行動電源，再確認防曬與雨具，最後檢查耳塞、小包、票卡和必要藥品。這個順序比出門前重新翻整整包更穩。", "價格、庫存、規格、活動與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("一日旅行一定要帶行動電源嗎？", "如果會長時間導航、拍照或使用行動支付，建議優先確認電力備案。相容性與容量限制請看商品頁。"),
            ("雨具應該放在哪裡？", "放在包外層或獨立袋中，避免和電子用品直接混放。"),
            ("防曬用品可以只看係數嗎？", "不建議。還要看使用情境、衣物遮蔽、補擦方便度與商品標示。"),
        ],
    },
    "after-work-home-scent-light-storage-upgrade-order": {
        "heroAlt": "下班後的現代客廳，溫暖桌燈、無字香氛陶器、收納盒、托盤與折疊毯安靜擺放",
        "audience": "想用收納、燈光與香氛整理下班後居家節奏的讀者",
        "excerpt": "下班後的居家升級應從收納與光線開始，香氛只負責最後一層情緒，不該拿來掩蓋混亂。",
        "tags": ["居家儀式", "香氛", "照明", "收納"],
        "intro": "下班後的家要安靜，不是先點香氛或買一盞新燈，而是先讓視線裡的雜物有地方回去。香氛、燈光與收納都能讓空間變得舒服，但它們的順序不能顛倒：先收掉視覺噪音，再調低光線，最後才讓氣味成為一層很輕的收尾。",
        "editorialAngle": "先收掉視覺噪音，再談光線與味道，家才會真正安靜。",
        "sections": [
            ("第一步不是香味，是把入口收乾淨", "下班進門後最先看到的包、鑰匙、外套、信件和購物袋，會決定家裡的第一個情緒。若玄關或邊桌沒有托盤和暫放位置，再好的香氛也只是蓋在混亂上。", "完美主義、燈后與 THANN 可放在收納、照明與氣味三個不同層次裡比較，不必把它們當成同一種問題的答案。"),
            ("光線要先讓身體知道工作結束", "下班後若仍使用刺眼白光，家很難安靜下來。桌燈、間接光或低亮度角落燈，可以先替客廳和臥室切出不同節奏。", "燈具選擇要看插座、亮度、色溫與位置，不宣稱任何光線能帶來心理或健康效果。"),
            ("香氛放在最後，只做空間句點", "香氛最適合放在整理、通風和清潔之後。若空間濕、雜物多或布品未清，味道容易變複雜，也更難維持。", "灰調、au fait 無非、蒔柒和 THANN 都可作為氣味選物參考；但本文不宣稱療癒、淨化、助眠或情緒改善效果。"),
            ("收納不是把東西藏起來，而是降低明天的阻力", "收納盒、托盤或邊櫃的價值，是讓明天早上不用重新找鑰匙、文件、充電器和常用小物。只把東西塞進盒子，沒有分類和回收位置，隔天仍會亂。", "下單前先量尺寸，確認放置位置、開合方式與清潔材質。"),
            ("常見錯誤：一次買滿儀式感", "香氛、燈、花器、毯子、收納盒同時進家，很容易讓空間看起來更滿。比較好的做法，是每週只處理一個角落，讓物件有時間被生活驗證。", "如果一件用品沒有固定使用時刻，先不要讓它佔據最顯眼的位置。"),
            ("下班後的三分鐘收尾", "鑰匙進托盤、包回固定處、主燈換成低光、窗邊通風三分鐘。完成這些再點香氛或開小燈，居家儀式才不會變成表演。", "所有價格、活動、規格、香味描述與庫存請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("下班後居家升級應先買香氛嗎？", "不建議作為第一步。先處理玄關、桌面與光線，再考慮香氛會更穩。"),
            ("燈光可以改善睡眠或情緒嗎？", "本文不做健康或心理效果宣稱，只從生活節奏與視覺舒適度討論。"),
            ("收納盒要怎麼選？", "先量使用位置，再看開合方式、材質與是否容易清潔，不要只看照片風格。"),
        ],
    },
    "second-monitor-laptop-stand-backup-work-setup": {
        "heroAlt": "明亮工作桌上，無品牌外接螢幕、筆電支架、備份硬碟、線材整理與桌燈形成高效率配置",
        "audience": "需要替居家辦公、顧問工作或創作流程配置第二螢幕與備份的人",
        "excerpt": "第二螢幕的價值在於工作動線，不是單純追求大尺寸；先看視窗數量、攜帶需求與資料備份。",
        "tags": ["第二螢幕", "筆電支架", "資料備份", "工作桌配置"],
        "intro": "第二螢幕常被當成提升效率的捷徑，但如果沒有先想清楚工作視窗、筆電高度、線材和資料備份，它很可能只是桌上更大的壓迫感。真正好的配置，是讓你少切換、少低頭、少找檔案，而不是把螢幕尺寸當成唯一答案。",
        "editorialAngle": "先看工作視窗數量與攜帶需求，再談螢幕尺寸與筆電規格。",
        "sections": [
            ("先數你每天真正會開幾個視窗", "如果你的工作只是單一文件與瀏覽器，第二螢幕未必需要很大；若是簡報、資料表、通訊軟體、研究頁面同時開啟，螢幕尺寸與比例才會明顯影響效率。", "REAICE、華克電腦與日本橋3C 可放在外接螢幕、筆電與周邊整合中比較；本文不捏造效能測試或相容性。"),
            ("筆電高度比很多人想得更重要", "第二螢幕放得再好，如果筆電仍然太低，肩頸和視線會被迫一直切換。支架、外接鍵盤與滑鼠的位置，應該和螢幕一起規劃。", "聯威電腦、Momax Taiwan 與 EZstick 可作為周邊、保護與線材補充參考；尺寸與相容性要回商品頁確認。"),
            ("備份不是最後才想的配件", "工作桌升級很容易先看螢幕和支架，卻忘了資料備份。外接硬碟、雲端流程、線材與固定備份時間，才是讓工作配置不只好看而且可靠的關鍵。", "任何容量、速度、保固和相容資訊都應以商品頁與官方說明為準。"),
            ("線材要在購買前就畫進配置", "螢幕、筆電、充電器、硬碟、鍵盤、滑鼠都需要線材或接收器。若沒有先安排走線，桌面很快會變成每天都要整理的地方。", "下單前先確認接口、線長、桌洞、插座與轉接需求，不要等商品到貨才發現缺少關鍵線材。"),
            ("常見錯誤：把規格當成效率", "更大的螢幕、更高的解析度或更強的筆電，不一定會讓工作更順。若流程本身混亂，規格只會讓混亂變得更寬。", "先列出每天最常切換的三個任務，再決定第二螢幕是否值得升級。"),
            ("下單前的工作桌檢查", "確認螢幕寬度、筆電高度、桌深、眼睛距離、資料備份位置和線材方向。這六件事比單看商品照更能決定是否會長期使用。", "價格、規格、活動、保固、相容性與庫存請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("第二螢幕越大越好嗎？", "不一定。要看桌深、視距、視窗數量與攜帶需求。過大反而可能壓縮桌面。"),
            ("筆電支架一定要買嗎？", "如果你長時間使用筆電螢幕，支架和外接鍵鼠通常更有利於視線安排；仍需看桌面空間。"),
            ("資料備份要和螢幕一起規劃嗎？", "建議一起規劃。工作配置若沒有備份和線材安排，容易只完成表面升級。"),
        ],
    },
    "office-afternoon-drinks-tea-sparkling-pantry-guide": {
        "heroAlt": "辦公室茶水間午後光線下，無標籤茶壺、玻璃氣泡水、空白紙盒飲品、茶包與杯具整齊排列",
        "audience": "需要替辦公室、共享茶水間或下午補給建立飲品順序的人",
        "excerpt": "辦公室飲品應以保存方式、糖度與共享便利性決定，無糖茶、氣泡飲與沖泡飲不要全部混在一起補。",
        "tags": ["辦公室飲品", "無糖茶", "氣泡飲", "下午茶補給"],
        "intro": "下午三點喝什麼，表面上是口味選擇，實際上是保存、共享和節奏管理。無糖茶、花草茶、氣泡飲、植物奶或沖泡飲都有不同保存方式與使用門檻；如果只照喜好補貨，茶水間很快會變成過期、重複和沒人想開封的集合。",
        "editorialAngle": "把飲品分成日常、共享、送禮與加班四種情境。",
        "sections": [
            ("先分日常飲、共享飲與備用飲", "每天會喝的飲品要穩定、保存簡單；共享飲要容易開封、份量清楚；備用飲則適合放在加班或臨時來客時使用。三者混在一起，就會很難判斷何時補貨。", "Teavoya、ACE TEA 與 KKM 可放在茶、冷泡或辦公室飲品補給中比較；食品與飲品資訊請以商品頁和包裝標示為準。"),
            ("糖度和咖啡因比包裝更重要", "辦公室飲品若要共享，糖度、咖啡因、沖泡方式和保存期限都比包裝風格更實際。有人需要無糖，有人想要氣泡，有人只需要熱水可沖。", "PV女性微甜草本飲、恩亞生活與 Zymoide 這類飲品店家可作為不同風味與補給參考；不得宣稱保健、代謝或療效。"),
            ("茶包、瓶裝與紙盒飲的收納要分開", "茶包怕濕，瓶裝怕重，紙盒飲要看開封後保存。若全部放在同一層，最容易發生的是快到期的看不見、已開封的被忘記。", "建議把飲品分成未開封、已開封、共享、個人四格，補貨時會清楚很多。"),
            ("送禮飲品要看對方是否會沖泡", "茶禮盒、植物奶或沖泡飲都可能很體面，但如果對方沒有沖泡習慣或保存空間，再漂亮也會增加負擔。送禮時應優先看份量、保存期限和使用門檻。", "若是辦公室共享，單份包裝通常比大包裝更容易被使用完。"),
            ("常見錯誤：把健康想像寫進飲品", "飲品可以是下午的停頓，但不應被寫成健康捷徑。無糖、草本、酵素、植物奶等字眼，都需要回到商品標示和個人飲食需求。", "本文只提供辦公室補給與收納順序，不構成營養、健康或個人化飲食建議。"),
            ("補貨前的三個問題", "誰會喝、多久喝完、開封後放哪裡。這三個答案比一次買齊更多口味更重要。", "價格、活動、庫存、成分、保存方式與配送請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("辦公室飲品應該買無糖嗎？", "若是共享，無糖通常較有彈性，但仍要看同事需求、咖啡因和保存方式。"),
            ("草本飲或酵素飲可以寫保健效果嗎？", "不可以。本文不宣稱保健、代謝、療效或改善效果，請以商品標示為準。"),
            ("下午飲品怎麼避免買太多？", "先分日常、共享、備用三類，設定兩週到一個月的補貨量，再看保存期限。"),
        ],
    },
}


def load_tracker() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], list[str]]:
    with TRACKER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return rows, {row["merchant_id"]: row for row in rows}, reader.fieldnames or []


def load_matrix_rows() -> list[dict[str, str]]:
    with MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[5:10]


def affiliate_url(row: dict[str, str]) -> str:
    return row.get("promo_link", "").strip() or row.get("store_link", "").strip()


def merchant_card(row: dict[str, str], slug: str) -> dict[str, str]:
    brand = row["brand"].strip()
    reason = row.get("content_angles", "").strip() or row.get("main_products", "").strip() or "可依商品頁資訊與實際使用情境比較。"
    return {
        "name": f"{brand} 選物頁",
        "merchantId": row["merchant_id"],
        "brandName": brand,
        "affiliateUrl": affiliate_url(row),
        "sourceProductUrl": row.get("store_link", "").strip() or f"https://www.momoshop.com.tw/TP/{row['merchant_id']}/main",
        "imageCredit": f"圖片來源：momo 店家頁｜{brand}",
        "selectionReason": f"{reason.rstrip('。')}。下單前請回到商品頁確認尺寸、材質、規格、活動與即時販售資訊。",
        "riskNote": "價格、規格、活動、庫存與配送條件請以下單前商品頁公告為準。",
        "subId": f"{slug}_{row['merchant_id']}",
    }


def prepare_cover(slug: str, hero_alt: str) -> str:
    source = Path(COVER_SOURCES[slug])
    if not source.exists():
        raise FileNotFoundError(f"Missing Codex generated cover source for {slug}: {source}")
    target = ROOT / "images" / "optimized" / "article-covers" / f"{slug}.jpg"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-vf",
            "scale=1200:630:force_original_aspect_ratio=increase,crop=1200:630",
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(target),
        ],
        check=True,
    )
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    manifest = json.loads(COVER_MANIFEST.read_text(encoding="utf-8")) if COVER_MANIFEST.exists() else {"version": 1, "covers": {}}
    manifest["updatedAt"] = pipeline.now_iso()
    manifest["generator"] = "codex-image-gen-editorial-no-logo"
    manifest.setdefault("covers", {})[slug] = {
        "provider": "codex-imagegen",
        "image": pipeline.relative_to_root(target),
        "output": pipeline.relative_to_root(target),
        "source": str(source),
        "sourceImage": str(source),
        "sha256": digest,
        "generatedAt": pipeline.now_iso(),
        "usage": "cover-og-twitter",
        "promptSummary": hero_alt,
        "review": "Manual visual check passed: no visible trademark logo, brand wordmark, watermark, readable text, or product label.",
    }
    pipeline.write_json(COVER_MANIFEST, manifest)
    return f"/images/optimized/article-covers/{slug}.jpg"


def build_sections(blueprint: dict[str, Any], matrix_row: dict[str, str], brand_names: list[str]) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for heading, p1, p2 in blueprint["sections"]:
        sections.append(
            {
                "heading": heading,
                "paragraphs": [
                    p1,
                    p2,
                    f"Elite Fashion 編輯團隊的具體判斷是：{matrix_row['elite_judgment']} 這讓 {brand_names[0]}、{brand_names[1]} 與其他選項能被放回同一個生活問題裡比較，而不是只看單一商品照片。",
                    f"下單前仍要回商品頁確認規格、尺寸、材質、活動、庫存與配送；若資訊不足，先暫緩，比把不確定的物品帶回家更成熟。",
                ],
                "bullets": [
                    "先確認使用位置與拿取頻率。",
                    "再看保存、清潔、線材或收納條件。",
                    "最後才比較品牌、活動與預算。",
                ],
            }
        )
    return sections


def build_article(matrix_row: dict[str, str], rows_by_merchant: dict[str, dict[str, str]], config: dict[str, Any], categories: dict[str, pipeline.CategoryConfig]) -> dict[str, Any]:
    slug = matrix_row["slug"]
    blueprint = BLUEPRINTS[slug]
    topic_hub = TOPIC_HUBS[slug]
    merchant_ids = [*matrix_row["primary_merchant_ids"].split(";"), *matrix_row["supporting_merchant_ids"].split(";")]
    merchant_rows = [rows_by_merchant[mid] for mid in merchant_ids]
    cards = [merchant_card(row, slug) for row in merchant_rows]
    brand_names = [row["brand"] for row in merchant_rows]
    category = categories[matrix_row["category"]]
    article = {
        "slug": slug,
        "category": matrix_row["category"],
        **topic_hub,
        "title": matrix_row["title"],
        "excerpt": blueprint["excerpt"],
        "tags": blueprint["tags"],
        "metaTitle": f"Elite Fashion｜{matrix_row['title']}",
        "metaDescription": f"{blueprint['excerpt']} 本文整理選購順序、常見錯誤與下單前確認重點。",
        "series": "城市生活選物",
        "listingTitle": matrix_row["title"],
        "listingExcerpt": blueprint["excerpt"],
        "heroImage": prepare_cover(slug, blueprint["heroAlt"]),
        "heroImageAlt": blueprint["heroAlt"],
        "coverImageStatus": "codex-generated",
        "intro": blueprint["intro"],
        "sections": build_sections(blueprint, matrix_row, brand_names),
        "faq": [{"question": q, "answer": a} for q, a in blueprint["faq"]],
        "extendedReading": [
            {"title": f"瀏覽更多{category.label}文章", "url": f"/{category.page}"},
            {"title": "瀏覽所有文章", "url": "/all-articles.html"},
            {"title": "查看站內搜尋", "url": "/search.html"},
        ],
        "cta": {
            "variant": "olive",
            "text": f"{matrix_row['answer_summary']} 先用本文順序縮小範圍，再回商品頁確認規格、價格、活動與庫存。",
            "links": [{"label": f"查看 {row['brand']}", "url": affiliate_url(row)} for row in merchant_rows[:4]],
        },
        "inlineCtas": [
            {
                "afterSection": 2,
                "variant": "gold",
                "eyebrow": "編輯精選",
                "heading": "先把最常發生的情境排出來",
                "text": blueprint["editorialAngle"],
                "links": [
                    {"label": cards[0]["name"], "url": cards[0]["affiliateUrl"]},
                    {"label": cards[1]["name"], "url": cards[1]["affiliateUrl"]},
                ],
            },
            {
                "afterSection": 4,
                "variant": "olive",
                "eyebrow": "下單前確認",
                "heading": "商品頁資訊是最後一道檢查",
                "text": matrix_row["risk_guardrail"],
                "links": [
                    {"label": cards[2]["name"], "url": cards[2]["affiliateUrl"]},
                    {"label": cards[3]["name"], "url": cards[3]["affiliateUrl"]},
                ],
            },
        ],
        "disclaimer": f"本文含品牌／商品導購連結；商品資訊、價格、規格、活動與庫存請以商品頁公告為準。{matrix_row['risk_guardrail']}",
        "audience": blueprint["audience"],
        "readTimeMinutes": 10,
        "sourceType": TRIGGER_TYPE,
        "status": "published",
        "queueId": QUEUE_ID,
        "mainProducts": cards[:4],
        "sidebarProducts": cards[4:],
        "featuredBrands": [
            {
                "name": row["brand"],
                "merchantId": row["merchant_id"],
                "role": "情境比較",
                "reason": row.get("content_angles") or row.get("main_products") or "可依商品頁資訊與使用情境比較。",
                "url": affiliate_url(row),
            }
            for row in merchant_rows
        ],
    }
    saved = pipeline.save_generated_article(article, QUEUE_ID, config, categories)
    pipeline.validate_generated_article(saved, config)
    saved["authenticityReview"] = pipeline.run_authenticity_review(saved, config)
    pipeline.write_json(ROOT / config["paths"]["generatedArticlesDir"] / f"{saved['slug']}.json", saved)
    pipeline.write_text(ROOT / config["paths"]["generatedArticlesDir"] / f"{saved['slug']}.md", saved["markdownBody"])
    pipeline.append_publish_log(config, saved, trigger_type=TRIGGER_TYPE, queue_id=QUEUE_ID)
    return saved


def reset_existing_batch_records(config: dict[str, Any]) -> None:
    slugs = set(BLUEPRINTS)
    publish_log_path = ROOT / config["paths"]["publishLogJson"]
    publish_log = pipeline.load_json(publish_log_path, default={"version": 1, "entries": []})
    publish_log["entries"] = [
        entry
        for entry in publish_log.get("entries", [])
        if entry.get("queueId") != QUEUE_ID and Path(str(entry.get("file", ""))).stem not in slugs
    ]
    publish_log["updatedAt"] = pipeline.now_iso()
    pipeline.write_json(publish_log_path, publish_log)

    authenticity_log_path = ROOT / "automation" / "content-authenticity-log.json"
    authenticity_log = pipeline.load_json(authenticity_log_path, default={"version": 1, "entries": []})
    authenticity_log["entries"] = [
        entry
        for entry in authenticity_log.get("entries", [])
        if entry.get("slug") not in slugs and not any(str(entry.get("articleId", "")).endswith(f"-{slug}") for slug in slugs)
    ]
    authenticity_log["updatedAt"] = pipeline.now_iso()
    pipeline.write_json(authenticity_log_path, authenticity_log)


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
        row["last_mentioned_at"] = TODAY
        note = "2026-06-21 momo 收益型內容第二組 5 篇已置入。"
        if note not in row.get("notes", ""):
            row["notes"] = (row.get("notes", "").rstrip() + (" " if row.get("notes", "").strip() else "") + note).strip()
    with TRACKER_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(tracker_rows)


def update_latest_run(config: dict[str, Any], articles: list[dict[str, Any]]) -> None:
    pipeline.write_json(
        ROOT / config["paths"]["latestRunJson"],
        {
            "version": 1,
            "updatedAt": pipeline.now_iso(),
            "status": "generated",
            "triggerType": TRIGGER_TYPE,
            "queueId": QUEUE_ID,
            "newsletter": "not_sent_manual_codex_publish",
            "articleIds": [article["id"] for article in articles],
            "articleSlugs": [article["slug"] for article in articles],
            "notes": "Codex 手動生成 momo 收益型內容第二組；直接推上 main 不會自動寄送電子報。",
        },
    )


def main() -> int:
    config, categories = pipeline.load_config()
    tracker_rows, rows_by_merchant, fieldnames = load_tracker()
    matrix_rows = load_matrix_rows()
    expected_slugs = set(BLUEPRINTS)
    found_slugs = {row["slug"] for row in matrix_rows}
    if found_slugs != expected_slugs:
        raise SystemExit(f"Matrix rows mismatch: expected {sorted(expected_slugs)}, found {sorted(found_slugs)}")
    for row in matrix_rows:
        ids = [*row["primary_merchant_ids"].split(";"), *row["supporting_merchant_ids"].split(";")]
        for merchant_id in ids:
            tracker_row = rows_by_merchant.get(merchant_id)
            if not tracker_row or not affiliate_url(tracker_row):
                raise SystemExit(f"Unavailable merchant for {row['slug']}: {merchant_id}")
        if not Path(COVER_SOURCES[row["slug"]]).exists():
            raise SystemExit(f"Missing Codex image source for {row['slug']}")
    reset_existing_batch_records(config)
    articles = [build_article(row, rows_by_merchant, config, categories) for row in matrix_rows]
    update_tracker(articles, tracker_rows, fieldnames)
    update_latest_run(config, articles)
    pipeline.rebuild_outputs(config, categories)
    pipeline.verify_outputs(config, categories)
    print(f"Generated {len(articles)} momo revenue growth articles:")
    for article in articles:
        print(f"- {article['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
