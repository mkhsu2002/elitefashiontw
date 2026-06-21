#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import math
import struct
import sys
import zlib
from collections import defaultdict
from pathlib import Path
from typing import Any

import content_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[1]
MATRIX_CSV = ROOT / "automation" / "reports" / "momo-affiliate-revenue-growth-matrix-2026-06-21.csv"
TRACKER_CSV = ROOT / "automation" / "momo-brand-recommendation-tracker.csv"
COVER_MANIFEST = ROOT / "automation" / "codex-generated-cover-manifest.json"
TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-one-no-newsletter"
QUEUE_ID = "MOMO-REV-2026-06-21-W01"
TODAY = "2026-06-21"


BLUEPRINTS: dict[str, dict[str, Any]] = {
    "commute-bag-size-strap-formality-rain-backup": {
        "heroAlt": "明亮通勤玄關中，一只結構俐落的肩背包、雨傘、筆記本與輕外套放在木質長凳旁",
        "coverTheme": "bag",
        "audience": "需要在通勤、會議與雨天之間保持俐落的城市工作者",
        "excerpt": "通勤包的價值不在容量最大，而在每天真正會帶什麼、肩帶是否舒服，以及進會議室時是否仍然得體。",
        "tags": ["通勤包", "雨天上班", "包款選購", "城市穿搭"],
        "intro": "一只通勤包如果只用容量判斷，很容易買到看似萬用、實際每天都讓肩膀疲憊的選項。真正會被長期留下的包，通常能在筆電、雨具、補妝小物與會議文件之間取得安靜的平衡。本文用容量、肩帶、正式感與雨天備案建立順序，讓包款選擇回到日常動線，而不是被外型或品牌名牽著走。",
        "editorialAngle": "先用每天一定會帶的三件物品決定基本容量，再用肩帶、開口與場合決定外型。",
        "sections": [
            ("先用每天必帶物決定容量", "通勤包不是旅行箱。每天真正會進包裡的物品，通常只有手機、錢包、鑰匙、耳機、補妝小物、文件或筆電其中幾項。先把必帶物放在桌上，比直接看商品頁容量更準。", "若你每天需要帶筆電，包身穩定度、底部支撐與肩帶寬度比多一個外袋更重要；若你主要搭捷運，開口安全與單手拿取會比超大容量更常被使用。"),
            ("肩帶與重量比尺寸更影響使用意願", "很多包買回來不用，不是因為不好看，而是裝滿後肩帶太細、包身太晃、或背起來讓外套變形。通勤包要先看肩帶與身體接觸的位置，再看它能裝多少。", "S′AIME 東京企劃、UD LAB 與 Heine 海恩後背包可分別放在正式感、小包機動與後背承重的不同位置比較；它們不是互相取代，而是對應不同移動方式。"),
            ("正式感來自線條，不一定來自黑色", "會議日需要的不是過度嚴肅，而是包款線條不要讓整體看起來臨時。包身太軟、裝滿後變形、肩帶五金太搶眼，都可能讓通勤穿搭失去乾淨度。", "若工作場合需要見客戶，建議先選輪廓清楚、開口好整理、顏色能和外套銜接的款式；若只是日常辦公，材質耐看與拿取便利會更重要。"),
            ("雨天備案要先想收納，而不是只想防水", "雨天包款最大的麻煩常常不是濕，而是傘、雨衣與文件混在一起。包內若沒有分層，防雨材質也只能解決一半問題。", "FULTON、KANGOL 或 Mister 手作皮件這類補充品牌，可以放在雨具、休閒風格與送禮情境裡比較；下單前仍要回商品頁確認材質、尺寸與保養限制。"),
            ("常見錯誤：把所有場合塞進同一只包", "一只包不必同時負責電腦包、旅行包、健身包與正式會議包。越想萬用，越容易在每天使用時顯得笨重。", "比較成熟的做法，是保留一只主要通勤包，再補一個雨天或一日外出的輕量備案；這樣比買一只過大的包更容易維持穿搭比例。"),
            ("下單前的三個確認", "確認最大物件能否平放、確認肩帶寬度與重量感、確認雨天物件是否有獨立位置。這三件事比單純看商品照更能決定是否會長期使用。", "本文含導購連結，但不宣稱任何包款一定耐用、防水或適合所有身形；價格、庫存、活動與規格請以下單前商品頁公告為準。"),
        ],
        "faq": [
            ("通勤包容量要怎麼估？", "先把每天一定會帶的物品列出來，再加上一個雨天或會議日的備案空間。若不是每天帶筆電，不必直接選最大容量。"),
            ("通勤包應該選肩背還是後背？", "若需要正式感與快速拿取，肩背包通常更俐落；若每天帶筆電或移動距離長，後背包能分散重量。"),
            ("雨天需要另外買包嗎？", "不一定。先確認現有通勤包是否能分開放濕傘、雨衣與文件；如果不能，再考慮輕量備案包或防雨材質。"),
        ],
    },
    "rainy-commute-umbrella-rain-shoes-bag-materials": {
        "heroAlt": "城市雨天玄關裡整齊放著抗風傘、雨鞋、防雨外套與深色通勤包",
        "coverTheme": "rain",
        "audience": "需要在梅雨、機車通勤與辦公室形象之間取得平衡的讀者",
        "excerpt": "雨天上班的關鍵不是買最多雨具，而是把抵達前、進門後與收納時的狼狽感降到最低。",
        "tags": ["雨天通勤", "抗風傘", "雨鞋", "上班穿搭"],
        "intro": "雨天上班最難的不是淋濕，而是從出門到進辦公室的每一步都變得不安定：傘滴水、鞋面濕、包身沾雨、外套找不到地方放。好的雨天配置，不是把自己包成戶外裝備，而是讓抗風傘、雨鞋、雨衣與包款材質各自負責一段動線。",
        "editorialAngle": "把雨天拆成抵達前、進門後、收納時三段，才能判斷哪一件雨具真正值得買。",
        "sections": [
            ("第一段：從家門到交通工具", "出門前的雨具要先解決雙手與視線。抗風傘、雨衣或防雨外套的選擇，取決於你是走路、搭捷運、騎機車，還是需要轉乘。", "OMBRA、FULTON 與左都雨傘適合放在不同雨勢與通勤方式裡比較；傘面、收傘長度、重量與握把都會影響每天是否願意帶。"),
            ("第二段：抵達辦公室前的鞋與包", "雨鞋與包款材質不是越厚越好。鞋子要看進辦公室後是否能自然銜接服裝，包則要看被雨沾到後是否容易擦拭、是否會讓文件與電子用品受影響。", "UD LAB 與 S′AIME 東京企劃可作為輕量包與正式包的兩種方向；如果你的工作需要開會，包身輪廓與材質安靜度仍然重要。"),
            ("第三段：濕物進門後放在哪裡", "很多雨天採買失敗，是因為只買了雨具，卻沒有想濕傘、雨衣與鞋套進門後要去哪。玄關或辦公桌下若沒有收納位置，再好的雨具都會變成狼狽來源。", "建議替折傘、長傘、雨衣或防雨外套預留固定位置；若需要放進包裡，請另外準備防水袋或可擦拭隔層。"),
            ("正式感不是不能穿雨具", "真正成熟的雨天穿搭，不是完全看不出雨具，而是雨具不要打斷整體線條。深色雨鞋、收束感好的外套、簡潔傘面，都比亮眼但難搭的單品更容易留下。", "如果你常在雨天見客戶或進會議室，建議優先選能和外套、長褲或裙裝銜接的款式，不要只看社群照片的即時吸引力。"),
            ("常見錯誤：只買傘，沒有買收尾", "只買一把好傘，卻沒有處理鞋、包與濕物收納，雨天仍然會失控。雨天通勤是系統，不是單品。", "下單前可以問自己：這件物品濕了以後放哪裡？回家後怎麼晾？進辦公室會不會太突兀？如果答不出來，先不要急著買。"),
            ("商品資訊與安全邊界", "雨具的防水、抗風、防滑與材質表現都應回到商品頁確認。本文只提供通勤情境與選購順序，不保證任何商品能應對所有天候或路況。", "若涉及機車、夜間或濕滑路面，請以安全為優先，必要時搭配反光配件、合適鞋底與官方交通規範。"),
        ],
        "faq": [
            ("抗風傘一定比一般傘好嗎？", "不一定。要看你所在城市風勢、通勤距離、收傘後長度與重量。每天願意帶出門，比規格看起來很強更重要。"),
            ("雨鞋可以穿進辦公室嗎？", "可以，但要看鞋型、顏色與工作場合。若辦公室正式度高，可以選低調輪廓或準備替換鞋。"),
            ("包包需要防水材質嗎？", "若常遇雨或需要帶電子用品，可優先看可擦拭材質與分層；但仍要以商品頁標示為準，不自行假設防水效果。"),
        ],
    },
    "phone-accessory-car-desk-charging-magsafe-system": {
        "heroAlt": "整潔工作桌與車用收納盤上放著手機支架、充電線、磁吸配件與耳機",
        "coverTheme": "phone",
        "audience": "想把手機配件從零散小物整理成通勤、車用與桌面系統的讀者",
        "excerpt": "手機配件不該只看保護殼外觀，車用、桌面、充電與外出收納各自有不同判斷順序。",
        "tags": ["手機配件", "MagSafe", "車用手機架", "桌面充電"],
        "intro": "手機早已不是只需要一個保護殼的物件。它在車上負責導航，在桌上負責會議與訊息，在外出時又牽涉充電、收納與拍攝。若配件只靠一時喜歡買，很快就會變成抽屜裡一團線材。本文把手機配件拆成車用、桌面、充電與外出四個場景，讓每一件小物都有明確位置。",
        "editorialAngle": "先區分車上、辦公桌、旅行三個場景，再決定是否需要同一品牌系統。",
        "sections": [
            ("車用配件先看固定與視線", "車用手機架或車充不能只看外型，最重要的是固定位置是否干擾視線、拿取是否安全、線材是否會影響駕駛動線。", "手些小子3C、TG3C 與 Momax Taiwan 可放在 Apple 周邊、手機配件與充電系統的不同方向比較；下單前請回商品頁確認相容性與安裝限制。"),
            ("桌面配件要讓手機回到固定位置", "桌面支架、充電座與磁吸配件的價值，是讓手機不要在桌面四處漂移。若你常開視訊會議或用手機看資料，支架高度與線材方向會比外觀更影響效率。", "muni 與 AiHome 這類配件店家適合補平板、手機與智慧充電情境；但任何充電速度、認證與支援型號都不能靠文章推測。"),
            ("充電系統不要混成一團", "最容易造成配件浪費的，是家裡、辦公室、車上與旅行用線材全部混用。比較好的做法，是替每個地點留固定組合：一條主要線、一個固定充電頭、一個外出備用。", "如果你已經有 MagSafe 或磁吸系統，新增配件時要確認殼、支架與充電器之間是否相容，不要只看單一商品照。"),
            ("外出收納重點是少而可替換", "通勤包裡不需要塞滿所有線材。真正會用到的是短線、行動電源、耳機或轉接頭其中幾項，且最好能用小袋集中。", "GoRig 或其他拍攝支架品牌可以放在內容創作情境裡比較，但日常通勤不一定需要完整拍攝配件。先分出工作、車用、拍攝與旅行，再決定是否購買。"),
            ("常見錯誤：每看到新規格就補一件", "手機配件更新快，但不代表每個新規格都會讓生活更順。若舊配件還能穩定完成任務，新配件應該補的是缺口，而不是替代焦慮。", "下單前先問：這件配件會固定放在哪？解決哪一個每天出現的麻煩？若答案只是『看起來方便』，可以先放進待比較清單。"),
            ("安全與規格回商品頁確認", "充電器、線材、車用配件、磁吸配件與支架都牽涉相容性與安全限制。本文只提供使用情境與整理順序，不宣稱充電速度、認證、散熱或支援型號。", "所有規格、價格、活動與庫存，請以下單前商品頁公告為準；車用配件使用時也應遵守交通安全規範。"),
        ],
        "faq": [
            ("手機配件要買同一品牌嗎？", "不一定。同一系統有整齊感，但更重要的是相容性、固定位置與日常使用頻率。"),
            ("車用手機架怎麼挑？", "先看是否影響視線與操作安全，再看固定方式、手機尺寸與車內空間。安裝限制請回商品頁確認。"),
            ("MagSafe 配件一定比較方便嗎？", "若你的手機殼、充電器與支架相容，磁吸系統會更順；若不相容，反而容易造成重複購買。"),
        ],
    },
    "office-coffee-beans-drip-bag-gift-box-guide": {
        "heroAlt": "辦公室茶水角落中擺放咖啡豆、濾掛包、掛耳包、馬克杯與簡潔禮盒",
        "coverTheme": "coffee",
        "audience": "需要替辦公室、會議或送禮情境建立咖啡補給的人",
        "excerpt": "辦公室咖啡補給先看沖泡門檻、保存方式與共享情境，再決定咖啡豆、濾掛、掛耳包或禮盒。",
        "tags": ["辦公室咖啡", "濾掛咖啡", "咖啡禮盒", "下午茶"],
        "intro": "辦公室咖啡不只是提神工具，它常常是會議前的停頓、下午三點的重整，也是送禮時不過度親密又不失禮的選項。真正好用的咖啡補給，不一定是最講究的器材，而是能符合辦公室沖泡條件、保存方式與共享頻率。本文用咖啡豆、濾掛、掛耳包與禮盒四個方向，整理出不容易浪費的採買順序。",
        "editorialAngle": "先看沖泡條件與共用情境，再決定豆、濾掛或禮盒。",
        "sections": [
            ("先看辦公室有沒有沖泡條件", "如果辦公室沒有磨豆機、手沖壺或穩定清洗空間，咖啡豆再好也可能變成擺設。濾掛與掛耳包的優勢，是讓每個人都能用低門檻完成一杯。", "歐力咖啡、Xinto Coffee 與馬克老爹可以分別放在日常補給、風味辨識與禮盒情境裡比較；但本文不替任何風味排名背書。"),
            ("共享情境比個人口味更重要", "替辦公室買咖啡，不能只看自己的喜好。酸度、焙度、包裝份量、保存方式，都會影響同事是否願意使用。", "如果是會議或客戶來訪，單份包裝通常比大包咖啡豆更穩；如果是固定小團隊，咖啡豆或大包濾掛才可能更划算。"),
            ("禮盒要看對方使用場景", "咖啡禮盒不應只看包裝是否漂亮，而要看對方是否有沖泡工具、是否常在辦公室飲用、是否需要低咖啡因或不同風味選擇。", "LEOBUNA、BINCOO 與 LamiFans 可作為補充選項：前者偏咖啡情境，後者可延伸到客製禮品或辦公室小物搭配。"),
            ("保存方式決定補貨頻率", "辦公室咖啡若一次買太多，風味與新鮮度可能下降；若買太少，又容易在忙碌週期斷貨。比較好的做法，是先抓兩週到一個月用量。", "濾掛與掛耳包適合放在抽屜或茶水間，咖啡豆則要確認密封、陰涼與使用速度。"),
            ("常見錯誤：把咖啡寫成品味表演", "辦公室咖啡不需要每次都像儀式表演。真正有價值的，是在忙碌日裡讓一杯咖啡穩定出現，而且不增加清潔與準備負擔。", "這也是 Elite Fashion 對辦公室補給的判斷：不是追求最專業，而是讓日常更有秩序。"),
            ("下單前確認風味與規格", "咖啡豆、濾掛、掛耳包與禮盒的規格、產地、焙度、包裝、價格與活動都會變動。本文只提供辦公室與送禮情境整理，不宣稱即時優惠或風味排名。", "若要送禮，請特別確認保存期限、包裝完整性與配送時間，避免把好意變成對方的壓力。"),
        ],
        "faq": [
            ("辦公室適合買咖啡豆嗎？", "如果有磨豆與沖泡條件、且有人願意維護器具，咖啡豆很適合；否則濾掛或掛耳包更穩定。"),
            ("送咖啡禮盒要注意什麼？", "先確認對方是否喝咖啡、是否有沖泡工具，再看包裝份量、保存期限與配送時間。"),
            ("濾掛和掛耳包有什麼差別？", "兩者都適合低門檻沖泡；實際風味、份量與包裝方式需看商品頁標示。"),
        ],
    },
    "bedtime-environment-earplugs-pillow-light-scent-order": {
        "heroAlt": "安靜臥室床邊放著耳塞、小夜燈、枕頭、香氛瓶與一本合上的書",
        "coverTheme": "bed",
        "audience": "想用低壓方式整理睡前環境、但不想把睡眠寫成療效承諾的讀者",
        "excerpt": "睡前環境應先處理聲音、光線與枕寢支撐，再考慮香氛；任何睡眠困擾都不應只靠商品解決。",
        "tags": ["睡前環境", "耳塞", "枕頭", "居家燈光"],
        "intro": "睡前環境不是買一樣東西就會立刻變好。聲音、光線、枕頭支撐、床邊雜物與空氣味道，往往一起影響夜晚的收尾感。本文用保守的生活整理角度，將耳塞、枕頭、燈光與香氛排出順序；它不承諾改善失眠，而是協助讀者把臥室裡最容易造成干擾的元素一一降下來。",
        "editorialAngle": "先降低干擾，再補舒適物件；香氛只能放在清潔與通風之後。",
        "sections": [
            ("第一步先處理聲音，而不是氣味", "如果窗外車聲、室友作息或家人活動是主要干擾，先看耳塞或白噪音等聲音管理方式，比急著買香氛更實際。", "耳根清靜可放在降噪與專注情境裡比較；但耳塞適配度、材質與隔音感受因人而異，不能寫成保證效果。"),
            ("第二步看枕頭與床寢支撐", "枕頭與床寢是身體每天接觸最久的物件。若枕頭高度、床墊支撐或床包材質讓身體一直微調，再多睡前儀式也很難安定。", "BETENSH、禾肯居家與紳娜多家居可以分別放在床墊、床包與枕寢補充情境中比較；實際尺寸、材質與保養方式要回商品頁確認。"),
            ("第三步把光線變低，而不是全暗", "睡前光線的重點不是追求戲劇感，而是讓眼睛知道白天已經結束。閱讀燈、小夜燈或間接光源都應避免刺眼與過亮。", "燈后與灰調這類照明/家飾選項，適合用來補床邊或臥室角落的光線層次；選購時要先看插座、放置位置與亮度調整。"),
            ("香氛只放在最後一層", "香氛、精油或木質氣味很容易讓臥室看起來完整，但若空間不通風、床邊雜物未整理、寢具也沒有定期清潔，氣味只會變得複雜。", "THANN、大檜仁心與 au fait 無非可作為氣味選物參考，但本文不宣稱療癒、助眠、淨化或健康效果。"),
            ("常見錯誤：把睡眠問題全交給商品", "如果長期失眠、焦慮、打鼾、疼痛或白天功能受影響，應尋求合格專業人員協助。商品可以整理環境，但不能取代醫療或心理支持。", "比較好的做法，是先把臥室做成低干擾空間，再觀察是否仍需要專業協助。"),
            ("下單前的保守確認", "耳塞看材質與配戴感，枕頭看高度與尺寸，燈具看亮度與放置位置，香氛看使用方式與通風條件。每一項都應回商品頁確認，不靠文章猜測。", "本文含導購連結，但僅供一般生活環境整理參考，不構成醫療、心理治療或個人化睡眠建議。"),
        ],
        "faq": [
            ("耳塞可以改善睡眠嗎？", "耳塞可能協助降低聲音干擾，但不保證改善失眠或睡眠品質。若長期睡不好，請諮詢醫師或專業人員。"),
            ("睡前香氛應該先買嗎？", "不建議作為第一步。先處理通風、清潔、聲音與光線，再考慮氣味，會比較穩。"),
            ("枕頭要怎麼選？", "先看睡姿、肩頸感受、床墊軟硬與尺寸，再回商品頁確認高度、材質與保養方式。"),
        ],
    },
}


TOPIC_HUBS: dict[str, dict[str, Any]] = {
    "commute-bag-size-strap-formality-rain-backup": {
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
    "rainy-commute-umbrella-rain-shoes-bag-materials": {
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
                "key": "body-rhythm-reset",
                "title": "身體節奏與恢復生活指南",
                "file": "body-rhythm-reset.html",
                "url": "/body-rhythm-reset",
                "category": "wellness-movement",
            }
        ],
    },
    "phone-accessory-car-desk-charging-magsafe-system": {
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
                "key": "commute-style-reset",
                "title": "通勤衣櫥與鞋包選物指南",
                "file": "commute-style-reset.html",
                "url": "/commute-style-reset",
                "category": "casual-chic",
            }
        ],
    },
    "office-coffee-beans-drip-bag-gift-box-guide": {
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
    "bedtime-environment-earplugs-pillow-light-scent-order": {
        "topicCategory": "sleep-recovery",
        "topicCategoryLabel": "睡眠與恢復",
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


def load_tracker() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], list[str]]:
    with TRACKER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return rows, {row["merchant_id"]: row for row in rows}, reader.fieldnames or []


def load_matrix_rows() -> list[dict[str, str]]:
    with MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[:5]


def affiliate_url(row: dict[str, str]) -> str:
    return row.get("promo_link", "").strip() or row.get("store_link", "").strip()


def merchant_card(row: dict[str, str], slug: str) -> dict[str, str]:
    brand = row["brand"].strip()
    products = row.get("main_products", "").strip()
    angle = row.get("content_angles", "").strip()
    reason = angle or products or "可依商品頁資訊與實際使用情境比較。"
    return {
        "name": f"{brand} 選物頁",
        "merchantId": row["merchant_id"],
        "brandName": brand,
        "affiliateUrl": affiliate_url(row),
        "sourceProductUrl": row.get("store_link", "").strip() or f"https://www.momoshop.com.tw/TP/{row['merchant_id']}/main",
        "imageCredit": f"圖片來源：momo 店家頁｜{brand}",
        "selectionReason": f"{reason}。下單前請回到商品頁確認尺寸、材質、規格、活動與即時販售資訊。",
        "riskNote": "價格、規格、活動、庫存與配送條件請以下單前商品頁公告為準。",
        "subId": f"{slug}_{row['merchant_id']}",
    }


def cover_palette(theme: str) -> tuple[str, str, str, str]:
    palettes = {
        "bag": ("#ece7df", "#233a35", "#b17846", "#7e8f86"),
        "rain": ("#e6edf2", "#263947", "#557a8b", "#c6a15b"),
        "phone": ("#edf0ec", "#1f2c32", "#718c74", "#c38f51"),
        "coffee": ("#eee5d8", "#332820", "#986a42", "#66806a"),
        "bed": ("#ece8e1", "#30374a", "#a78d72", "#6c7d8f"),
    }
    return palettes.get(theme, palettes["bag"])


def hex_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def write_png(path: Path, width: int, height: int, pixels: bytearray) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    stride = width * 3
    raw = b"".join(b"\x00" + bytes(pixels[y * stride : (y + 1) * stride]) for y in range(height))
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, level=9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(png)


class Canvas:
    def __init__(self, width: int, height: int, bg: str):
        self.width = width
        self.height = height
        self.pixels = bytearray(hex_rgb(bg) * (width * height))

    def pixel(self, x: int, y: int, color: str) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            index = (y * self.width + x) * 3
            self.pixels[index : index + 3] = bytes(hex_rgb(color))

    def rect(self, box: tuple[int, int, int, int], fill: str) -> None:
        x1, y1, x2, y2 = box
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(self.width, x2), min(self.height, y2)
        rgb = bytes(hex_rgb(fill))
        for y in range(y1, y2):
            start = (y * self.width + x1) * 3
            self.pixels[start : start + (x2 - x1) * 3] = rgb * (x2 - x1)

    def ellipse(self, box: tuple[int, int, int, int], fill: str) -> None:
        x1, y1, x2, y2 = box
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        rx, ry = max(1, (x2 - x1) / 2), max(1, (y2 - y1) / 2)
        for y in range(max(0, y1), min(self.height, y2)):
            normalized_y = ((y + 0.5 - cy) / ry) ** 2
            if normalized_y > 1:
                continue
            span = int(rx * math.sqrt(1 - normalized_y))
            self.rect((int(cx - span), y, int(cx + span), y + 1), fill)

    def rounded_rect(self, box: tuple[int, int, int, int], radius: int, fill: str) -> None:
        x1, y1, x2, y2 = box
        radius = max(0, min(radius, (x2 - x1) // 2, (y2 - y1) // 2))
        self.rect((x1 + radius, y1, x2 - radius, y2), fill)
        self.rect((x1, y1 + radius, x2, y2 - radius), fill)
        self.ellipse((x1, y1, x1 + radius * 2, y1 + radius * 2), fill)
        self.ellipse((x2 - radius * 2, y1, x2, y1 + radius * 2), fill)
        self.ellipse((x1, y2 - radius * 2, x1 + radius * 2, y2), fill)
        self.ellipse((x2 - radius * 2, y2 - radius * 2, x2, y2), fill)

    def line(self, start: tuple[int, int], end: tuple[int, int], fill: str, width: int) -> None:
        x1, y1 = start
        x2, y2 = end
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        radius = max(1, width // 2)
        for step in range(steps + 1):
            t = step / steps
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            self.ellipse((x - radius, y - radius, x + radius, y + radius), fill)


def draw_cover(theme: str, path: Path) -> None:
    bg, ink, accent, soft = cover_palette(theme)
    canvas = Canvas(1200, 630, bg)
    canvas.rect((0, 455, 1200, 630), "#d8d2c6")
    canvas.rect((0, 0, 1200, 80), "#f7f3ec")
    canvas.ellipse((820, -160, 1320, 340), "#f5efe4")
    canvas.ellipse((-120, 250, 260, 700), "#dce3dc")

    if theme == "bag":
        canvas.rounded_rect((430, 235, 760, 470), 34, ink)
        canvas.line((500, 255), (595, 155), ink, 16)
        canvas.line((595, 155), (705, 255), ink, 16)
        canvas.rounded_rect((465, 275, 725, 435), 22, "#354f48")
        canvas.rect((820, 265, 910, 430), accent)
        canvas.line((820, 290), (865, 200), accent, 14)
        canvas.line((865, 200), (910, 290), accent, 14)
        canvas.rounded_rect((250, 330, 390, 420), 12, "#f8f5ee")
    elif theme == "rain":
        canvas.ellipse((310, 120, 890, 520), soft)
        canvas.rect((310, 320, 890, 520), bg)
        canvas.line((600, 315), (600, 520), ink, 16)
        canvas.line((600, 520), (655, 540), ink, 12)
        canvas.rounded_rect((815, 330, 910, 505), 18, ink)
        canvas.rounded_rect((915, 350, 1015, 505), 18, "#344d5a")
        canvas.rounded_rect((205, 315, 345, 465), 26, accent)
    elif theme == "phone":
        canvas.rounded_rect((500, 145, 700, 430), 34, ink)
        canvas.rounded_rect((525, 175, 675, 390), 20, "#f2f0ea")
        canvas.rounded_rect((735, 275, 900, 390), 22, accent)
        canvas.line((650, 435), (790, 520), ink, 10)
        canvas.rounded_rect((290, 330, 430, 425), 20, soft)
        canvas.ellipse((333, 356, 390, 413), "#f7f3ec")
    elif theme == "coffee":
        canvas.ellipse((465, 300, 720, 500), "#f5f0e6")
        canvas.ellipse((520, 335, 665, 435), "#5c3b25")
        canvas.line((690, 370), (780, 350), ink, 12)
        canvas.line((780, 350), (790, 420), ink, 12)
        canvas.rounded_rect((285, 300, 420, 455), 18, accent)
        canvas.rounded_rect((820, 270, 960, 455), 16, soft)
        canvas.rect((850, 300, 930, 420), "#efe6d7")
    elif theme == "bed":
        canvas.rounded_rect((260, 330, 930, 500), 28, "#f6f0e8")
        canvas.rounded_rect((310, 250, 540, 355), 36, "#d9c9b5")
        canvas.rounded_rect((565, 250, 795, 355), 36, "#c7d0d8")
        canvas.rounded_rect((850, 230, 940, 430), 18, accent)
        canvas.ellipse((865, 205, 925, 245), "#fff5d6")
        canvas.rounded_rect((210, 390, 270, 445), 18, ink)

    write_png(path, 1200, 630, canvas.pixels)


def prepare_cover(article: dict[str, Any]) -> str:
    target = ROOT / "images" / "optimized" / "article-covers" / f"{article['slug']}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    draw_cover(article["coverTheme"], target)
    manifest = json.loads(COVER_MANIFEST.read_text(encoding="utf-8")) if COVER_MANIFEST.exists() else {"version": 1, "covers": {}}
    manifest["updatedAt"] = pipeline.now_iso()
    manifest["generator"] = "codex-pil-editorial-cover"
    manifest.setdefault("covers", {})[article["slug"]] = {
        "image": pipeline.relative_to_root(target),
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "promptSummary": article["heroImageAlt"],
    }
    pipeline.write_json(COVER_MANIFEST, manifest)
    return pipeline.relative_to_root(target)


def build_sections(blueprint: dict[str, Any], brand_names: list[str]) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for heading, p1, p2 in blueprint["sections"]:
        sections.append(
            {
                "heading": heading,
                "paragraphs": [
                    p1,
                    p2,
                    f"本段的選物會把 {brand_names[0]}、{brand_names[1]} 與其他相關品牌放在同一個生活問題裡看，而不是把品牌名稱排成購物清單。這樣能避免讀者被單一商品牽動，也更接近 Elite Fashion 想保留的編輯判斷。",
                ],
                "bullets": [
                    "先確認使用頻率，再確認收納位置。",
                    "下單前回商品頁確認規格、活動、價格與庫存。",
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
        "metaDescription": f"{blueprint['excerpt']} 本文整理選購順序、常見錯誤與可比較品牌，商品資訊請以商品頁公告為準。",
        "series": "城市效率選物",
        "listingTitle": matrix_row["title"],
        "listingExcerpt": blueprint["excerpt"],
        "heroImageAlt": blueprint["heroAlt"],
        "coverTheme": blueprint["coverTheme"],
        "intro": blueprint["intro"],
        "sections": build_sections(blueprint, brand_names),
        "faq": [{"question": q, "answer": a} for q, a in blueprint["faq"]],
        "extendedReading": [
            {"title": f"瀏覽更多{category.label}文章", "url": f"/{category.page}"},
            {"title": "瀏覽所有文章", "url": "/all-articles.html"},
            {"title": "查看站內搜尋", "url": "/search.html"},
        ],
        "cta": {
            "variant": "gold",
            "text": "先用本文的選購順序縮小範圍，再回商品頁確認規格、價格、活動與庫存，讓每一次下單都更接近日常真正需要。",
            "links": [{"label": f"查看 {row['brand']}", "url": affiliate_url(row)} for row in merchant_rows[:4]],
        },
        "inlineCtas": [
            {
                "afterSection": 2,
                "variant": "gold",
                "eyebrow": "編輯精選",
                "heading": "先看最常用的場景，再比較品牌",
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
                "heading": "把商品頁資訊放在最後一道檢查",
                "text": "價格、規格、活動與庫存都可能變動；本文提供的是選購順序與使用情境，不取代商品頁。",
                "links": [
                    {"label": cards[2]["name"], "url": cards[2]["affiliateUrl"]},
                    {"label": cards[3]["name"], "url": cards[3]["affiliateUrl"]},
                ],
            },
        ],
        "disclaimer": blueprint.get("disclaimer")
        or "本文含品牌／商品導購連結；商品資訊、價格、規格、活動與庫存請以商品頁公告為準。本文不宣稱療效、保健效果、耐用年限、防水或任何未經查證的商品結果。",
        "audience": blueprint["audience"],
        "readTimeMinutes": 9,
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
    article["heroImage"] = prepare_cover(article)
    saved = pipeline.save_generated_article(article, QUEUE_ID, config, categories)
    pipeline.validate_generated_article(saved, config)
    saved["authenticityReview"] = pipeline.run_authenticity_review(saved, config)
    pipeline.write_json(ROOT / config["paths"]["generatedArticlesDir"] / f"{saved['slug']}.json", saved)
    pipeline.append_publish_log(config, saved, trigger_type=TRIGGER_TYPE, queue_id=QUEUE_ID)
    return saved


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
        for article in hits:
            if article["slug"] not in slugs:
                slugs.append(article["slug"])
            if article["url"] not in urls:
                urls.append(article["url"])
        row["article_slug"] = ";".join(slugs)
        row["live_url"] = ";".join(urls)
        try:
            existing_mentions = int(row.get("mention_count") or 0)
        except ValueError:
            existing_mentions = 0
        row["mention_count"] = str(existing_mentions + len(hits))
        row["last_mentioned_at"] = TODAY
        note = "2026-06-21 momo 收益型內容第一批 5 篇已置入。"
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
            "notes": "Codex 手動生成 momo 收益型內容第一批；直接推上 main 不會自動寄送電子報。",
        },
    )


def main() -> int:
    config, categories = pipeline.load_config()
    tracker_rows, rows_by_merchant, fieldnames = load_tracker()
    matrix_rows = load_matrix_rows()
    missing_blueprints = [row["slug"] for row in matrix_rows if row["slug"] not in BLUEPRINTS]
    if missing_blueprints:
        raise SystemExit(f"Missing blueprints: {', '.join(missing_blueprints)}")
    for row in matrix_rows:
        ids = [*row["primary_merchant_ids"].split(";"), *row["supporting_merchant_ids"].split(";")]
        for merchant_id in ids:
            tracker_row = rows_by_merchant.get(merchant_id)
            if not tracker_row or not affiliate_url(tracker_row):
                raise SystemExit(f"Unavailable merchant for {row['slug']}: {merchant_id}")
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
