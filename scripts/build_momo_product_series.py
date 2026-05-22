#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

import content_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[1]
SOURCE_XLSX = ROOT / "momo首批600商品.xlsx"
TRACKER_CSV = ROOT / "automation" / "momo-brand-recommendation-tracker.csv"
IMAGE_CACHE = ROOT / "automation" / "momo-product-image-cache.json"
CODEX_GENERATED_COVER_MANIFEST = ROOT / "automation" / "codex-generated-cover-manifest.json"
TODAY = "2026-05-22"
TRIGGER_TYPE = "manual-codex-momo-product-affiliate-no-newsletter"
BAD_IMAGE_CODES = {
    "TP00066690016472",
    "TP00066690016603",
}


MERCHANT_META: dict[str, dict[str, Any]] = {
    "TP0005709": {
        "brand": "藤木居家具",
        "grade": "B",
        "score": "70.0",
        "products": "收納箱、鞋櫃、換鞋凳、書桌、衣物整理櫃",
        "angle": "小宅收納、玄關動線、工作角落家具、租屋家具清單",
        "theme": "home-ritual-lifestyle",
        "role": "推薦店家",
        "source": "居家_家具_寢具_收納",
    },
    "TP0003625": {
        "brand": "☁凌雲家居",
        "grade": "B",
        "score": "70.0",
        "products": "收納櫃、鞋盒、桌面收納、透明整理箱、餐桌書桌",
        "angle": "租屋整理、衣櫃分類、桌面秩序、玄關鞋盒配置",
        "theme": "home-ritual-lifestyle",
        "role": "推薦店家",
        "source": "居家_家具_寢具_收納",
    },
    "TP0007407": {
        "brand": "RED HOUSE 家具工廠",
        "grade": "B",
        "score": "73.0",
        "products": "床底收納、雨傘架、鞋櫃、辦公桌椅、玩具收納",
        "angle": "玄關收納、工作桌椅、臥室整理、家庭收納清單",
        "theme": "home-ritual-lifestyle",
        "role": "推薦店家",
        "source": "居家_家具_寢具_收納",
    },
    "TP0002179": {
        "brand": "888便利購 兒童玩具專賣店",
        "grade": "A",
        "score": "82.0",
        "products": "拼圖、迷宮球、風箏、磁性畫板、桌遊與遊戲組",
        "angle": "家庭禮物、週末共玩、親子桌面活動、玩具收納搭配",
        "theme": "family-parenting-future",
        "role": "推薦店家",
        "source": "親子_母嬰_玩具",
    },
    "TP0004379": {
        "brand": "凱莎精選家具城",
        "grade": "B",
        "score": "68.0",
        "products": "廚房架、椅凳、桌子、床頭櫃、置物架",
        "angle": "廚房垂直收納、租屋輕家具、餐廚整理",
        "theme": "home-ritual-lifestyle",
        "role": "推薦店家",
        "source": "居家_家具_寢具_收納",
    },
    "TP0006348": {
        "brand": "LamiFans",
        "grade": "A",
        "score": "87.0",
        "products": "耳掛式耳罩、3C小物、客製禮品",
        "angle": "工作角落配件、會議與專注場景、小型禮品搭配",
        "theme": "creator-work-gear",
        "role": "推薦店家",
        "source": "家電_3C_通訊",
    },
    "TP0006481": {
        "brand": "悅家傢具城",
        "grade": "B",
        "score": "68.0",
        "products": "鞋櫃、換鞋凳、衣物收納箱、餐邊櫃、床頭櫃",
        "angle": "玄關鞋櫃、臥室收納、餐邊儲物、小宅家具補位",
        "theme": "home-ritual-lifestyle",
        "role": "推薦店家",
        "source": "居家_家具_寢具_收納",
        "note": "2026-05-22 已依商品頁可開啟、品項線清楚且符合小宅收納題補評為可用。",
    },
    "TP0003642": {
        "brand": "楡青企業社",
        "grade": "B",
        "score": "70.0",
        "products": "水槽、垃圾桶、衣櫃、床頭櫃、鞋櫃與辦公桌",
        "angle": "廚房清潔收納、玄關鞋櫃、工作角落家具、臥室邊櫃",
        "theme": "home-ritual-lifestyle",
        "role": "推薦店家",
        "source": "居家_家具_寢具_收納",
        "note": "2026-05-22 依商品頁可開啟、商品線清楚且符合居家整理題新增為可用。",
    },
    "TP0006669": {
        "brand": "景敦商行",
        "grade": "B",
        "score": "68.0",
        "products": "垃圾桶、鞋架、廚房架、收納箱、雨傘架",
        "angle": "廚房收納、玄關鞋架、垃圾桶與日常整理",
        "theme": "home-ritual-lifestyle",
        "role": "推薦店家",
        "source": "居家_家具_寢具_收納",
        "note": "2026-05-22 依商品頁可開啟、品項線清楚且符合居家整理題新增為可用。",
    },
    "TP0006860": {
        "brand": "佑澄企業社",
        "grade": "B",
        "score": "68.0",
        "products": "夾縫收納櫃、水槽、靠枕、鞋櫃、平板拖把",
        "angle": "夾縫收納、餐廚整理、工作角落支撐、玄關櫃",
        "theme": "home-ritual-lifestyle",
        "role": "推薦店家",
        "source": "居家_家具_寢具_收納",
        "note": "2026-05-22 依商品頁可開啟、品項線清楚且符合小宅收納題新增為可用。",
    },
}


ARTICLES: list[dict[str, Any]] = [
    {
        "slug": "small-home-storage-products-entry-closet-underbed",
        "category": "lifestyle-culture",
        "title": "小宅不是缺櫃子，是缺回家的位置：12 件收納單品讓玄關、衣櫃和床底安靜下來",
        "excerpt": "從玄關、衣櫃到床底，小宅收納要先決定物品回家的位置，再挑折疊箱、抽屜櫃、床底盒與夾縫櫃。",
        "tags": ["小宅收納", "玄關整理", "衣櫃收納", "床底收納"],
        "series": "小宅收納與居家整理商品推薦",
        "listingTitle": "小宅收納單品：玄關、衣櫃、床底一次整理",
        "listingExcerpt": "12 件收納單品，從回家動線、衣物分類到床底空間做完整配置。",
        "heroAlt": "明亮小宅玄關連接衣櫃與臥室床底收納，木質家具與柔和自然光，無品牌文字",
        "coverLabel": "Small Home Storage",
        "palette": ("#f4efe6", "#4d6b63", "#c6864a", "#2a2a28"),
        "intro": "小宅最困擾的不是東西太多，而是每件物品都沒有固定停靠點。回家放包、拆外套、收雨傘、換季衣物和床底備品如果全部擠在同一個角落，空間很快就會看起來疲憊。這篇把收納視為日常動線問題，先整理使用順序，再挑能放進台灣小坪數住宅的箱櫃與置物單品。",
        "main": [
            "TP00057090016048", "TP00036250013730", "TP00074070008912", "TP00057090011809",
            "TP00074070007497", "TP00036250015378", "TP00068600014030", "TP00064810014169",
        ],
        "sidebar": [
            "TP00036250015383", "TP00066690008320", "TP00068600014033",
            "TP00074070007500", "TP00057090014631", "TP00036420022460",
        ],
        "brand_ids": ["TP0005709", "TP0003625", "TP0007407", "TP0006860", "TP0006481"],
        "sections": [
            ("先決定物品回家的順序", "玄關、衣櫃、床底與夾縫櫃要分工，而不是把所有東西塞進最大的櫃子。先把每天進門會碰到的包、鑰匙、雨傘與外套放在最外層，再把換季、備品、紀念性物件往內移。", "只買大容量箱子，卻沒有決定誰該放在第一層，是小宅最常見的失誤。"),
            ("透明、翻蓋與抽屜的差別", "透明箱適合需要快速辨識的衣物與雜貨，翻蓋箱適合不常拿的備品，抽屜櫃則適合每天都會取用的小物。三者不是誰比較好，而是取物頻率不同。", "若把每天要用的東西放進深箱，最後仍會堆回椅子或地板。"),
            ("床底收納只放低頻物品", "床底最適合放換季被套、旅行袋、備用毛巾與紀念物，不適合放每天都會拿的衣物。選扁平箱時要先量床腳高度，也要留出手能拉出的縫。", "箱子剛好塞滿不等於好用，抽拉空間比容量更重要。"),
            ("夾縫櫃適合補動線，不適合承擔全部整理", "冰箱邊、衣櫃旁、書桌側邊的夾縫櫃，可以承接零散物件，但不能把它當成主要收納。它的價值在於讓小物離使用位置更近。", "越窄的櫃體越要注意高度與抽屜深度，避免拿取時整櫃晃動。"),
            ("把收納箱當成家具的一部分", "若收納箱會長期外露，就要注意色彩、材質與周邊家具是否協調。小宅裡每個箱子都會被看見，安靜的外觀反而能讓空間更放鬆。", "同一區域最多保留兩種視覺語言，會比每個角落都買不同款式更穩。"),
            ("每季做一次撤退清單", "收納的終點不是買更多盒子，而是定期讓物品退出。季節轉換時，把一年沒用、尺寸不合、用途重複的東西分開，空間才會真的鬆開。", "整理前先保留一個待處理箱，比立刻大掃除更容易持續。"),
        ],
        "faq": [
            ("小宅收納要先買櫃子還是先分類？", "先分類。知道每天、每週、每季會拿哪些東西後，再決定透明箱、翻蓋箱、抽屜櫃或床底盒。"),
            ("床底收納可以放衣服嗎？", "可以放換季或備用衣物，但不建議放每天穿的衣服。床底拿取成本高，適合低頻物品。"),
            ("收納箱要選透明還是不透明？", "常拿、需要快速辨識的物品適合透明；會外露且想維持視覺安靜的區域，可選不透明或同色系款式。"),
        ],
        "disclaimer": "本文為一般居家收納情境整理，未宣稱商品承重、耐用年限或個別空間必然適用。實際尺寸、材質、活動、價格與庫存請以 momo 商品頁公告為準。",
    },
    {
        "slug": "entryway-shoe-cabinet-umbrella-rack-product-guide",
        "category": "lifestyle-culture",
        "title": "玄關一打開就有秩序：鞋櫃、雨傘架、換鞋凳的 10 個實用選擇",
        "excerpt": "玄關收納先看開門寬度、鞋量、雨傘滴水位置與換鞋動線，再挑鞋櫃、鞋盒、鞋架與換鞋凳。",
        "tags": ["玄關鞋櫃", "鞋架", "雨傘架", "換鞋凳"],
        "series": "小宅收納與居家整理商品推薦",
        "listingTitle": "玄關鞋櫃、雨傘架與換鞋凳的實用選擇",
        "listingExcerpt": "從鞋量、門片開合、雨傘位置到換鞋凳，一次整理玄關動線。",
        "heroAlt": "整齊玄關有鞋櫃、雨傘架、換鞋凳與自然光，畫面乾淨無品牌文字",
        "coverLabel": "Entryway Order",
        "palette": ("#edf1ec", "#345c58", "#d1a15c", "#202522"),
        "intro": "玄關是家裡最容易露出生活狀態的地方。門一開，如果鞋子、傘、包包和外套沒有各自的位置，空間再大也會顯得凌亂。這篇用鞋量、開門寬度、雨天動線和換鞋習慣作為判斷，把鞋櫃、鞋盒、鞋架、雨傘架與換鞋凳拆成可以實際比較的選項。",
        "main": [
            "TP00057090016084", "TP00057090014891", "TP00057090013358", "TP00057090015152",
            "TP00057090015133", "TP00036250012385", "TP00036250012378", "TP00074070003196",
            "TP00074070007529", "TP00064810021151",
        ],
        "sidebar": [
            "TP00064810020979", "TP00064810021883", "TP00064810023296",
            "TP00036420026826", "TP00068600008259", "TP00066690005781",
        ],
        "brand_ids": ["TP0005709", "TP0003625", "TP0007407", "TP0006481", "TP0003642"],
        "sections": [
            ("先量門片、走道與鞋櫃深度", "玄關家具第一個限制不是鞋量，而是門打開後還剩多少寬度。鞋櫃深度、門片開合方向和人轉身的位置都要一起看，窄玄關尤其不能只追求容量。", "沒有量門後空間就買落地櫃，是玄關最容易卡住的原因。"),
            ("鞋櫃、鞋架、鞋盒分別適合不同鞋量", "鞋櫃適合想把視覺藏起來的家庭，開放鞋架適合通風與快速拿取，透明鞋盒則適合球鞋或季節鞋分類。真正的關鍵是常穿鞋放外層，低頻鞋往高處或深處移。", "把所有鞋都放在同一種收納裡，通常會讓最常穿的鞋反而最難拿。"),
            ("雨傘架要靠近濕區", "雨傘架最好放在進門後不會穿越客廳的位置，底盤、排水和高度都要看。長傘、折傘與雨衣若混在一起，雨天回家會更混亂。", "傘架不是裝飾品，能不能讓濕傘自然停下來才是重點。"),
            ("換鞋凳要看坐下後的膝蓋與通道", "換鞋凳很實用，但它會佔走玄關轉身空間。若家中長輩、孩子或常穿綁帶鞋，坐凳一體鞋櫃會更有存在感；若玄關很窄，就改用薄型凳或可移動凳。", "凳面太高或太低都會不好用，建議以實際坐下的姿勢評估。"),
            ("玄關不要承擔全家的雜物", "玄關可以放出門必需品，但不應該放所有備品。安全帽、購物袋、清潔物、快遞箱如果全留在門口，很快會讓鞋櫃失效。", "玄關只保留『出門會用』與『回家會放』兩類物品，視覺會立即變乾淨。"),
            ("每個人的鞋位要明確", "多人家庭的玄關，最好直接分配每人鞋位，而不是共用一排。這比多買一層架更重要，因為秩序來自清楚的位置，而不是更多空格。", "常穿鞋控制在每人二到三雙，玄關會更容易維持。"),
        ],
        "faq": [
            ("玄關很窄還適合放鞋櫃嗎？", "可以，但要優先看門片開合、走道寬度與鞋櫃深度，必要時選薄型鞋櫃或透明鞋盒。"),
            ("雨傘架要選大容量嗎？", "不一定。要看家中傘的數量、是否有長傘與濕傘停放位置，大容量若放錯位置也會妨礙動線。"),
            ("換鞋凳有必要嗎？", "若家中常穿綁帶鞋、長靴，或需要坐下整理包包，換鞋凳會很實用；玄關很窄則要選可移動或窄版款式。"),
        ],
        "disclaimer": "本文為一般玄關家具與收納情境整理，不宣稱商品承重、防潮或耐用效果。實際尺寸、材質、活動、價格與庫存請以 momo 商品頁公告為準。",
    },
    {
        "slug": "home-office-corner-desk-storage-furniture-guide",
        "category": "ai-innovation",
        "title": "在家工作角落不再臨時：書桌、邊櫃、靠枕與桌面收納怎麼配",
        "excerpt": "居家工作角落要先確認桌面深度、椅子高度、側邊收納與視訊背景，再挑書桌、邊櫃、靠枕與桌面架。",
        "tags": ["居家辦公", "工作角落", "書桌", "桌面收納"],
        "series": "小宅收納與居家整理商品推薦",
        "listingTitle": "在家工作角落怎麼配：書桌、邊櫃與桌面收納",
        "listingExcerpt": "把居家工作角落從臨時桌面變成穩定可用的日常配置。",
        "heroAlt": "安靜居家工作角落有木質書桌、邊櫃、桌面收納與柔和窗光，無品牌文字",
        "coverLabel": "Work Corner",
        "palette": ("#eef2f5", "#2f5364", "#b77b4d", "#202126"),
        "intro": "在家工作最怕『只是暫時用一下』，結果暫時變成一年。真正好用的工作角落，不一定要整間書房，而是桌面深度、椅子位置、側邊收納、充電線與視訊背景都能穩定重複。這篇用會議、文件、筆電與休息姿勢作為判斷，把書桌、辦公椅、床頭櫃、靠枕與桌面小收納放在同一套配置裡看。",
        "main": [
            "TP00074070008959", "TP00057090017605", "TP00036250008928", "TP00036420030389",
            "TP00074070006604", "TP00074070006142", "TP00036250015397", "TP00063480000421",
        ],
        "sidebar": [
            "TP00036250015650", "TP00068600007773", "TP00068600008563",
            "TP00064810020083", "TP00036420027143",
        ],
        "brand_ids": ["TP0007407", "TP0005709", "TP0003625", "TP0003642", "TP0006348"],
        "sections": [
            ("桌面深度先於桌面寬度", "筆電、外接鍵盤、筆記本與水杯如果全部擠在同一條線，桌面再寬也會亂。居家工作桌先看深度與手肘位置，再看是否需要抽屜或側邊櫃。", "只看桌子寬度，容易買到看起來大、實際工作距離不足的桌面。"),
            ("側邊櫃比大抽屜更能維持桌面", "文件、充電器、藍牙耳機、眼鏡與筆記本都需要離手近但不佔桌面的位置。側邊櫃、床頭櫃或小型抽屜櫃，可以把工作物品集中在手一伸就到的地方。", "把雜物全部放進桌面抽屜，常會讓抽屜變成第二個雜物箱。"),
            ("椅子與靠背要看工作時長", "偶爾回信和長時間會議需要的椅子不同。若工作角落兼具閱讀或休息功能，靠枕和椅背支撐可以補足姿勢切換，但仍要以自身坐感與空間尺度判斷。", "不要把舒適感寫成保證，實際使用仍取決於身高、椅面與工作時長。"),
            ("視訊背景也是收納的一部分", "視訊時會被看見的牆面、層架和桌邊櫃，會影響工作角落的專業感。把文件、線材與雜物退到鏡頭外，比堆更多裝飾更有效。", "背景裡保留一個乾淨垂直面，通常比擺滿物件更耐看。"),
            ("桌面小收納只留下每天會碰的東西", "筆筒、杯架、桌面架適合放每天真的會拿的物件。若只是把雜物展示出來，桌面會更吵。挑桌面收納時要先列出固定留下的五類物品。", "每個收納盒都應該有明確用途，否則很快會變成暫放區。"),
            ("工作角落要能下班", "居家工作角落最需要的是收尾。筆電線、耳機、文件和水杯都有固定位置，晚上才能從工作狀態退出。這是家具配置裡最容易被忽略的一步。", "讓最後一個動作變簡單，隔天早上才會願意維持。"),
        ],
        "faq": [
            ("小坪數適合買大書桌嗎？", "不一定。先看桌面深度、椅子退出距離與側邊收納位置，大書桌若壓縮動線反而不好用。"),
            ("工作角落需要床頭櫃或邊櫃嗎？", "若桌面常堆文件、線材或小物，邊櫃會比單純加大桌面更有幫助。"),
            ("桌面收納要買越多越好嗎？", "不是。只放每天會拿的物品即可，過多收納盒會讓桌面視覺更雜。"),
        ],
        "disclaimer": "本文為一般居家工作家具與桌面整理情境整理，不宣稱商品人體工學、健康或舒適效果。實際尺寸、材質、活動、價格與庫存請以 momo 商品頁公告為準。",
    },
    {
        "slug": "home-organization-cleaning-kitchen-storage-products",
        "category": "lifestyle-culture",
        "title": "居家整理不用等大掃除：垃圾桶、廚房架、水槽與清潔收納的選購清單",
        "excerpt": "日常整理先看垃圾分類、廚房檯面、清潔工具停放點與餐邊收納，再挑垃圾桶、廚房架、水槽與儲物櫃。",
        "tags": ["居家整理", "廚房收納", "垃圾桶", "清潔工具收納"],
        "series": "小宅收納與居家整理商品推薦",
        "listingTitle": "居家整理清單：垃圾桶、廚房架、水槽與清潔收納",
        "listingExcerpt": "不用等大掃除，先把每天會用的垃圾桶、廚房架與清潔工具位置整理好。",
        "heroAlt": "乾淨廚房與餐邊區有垃圾桶、廚房架、水槽與清潔工具收納，明亮自然光無品牌文字",
        "coverLabel": "Daily Home Reset",
        "palette": ("#f5f1e8", "#5f6f4f", "#d28a4c", "#27231f"),
        "intro": "居家整理不必等到大掃除。真正讓家看起來舒服的，是垃圾桶有位置、廚房檯面不堆滿、清潔工具收得回去，餐邊櫃能承接日常備品。這篇從每天會發生的整理動作出發，選擇垃圾桶、廚房架、水槽、餐邊櫃與拖把收納時，都以動線、尺寸與使用頻率為核心。",
        "main": [
            "TP00066690016472", "TP00036420030716", "TP00043790000335", "TP00066690003884",
            "TP00068600006435", "TP00068600006426", "TP00036420030071", "TP00064810020941",
        ],
        "sidebar": [
            "TP00068600002516", "TP00066690016603", "TP00036420030088",
            "TP00068600006424", "TP00074070000042", "TP00074070000035",
        ],
        "brand_ids": ["TP0006669", "TP0003642", "TP0004379", "TP0006860", "TP0006481"],
        "sections": [
            ("垃圾桶先看分類位置", "垃圾桶不是越大越好，而是要放在最容易完成分類的位置。廚房、餐邊、工作區與玄關可能需要不同尺寸，先決定垃圾會在哪裡產生，再決定桶型。", "垃圾桶放太遠，最後垃圾會先堆在檯面或桌角。"),
            ("廚房架要釋放檯面，不是堆高檯面", "微波爐架、抽拉架與多層置物架可以讓檯面回到料理用途，但若放太多不常用鍋具，反而增加視覺壓力。先把每日會用的物件留下，再安排垂直層次。", "架子高度、抽拉方向與插座位置要一起確認。"),
            ("水槽選擇看檯面、管線與清潔習慣", "水槽相關商品要以尺寸、安裝條件與日常清潔方式為準。本文只作一般空間整理角度，不把材質或功能寫成效果承諾。", "更換水槽前應確認安裝條件，必要時由專業人員評估。"),
            ("餐邊櫃是廚房外溢的緩衝區", "若廚房櫃體不足，餐邊櫃可以收杯具、茶包、備用紙品與小家電。但餐邊櫃不是倉庫，最好讓每一層都有明確用途。", "把所有備品全塞進餐邊櫃，只會把整理問題往外移。"),
            ("清潔工具需要乾燥與停放點", "拖把、刷具與清潔備品要有收尾位置。比起買更多工具，更重要的是使用後能停在哪裡、是否會擋住走道、是否容易拿回。", "本文不宣稱清潔或衛生效果，實際使用仍以商品說明與居家條件為準。"),
            ("小整理每天三分鐘就能開始", "每天晚餐後把垃圾、檯面、餐邊櫃和清潔工具各處理一個小動作，比週末一次全部整理更容易維持。商品只是幫助動線成立，習慣才是最後的關鍵。", "先從最常亂的單一區域開始，會比全家一起重整更容易成功。"),
        ],
        "faq": [
            ("垃圾桶要選腳踩還是開蓋式？", "要看放置位置與使用習慣。廚房常見腳踩式較方便，工作區或客廳可依空間選擇較安靜的款式。"),
            ("廚房架會不會讓空間更亂？", "如果沒有先分類就直接上架，確實可能更亂。建議只放每天或每週會使用的物品。"),
            ("本文推薦水槽是否代表安裝適合所有廚房？", "不是。水槽需依檯面、管線與安裝條件判斷，實際規格與施工請以商品頁與專業評估為準。"),
        ],
        "disclaimer": "本文為一般居家整理與餐廚收納情境整理，僅提供尺寸、動線與收納位置的選購參考，不涉及衛生、醫療或個別風險判斷。實際尺寸、材質、活動、價格、安裝條件與庫存請以 momo 商品頁公告為準。",
    },
    {
        "slug": "family-gift-toys-puzzles-kites-storage-guide",
        "category": "lifestyle-culture",
        "title": "不只買玩具：親子禮物可以這樣挑，從拼圖、風箏到收納箱都更耐玩",
        "excerpt": "親子禮物不只看玩具本身，也要看收納、共玩時間、戶外使用條件與收尾方式，從拼圖、迷宮球、風箏到收納箱整理選購順序。",
        "tags": ["親子禮物", "拼圖", "風箏", "玩具收納"],
        "series": "小宅收納與居家整理商品推薦",
        "listingTitle": "親子禮物怎麼挑：拼圖、風箏、畫板與收納箱",
        "listingExcerpt": "從週末共玩、戶外活動到收納方式，挑更容易被使用的親子禮物。",
        "heroAlt": "明亮家庭客廳桌面有拼圖、風箏、磁性畫板與收納箱，無品牌文字",
        "coverLabel": "Family Gift Picks",
        "palette": ("#f3efe4", "#466b7d", "#d58a5d", "#2a2421"),
        "intro": "親子禮物最怕只看外盒，拆開後才發現沒有時間玩、沒有地方收，或需要的陪伴比想像多。好的禮物不一定最大盒，而是能在家庭節奏裡被自然拿出來、玩完能收回去。這篇用共玩時間、戶外條件、零件收納與使用頻率來挑拼圖、迷宮球、風箏、磁性畫板、桌遊和收納型禮物。",
        "main": [
            "TP00021790000643", "TP00021790000561", "TP00021790000560", "TP00021790000305",
            "TP00021790000328", "TP00021790000123", "TP00021790000998", "TP00021790001178",
            "TP00021790000415", "TP00021790000620",
        ],
        "sidebar": [
            "TP00021790001126", "TP00021790000372", "TP00021790000320", "TP00021790000336",
            "TP00021790001111", "TP00021790000609", "TP00021790000610", "TP00074070002470",
        ],
        "brand_ids": ["TP0002179", "TP0007407", "TP0003625", "TP0005709"],
        "sections": [
            ("先看是否需要陪玩", "拼圖、迷宮球、桌遊、積木軌道和磁性畫板，都有不同陪玩程度。送禮前先想收禮家庭是否有時間一起打開，而不是只看包裝是否熱鬧。", "本文不把玩具寫成學習成果，只整理日常使用情境與收納判斷。"),
            ("拼圖與迷宮球適合安靜桌面時間", "拼圖和迷宮球適合週末下午、雨天或等餐前後的安靜時間。挑選時要看片數、零件大小、是否容易收回盒中，以及大人是否需要在旁協助。", "太多零件若沒有收納位置，玩一次後就可能散在抽屜裡。"),
            ("風箏是戶外禮物，也要看場地與收納", "風箏禮物有很強的戶外感，但需要風況、場地與成人陪同。選擇時要看尺寸、線輪、收納長度與是否方便帶出門。", "風箏不適合把安全感寫成保證，實際使用仍需依場地與商品說明判斷。"),
            ("磁性畫板與桌遊適合反覆拿出來", "磁性畫板、桌上遊戲和簡單互動玩具的好處，是不用每次都重新設定太多。它們適合放在客廳或餐桌附近，讓短時間也能開始。", "若規則太複雜，家庭平日晚上通常很難啟動。"),
            ("收納箱是禮物的一部分", "親子禮物如果零件多，收納箱就不是附屬品，而是禮物能不能長期留下來的關鍵。透明抽屜、玩具箱或繪本置物架都能讓收尾更簡單。", "送禮時同時想『玩完放哪裡』，比再多買一件玩具更貼心。"),
            ("把禮物分成室內、戶外與收納三類", "室內禮物重視桌面與收納，戶外禮物重視攜帶與場地，收納型禮物則負責讓前兩者能被保存。這樣挑禮物，比單純追求驚喜感更不容易失手。", "每一份禮物都要有打開方式與收尾方式，家庭才會真的使用它。"),
        ],
        "faq": [
            ("親子禮物要選越有教育感越好嗎？", "不一定。本文不宣稱教育成果，建議先看年齡標示、共玩時間、收納方式與家庭是否容易使用。"),
            ("風箏適合當禮物嗎？", "適合喜歡戶外活動的家庭，但要看場地、風況、尺寸與成人陪同需求，並依商品頁說明使用。"),
            ("玩具收納箱也可以當禮物嗎？", "可以。若收禮家庭已有許多玩具，收納箱或置物架反而能讓既有物品更容易被看見與使用。"),
        ],
        "disclaimer": "本文為一般親子禮物與家庭共玩情境整理，僅提供年齡標示、共玩時間、收納方式與場地條件的選購參考。玩具與用品請依商品說明與成人陪同需求使用；實際價格、規格與庫存請以 momo 商品頁公告為準。",
    },
]


def load_products() -> dict[str, dict[str, Any]]:
    if not SOURCE_XLSX.exists():
        raise SystemExit(f"找不到商品來源：{SOURCE_XLSX}")
    frame = pd.read_excel(SOURCE_XLSX, dtype=str).fillna("")
    products: dict[str, dict[str, Any]] = {}
    for _, row in frame.iterrows():
        code = row["商品編號"].strip()
        if not code:
            continue
        merchant_id = code[:9]
        products[code] = {
            "code": code,
            "merchantId": merchant_id,
            "rawName": row["商品名稱"].strip(),
            "merchantRawName": row["商店名稱"].strip(),
            "commissionRate": row["分潤率"].strip(),
            "sourceProductUrl": row["商品連結"].strip(),
            "affiliateUrl": row["推廣連結"].strip(),
        }
    return products


def short_product_name(raw: str) -> str:
    text = html.unescape(raw)
    text = re.sub(r"【888便利購】", "", text)
    text = re.sub(r"\[[^\]]+\]", "", text)
    text = re.sub(r"[💖✨♔]+", "", text)
    text = re.sub(r"(免運到府|免運|可打統編|人氣爆款|爆款熱銷|優質|新款|2025新款)", "", text)
    text = re.sub(r"\s+", " ", text).strip(" -／/")
    text = text.replace("（安全塑料）", "").replace("（安全漆ST903C）", "").replace("（安全漆ST903B）", "")
    if len(text) > 34:
        text = text[:34].rstrip(" ，、-／/") + "..."
    return text


def product_reason(name: str, article_slug: str) -> str:
    if "鞋" in name:
        return "適合放在玄關動線中比較鞋量、深度與門片開合，讓常穿鞋與低頻鞋分層管理。"
    if "雨傘" in name or "傘" in name:
        return "適合安排在進門濕區旁，讓長傘、折傘和雨天物件有明確停放點。"
    if "垃圾桶" in name:
        return "適合用來檢查垃圾分類位置與日常丟棄動線，避免垃圾先堆在桌面或檯面。"
    if "水槽" in name:
        return "適合納入餐廚更新清單，重點是尺寸、安裝條件與日常清潔動線。"
    if "廚房" in name or "置物架" in name or "餐邊" in name:
        return "適合釋放檯面與餐邊區，把每天會拿的物品集中在可視、可取的位置。"
    if "書桌" in name or "辦公桌" in name or "桌" in name:
        return "適合建立穩定工作桌面，先看深度、手肘位置、線材與文件收納需求。"
    if "椅" in name or "靠枕" in name:
        return "適合補足工作角落或閱讀角的坐姿轉換，仍需依個人身高與空間尺度判斷。"
    if "拼圖" in name or "迷宮" in name:
        return "適合安排安靜桌面時間，挑選時同步看片數、零件大小與收回盒中的便利性。"
    if "風箏" in name:
        return "適合戶外共玩禮物，挑選時要看尺寸、線輪、攜帶方式與成人陪同需求。"
    if "畫板" in name or "桌上遊戲" in name or "積木" in name or "砂畫" in name:
        return "適合短時間共玩或創作使用，重點是收尾是否簡單、零件是否容易歸位。"
    if "耳" in name:
        return "適合放在工作角落的小型配件清單中，重點是使用情境、收納位置與商品規格。"
    if "包" in name:
        return "適合安排在玄關或臥室收納旁，讓包款從椅背與地面回到固定位置。"
    if "收納" in name or "儲物" in name or "整理" in name or "櫃" in name:
        return "適合建立物品固定停靠點，先依使用頻率決定放在外層、內層或床底。"
    if article_slug == "family-gift-toys-puzzles-kites-storage-guide":
        return "適合放入親子禮物清單，挑選時同步考慮共玩時間、收納方式與年齡標示。"
    return "適合納入同一空間任務比較，重點是尺寸、使用頻率、拿取動線與收尾方式。"


def product_risk_note(name: str, article_slug: str) -> str:
    if article_slug == "family-gift-toys-puzzles-kites-storage-guide":
        return "請依商品年齡標示、場地條件與成人陪同需求使用；本文不承諾教育或安全效果。"
    if "水槽" in name:
        return "安裝條件、尺寸與配件請以商品頁與專業評估為準。"
    if "椅" in name or "靠枕" in name:
        return "坐感與支撐因人而異，請依尺寸、材質與個人需求評估。"
    return "價格、規格、活動與庫存請以 momo 商品頁公告為準。"


def load_image_cache() -> dict[str, str]:
    if IMAGE_CACHE.exists():
        return pipeline.load_json(IMAGE_CACHE, default={})
    return {}


def fetch_og_image(url: str) -> str:
    if not url:
        return ""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=14) as response:
            body = response.read(900_000).decode("utf-8", errors="ignore")
    except (urllib.error.URLError, TimeoutError):
        return ""
    patterns = [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<img[^>]+src=["\']([^"\']*momoshop[^"\']+)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, body, flags=re.I)
        if match:
            image_url = html.unescape(match.group(1)).strip()
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            if image_url.startswith("http"):
                return image_url
    return ""


def build_product(code: str, products: dict[str, dict[str, Any]], image_cache: dict[str, str], article_slug: str) -> dict[str, Any]:
    source = products[code]
    merchant_id = source["merchantId"]
    meta = MERCHANT_META[merchant_id]
    name = short_product_name(source["rawName"])
    image_url = image_cache.get(code, "")
    if code in BAD_IMAGE_CODES:
        image_url = ""
        image_cache[code] = ""
    elif not image_url:
        image_url = fetch_og_image(source["sourceProductUrl"])
        image_cache[code] = image_url
        time.sleep(0.05)
    return {
        "code": code,
        "name": name,
        "merchantId": merchant_id,
        "brandName": meta["brand"],
        "affiliateUrl": source["affiliateUrl"],
        "sourceProductUrl": source["sourceProductUrl"],
        "imageUrl": image_url,
        "imageCredit": f"圖片來源：momo 商品頁｜{name}",
        "selectionReason": product_reason(name, article_slug),
        "riskNote": product_risk_note(name, article_slug),
    }


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size, index=1 if bold else 0)
            except OSError:
                continue
    return ImageFont.load_default()


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], width: int, fill: str, font_obj: ImageFont.ImageFont, line_gap: int = 10) -> int:
    x, y = xy
    line = ""
    for char in text:
        trial = line + char
        box = draw.textbbox((x, y), trial, font=font_obj)
        if box[2] - box[0] > width and line:
            draw.text((x, y), line, fill=fill, font=font_obj)
            y += (box[3] - box[1]) + line_gap
            line = char
        else:
            line = trial
    if line:
        draw.text((x, y), line, fill=fill, font=font_obj)
        box = draw.textbbox((x, y), line, font=font_obj)
        y += (box[3] - box[1]) + line_gap
    return y


def codex_generated_cover_path(slug: str) -> str:
    if not CODEX_GENERATED_COVER_MANIFEST.exists():
        raise FileNotFoundError(f"Missing Codex generated cover manifest: {CODEX_GENERATED_COVER_MANIFEST}")
    manifest = json.loads(CODEX_GENERATED_COVER_MANIFEST.read_text(encoding="utf-8"))
    entry = manifest.get("covers", {}).get(slug)
    if not entry:
        raise RuntimeError(f"Missing Codex generated cover manifest entry for {slug}")
    image_rel = str(entry.get("image", ""))
    image_path = ROOT / image_rel
    if not image_path.exists():
        raise FileNotFoundError(f"Missing Codex generated cover image for {slug}: {image_rel}")
    expected_hash = str(entry.get("sha256", ""))
    actual_hash = hashlib.sha256(image_path.read_bytes()).hexdigest()
    if expected_hash and actual_hash != expected_hash:
        raise RuntimeError(f"Codex generated cover hash mismatch for {slug}")
    return pipeline.relative_to_root(image_path)


def create_cover(article: dict[str, Any]) -> str:
    try:
        return codex_generated_cover_path(article["slug"])
    except (FileNotFoundError, RuntimeError) as exc:
        raise RuntimeError(
            "momo product articles require a Codex image-generated 1200x630 cover. "
            "Generate the cover with image_gen, save it under images/optimized/article-covers/, "
            "and record it in automation/codex-generated-cover-manifest.json before publishing."
        ) from exc


def brand_cards(brand_ids: list[str]) -> list[dict[str, str]]:
    cards = []
    for merchant_id in brand_ids:
        meta = MERCHANT_META[merchant_id]
        cards.append(
            {
                "name": meta["brand"],
                "merchantId": merchant_id,
                "role": meta["role"],
                "reason": meta["angle"],
                "url": f"https://www.momoshop.com.tw/TP/{merchant_id}/main",
            }
        )
    return cards


def build_sections(spec: dict[str, Any]) -> list[dict[str, Any]]:
    sections = []
    brand_names = "、".join(MERCHANT_META[mid]["brand"] for mid in spec["brand_ids"][:4])
    for heading, body, mistake in spec["sections"]:
        sections.append(
            {
                "heading": heading,
                "paragraphs": [
                    body,
                    f"編輯團隊會把 {brand_names} 等店家的商品放在同一個生活情境裡比較，但不把單一商品寫成唯一答案。判斷順序是尺寸、動線、拿取頻率、收尾方式，最後才看外觀是否與既有家具協調。",
                    f"常見錯誤是{mistake} 建議先用紙膠帶在地面標出寬度與深度，確認開門、轉身、拿取與收納都順手，再決定是否下單。",
                ],
                "bullets": [
                    "先量寬度、深度、高度與開合方向，再看容量。",
                    "保留一個固定收尾位置，比多買一件單品更能維持秩序。",
                ],
            }
        )
    return sections


def make_article(spec: dict[str, Any], products: dict[str, dict[str, Any]], image_cache: dict[str, str], config: dict[str, Any], categories: dict[str, pipeline.CategoryConfig]) -> dict[str, Any]:
    main_products = [build_product(code, products, image_cache, spec["slug"]) for code in spec["main"]]
    sidebar_products = [build_product(code, products, image_cache, spec["slug"]) for code in spec["sidebar"]]
    hero_image = create_cover(spec)
    category = categories[spec["category"]]
    article = {
        "slug": spec["slug"],
        "category": spec["category"],
        "title": spec["title"],
        "excerpt": spec["excerpt"],
        "tags": spec["tags"],
        "metaTitle": f"Elite Fashion｜{spec['title'][:50]}",
        "metaDescription": spec["excerpt"][:155],
        "series": spec["series"],
        "listingTitle": spec["listingTitle"],
        "listingExcerpt": spec["listingExcerpt"],
        "heroImageAlt": spec["heroAlt"],
        "intro": spec["intro"],
        "sections": build_sections(spec),
        "faq": [{"question": q, "answer": a} for q, a in spec["faq"]],
        "extendedReading": [
            {"title": f"瀏覽更多{category.label}文章", "url": f"/{category.page}"},
            {"title": "質感送禮怎麼選", "url": "/lifestyle-culture/quality-gifting-coffee-tea-massage-umbrella-custom.html"},
            {"title": "家庭禮物與益智玩具怎麼挑", "url": "/lifestyle-culture/family-gifts-blocks-books-puzzles-learning-toys.html"},
        ],
        "cta": {
            "variant": "gold",
            "text": "挑選前先確認尺寸、動線、使用頻率與收尾方式；若要延伸比較，可從本篇整理的店家頁與商品頁逐一查看規格。",
            "links": [
                {"label": f"前往 {MERCHANT_META[mid]['brand']}", "url": f"https://www.momoshop.com.tw/TP/{mid}/main"}
                for mid in spec["brand_ids"][:4]
            ],
        },
        "inlineCtas": [
            {
                "afterSection": 2,
                "variant": "olive",
                "eyebrow": "先看尺寸，再看款式",
                "heading": "把常用物放在手能到的位置",
                "text": "回家、工作、整理與收尾都需要固定位置；先建立動線，再挑商品會更穩。",
                "links": [
                    {"label": main_products[0]["name"], "url": main_products[0]["affiliateUrl"]},
                    {"label": main_products[1]["name"], "url": main_products[1]["affiliateUrl"]},
                ],
            }
        ],
        "disclaimer": spec["disclaimer"],
        "audience": "重視居家效率、工作秩序、送禮質感與日常整理的讀者",
        "readTimeMinutes": 10 if len(spec["main"]) <= 8 else 11,
        "heroImage": hero_image,
        "sourceType": "manual-codex-momo-product-affiliate",
        "status": "published",
        "queueId": None,
        "mainProducts": main_products,
        "sidebarProducts": sidebar_products,
        "featuredBrands": brand_cards(spec["brand_ids"]),
    }
    saved = pipeline.save_generated_article(article, None, config, categories)
    pipeline.validate_generated_article(saved, config)
    pipeline.append_publish_log(config, saved, trigger_type=TRIGGER_TYPE, queue_id=None)
    return saved


def update_latest_run(config: dict[str, Any], articles: list[dict[str, Any]]) -> None:
    payload = {
        "version": 1,
        "updatedAt": pipeline.now_iso(),
        "status": "generated",
        "triggerType": TRIGGER_TYPE,
        "newsletter": "not_sent_manual_codex_publish",
        "articleIds": [article["id"] for article in articles],
        "articleSlugs": [article["slug"] for article in articles],
        "notes": "手動產文並推送 main 不會自動寄送電子報；本批已記錄為未寄送。",
    }
    pipeline.write_json(ROOT / config["paths"]["latestRunJson"], payload)


def update_tracker(articles: list[dict[str, Any]]) -> None:
    with TRACKER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    by_merchant = {row["merchant_id"]: row for row in rows}
    mentions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in articles:
        merchant_ids = {
            product["merchantId"]
            for product in [*article.get("mainProducts", []), *article.get("sidebarProducts", [])]
        }
        merchant_ids.update(brand["merchantId"] for brand in article.get("featuredBrands", []))
        for merchant_id in merchant_ids:
            mentions[merchant_id].append(article)
    for merchant_id, article_hits in mentions.items():
        meta = MERCHANT_META[merchant_id]
        row = by_merchant.get(merchant_id)
        if row is None:
            row = {name: "" for name in fieldnames}
            row["merchant_id"] = merchant_id
            rows.append(row)
            by_merchant[merchant_id] = row
        row["brand"] = meta["brand"]
        row["source_sheet"] = meta["source"]
        row["recommendation_grade"] = meta["grade"]
        row["score"] = meta["score"]
        row["commission_rate"] = "11.0%"
        row["main_products"] = meta["products"]
        row["content_angles"] = meta["angle"]
        row["promo_link_check"] = "OK"
        row["store_link"] = f"https://www.momoshop.com.tw/TP/{merchant_id}/main"
        row["assigned_theme"] = meta["theme"]
        row["brand_role"] = meta["role"]
        row["coverage_status"] = "live"
        row["article_created"] = "true"
        row["link_status"] = "usable"
        row["risk_notes"] = row.get("risk_notes") or "不使用誇大推薦語氣，商品規格以 momo 商品頁為準"
        existing_slugs = [part for part in row.get("article_slug", "").split(";") if part]
        existing_urls = [part for part in row.get("live_url", "").split(";") if part]
        for article in article_hits:
            if article["slug"] not in existing_slugs:
                existing_slugs.append(article["slug"])
            if article["url"] not in existing_urls:
                existing_urls.append(article["url"])
        row["article_slug"] = ";".join(existing_slugs)
        row["live_url"] = ";".join(existing_urls)
        current_mentions = int(row.get("mention_count") or 0)
        row["mention_count"] = str(current_mentions + len(article_hits))
        row["last_mentioned_at"] = TODAY
        note = meta.get("note") or "2026-05-22 小宅收納、玄關、工作角落、居家整理與親子禮物商品推薦系列已置入。"
        if note not in row.get("notes", ""):
            row["notes"] = (row.get("notes", "").rstrip() + (" " if row.get("notes", "").strip() else "") + note).strip()
    with TRACKER_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validate_products(articles: list[dict[str, Any]]) -> None:
    errors: list[str] = []
    for article in articles:
        main_count = len(article.get("mainProducts", []))
        sidebar_count = len(article.get("sidebarProducts", []))
        brand_count = len(article.get("featuredBrands", []))
        if not 6 <= main_count <= 10:
            errors.append(f"{article['slug']} mainProducts 數量錯誤：{main_count}")
        if not 5 <= sidebar_count <= 8:
            errors.append(f"{article['slug']} sidebarProducts 數量錯誤：{sidebar_count}")
        if not 3 <= brand_count <= 5:
            errors.append(f"{article['slug']} featuredBrands 數量錯誤：{brand_count}")
        for product in [*article.get("mainProducts", []), *article.get("sidebarProducts", [])]:
            missing = [
                key
                for key in ("name", "merchantId", "brandName", "affiliateUrl", "sourceProductUrl", "imageCredit", "selectionReason", "riskNote")
                if not product.get(key)
            ]
            if missing:
                errors.append(f"{article['slug']} {product.get('code')} 缺欄位：{', '.join(missing)}")
    if errors:
        raise SystemExit("\n".join(errors))


def main() -> int:
    config, categories = pipeline.load_config()
    products = load_products()
    image_cache = load_image_cache()
    required_codes = {code for article in ARTICLES for code in [*article["main"], *article["sidebar"]]}
    missing = sorted(required_codes - products.keys())
    if missing:
        raise SystemExit(f"Excel 缺少商品：{', '.join(missing)}")
    articles = [make_article(spec, products, image_cache, config, categories) for spec in ARTICLES]
    pipeline.write_json(IMAGE_CACHE, image_cache)
    validate_products(articles)
    update_tracker(articles)
    update_latest_run(config, articles)
    print(f"Generated {len(articles)} momo product articles:")
    for article in articles:
        print(f"- {article['slug']} -> {article['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
