#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

import content_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[1]
TRACKER_CSV = ROOT / "automation" / "momo-brand-recommendation-tracker.csv"
COVER_MANIFEST = ROOT / "automation" / "codex-generated-cover-manifest.json"
GENERATED_IMAGE_DIR = Path("/Users/mkhsu/.codex/generated_images/019e6f48-25a3-70e3-af05-01a11108fe4d")
TRIGGER_TYPE = "manual-codex-momo-new-audience-no-newsletter"
TODAY = "2026-05-28"
QUEUE_ID = "Q-0016"


ARTICLES: list[dict[str, Any]] = [
    {
        "slug": "bathroom-vanity-hair-scalp-makeup-storage",
        "title": "頭髮、頭皮與妝容收納：把浴室與梳妝台整理成低壓工作站",
        "category": "lifestyle-culture",
        "audience": "上班族、日常保養、美妝入門讀者",
        "items": ["髮品", "頭皮照護", "妝容收納", "梳妝台"],
        "brands": ["TP0009062", "TP0005464", "TP0003175", "TP0000997", "TP0001433"],
        "cover": "ig_0dafceb8339b7ef4016a18c72e585c81939fdff1bc6d5b362c.png",
        "heroAlt": "明亮梳妝台上的髮梳、髮品、彩妝托盤與浴室收納用品",
        "excerpt": "把髮品、保養與彩妝依早晨、洗後、補妝三條動線分開，梳妝台才不會每天重來一次。",
        "intro": "浴室與梳妝台最容易變成瓶罐集合地：洗後髮品放在化妝鏡前，補妝品丟在浴室邊，真正趕時間時卻找不到會用的那幾樣。整理這個角落，不是追求完整儀式，而是讓早晨、洗後與出門前的動作各自有位置。",
        "decision": "先用時間順序分區，而不是用產品類別分區。",
        "sceneLine": "早晨出門、下班洗頭、週末整理與臨時補妝，是最常把浴室和梳妝台弄亂的四個時刻。",
        "priorityLine": "每天會碰到的梳子、髮圈、唇彩和免沖洗髮品，應該比備品與特殊造型工具更靠近手邊。",
        "mistakeLine": "最常見的錯誤，是把所有瓶罐都放在同一層，看似整齊，實際上每次都要重新翻找。",
        "taiwanLine": "台灣浴室濕氣高，備品不一定適合長期放在水氣最重的位置；開封品、備品與旅行小樣要分開。",
        "maintenanceLine": "每兩週清一次托盤，比半年大整理一次更容易持續，也能順手檢查開封日期。",
        "cautionLine": "涉及頭皮、皮膚或眼周不適時，請停止使用相關用品並諮詢合格專業人員。",
        "disclaimer": "本文僅供一般梳妝台、髮品與美妝收納參考，不構成醫療、皮膚治療或個人化建議；商品成分與適用資訊請以商品頁公告為準。",
        "brandReasons": {
            "TP0009062": "可從髮品、洗後整理與頭髮日常用品方向查看",
            "TP0005464": "適合補充保養、彩妝與梳妝台小物",
            "TP0003175": "可作為美妝保養與日常儀容用品參考",
            "TP0000997": "適合查看美妝保養與生活選品",
            "TP0001433": "可補充髮品、造型與日常照護用品",
        },
    },
    {
        "slug": "school-study-corner-stationery-books-kids-toothbrush",
        "title": "開學與學習角落整理：文具、考試書、兒童電動牙刷與生活用品",
        "category": "lifestyle-culture",
        "audience": "新手爸媽、家庭學習與日用品補貨讀者",
        "items": ["文具", "考試書", "兒童電動牙刷", "家庭用品"],
        "brands": ["TP0001367", "TP0001495", "TP0001633", "TP0000500", "TP0004956"],
        "cover": "ig_0dafceb8339b7ef4016a18c7692d6081938c4165d2e92a35ce.png",
        "heroAlt": "窗邊學習角落中的書本、文具盒、收納籃與兒童盥洗用品",
        "excerpt": "開學前先把書桌、書本、文具與早晚盥洗動線排好，家庭學習角落會比一次買齊更穩。",
        "intro": "開學前的採買很容易失焦：文具想補、書想買、盥洗用品也剛好快用完。真正讓早晨順下來的，不是清單越長越好，而是書桌、書包、浴室與玄關之間能不能形成固定路線。",
        "decision": "先補會每天消耗與每天移動的物件，再看進階書籍或禮物型用品。",
        "sceneLine": "平日早晨、放學回家、寫作業前與睡前刷牙，是家庭用品最容易散落的四個節點。",
        "priorityLine": "筆、橡皮擦、作業夾、書本與盥洗用品要各有固定位置，孩子與照顧者才不用每天重新找。",
        "mistakeLine": "常見錯誤是一次買太多新文具，卻沒有淘汰壞掉、重複或已經不合年級需求的用品。",
        "taiwanLine": "補習、才藝課和通勤接送會讓書包變重，學習角落要替隔天用品留一個不必翻抽屜的位置。",
        "maintenanceLine": "每週固定一次把書包、文具盒與浴室用品看一輪，比等到開學前一天才採買更穩。",
        "cautionLine": "兒童用品請依年齡、商品標示與照顧者判斷選擇，不宣稱學習、口腔或教養效果。",
        "disclaimer": "本文為一般家庭學習角落與兒童日用品整理參考，不構成教育、醫療或口腔照護建議；兒童用品請以商品標示與照顧者判斷為準。",
        "brandReasons": {
            "TP0001367": "可從考試書、書籍與學習資料方向查看",
            "TP0001495": "適合作為文具、手帳與桌面用品參考",
            "TP0001633": "可補充兒童電動牙刷與日常盥洗用品",
            "TP0000500": "適合查看嬰兒、兒童、寵物與家居百貨",
            "TP0004956": "可作為母嬰用品與居家生活補位參考",
        },
    },
    {
        "slug": "swimming-outdoor-class-kids-prep",
        "title": "游泳課與戶外課前準備：泳鏡、童裝、早餐與親子外出小物",
        "category": "outdoor-escapes",
        "audience": "親子家庭、戶外課與週末活動讀者",
        "items": ["泳鏡", "童裝", "早餐", "外出小物"],
        "brands": ["TP0003976", "TP0006789", "TP0004495", "TP0000485", "TP0003190"],
        "cover": "ig_0dafceb8339b7ef4016a18c79df4ec81938817895351e2c17c.png",
        "heroAlt": "泳池邊長椅上的泳鏡、毛巾、童裝、早餐盒與水瓶",
        "excerpt": "游泳課與戶外課要先把濕物、換洗衣物、早餐與回家後清潔動線排好，出門前才不會手忙腳亂。",
        "intro": "親子戶外課最容易卡住的，不是缺某一件裝備，而是出門前、下課後與回家清洗之間沒有順序。泳鏡、童裝、早餐和外出小物若各放各的，早晨會一直重複找東西。",
        "decision": "先整理濕物路線，再補泳具與童裝。",
        "sceneLine": "出門前換裝、課前等待、下課收濕物與回家清洗，是游泳課和戶外課最容易混亂的四段。",
        "priorityLine": "泳鏡、毛巾、備用衣物、早餐與水瓶要能放進同一個可分層外出袋，濕乾用品不要混在一起。",
        "mistakeLine": "最常見的錯誤，是只看泳具本身，忘了準備濕袋、替換衣物與課後收尾位置。",
        "taiwanLine": "夏季午後雷雨與室內外溫差都常見，薄外套、替換衣物和防水收納比多帶一堆小物更重要。",
        "maintenanceLine": "每次回家先清空濕袋、晾毛巾、補早餐用品，下一次課前才不用重新檢查一遍。",
        "cautionLine": "泳具與兒童用品請以商品標示、適用年齡、場館規範與照顧者判斷為準，不保證安全或表現。",
        "disclaimer": "本文為一般游泳課與親子戶外課用品整理參考，不構成安全、教學或健康建議；請依場館規範、商品標示與照顧者判斷準備。",
        "brandReasons": {
            "TP0003976": "可從泳鏡與泳具配件方向查看",
            "TP0006789": "適合作為童裝、換洗衣物與兒童穿搭參考",
            "TP0004495": "可補充早餐、點心與家庭分享品項",
            "TP0000485": "適合比較童裝、玩具與母嬰生活用品",
            "TP0003190": "可從親子用品、童裝與禮物方向查看",
        },
    },
    {
        "slug": "road-trip-camping-dashcam-jump-starter-cookware",
        "title": "自駕與露營路上的備用清單：行車記錄器、救車電源、餐廚與戶外小物",
        "category": "outdoor-escapes",
        "audience": "自駕、家庭旅行與戶外移動讀者",
        "items": ["行車記錄器", "救車電源", "餐廚", "戶外小物"],
        "brands": ["TP0001376", "TP0007559", "TP0000363", "TP0009471", "TP0000074"],
        "cover": "ig_0dafceb8339b7ef4016a18c7d631b08193b7fa1d11f4f2ca81.png",
        "heroAlt": "山路旁車尾箱中的行車記錄器、救車電源、鍋具與戶外收納包",
        "excerpt": "自駕與露營前先把車內、餐廚、雨天與回家收納分區，備用品才不會變成車廂雜物。",
        "intro": "自駕旅行和輕露營的備用品很容易越買越多：行車記錄器、救車電源、鍋具、收納包和雨具全部放進車裡，最後卻沒有人知道在哪一格。備用清單的重點不是塞滿後車廂，而是讓關鍵用品在需要時找得到。",
        "decision": "先分車用、餐廚、天候與收納四區，再決定補什麼。",
        "sceneLine": "上路前檢查、途中臨停、營地用餐與回家整理，是自駕用品最容易失序的四段。",
        "priorityLine": "車用電子品、電源線、餐廚工具和戶外小物要分袋放，不要和衣物、食品或濕物混在一起。",
        "mistakeLine": "常見錯誤是買了看似安心的備用品，卻沒有確認規格、充電狀態、固定方式和收納位置。",
        "taiwanLine": "山區天候變化快，雨具、照明和收納袋要比裝飾性露營小物更優先，也要避免遮擋駕駛視線。",
        "maintenanceLine": "每次出發前看電量、線材和餐具清潔；回家後把車用用品放回固定箱，下一趟才不會從零開始。",
        "cautionLine": "車用電子、救援用品與戶外裝備請依商品規格、車型限制與安全規範使用，不承諾安全結果。",
        "disclaimer": "本文為一般自駕與戶外備用品整理參考，不構成行車安全、救援或露營專業建議；車用與戶外用品請依商品規格和實際情境使用。",
        "brandReasons": {
            "TP0001376": "可從行車記錄器與車用視線紀錄方向查看",
            "TP0007559": "適合補充救車電源、小家電與戶外用電用品",
            "TP0000363": "可作為餐具、鍋具與戶外餐廚用品參考",
            "TP0009471": "適合查看戶外部品、露營與移動小物",
            "TP0000074": "可補充旅行、戶外與露營配件",
        },
    },
    {
        "slug": "elder-travel-vision-reading-sunglasses-luggage",
        "title": "長輩與戶外旅行的視線管理：老花眼鏡、偏光太陽眼鏡與旅行配件",
        "category": "outdoor-escapes",
        "audience": "家庭旅行、戶外移動與送禮讀者",
        "items": ["老花眼鏡", "偏光太陽眼鏡", "旅行配件", "箱包"],
        "brands": ["TP0009515", "TP0000151", "TP0005391", "TP0002546"],
        "cover": "ig_0dafceb8339b7ef4016a18c816a8e481939d18f3c03ba1e828.png",
        "heroAlt": "機場窗邊桌上的老花眼鏡、偏光太陽眼鏡、登機箱與旅行收納小物",
        "excerpt": "家庭旅行不只要帶箱包，也要讓閱讀、看路、找票與戶外光線都有清楚的位置。",
        "intro": "和家人旅行時，最常被忽略的是視線動線：票券要看、手機要看、菜單要看，戶外又有刺眼陽光。眼鏡、太陽眼鏡和旅行配件若沒有固定位置，行程會被許多小停頓打斷。",
        "decision": "先把閱讀、戶外光線與行李拿取分成三條路線。",
        "sceneLine": "機場報到、車站轉乘、戶外步行與餐廳點餐，是家庭旅行最容易需要快速看清楚的四個時刻。",
        "priorityLine": "老花眼鏡、偏光太陽眼鏡、票券小袋和常用藥品收納要放在容易拿的位置，不要全部塞進行李箱深處。",
        "mistakeLine": "常見錯誤是替家人買了眼鏡或箱包，卻沒有確認度數、配戴習慣、重量、開合方式與收納高度。",
        "taiwanLine": "台灣夏季日照強、午後雨多，戶外旅行要同時考慮遮光、收納、防雨與上下車拿取便利。",
        "maintenanceLine": "出門前把眼鏡盒、拭鏡布和票券包放在同一層，回家後再把旅行配件固定歸位。",
        "cautionLine": "眼鏡與視力相關用品請依個人需求、商品標示與合格專業人員建議選擇，不作視力改善承諾。",
        "disclaimer": "本文為一般旅行配件與視線動線整理參考，不構成醫療或視力矯正建議；眼鏡、太陽眼鏡與箱包資訊請以商品頁公告為準。",
        "brandReasons": {
            "TP0009515": "可從老花眼鏡、偏光太陽眼鏡與日常選鏡方向查看",
            "TP0000151": "適合補充旅行用品與出國收納配件",
            "TP0005391": "可作為行李箱與旅行箱包參考",
            "TP0002546": "適合查看箱包、登機箱與外出收納用品",
        },
    },
    {
        "slug": "pet-birthday-gift-cake-snack-toy",
        "title": "毛孩生日與送禮怎麼準備：寵物蛋糕、零食、玩具與慶生小物",
        "category": "lifestyle-culture",
        "audience": "寵物家庭、送禮與週末聚會讀者",
        "items": ["寵物蛋糕", "零食", "玩具", "慶生小物"],
        "brands": ["TP0001817", "TP0009366", "TP0002315", "TP0000155", "TP0006730"],
        "cover": "ig_0dafceb8339b7ef4016a18c85e06748193a87b7419c0c05727.png",
        "heroAlt": "客廳矮桌上的寵物生日蛋糕盒、零食罐、玩具與清潔用品",
        "excerpt": "寵物生日不必買滿一整桌，先確認食用限制、清潔收尾、玩具安全與拍照動線，慶生才不會變成壓力。",
        "intro": "替毛孩慶生很可愛，但真正重要的是安全、標示與收尾。蛋糕、零食、玩具和拍照小物如果全部一起上桌，寵物可能興奮，人也容易忘記成分、份量和清潔。",
        "decision": "先確認能不能吃、能不能咬、能不能清潔，再談佈置。",
        "sceneLine": "訂蛋糕、拍照、分食、收玩具與清理地面，是寵物生日最容易混亂的幾個時刻。",
        "priorityLine": "食品和玩具要分開準備，清潔用品要先放在旁邊，不要等到弄髒地板才找抹布。",
        "mistakeLine": "常見錯誤是只看慶生照片好不好看，沒有先確認成分標示、適用對象、玩具材質和寵物平常習慣。",
        "taiwanLine": "台灣家庭常在小客廳或陽台慶生，空間有限時，低高度桌面、可清潔地墊和簡單佈置比大型背景更實用。",
        "maintenanceLine": "慶生後把未開封零食、玩具和清潔品分盒收好，避免之後變成到處散落的小物。",
        "cautionLine": "寵物食品與用品請依商品標示、寵物狀況與獸醫建議判斷，不宣稱健康、營養或行為改善效果。",
        "disclaimer": "本文為一般寵物生日與送禮用品整理參考，不構成獸醫、營養或行為建議；寵物食品與用品請依商品標示和專業建議選擇。",
        "brandReasons": {
            "TP0001817": "可從寵物蛋糕、寵物零食與生日用品方向查看",
            "TP0009366": "適合補充寵物周邊、服飾、玩具與生活用品",
            "TP0002315": "可作為寵物精品、玩具與外出用品參考",
            "TP0000155": "適合查看寵物日用品、玩具與清潔用品",
            "TP0006730": "可補充寵物食品、零食與日常用品",
        },
    },
    {
        "slug": "aquarium-reptile-small-pet-restock-list",
        "title": "不只貓狗：水族、爬蟲與小寵家庭的補貨清單",
        "category": "lifestyle-culture",
        "audience": "水族、爬蟲、小寵與寵物新手讀者",
        "items": ["水族用品", "爬蟲用品", "小寵飼料", "清潔工具"],
        "brands": ["TP0009226", "TP0008082", "TP0000551", "TP0004035"],
        "cover": "ig_0dafceb8339b7ef4016a18c8a255508193996f626efcc500f6.png",
        "heroAlt": "明亮層架上的小型水族缸、飼料盒、清潔工具與小寵用品收納",
        "excerpt": "小眾寵物家庭更需要固定補貨節奏，把餌料、底材、清潔工具與保存方式分清楚。",
        "intro": "水族、爬蟲與小寵家庭的補貨壓力，常常不是一次買不到，而是每種用品的保存方式和使用頻率都不同。餌料、底材、清潔工具和外出用品如果混在一起，照顧流程很容易被打斷。",
        "decision": "先按保存條件分類，再按使用頻率補貨。",
        "sceneLine": "餵食、換水或清潔、底材更換與臨時外出，是小眾寵物家庭最需要穩定用品位置的四個場景。",
        "priorityLine": "冷凍、乾燥、清潔與消耗用品要分開收，不同寵物的用品也要避免混放。",
        "mistakeLine": "常見錯誤是用貓狗用品邏輯看所有寵物，忽略水族、爬蟲和小寵對溫度、保存與清潔的要求不同。",
        "taiwanLine": "潮濕天氣會影響保存，飼料、底材與清潔工具要留意密封、標示日期與擺放通風。",
        "maintenanceLine": "每週做一次補貨盤點，將即將用完、已開封和備品分開，會比一次囤很多更容易掌握。",
        "cautionLine": "寵物食品、餌料與環境用品請依商品標示、物種需求與獸醫或專業店家建議判斷。",
        "disclaimer": "本文為一般水族、爬蟲與小寵家庭補貨整理參考，不構成獸醫、飼養或營養建議；用品選擇請依物種需求、商品標示與專業建議判斷。",
        "brandReasons": {
            "TP0009226": "可從水族、爬蟲與小寵用品方向查看",
            "TP0008082": "適合補充寵物食品、用品與日常照護選項",
            "TP0000551": "可作為寵物食品與日用品補貨參考",
            "TP0004035": "適合查看寵物用品、玩具與日常補貨品項",
        },
    },
    {
        "slug": "office-sitting-low-barrier-stretch-snack-pillow",
        "title": "辦公室久坐後的低門檻活動清單：伸展小物、枕頭與低負擔點心",
        "category": "wellness-movement",
        "audience": "久坐上班族、輕運動與辦公室補給讀者",
        "items": ["伸展小物", "枕頭", "低負擔點心", "辦公室補給"],
        "brands": ["TP0008962", "TP0008981", "TP0006455", "TP0007439"],
        "cover": "ig_0dafceb8339b7ef4016a18c8e240008193af3865c18a3d88a9.png",
        "heroAlt": "辦公桌旁的伸展帶、按摩球、人體工學枕、水瓶與點心罐",
        "excerpt": "久坐後先把能確實做得到的小活動放進工作日，伸展小物、枕頭與點心都要回到使用頻率判斷。",
        "intro": "久坐後想活動一下，最難的不是買到很多器材，而是找到真的會在工作日使用的低門檻方式。伸展帶、枕頭、按摩球和點心如果只是放在櫃子裡，就不會改變一天的節奏。",
        "decision": "先設定一個不換衣服也能完成的小活動，再看用品。",
        "sceneLine": "會議前後、午餐後、下班前和加班時段，是最容易感到僵住、想吃點東西或想靠一下的時刻。",
        "priorityLine": "伸展小物要能放在抽屜或桌邊，枕頭要配合座位高度，點心則要看保存、份量和個人飲食狀況。",
        "mistakeLine": "常見錯誤是買太複雜的器材，最後需要換衣服、移桌子或找大空間，反而更難持續。",
        "taiwanLine": "辦公室空間有限，動作幅度、旁人距離和收納位置都要考慮；不適合把家用大型器材硬搬進工作角落。",
        "maintenanceLine": "把用品固定放在同一格抽屜，每週清點一次點心與水瓶，活動才不會變成臨時想起來的事。",
        "cautionLine": "若有疼痛、麻木、受傷、慢性病或特殊飲食需求，請先諮詢合格專業人員；本文不承諾改善或恢復效果。",
        "disclaimer": "本文為一般辦公室活動與用品整理參考，不構成醫療、復健、營養或運動處方；若有不適或特殊需求，請諮詢合格專業人員。",
        "brandReasons": {
            "TP0008962": "可從運動配件、伸展與低門檻活動用品方向查看",
            "TP0008981": "適合補充枕頭、靠墊與居家辦公支撐用品",
            "TP0006455": "可作為低醣點心與辦公室補給參考",
            "TP0007439": "適合查看醫材通路與生活輔助用品標示",
        },
    },
]


def load_tracker() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], list[str]]:
    with TRACKER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    return rows, {row["merchant_id"]: row for row in rows}, fieldnames


def merchant_card(row: dict[str, str], article_slug: str, reason: str) -> dict[str, str]:
    brand = row["brand"].strip()
    promo = row.get("promo_link", "").strip()
    store = row.get("store_link", "").strip() or f"https://www.momoshop.com.tw/TP/{row['merchant_id']}/main"
    public_reason = reason.rstrip("。.!！")
    return {
        "name": f"{brand} 選物頁",
        "merchantId": row["merchant_id"],
        "brandName": brand,
        "affiliateUrl": promo or store,
        "sourceProductUrl": store,
        "imageCredit": f"圖片來源：momo 店家頁｜{brand}",
        "selectionReason": f"{public_reason}；下單前請搭配商品頁的規格、材質與配送資訊確認。",
        "riskNote": "規格、活動與即時販售資訊請以下單前商品頁公告為準。",
        "subId": f"{article_slug}_{row['merchant_id']}",
    }


def prepare_cover(article: dict[str, Any]) -> str:
    source = GENERATED_IMAGE_DIR / article["cover"]
    if not source.exists():
        raise FileNotFoundError(f"Missing generated cover: {source}")
    target = ROOT / "images" / "optimized" / "article-covers" / f"{article['slug']}.jpg"
    image = Image.open(source).convert("RGB")
    image = ImageOps.fit(image, (1200, 630), method=Image.Resampling.LANCZOS)
    image.save(target, "JPEG", quality=88, optimize=True)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    manifest = pipeline.load_json(COVER_MANIFEST, default={"version": 1, "covers": {}})
    manifest.setdefault("covers", {})[article["slug"]] = {
        "provider": "codex-imagegen",
        "sourceImage": str(source),
        "output": str(target.relative_to(ROOT)),
        "sha256": digest,
        "generatedAt": pipeline.now_iso(),
        "usage": "cover-og-twitter",
        "notes": "同一張 Codex 生成圖片用於文章封面、OG 與 Twitter 預覽。",
    }
    manifest["updatedAt"] = pipeline.now_iso()
    pipeline.write_json(COVER_MANIFEST, manifest)
    return f"/images/optimized/article-covers/{article['slug']}.jpg"


def make_sections(spec: dict[str, Any], cards: list[dict[str, str]]) -> list[dict[str, Any]]:
    item_text = "、".join(spec["items"])
    first_brand = cards[0]["brandName"]
    second_brand = cards[1]["brandName"] if len(cards) > 1 else cards[0]["brandName"]
    brand_sentence = "、".join(card["brandName"] for card in cards[:6])
    return [
        {
            "heading": "先把真正會發生的場景排出來",
            "paragraphs": [
                spec["sceneLine"],
                f"先不要急著把{item_text}一次買齊。比較穩的做法，是把一天或一次出門會經過的動作寫下來：拿取、使用、暫放、清潔、歸位。只要其中一段沒有位置，物件很快就會散落。",
                f"Elite Fashion 編輯團隊的判斷是：{spec['decision']} 這個順序能避免把預算花在照片裡好看、但生活中不會常用的品項上。",
            ],
            "bullets": [f"先確認{spec['items'][0]}的使用位置。", f"再看{spec['items'][1]}是否每天會用。", "最後才補低頻或送禮型用品。"],
        },
        {
            "heading": "常用物要靠近手，不常用物要有邊界",
            "paragraphs": [
                spec["priorityLine"],
                f"如果一件物品每週只用一次，它不需要佔據最順手的位置；如果每天都要用，就不該被壓在備品下面。{item_text}的採買重點，是讓使用頻率和收納位置一致。",
                f"{spec['mistakeLine']} 下單前可以先看商品頁的尺寸、材質、適用範圍、保存方式和清潔限制，再決定它適合放在哪裡。",
            ],
            "bullets": ["常用品留在視線高度。", "備品標示開封或補貨日期。", "低頻用品集中，不分散在每個角落。"],
        },
        {
            "heading": "品牌與店家只放在適合的情境裡比較",
            "paragraphs": [
                f"{first_brand} 和 {second_brand} 可以先從本篇核心情境查看，但不要把單一店家當成唯一答案。真正該比較的是用途、尺寸、材質、保存條件與退換規則。",
                f"{brand_sentence} 這些店家適合放在同主題選物中作為參考。本文不寫死價格、庫存、活動或商品規格，因為這些資訊都會變動，應以下單前商品頁公告為準。",
                "若某個品項涉及身體、兒童、寵物、食品、車用或戶外安全，請把商品標示放在風格之前。看起來順眼只是第一步，能不能正確使用和維護才是長期留下來的原因。",
            ],
            "bullets": [],
        },
        {
            "heading": "台灣生活裡最容易被忽略的是收尾",
            "paragraphs": [
                spec["taiwanLine"],
                "很多採買清單只寫出門前要準備什麼，卻沒有寫回家後要怎麼收。濕物、粉塵、食品、線材、玩具或開封用品如果沒有回收位置，下一次使用前就會重新混亂。",
                "比較好的做法，是替每一類物件設一個結束動作：清潔、晾乾、補貨、充電、貼標或放回固定袋。這些收尾動作比買更多收納盒更能維持秩序。",
            ],
            "bullets": ["把回家後的第一個動作寫清楚。", "需要清潔或晾乾的用品不要密封收起。", "補貨訊號要比完全用完更早出現。"],
        },
        {
            "heading": "不適合的情境要先排除",
            "paragraphs": [
                f"{spec['cautionLine']} 如果商品頁標示和你的生活情境不一致，就算外觀、價格或評價吸引人，也應該先暫緩。",
                "送禮或替家人採買時，請避免用自己的偏好替對方做完整決定。尺寸、氣味、材質、飲食、使用習慣和清潔意願，都會影響一件物品能不能被真正使用。",
                "這也是這類選購整理的共同原則：不要把購物清單寫成標準答案，而是提供一套可以回到自家動線檢查的順序。",
            ],
            "bullets": [],
        },
        {
            "heading": "最後一輪確認：尺寸、保存、清潔與替換",
            "paragraphs": [
                spec["maintenanceLine"],
                f"下單前請回到商品頁確認{item_text}的規格、材質、配送、保存和退換資訊。若資訊不足，先收藏或改找標示更清楚的品項，不需要急著一次買完。",
                "也可以替這類用品留一張簡單備忘：買了什麼、放在哪裡、多久會用完、誰最常使用。下一次補貨時，這張備忘會比重新瀏覽一長串商品更可靠。",
                "能長期留下來的物件，通常不是最吸睛的那一件，而是你知道放哪裡、怎麼清、何時補、誰會用的那一件。採買到這一步，才比較像真的替生活減少摩擦。",
            ],
            "bullets": [],
        },
    ]


def make_faq(spec: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "question": "這份清單可以直接照單購買嗎？",
            "answer": "不建議。請先依自己的空間、家庭成員、寵物狀況、出門路線或工作型態盤點，再回到商品頁確認規格與限制。",
        },
        {
            "question": "價格、活動或庫存可以以文章為準嗎？",
            "answer": "不可以。價格、活動、庫存、規格、尺寸與配送條件都可能變動，請以下單前看到的 momo 商品頁或店家頁公告為準。",
        },
        {
            "question": "涉及兒童、寵物、食品、照護或運動用品時要注意什麼？",
            "answer": "請優先看商品標示、適用對象、保存方式與專業建議。本文只提供一般生活整理與選購順序，不宣稱安全、健康、學習、營養或恢復效果。",
        },
    ]


def build_article(
    spec: dict[str, Any],
    rows_by_merchant: dict[str, dict[str, str]],
    config: dict[str, Any],
    categories: dict[str, pipeline.CategoryConfig],
) -> dict[str, Any]:
    category = categories[spec["category"]]
    brand_rows = [rows_by_merchant[mid] for mid in spec["brands"]]
    cards = [
        merchant_card(row, spec["slug"], spec["brandReasons"].get(row["merchant_id"], "可依商品頁資訊與實際使用情境比較"))
        for row in brand_rows
    ]
    cta_links = [{"label": f"查看 {card['brandName']}", "url": card["affiliateUrl"]} for card in cards[:4]]
    article = {
        "slug": spec["slug"],
        "category": spec["category"],
        "title": spec["title"],
        "metaTitle": f"Elite Fashion｜{spec['title'][:48]}",
        "metaDescription": spec["excerpt"],
        "excerpt": spec["excerpt"],
        "tags": [*spec["items"], "選物指南", "生活採買"],
        "series": "日常選物指南",
        "listingTitle": spec["title"],
        "listingExcerpt": spec["excerpt"],
        "intro": spec["intro"],
        "sections": make_sections(spec, cards),
        "faq": make_faq(spec),
        "extendedReading": [
            {"title": f"瀏覽更多{category.label}文章", "url": f"/{category.page}"},
            {"title": "查看生活品味文章", "url": "/lifestyle-culture.html"},
            {"title": "查看站內搜尋", "url": "/search.html"},
        ],
        "cta": {
            "text": f"先用{spec['decision']}的順序盤點，再回到商品頁確認規格、材質與使用限制。",
            "links": cta_links,
        },
        "inlineCtas": [
            {
                "afterSection": 2,
                "variant": "olive",
                "eyebrow": "同場景參考",
                "heading": "先看會每天用到的那一格",
                "text": "把常用品放在最順手的位置，低頻用品集中收納，採買就不會被漂亮照片牽著走。",
                "links": [{"label": cards[0]["name"], "url": cards[0]["affiliateUrl"]}, {"label": cards[1]["name"], "url": cards[1]["affiliateUrl"]}],
            }
        ],
        "disclaimer": spec["disclaimer"],
        "audience": spec["audience"],
        "readTimeMinutes": 11,
        "sourceType": "manual-codex-momo-new-audience-affiliate",
        "status": "published",
        "queueId": QUEUE_ID,
        "heroImage": prepare_cover(spec),
        "heroImageAlt": spec["heroAlt"],
        "coverImageStatus": "codex-generated",
        "mainProducts": cards[:4],
        "sidebarProducts": cards[:6],
        "featuredBrands": [
            {
                "name": row["brand"],
                "merchantId": row["merchant_id"],
                "role": "品牌參考",
                "reason": spec["brandReasons"].get(row["merchant_id"], "可依商品頁資訊與實際使用情境比較"),
                "url": row.get("promo_link") or row.get("store_link"),
            }
            for row in brand_rows
        ],
    }
    saved = pipeline.save_generated_article(article, QUEUE_ID, config, categories)
    pipeline.validate_generated_article(saved, config)
    saved["authenticityReview"] = pipeline.run_authenticity_review(saved, config)
    pipeline.write_json(ROOT / config["paths"]["generatedArticlesDir"] / f"{saved['slug']}.json", saved)
    pipeline.write_text(ROOT / config["paths"]["generatedArticlesDir"] / f"{saved['slug']}.md", saved["markdownBody"])
    pipeline.append_publish_log(config, saved, trigger_type=TRIGGER_TYPE, queue_id=QUEUE_ID)
    return saved


def update_queue(articles: list[dict[str, Any]], config: dict[str, Any]) -> None:
    path = ROOT / config["paths"]["queueJson"]
    queue = pipeline.load_json(path)
    by_slug = {article["slug"]: article for article in articles}
    series = next((item for item in queue["series"] if item.get("queueId") == QUEUE_ID), None)
    if series is None:
        series = {
            "queueId": QUEUE_ID,
            "topic": "梳妝台、親子學習、戶外課、自駕旅行、寵物與辦公室活動補強",
            "direction": "延伸新受眾到家庭學習、戶外移動、小眾寵物與辦公室低門檻活動；每篇以真實動線、保守提醒和可查證商品頁資訊建立選購順序。",
            "plannedCount": len(ARTICLES),
            "status": "planned",
            "source": "momo-ab-new-audience-roadmap",
            "createdAt": pipeline.now_iso(),
            "seriesName": "momo 新受眾第四批",
            "items": [
                {
                    "order": index,
                    "slug": spec["slug"],
                    "title": spec["title"],
                    "targetReader": spec["audience"],
                    "category": spec["category"],
                    "status": "planned",
                }
                for index, spec in enumerate(ARTICLES, start=1)
            ],
        }
        queue["series"].append(series)
        queue["nextQueueSequence"] = max(int(queue.get("nextQueueSequence", 1)), 17)
    spec_by_slug = {spec["slug"]: spec for spec in ARTICLES}
    for index, item in enumerate(series["items"], start=1):
        spec = spec_by_slug.get(item.get("slug"), {})
        item.setdefault("order", index)
        if spec:
            item.setdefault("targetReader", spec["audience"])
            item.setdefault("category", spec["category"])
            item.setdefault("title", spec["title"])
        article = by_slug.get(item.get("slug"))
        if article:
            item["status"] = "published"
            item["articleId"] = article["id"]
            item["file"] = article["file"]
            item["publishedAt"] = article["publishedAt"]
    series["status"] = "completed" if all(item.get("status") == "published" for item in series["items"]) else "in_progress"
    queue["updatedAt"] = pipeline.now_iso()
    pipeline.write_json(path, queue)


def update_tracker(articles: list[dict[str, Any]], tracker_rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    by_merchant = {row["merchant_id"]: row for row in tracker_rows}
    mentions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in articles:
        merchant_ids = {product["merchantId"] for product in [*article.get("mainProducts", []), *article.get("sidebarProducts", [])]}
        merchant_ids.update(brand["merchantId"] for brand in article.get("featuredBrands", []))
        for merchant_id in merchant_ids:
            mentions[merchant_id].append(article)
    for merchant_id, hits in mentions.items():
        row = by_merchant[merchant_id]
        row["coverage_status"] = "live"
        row["article_created"] = "true"
        row["link_status"] = "usable"
        row["risk_notes"] = row.get("risk_notes") or "不使用誇大推薦語氣，商品規格以 momo 商品頁為準"
        existing_slugs = [part for part in row.get("article_slug", "").split(";") if part]
        existing_urls = [part for part in row.get("live_url", "").split(";") if part]
        increment = 0
        for article in hits:
            if article["slug"] not in existing_slugs:
                existing_slugs.append(article["slug"])
                increment += 1
            if article["url"] not in existing_urls:
                existing_urls.append(article["url"])
        row["article_slug"] = ";".join(existing_slugs)
        row["live_url"] = ";".join(existing_urls)
        if increment:
            row["mention_count"] = str(int(row.get("mention_count") or 0) + increment)
        row["last_mentioned_at"] = TODAY
        note = "2026-05-28 momo 新受眾第四批親子戶外寵物與辦公室活動文章已置入。"
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
            "notes": "Codex 手動分批撰文與封面生成；直接推上 main 不會自動寄送電子報。",
        },
    )


def strip_article_trailing_whitespace(articles: list[dict[str, Any]]) -> None:
    for article in articles:
        path = ROOT / article["file"]
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def reset_existing_batch_records(config: dict[str, Any]) -> None:
    slugs = {spec["slug"] for spec in ARTICLES}
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


def main() -> int:
    config, categories = pipeline.load_config()
    tracker_rows, rows_by_merchant, fieldnames = load_tracker()
    missing = sorted({mid for spec in ARTICLES for mid in spec["brands"] if mid not in rows_by_merchant})
    if missing:
        raise SystemExit(f"Tracker missing merchants: {', '.join(missing)}")
    reset_existing_batch_records(config)
    articles = []
    for spec in ARTICLES:
        print(f"Building {spec['slug']}...")
        articles.append(build_article(spec, rows_by_merchant, config, categories))
    update_queue(articles, config)
    update_tracker(articles, tracker_rows, fieldnames)
    update_latest_run(config, articles)
    pipeline.rebuild_outputs(config, categories)
    strip_article_trailing_whitespace(articles)
    pipeline.verify_outputs(config, categories)
    print(f"Generated {len(articles)} {QUEUE_ID} momo new-audience articles:")
    for article in articles:
        print(f"- {article['slug']} -> {article['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
