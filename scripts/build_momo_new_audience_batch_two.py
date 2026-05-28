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
TRIGGER_TYPE = "manual-codex-momo-new-audience-no-newsletter"
TODAY = "2026-05-28"
QUEUE_ID = "Q-0014"
GENERATED_IMAGE_DIR = Path("/Users/mkhsu/.codex/generated_images/019e6f48-25a3-70e3-af05-01a11108fe4d")


ARTICLES: list[dict[str, Any]] = [
    {
        "slug": "mens-commute-shirt-trousers-jacket-shoes",
        "title": "男士通勤不只一套西裝：襯衫、西裝褲、外套與皮鞋的場合清單",
        "category": "casual-chic",
        "audience": "男性上班族、伴侶送禮、婚禮與面試需求者",
        "items": ["襯衫", "西裝褲", "外套", "皮鞋"],
        "brands": ["TP0003817", "TP0005310", "TP0003665"],
        "cover": "ig_04a46ee67450d745016a1890c11e9c819681e4639de1d5e7de.png",
        "heroAlt": "明亮玄關裡整理好的男士襯衫、西裝褲、外套、皮鞋與通勤包",
        "excerpt": "用會議、日常通勤、婚禮與面試四種場合，整理男士衣櫥真正需要先補的單品。",
        "metaDescription": "男士通勤與正式場合穿搭指南，從襯衫、西裝褲、外套到皮鞋，整理會議、面試、婚禮與日常上班的選款順序。",
        "intro": "男士通勤衣櫥不必靠一整套西裝撐住所有場合。真正常見的困擾，是平日會議、臨時拜訪、婚禮邀約和面試通知都擠在同一季，卻只有幾件彼此不太能搭的單品。先把場合分清楚，再補襯衫、西裝褲、外套與皮鞋，衣櫥會比盲目添購成套服裝更靈活。",
        "sections": [
            {
                "heading": "先分出三種正式程度",
                "paragraphs": [
                    "第一層是日常上班：乾淨襯衫、好活動的長褲和低調鞋款就足夠。第二層是對外會議：外套、皮帶、鞋面狀態和襯衫領口會被放大。第三層才是婚禮、面試或重要簡報，需要更完整的正式感。",
                    "把衣櫥按正式程度排好，會知道下一件該補什麼，而不是每次都買一件看似安全的深色上衣。",
                ],
                "bullets": ["日常上班：重視耐穿、好洗、好活動。", "對外會議：重視領口、褲線與鞋面整潔。", "正式場合：重視整體比例與材質一致。"],
            },
            {
                "heading": "襯衫先看領口和肩線",
                "paragraphs": [
                    "襯衫最先被看見的位置，不是花色，而是領口是否服貼、肩線是否落在正確位置。若平日常背包或久坐，袖長和腋下活動量也比布料名稱更早影響舒適度。",
                    "白色、淺藍或細紋襯衫最容易進入通勤衣櫥；想送禮時，建議先確認對方常穿的尺寸與洗滌習慣，再挑款式。",
                ],
                "bullets": ["領口能扣上但不勒。", "肩線不要明顯外滑。", "袖口露出外套一點即可。"],
            },
            {
                "heading": "褲子決定整體是否俐落",
                "paragraphs": [
                    "一件好的通勤褲，不只要看腰圍，也要看坐下、走路、搭車時是否拉扯。西裝褲適合對外場合，休閒長褲適合日常辦公；如果一天中會在辦公室、客戶現場和通勤之間切換，布料彈性和抗皺感會很重要。",
                    "GIBBON 男裝、豪挺紳士西服與 NARMES 可以分別從日常通勤、正式西服和不同版型需求切入。比較時請回到商品頁確認尺寸表、材質和洗滌方式。",
                ],
                "bullets": [],
            },
            {
                "heading": "外套和鞋子是場合開關",
                "paragraphs": [
                    "同一件襯衫和長褲，搭上不同外套與鞋子，正式程度會立刻改變。深色外套適合重要會議，輕薄夾克適合日常通勤；皮鞋或乾淨休閒鞋則會決定整體是否像準備好出門。",
                    "鞋子不一定要多，但需要維持乾淨。若鞋面磨損明顯，即使衣服合身，也會讓正式感下降。",
                ],
                "bullets": ["會議日：外套和皮鞋先準備。", "一般通勤：保持鞋面乾淨比款式更重要。", "婚禮面試：避免臨時穿新鞋上場。"],
            },
            {
                "heading": "建立一套備用正式組合",
                "paragraphs": [
                    "衣櫥裡最好保留一套不用思考就能穿出門的正式組合：襯衫、長褲、外套、皮帶和鞋子都能彼此搭配。它不是每天穿，而是替臨時場合留餘裕。",
                    "這套組合越簡單越好，顏色以白、深藍、灰、黑和咖啡為主，日後再用領帶、包款或外套微調個性。",
                ],
                "bullets": [],
            },
        ],
        "inline": {"eyebrow": "通勤衣櫥", "heading": "先補一套能應急的正式組合", "text": "當襯衫、長褲、外套和鞋子能彼此搭配，臨時會議就不會變成衣櫥壓力。"},
        "ctaText": "先盤點一週最常出現的場合，再從襯衫、褲子、外套與鞋子補齊一套穩定通勤組合。",
        "disclaimer": "商品尺寸、版型、材質與庫存請以下單前商品頁公告為準；送禮前建議先確認對方常穿尺寸與使用情境。",
        "brandReasons": {
            "TP0003817": "可從日常男裝、通勤褲與上衣開始參考。",
            "TP0005310": "適合查看西服、襯衫與正式場合單品。",
            "TP0003665": "可作為不同版型、長褲與上衣需求的補充參考。",
        },
    },
    {
        "slug": "family-weekend-restock-kids-clothes-toys-breakfast",
        "title": "親子家庭的週末補貨清單：童裝、玩具、早餐與兒童用品",
        "category": "lifestyle-culture",
        "audience": "新手爸媽、親子禮物、家庭學習與日用品補貨",
        "items": ["童裝", "玩具", "早餐", "兒童用品"],
        "brands": ["TP0003190", "TP0000485", "TP0006789", "TP0008430", "TP0004495"],
        "cover": "ig_04a46ee67450d745016a18913bf14881968f690318a8338cb5.png",
        "heroAlt": "週末餐桌上整理好的童裝、玩具、早餐點心、水壺與兒童用品",
        "excerpt": "把週末補貨分成衣物、玩具、早餐和出門用品，讓親子家庭少一點臨時採買。",
        "metaDescription": "親子家庭週末補貨指南，整理童裝、玩具、早餐、兒童用品和外出小物的採買順序，適合家庭日常補貨與送禮參考。",
        "intro": "親子家庭的週末，常常不是沒有行程，而是每件事都需要一點準備。童裝要替換、玩具要輪替、早餐要快速上桌，水壺和外出小物也要在出門前找得到。把補貨分成四個抽屜思考，週一早上會輕鬆很多。",
        "sections": [
            {
                "heading": "先補會消耗的，再補可愛的",
                "paragraphs": [
                    "童裝、襪子、內搭、早餐食材和清潔用品，是親子家庭最容易突然不夠的東西。這些物件先補齊，玩具與禮物再慢慢挑，家裡比較不會被臨時需求推著跑。",
                    "如果是替孩子送禮，也建議先問年齡、尺寸和家長偏好。實用不等於無聊，真正會被使用的物品，通常比只打開一次的玩具更有存在感。",
                ],
                "bullets": ["童裝：先看季節、尺寸和好洗程度。", "早餐：選擇容易保存、準備時間短的品項。", "玩具：先看安全標示、年齡與收納方式。"],
            },
            {
                "heading": "童裝用一週行程來排",
                "paragraphs": [
                    "孩子的衣物不只看可愛，也要看一週會遇到的場景：上學、戶外、才藝課、拜訪親友或在家活動。耐洗、好活動、容易搭配，會比單件漂亮更重要。",
                    "週末整理衣櫃時，可以先把明顯不合身或季節不對的衣物收起來，再補真正缺的款式，避免重複買到相似品。",
                ],
                "bullets": ["上學日：舒適、耐洗、好穿脫。", "戶外日：活動量、帽子與備用衣物。", "拜訪日：乾淨整齊，比過度正式更重要。"],
            },
            {
                "heading": "玩具要能輪替，也要能收尾",
                "paragraphs": [
                    "玩具不是越多越好。一次拿出太多，孩子容易分心，大人也很難收拾。比較好的做法，是把玩具分成安靜遊戲、動手操作、角色扮演和外出小物，每次只留一部分在外面。",
                    "花兒朵朵、Arbea 購物、Baby 童衣、包寧安／櫻桃小丸子官方旗艦店與花漾饅頭屋，可以從童裝、玩具、母嬰用品和早餐點心方向延伸；選購時請看適用年齡、成分標示、尺寸和保存方式。",
                ],
                "bullets": [],
            },
            {
                "heading": "早餐和出門用品放在同一條動線",
                "paragraphs": [
                    "週一早晨最怕一邊找襪子，一邊準備早餐。水壺、餐盒、外套、濕紙巾和早餐備品如果能放在固定區域，早上的摩擦會少很多。",
                    "早餐補貨不需要複雜，重點是能快速上桌、保存清楚、家人知道怎麼拿。若涉及過敏、特殊飲食或幼兒食用限制，請優先看標示並依照照顧者判斷。",
                ],
                "bullets": ["外出包固定放補充用品。", "早餐備品標示日期。", "玩具和食物分區收納。"],
            },
            {
                "heading": "週末只做一次小盤點",
                "paragraphs": [
                    "不需要每天整理家庭用品。每週固定 15 分鐘，把衣物、早餐、清潔和外出用品看一輪，就能減少很多臨時補買。",
                    "補貨清單越短越容易持續。先讓家庭日常穩定，再把預算留給真正有紀念感的禮物或親子活動。",
                ],
                "bullets": [],
            },
        ],
        "inline": {"eyebrow": "家庭補貨", "heading": "先穩住週一早晨會用到的東西", "text": "衣物、早餐和外出用品有固定位置，親子家庭的週末會少很多臨時採買。"},
        "ctaText": "先整理家中最常缺的用品，再依童裝、早餐、玩具與外出動線補貨。",
        "disclaimer": "兒童用品、食品與玩具請依商品標示、適用年齡、成分與照顧者判斷選擇；本文不宣稱教養或學習效果。",
        "brandReasons": {
            "TP0003190": "可從親子用品、童裝與禮物方向查看。",
            "TP0000485": "適合比較童裝、玩具與母嬰生活用品。",
            "TP0006789": "可作為童裝、兒童穿搭與季節替換參考。",
            "TP0008430": "適合補充兒童用品與家庭日常備品。",
            "TP0004495": "可從早餐、點心與家庭分享品項方向參考。",
        },
    },
    {
        "slug": "ten-minute-morning-grooming-lip-makeup-kit",
        "title": "早上十分鐘也能整理好：唇膏、妝前保養與日系韓系美妝小物",
        "category": "casual-chic",
        "audience": "上班族、日常保養、送禮、美妝入門讀者",
        "items": ["唇膏", "妝前保養", "美妝小物", "收納包"],
        "brands": ["TP0003331", "TP0005089", "TP0009526", "TP0009171", "TP0007447"],
        "cover": "ig_04a46ee67450d745016a1891837d28819693bca3f230b96647.png",
        "heroAlt": "晨間梳妝台上的唇膏、妝前保養、粉盒、髮夾與小收納包",
        "excerpt": "把早晨儀容拆成唇色、底妝、眉眼和隨身補妝，十分鐘也能出門得體。",
        "metaDescription": "早上十分鐘儀容整理指南，從唇膏、妝前保養、日系韓系美妝小物到隨身補妝包，整理上班日快速出門順序。",
        "intro": "早上真正困難的不是少一支唇膏，而是時間太短、光線太急、桌面太亂。十分鐘儀容整理需要的不是完整妝容，而是一套固定順序：讓膚況看起來乾淨、唇色有精神、髮絲不凌亂，出門後還有簡單補妝的餘地。",
        "sections": [
            {
                "heading": "先決定今天要被看見的重點",
                "paragraphs": [
                    "早晨時間有限，妝容最好只抓一個主角。會議日可以把唇色放前面，拍照日留意底妝與髮絲，外勤日則重視持妝、收納和補擦方便。",
                    "把重點縮小，反而更容易整理好。唇膏、粉餅、眉筆、髮夾和小鏡子只要固定放在同一個盤子或包內，早晨就不用重新找一輪。",
                ],
                "bullets": ["會議日：唇色和眉眼乾淨。", "拍照日：底妝和髮絲服貼。", "外勤日：小包補妝與防曬補擦更重要。"],
            },
            {
                "heading": "妝前保養不要變成全套保養",
                "paragraphs": [
                    "早上的妝前保養重點是讓後續妝容服貼，不需要把夜間保養完整搬過來。清爽、好吸收、能和底妝相容，比堆很多層更實際。",
                    "如果膚況敏感或正在使用特殊保養品，早晨越應該簡化。任何成分效果、修復或改善宣稱，都應回到商品標示與個人狀況評估。",
                ],
                "bullets": ["洗臉後先觀察膚況。", "妝前品項越少越容易穩定。", "新產品不要在重要日早上第一次使用。"],
            },
            {
                "heading": "唇膏是最快的精神開關",
                "paragraphs": [
                    "唇色是十分鐘妝容裡最有效率的部分。日常通勤可選接近原唇色、氣色自然的色調；正式場合再提高一點飽和度。若要送禮，避免只憑流行色，先看對方平常穿搭和膚色偏好。",
                    "傳奇今生唇膏、K-Belle、韓國美妝精選、新幹線 JAPAN 與 KORENA 珂蕾娜，可以從唇彩、日韓彩妝與保養小物方向參考；請以商品頁色號、成分與使用說明為準。",
                ],
                "bullets": [],
            },
            {
                "heading": "補妝包只放會用的五樣",
                "paragraphs": [
                    "隨身補妝包不需要把梳妝台搬出去。小鏡子、唇膏、吸油或面紙、髮夾、旅行尺寸保養或護手用品，通常已經足夠應付半天外出。",
                    "包內品項越少，越容易每天帶出門，也越不會忘記清理過期或沾染的產品。",
                ],
                "bullets": ["小鏡子。", "常用唇膏。", "紙巾或吸油用品。", "髮夾或髮圈。", "小容量護手或保濕用品。"],
            },
            {
                "heading": "讓梳妝台每天晚上歸位",
                "paragraphs": [
                    "十分鐘儀容整理的關鍵，其實在前一晚。把會用的產品放回盤中，髮夾和唇膏不散落在包裡，隔天早上就能省下最混亂的幾分鐘。",
                    "美妝品涉及個人膚況與過敏風險，使用前請依商品標示與自身狀況評估；若有皮膚不適，應停止使用並尋求專業建議。",
                ],
                "bullets": [],
            },
        ],
        "inline": {"eyebrow": "晨間儀容", "heading": "十分鐘只需要一個妝容重點", "text": "唇色、眉眼或底妝選一個主角，早晨會比追求完整妝容更穩。"},
        "ctaText": "先固定早晨會用的五樣小物，再依通勤、會議與外勤日補上合適美妝選擇。",
        "disclaimer": "本文僅供一般美妝與生活整理參考，不構成醫療或皮膚治療建議；商品成分、色號與適用資訊請以商品頁公告為準。",
        "brandReasons": {
            "TP0003331": "可從唇膏、唇彩與送禮色號方向查看。",
            "TP0005089": "適合參考韓系彩妝與保養小物。",
            "TP0009526": "可補充韓國美妝選品與日常妝容用品。",
            "TP0009171": "適合查看日本彩妝與保養用品。",
            "TP0007447": "可作為日常美妝與儀容小物參考。",
        },
    },
    {
        "slug": "simple-skincare-haircare-day-night-routine",
        "title": "保養流程越簡單越要選對：極簡保養、髮品與日夜照護清單",
        "category": "lifestyle-culture",
        "audience": "上班族、日常保養、送禮、美妝入門讀者",
        "items": ["極簡保養", "髮品", "日夜照護", "浴室收納"],
        "brands": ["TP0004588", "TP0001433", "TP0000997", "TP0008542", "TP0004045", "TP0008876"],
        "cover": "ig_04a46ee67450d745016a1891b9ac388196b4b68fc59a2eeab6.png",
        "heroAlt": "明亮浴室與臥室交界處的保養托盤、髮品、毛巾、梳子與夜燈",
        "excerpt": "把保養和髮品拆成早晨、洗後與夜間三段，讓流程簡單但不隨便。",
        "metaDescription": "極簡保養與髮品整理指南，從早晨保養、洗後髮品、夜間照護到浴室收納，建立簡單可持續的日夜流程。",
        "intro": "保養流程越簡單，越需要知道每一步在做什麼。早晨要清爽、夜間要穩定，洗後髮品要好吹整，浴室收納也要讓產品看得見、拿得到。與其追逐複雜步驟，不如建立一套真的會每天完成的日夜節奏。",
        "sections": [
            {
                "heading": "早晨流程只保留必要步驟",
                "paragraphs": [
                    "早晨保養的任務，是讓肌膚和妝容準備好面對一天，而不是完成所有保養願望。清潔、保濕、防曬或妝前準備，依個人習慣簡化即可。",
                    "如果產品太多，最容易發生的是每一瓶都用一點，卻沒有任何一步穩定持續。先固定少數品項，觀察一段時間再調整。",
                ],
                "bullets": ["清潔後先看膚況。", "保濕和防曬依個人需求安排。", "新產品不要一次加入太多。"],
            },
            {
                "heading": "髮品要配合洗後動線",
                "paragraphs": [
                    "髮品最容易被買錯，是因為沒有想清楚洗後會不會使用。免沖洗、造型、護髮或頭皮相關品項，都要放在吹風機、毛巾和梳子附近，才不會被遺忘。",
                    "若早上時間短，前一晚的吹整和收納更重要。把梳子、髮品、髮圈放在同一個區域，隔天就不必在浴室和臥室來回找。",
                ],
                "bullets": ["洗後會用的放浴室出口。", "造型品放梳妝台或外出區。", "開封日期明顯標示。"],
            },
            {
                "heading": "日夜產品不要互相搶位置",
                "paragraphs": [
                    "早晨用品和夜間用品最好分開。早晨重視速度與服貼，夜間重視穩定與舒適；把兩者混在同一個托盤，反而容易拿錯或重複使用。",
                    "OBHL 極簡保養、MEDUSA、Make Friends、ENIE 雅如詩、LOYE 樂妍與 IRIYA，可從保養、髮品與日常美妝照護方向延伸。涉及成分、頭皮、肌膚或敏感狀況時，請以商品標示和個人狀況保守評估。",
                ],
                "bullets": [],
            },
            {
                "heading": "浴室收納要防潮，也要防過期",
                "paragraphs": [
                    "浴室潮濕，產品如果長期堆在角落，容易忘記開封時間和使用狀態。透明盒、分層架和開封貼紙，比漂亮瓶罐更能維持流程。",
                    "若某瓶產品連續兩週沒有被使用，就可以移到觀察區。真正適合自己的流程，不應該每天都像在翻庫存。",
                ],
                "bullets": ["常用品放視線高度。", "備品不要和開封品混放。", "旅行小樣定期清掉。"],
            },
            {
                "heading": "簡單流程也需要停損",
                "paragraphs": [
                    "任何產品只要讓肌膚、頭皮或眼周明顯不適，就不該為了用完而硬撐。保養和髮品都是生活用品，不是越刺激越有效。",
                    "本文只作一般生活整理，不宣稱抗老、修復、改善膚況或治療效果；若有皮膚、頭皮或過敏問題，請諮詢合格專業人員。",
                ],
                "bullets": [],
            },
        ],
        "inline": {"eyebrow": "日夜保養", "heading": "簡單流程要能每天完成", "text": "把早晨、洗後和夜間用品分開放，流程會比堆滿瓶罐更清楚。"},
        "ctaText": "先把早晨、洗後與夜間用品分區，再依實際使用頻率補保養與髮品。",
        "disclaimer": "本文僅供一般保養與生活整理參考，不構成醫療、皮膚治療或個人化建議；若有不適請諮詢合格專業人員。",
        "brandReasons": {
            "TP0004588": "可從極簡保養和日常保養品方向查看。",
            "TP0001433": "適合補充髮品、造型與日常照護用品。",
            "TP0000997": "可作為美妝保養與日常選品參考。",
            "TP0008542": "適合查看專業髮品和洗後照護用品。",
            "TP0004045": "可從保養、美妝與日常照護方向參考。",
            "TP0008876": "適合補充保養、髮品與儀容用品。",
        },
    },
    {
        "slug": "home-care-supplies-medical-aid-consumables",
        "title": "家裡有人需要照護時，先整理哪些用品：醫材通路、輔具與生活消耗品",
        "category": "wellness-movement",
        "audience": "照護家庭、久坐上班族、輕運動與長輩用品讀者",
        "items": ["照護用品", "輔具", "醫材通路", "生活消耗品"],
        "brands": ["TP0004194", "TP0005998", "TP0007439", "TP0005096"],
        "cover": "ig_04a46ee67450d745016a18923cf5f081969bbc5b587c0b7c74.png",
        "heroAlt": "居家桌面上整理好的口罩、酒精、收納籃、輔助握把、筆記本與照護用品",
        "excerpt": "照護用品先分成安全動線、日常消耗、清潔防護與專業確認，家裡才不會被臨時需求打亂。",
        "metaDescription": "居家照護用品整理指南，從醫材通路、輔具、口罩酒精、生活消耗品到家庭動線，建立保守安全的採買順序。",
        "intro": "當家裡有人需要照護，最急的通常不是買最多用品，而是先讓動線安全、消耗品找得到、清潔防護不斷貨。照護採買牽涉每個人的身體狀況與居家格局，不能用單一清單套用；這篇只整理家庭可以先盤點的方向，專業判斷仍應交給醫師、護理師、藥師或治療師。",
        "sections": [
            {
                "heading": "先盤點家裡的三條路線",
                "paragraphs": [
                    "第一條是起身到浴室，第二條是床邊到餐桌，第三條是玄關到外出。這三條路線若有地墊、雜物、電線或光線不足，輔具買再多也未必能真正降低照護壓力。",
                    "先整理路線，再看是否需要扶手、防滑、夜燈、收納籃或移動輔助。任何涉及安裝、承重或身體支撐的用品，都建議先詢問專業人員。",
                ],
                "bullets": ["床邊到浴室：光線與防滑優先。", "餐桌到客廳：移除電線與低矮障礙。", "玄關到外出：鞋子、雨具與輔具固定位置。"],
            },
            {
                "heading": "消耗品要有固定補貨量",
                "paragraphs": [
                    "口罩、酒精、手套、清潔用品、紙巾、濕紙巾或照護墊等消耗品，最怕一下子不夠，也怕過度囤積後忘記期限。家庭可以用一週或兩週為單位建立安全庫存。",
                    "標籤比收納盒更重要。每個人都知道哪一盒已開封、哪一盒是備品，照護者交接時會少很多口頭說明。",
                ],
                "bullets": ["開封品和備品分開。", "標示期限和補貨日期。", "容易拿取，但不要散落各處。"],
            },
            {
                "heading": "醫材與輔具先看適用情境",
                "paragraphs": [
                    "醫材和輔具不適合只看照片或價格。尺寸、承重、材質、清潔方式、是否需專業調整，都會影響能不能安心使用。",
                    "里享生活醫材、強哥批發、富達醫材與志遠書局，可以從醫材通路、生活防護用品、照護器材與相關書籍資訊方向參考；選購前請回到商品頁標示與專業建議確認。",
                ],
                "bullets": [],
            },
            {
                "heading": "把照護筆記放在用品旁邊",
                "paragraphs": [
                    "照護家庭常有多人輪流協助。比起每次口頭交代，一本放在用品旁的筆記本更可靠：記錄補貨、使用方式、注意事項、專業人員提醒與下次回診問題。",
                    "這份筆記不是醫療紀錄的替代品，而是讓家庭成員知道日常用品怎麼拿、何時補、哪些情況要詢問專業人員。",
                ],
                "bullets": ["記錄用品位置。", "記錄開封和補貨日期。", "記錄需要詢問專業人員的問題。"],
            },
            {
                "heading": "不要用採買取代專業判斷",
                "paragraphs": [
                    "照護用品的目標，是讓日常更有秩序，不是保證安全、治療或改善身體狀況。若涉及跌倒風險、傷口、慢性病、復健、營養或用藥，請先諮詢合格專業人員。",
                    "採買時保持保守，先買真正會用、能正確清潔、能被家人理解的用品，再依照實際照護情況調整。",
                ],
                "bullets": [],
            },
        ],
        "inline": {"eyebrow": "居家照護整理", "heading": "先整理動線，再補用品", "text": "照護採買應該服務家裡的真實路線，而不是用一張清單套所有家庭。"},
        "ctaText": "先盤點床邊、浴室與玄關動線，再依專業建議補齊消耗品與輔助用品。",
        "disclaimer": "本文僅供一般生活資訊與照護用品整理參考，不構成醫療、復健、用藥或個人化建議；若涉及健康、照護、傷口、跌倒風險或輔具使用，請先諮詢合格專業人員。",
        "brandReasons": {
            "TP0004194": "可從醫材通路與居家照護用品方向查看。",
            "TP0005998": "適合補充口罩、酒精、生活防護與消耗用品。",
            "TP0007439": "可作為醫材與照護相關用品參考。",
            "TP0005096": "適合查看照護、健康書籍與部分保健器材資訊。",
        },
    },
    {
        "slug": "phone-accessory-commute-car-charging-desk",
        "title": "手機不是只要保護殼：通勤、車用、充電與桌面的配件整理法",
        "category": "ai-innovation",
        "audience": "手機使用者、通勤族、手機拍攝與桌面控",
        "items": ["手機殼", "保護貼", "充電", "車用配件"],
        "brands": ["TP0000669", "TP0009160", "TP0007239", "TP0009130", "TP0006731"],
        "cover": "ig_04a46ee67450d745016a1892885cc8819694fd8ea80f76d37c.png",
        "heroAlt": "通勤桌面上的手機殼、保護貼、充電線、車用支架、行動電源與耳機盒",
        "excerpt": "手機配件先依通勤、車用、充電和桌面四個場景整理，保護殼只是第一步。",
        "metaDescription": "手機配件整理指南，從手機殼、保護貼、充電線、車用支架、桌面支架與行動電源，建立通勤和工作桌的配件系統。",
        "intro": "手機每天跟著我們通勤、開會、導航、付款和拍照，卻常常只被當成保護殼問題。真正好用的手機配件，應該把通勤、車用、充電與桌面四個場景一起看，讓線材、支架和保護用品都回到固定位置。",
        "sections": [
            {
                "heading": "先分清楚手機在哪裡被使用",
                "paragraphs": [
                    "通勤時需要好拿、防滑和不怕臨時收進包裡；車用情境需要穩定固定和不遮視線；工作桌需要充電、支架和螢幕角度；外出拍攝則需要電量和收納。",
                    "這四個場景不該用同一個配件解決。先把需求分開，才不會買到看起來很多功能、實際上每個位置都不好用的東西。",
                ],
                "bullets": ["通勤：防滑、輕薄、好拿取。", "車用：穩定固定，不妨礙視線。", "桌面：角度、充電與線材整潔。", "拍攝：電量、收納與握持。"],
            },
            {
                "heading": "保護殼和保護貼先看習慣",
                "paragraphs": [
                    "保護殼不是越厚越安心。常放口袋的人需要輕薄，常放包裡的人要看邊角保護，常拍照的人則要留意鏡頭開孔和握持手感。",
                    "保護貼則要看觸控、反光和清潔習慣。若你常在戶外或捷運上使用手機，抗反光和指紋清潔會比包裝上的形容詞更有感。",
                ],
                "bullets": ["口袋使用：薄、滑順、不刮手。", "包內使用：邊角保護與好清潔。", "拍攝使用：鏡頭區域與握持感。"],
            },
            {
                "heading": "充電系統要少線，不能亂線",
                "paragraphs": [
                    "桌面上最容易失控的是充電線。手機、耳機、行動電源和手錶如果各用一條線，桌面很快就會亂。先決定固定充電區，再選線長、支架和收納方式。",
                    "手些小子3C、TG3C、muni 3C、AiHome 與湯米3C，可以從手機殼、保護貼、充電、支架和 Apple 周邊方向參考；規格相容性請以下單前商品頁標示為準。",
                ],
                "bullets": [],
            },
            {
                "heading": "車用配件先看安全位置",
                "paragraphs": [
                    "車用支架不應遮擋視線或影響操作。安裝位置、固定方式、手機大小和充電線走向，都要先在車內模擬一次。",
                    "若不是開車，也可以把車用思維換成通勤包：耳機盒、行動電源、短線和手機支架放在同一個小袋，移動時會更穩。",
                ],
                "bullets": ["支架不要擋視線。", "線材不要干擾排檔或手部操作。", "通勤小袋固定放電源與短線。"],
            },
            {
                "heading": "每週整理一次配件袋",
                "paragraphs": [
                    "手機配件最容易默默變多。每週把包裡、車上和桌面線材倒出來看一次，留下真正會用的線和轉接頭，其餘放回備品區。",
                    "不要假設所有配件都相容。充電功率、接頭、磁吸、手機尺寸和保護殼厚度，都請回到商品頁規格確認。",
                ],
                "bullets": [],
            },
        ],
        "inline": {"eyebrow": "手機配件系統", "heading": "保護、充電、固定要分開想", "text": "一支手機會出現在不同場景，配件也應該各自有任務和收納位置。"},
        "ctaText": "先分出通勤、車用、桌面和拍攝四個場景，再補保護殼、充電與支架配件。",
        "disclaimer": "商品相容性、規格、功率、尺寸與庫存請以下單前商品頁公告為準；本文未進行個別商品實測。",
        "brandReasons": {
            "TP0000669": "可從 Apple 周邊、手機殼與保護貼方向查看。",
            "TP0009160": "適合比較手機配件、保護與充電用品。",
            "TP0007239": "可補充手機與平板周邊配件。",
            "TP0009130": "適合查看充電、桌面與智慧生活配件。",
            "TP0006731": "可作為手機殼、線材與日常配件參考。",
        },
    },
    {
        "slug": "seasonal-bedding-tencel-cotton-protector-guide",
        "title": "床包不是看花色而已：天絲、純棉、涼被與保潔墊的換季順序",
        "category": "lifestyle-culture",
        "audience": "重視居家舒適、剛搬家、換季整理讀者",
        "items": ["床包", "涼被", "保潔墊", "枕套"],
        "brands": ["TP0001300", "TP0001106", "TP0007471", "TP0002795", "TP0003841"],
        "cover": "ig_04a46ee67450d745016a1892e7dc548196becd336c6fe56899.png",
        "heroAlt": "明亮臥室裡正在更換的床包、純棉寢具、涼被、枕套與保潔墊",
        "excerpt": "換季寢具先看床墊尺寸、材質觸感、清洗頻率和收納空間，再決定花色。",
        "metaDescription": "換季寢具選購指南，整理天絲、純棉、涼被、保潔墊、床包和枕套的更換順序，適合剛搬家和居家整理讀者。",
        "intro": "床包不是只看花色。真正影響日常的是材質觸感、床墊尺寸、清洗頻率和收納空間。換季時先把這些條件整理好，再看顏色和風格，臥室會更容易維持乾淨，也不會買到漂亮但難照顧的寢具。",
        "sections": [
            {
                "heading": "先確認床墊尺寸和厚度",
                "paragraphs": [
                    "床包最常買錯的原因，是只看單人、雙人或加大，卻忘了床墊厚度。若床墊較厚、加了保潔墊或薄墊，床包包覆深度就會影響是否容易鬆脫。",
                    "買之前先量長、寬、高，再看商品頁尺寸。這一步比挑花色更重要，因為尺寸不對的床包，每次整理床都會讓人煩躁。",
                ],
                "bullets": ["量床墊長寬高。", "確認是否有加薄墊或保潔墊。", "看床包可包覆高度。"],
            },
            {
                "heading": "材質要對應季節與清洗習慣",
                "paragraphs": [
                    "天絲、純棉、涼感或磨毛材質，各有不同觸感與維護方式。容易流汗、家中有孩子或寵物、洗衣頻率高的人，更要把清洗和乾燥速度放在花色前面。",
                    "涼被也不必一次買很多條。先確認夏季是否需要冷氣房、午睡、客用或旅行備用，再決定厚薄和收納方式。",
                ],
                "bullets": ["夏季：透氣、好洗、快乾優先。", "冷氣房：留意涼被厚薄。", "客用：收納體積和清潔頻率優先。"],
            },
            {
                "heading": "保潔墊是維護，不是裝飾",
                "paragraphs": [
                    "保潔墊的重點是延長床墊日常維護的彈性，不是用來改變睡眠品質。選擇時要看包覆方式、清洗方式、是否容易悶熱，以及和床包是否能一起固定。",
                    "Arvo Home、久賴家居、夢露家居、宜室家居與日創家居，可以從床包、被套、涼被、枕套與保潔墊方向參考；材質、尺寸和洗滌方式請以商品頁標示為準。",
                ],
                "bullets": [],
            },
            {
                "heading": "枕套和床包可以先同色系",
                "paragraphs": [
                    "臥室要看起來安定，不一定要全套同花色。先選一個主色，再讓枕套、床包和涼被維持相近色階，房間會比混搭很多圖案更清爽。",
                    "如果家裡收納有限，建議每張床先準備兩組床包枕套輪替，再依季節補一條涼被或薄被。數量少但輪替清楚，會比堆滿櫃子更好維護。",
                ],
                "bullets": ["一組使用，一組清洗輪替。", "枕套可多備一組。", "換季前先清點舊寢具。"],
            },
            {
                "heading": "收納前先確認完全乾燥",
                "paragraphs": [
                    "寢具收納最怕濕氣。換季前務必確認完全乾燥，再用透氣收納袋或固定櫃位保存，避免隔季拿出來才發現異味或泛黃。",
                    "本文不宣稱任何寢具能改善睡眠或健康狀況；選購應回到材質、尺寸、清潔與個人觸感偏好。",
                ],
                "bullets": [],
            },
        ],
        "inline": {"eyebrow": "換季寢具", "heading": "尺寸和清洗頻率，比花色更先決定答案", "text": "床包合不合、涼被好不好洗，會比照片裡的顏色更影響每天使用。"},
        "ctaText": "先量床墊、整理清洗頻率，再依季節挑床包、涼被與保潔墊。",
        "disclaimer": "本文僅供一般居家整理與選購參考，不宣稱寢具能改善睡眠或健康；商品材質、尺寸與洗滌方式請以商品頁公告為準。",
        "brandReasons": {
            "TP0001300": "可從床包、枕套、被套與家飾用品方向查看。",
            "TP0001106": "適合比較天絲床包、涼被、棉被與枕頭。",
            "TP0007471": "可補充床包、被套、涼被與保潔墊選項。",
            "TP0002795": "適合查看床包、兩用被與寢具組合。",
            "TP0003841": "可作為床包、被套、保潔墊與涼被參考。",
        },
    },
    {
        "slug": "rental-home-refresh-sticker-light-storage",
        "title": "不用裝潢，也能讓租屋處變好住：貼皮、燈具、收納與日用小物清單",
        "category": "lifestyle-culture",
        "audience": "租屋族、小宅家庭、剛搬家讀者",
        "items": ["貼皮", "燈具", "收納", "日用小物"],
        "brands": ["TP0009317", "TP0008153", "TP0004819", "TP0009671", "TP0008643", "TP0001200"],
        "cover": "ig_04a46ee67450d745016a189329efc081968f5e9fcb5a49c15b.png",
        "heroAlt": "小型租屋房間裡的貼皮樣本、桌燈、收納籃、量尺、掛鉤與生活小物",
        "excerpt": "租屋改造先抓可逆、低破壞、好清潔三個原則，再補貼皮、燈具和收納。",
        "metaDescription": "租屋改造與小宅生活指南，整理貼皮、燈具、收納、掛鉤與日用小物的低破壞採買順序，適合剛搬家讀者。",
        "intro": "租屋處要變好住，不一定要裝潢。真正能改變日常感受的，常常是桌面光線、入口收納、牆面髒污和小物歸位。只要遵守可逆、低破壞、好清潔三個原則，租屋生活也能慢慢變得順手。",
        "sections": [
            {
                "heading": "先拍下最困擾的三個角落",
                "paragraphs": [
                    "剛搬家時不要急著買滿。先拍下玄關、工作桌和床邊三個最常用角落，觀察哪裡最暗、哪裡最亂、哪裡最常堆東西。照片會比想像更誠實。",
                    "如果問題是光線，先看燈具；如果問題是表面老舊，再看貼皮；如果問題是東西沒有家，收納會比裝飾更早出場。",
                ],
                "bullets": ["玄關：鞋、鑰匙、雨傘先有位置。", "工作桌：光線、插座和線材先整理。", "床邊：夜燈、書本和充電用品固定歸位。"],
            },
            {
                "heading": "貼皮先做小面積測試",
                "paragraphs": [
                    "貼皮適合修飾桌面、櫃面或局部牆面，但租屋處要先確認能否移除、是否傷材質，以及房東或合約是否允許。先用小面積測試，比一開始貼滿整面更安全。",
                    "施工時也要留意清潔、裁切和邊角收尾。若表面潮濕、粉化或凹凸太多，貼皮效果可能不如預期，這時應先處理清潔與穩定性。",
                ],
                "bullets": ["先讀租約與房東規定。", "小面積試貼。", "保留移除和修復空間。"],
            },
            {
                "heading": "燈具改變房間使用方式",
                "paragraphs": [
                    "租屋照明常常只有一盞頂燈，工作、閱讀、吃飯和休息都被迫使用同一種光。增加桌燈、立燈或小夜燈，可以讓不同活動有不同亮度，而不是只靠裝飾品改變氣氛。",
                    "靚點燈飾、XINGMU 興沐與趁財財燈飾可從吸頂燈、桌燈、立燈和照明小物方向延伸；選購時請確認尺寸、安裝方式、用電需求與租屋可否更換。",
                ],
                "bullets": [],
            },
            {
                "heading": "收納要先服務動線",
                "paragraphs": [
                    "收納不是把所有東西藏起來，而是讓常用物能回到固定位置。玄關放外出物、桌邊放文具和充電、床邊放睡前用品，分區清楚後，房間自然會安靜很多。",
                    "Urban Nest 悠巢、藍貓 BlueCat 與奇米家，可以從居家用品、收納、貼皮和日用小物方向參考；比較時先看尺寸、承重、材質與清潔方式。",
                ],
                "bullets": ["常用物放外面，但要有容器。", "備品放櫃內，標示清楚。", "不要用大型收納遮住插座或通道。"],
            },
            {
                "heading": "租屋改造要保留退場方式",
                "paragraphs": [
                    "好的租屋改造，搬走時也能收尾。可移動家具、可拆掛鉤、可清潔貼皮和不傷牆的照明，比一次做很重的改造更適合多數租屋生活。",
                    "下手前先量尺寸、拍原始狀態、保存商品說明。讓房間變好住，也要讓未來搬家時不增加麻煩。",
                ],
                "bullets": [],
            },
        ],
        "inline": {"eyebrow": "租屋更新", "heading": "先讓常用角落變順手", "text": "光線、收納和表面整理做好，租屋處會比添很多裝飾更好住。"},
        "ctaText": "先拍下玄關、工作桌與床邊，再依光線、表面和收納三條線補上可逆小物。",
        "disclaimer": "租屋改造請先確認租約、房東規定、安裝方式與可移除性；商品尺寸、材質與使用限制請以商品頁公告為準。",
        "brandReasons": {
            "TP0009317": "可從 DIY 貼皮與表面更新方向查看。",
            "TP0008153": "適合比較吸頂燈、LED 照明與房間光源。",
            "TP0004819": "可補充燈飾、桌燈與空間照明選項。",
            "TP0009671": "適合查看燈具與照明小物。",
            "TP0008643": "可從居家收納與生活用品方向參考。",
            "TP0001200": "適合補充家居生活館小物與收納用品。",
        },
    },
]


SECTION_EXTRAS: dict[str, list[str]] = {
    "mens-commute-shirt-trousers-jacket-shoes": [
        "若衣櫥目前只有休閒服，第一件不必追求華麗，而是挑一件能搭三種褲子的襯衫。它能出現在週一會議，也能在週五晚餐不顯得太正式。",
        "褲長也是常被忽略的細節。褲腳堆太多會顯得拖沓，太短則容易讓正式感下降；若不確定，先選能修改褲長的款式會更有彈性。",
        "外套則可以先用季節來分。春夏重視薄、挺和不悶，秋冬再看內搭空間；這樣同一件外套才不會只在少數場合出現。",
        "真正能留下來的通勤單品，通常不是最搶眼的那件，而是洗後好整理、早上好搭配、坐一整天也不彆扭的那件。這種標準看似樸素，卻最接近每天會穿出門的現實，也最能減少臨時出門前的猶豫。",
    ],
    "family-weekend-restock-kids-clothes-toys-breakfast": [
        "週末補貨也可以把孩子一起納入整理流程。讓孩子知道玩具放哪裡、早餐備品在哪一層，日常會慢慢形成可預期的節奏。",
        "若家中有不同年齡的孩子，用品更要分層。大孩子的文具和小玩具，不應和幼兒會放入口中的物件混在同一個籃子裡。",
        "外出用品也可以固定成一個小袋：濕紙巾、備用衣物、餐具和小玩具分層放，臨時出門時不必重新準備。",
    ],
    "ten-minute-morning-grooming-lip-makeup-kit": [
        "如果辦公室光線偏白，早晨可以先在窗邊確認唇色和底妝邊界。自然光下看起來舒服，通常比浴室黃光下的濃度更適合白天。",
        "補妝包也需要定期清理。唇膏蓋、粉盒邊緣和小鏡子若長期沾染，會讓每天出門前的儀容感打折。",
        "送禮時則建議避開太個人化的底妝色號，改選唇彩、手部保養或實用小物，踩雷機率會低很多。",
        "如果早晨常常趕時間，可以把會用到的產品按順序排成一列，而不是全部放進抽屜。視線先看到的物品越少，越容易在有限時間內完成，也更容易維持乾淨。",
    ],
    "simple-skincare-haircare-day-night-routine": [
        "如果你經常出差或健身，建議另外準備一組小容量旅行包。它不必完整，只要能支撐清潔、保濕和洗後整理，回家後再回到日常流程。",
        "頭髮和臉部用品也不一定要放在一起。把髮品靠近吹風機，保養品靠近鏡子，使用動作會自然很多，也更容易持續。",
        "想送保養或髮品時，最好選擇對方已熟悉的品類或較低敏感度的小物，不要把高濃度、強功能感產品當成驚喜，對方也比較容易自然用進日常。",
        "日夜流程也可以用顏色或托盤區分。早晨托盤放清爽、快速、出門前會用的品項；夜間托盤放洗後、吹整後或睡前會用的品項，視覺上清楚，手就不容易拿錯。",
        "如果家裡浴室潮濕，保養品不一定都適合長期放浴室。可以把備品移到乾燥櫃位，只留下當週會用的瓶罐，減少受潮與重複購買，也讓台面維持清爽。",
    ],
    "home-care-supplies-medical-aid-consumables": [
        "照護用品也要考慮照護者的動線。若每次拿手套、酒精或毛巾都要彎腰翻找，長期下來也會增加疲勞。",
        "家庭成員之間最好約定一個補貨訊號，例如剩下一週用量就寫在筆記本。這比等到完全用完才臨時採買更穩。",
        "若用品需要多人操作，請把商品說明保留在同一個收納區。看得到使用限制，比憑印象操作更安全。",
    ],
    "phone-accessory-commute-car-charging-desk": [
        "如果你常用手機當工作輔助螢幕，桌面支架高度要讓視線自然落下，不要讓脖子長時間前傾。這是使用姿勢問題，不是支架越高越好。",
        "行動電源也要跟包款一起想。每天背小包的人，需要的是穩定和輕量；長時間外出的人，才需要把容量放得更前面。",
        "保護貼和手機殼最好一起確認。殼太厚、邊框太高或保護貼太滿版，都可能影響彼此密合度。",
        "若你經常換手機殼，充電支架和車架更要先確認厚度容忍度。能不用拆殼就完成充電、導航或桌面查看，才是真正每天會用的配置。",
        "也別忽略備用線材的標示。家裡、公司、車上各放一條用途明確的線，比把所有線丟在同一個抽屜更好管理。",
    ],
    "seasonal-bedding-tencel-cotton-protector-guide": [
        "換季時也要看洗衣條件。家中如果沒有烘衣設備，厚重被品就要更重視晾乾時間和收納空間。",
        "枕頭和枕套的搭配也會影響整潔感。枕套若太鬆或太緊，即使花色漂亮，床面也容易看起來凌亂。",
        "如果臥室濕氣重，寢具數量更不宜過多。少量輪替、完全乾燥後再收納，會比囤滿整櫃更實際。",
    ],
    "rental-home-refresh-sticker-light-storage": [
        "租屋改造最值得先處理的是每天碰到的表面：桌面、床邊、玄關和廚房小檯面。這些地方變順手，生活感受會比裝飾牆面更快改善。",
        "若預算有限，先買能移動到下一個家的物件。燈具、收納籃、小桌和掛鉤通常比固定式改造更適合租屋生活。",
        "拍照紀錄也很重要。改造前後都留下照片，未來退租或恢復原狀時，會比只靠記憶更清楚。",
        "如果房間採光不足，先用桌燈和立燈補出活動區，再決定是否需要貼皮或裝飾。光線改善後，很多原本看起來雜亂的角落會更容易整理。",
        "小宅也要保留空白面。每一面牆都掛滿收納，反而會讓房間更壓迫；留出一塊乾淨牆面，視覺上會更像真正能休息的家。",
    ],
}


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
    return {
        "name": f"{brand} 選物頁",
        "merchantId": row["merchant_id"],
        "brandName": brand,
        "affiliateUrl": promo or store,
        "sourceProductUrl": store,
        "imageCredit": f"圖片來源：momo 店家頁｜{brand}",
        "selectionReason": reason,
        "riskNote": "價格、規格、活動與庫存請以下單前商品頁公告為準。",
        "subId": f"{article_slug}_{row['merchant_id']}",
    }


def prepare_cover(article: dict[str, Any]) -> str:
    source = GENERATED_IMAGE_DIR / article["cover"]
    if not source.exists():
        raise FileNotFoundError(f"Missing generated cover source: {source}")
    target = ROOT / "images" / "optimized" / "article-covers" / f"{article['slug']}.jpg"
    with Image.open(source) as image:
        image = ImageOps.fit(image.convert("RGB"), (1200, 630), method=Image.Resampling.LANCZOS)
        image.save(target, "JPEG", quality=92, optimize=True)
    sha = hashlib.sha256(target.read_bytes()).hexdigest()
    manifest = json.loads(COVER_MANIFEST.read_text(encoding="utf-8")) if COVER_MANIFEST.exists() else {}
    manifest.setdefault("version", 1)
    manifest["updatedAt"] = "2026-05-28T00:00:00-07:00"
    manifest["generator"] = manifest.get("generator") or "codex-imagegen-built-in"
    manifest.setdefault("covers", {})
    manifest["covers"][article["slug"]] = {
        "image": pipeline.relative_to_root(target),
        "source": str(source),
        "sha256": sha,
        "promptSummary": article["heroAlt"],
    }
    pipeline.write_json(COVER_MANIFEST, manifest)
    return pipeline.relative_to_root(target)


def build_article(spec: dict[str, Any], rows_by_merchant: dict[str, dict[str, str]], config: dict[str, Any], categories: dict[str, pipeline.CategoryConfig]) -> dict[str, Any]:
    brand_rows = [rows_by_merchant[mid] for mid in spec["brands"]]
    cards = [merchant_card(row, spec["slug"], spec["brandReasons"].get(row["merchant_id"], "可依商品頁資訊與實際使用情境比較。")) for row in brand_rows]
    category = categories[spec["category"]]
    hero_image = prepare_cover(spec)
    sections = [
        {**section, "paragraphs": list(section.get("paragraphs", [])), "bullets": list(section.get("bullets", []))}
        for section in spec["sections"]
    ]
    extras = SECTION_EXTRAS.get(spec["slug"], [])
    for index, paragraph in enumerate(extras):
        sections[min(index, len(sections) - 1)]["paragraphs"].append(paragraph)
    article = {
        "slug": spec["slug"],
        "category": spec["category"],
        "title": spec["title"],
        "excerpt": spec["excerpt"],
        "tags": [category.label, "生活採買", spec["items"][0], spec["items"][-1]],
        "metaTitle": f"Elite Fashion｜{spec['title'][:48]}",
        "metaDescription": spec["metaDescription"],
        "series": "通勤儀容、家庭補貨、照護與居家更新指南",
        "listingTitle": spec["title"],
        "listingExcerpt": spec["excerpt"],
        "heroImage": hero_image,
        "heroImageAlt": spec["heroAlt"],
        "intro": spec["intro"],
        "sections": sections,
        "faq": [
            {
                "question": "這篇文章適合直接照單購買嗎？",
                "answer": "不建議。每個家庭、通勤路線、身形、膚況或空間條件都不同，請先用文中的順序盤點自己的使用情境，再回到商品頁確認規格。",
            },
            {
                "question": "商品價格、活動或庫存可以以本文為準嗎？",
                "answer": "不可以。價格、活動、庫存、規格、尺寸與配送條件都可能變動，請以下單前看到的商品頁或店家頁公告為準。",
            },
            {
                "question": "涉及保養、照護、兒童或健康用品時要注意什麼？",
                "answer": "請把本文視為一般生活整理與選購情境參考；若涉及健康、照護、皮膚、兒童食用或輔具使用，應優先看商品標示並諮詢合格專業人員。",
            },
        ],
        "extendedReading": [
            {"title": f"瀏覽更多{category.label}文章", "url": f"/{category.page}"},
            {"title": "查看生活品味文章", "url": "/lifestyle-culture.html"},
            {"title": "查看站內搜尋", "url": "/search.html"},
        ],
        "cta": {
            "variant": "gold",
            "text": spec["ctaText"],
            "links": [{"label": f"查看 {row['brand']}", "url": row.get("promo_link") or row.get("store_link")} for row in brand_rows[:4]],
        },
        "inlineCtas": [
            {
                "afterSection": 2,
                "variant": "olive",
                "eyebrow": spec["inline"]["eyebrow"],
                "heading": spec["inline"]["heading"],
                "text": spec["inline"]["text"],
                "links": [{"label": cards[0]["name"], "url": cards[0]["affiliateUrl"]}, {"label": cards[1]["name"], "url": cards[1]["affiliateUrl"]}],
            }
        ],
        "disclaimer": spec["disclaimer"],
        "audience": spec["audience"],
        "readTimeMinutes": 9,
        "sourceType": "manual-codex-momo-new-audience-affiliate",
        "status": "published",
        "queueId": QUEUE_ID,
        "mainProducts": cards[:4],
        "sidebarProducts": cards[4:],
        "featuredBrands": [
            {
                "name": row["brand"],
                "merchantId": row["merchant_id"],
                "role": "品牌參考",
                "reason": spec["brandReasons"].get(row["merchant_id"], "可依商品頁資訊與實際使用情境比較。"),
                "url": row.get("promo_link") or row.get("store_link"),
            }
            for row in brand_rows
        ],
    }
    saved = pipeline.save_generated_article(article, QUEUE_ID, config, categories)
    pipeline.validate_generated_article(saved, config)
    saved["authenticityReview"] = pipeline.run_authenticity_review(saved, config)
    pipeline.write_json(ROOT / config["paths"]["generatedArticlesDir"] / f"{saved['slug']}.json", saved)
    pipeline.append_publish_log(config, saved, trigger_type=TRIGGER_TYPE, queue_id=QUEUE_ID)
    return saved


def update_queue(articles: list[dict[str, Any]], config: dict[str, Any]) -> None:
    path = ROOT / config["paths"]["queueJson"]
    queue = pipeline.load_json(path)
    by_slug = {article["slug"]: article for article in articles}
    for series in queue["series"]:
        if series["queueId"] != QUEUE_ID:
            continue
        for item in series["items"]:
            article = by_slug.get(item.get("slug"))
            if article:
                item["status"] = "published"
                item["articleId"] = article["id"]
                item["file"] = article["file"]
                item["publishedAt"] = article["publishedAt"]
        series["status"] = "completed" if all(item["status"] == "published" for item in series["items"]) else "in_progress"
        queue["updatedAt"] = pipeline.now_iso()
        pipeline.write_json(path, queue)
        return
    raise RuntimeError(f"Missing queue series: {QUEUE_ID}")


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
        for article in hits:
            if article["slug"] not in existing_slugs:
                existing_slugs.append(article["slug"])
            if article["url"] not in existing_urls:
                existing_urls.append(article["url"])
        row["article_slug"] = ";".join(existing_slugs)
        row["live_url"] = ";".join(existing_urls)
        row["mention_count"] = str(int(row.get("mention_count") or 0) + len(hits))
        row["last_mentioned_at"] = TODAY
        note = "2026-05-28 momo 新受眾第二批通勤家庭照護文章已置入。"
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


def main() -> int:
    config, categories = pipeline.load_config()
    tracker_rows, rows_by_merchant, fieldnames = load_tracker()
    missing = sorted({mid for spec in ARTICLES for mid in spec["brands"] if mid not in rows_by_merchant})
    if missing:
        raise SystemExit(f"Tracker missing merchants: {', '.join(missing)}")
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
    print(f"Generated {len(articles)} Q-0014 momo new-audience articles:")
    for article in articles:
        print(f"- {article['slug']} -> {article['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
