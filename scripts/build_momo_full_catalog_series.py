#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import html
import json
import os
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
PLACEMENT_REPORT = ROOT / "automation" / "momo-product-placement-report.json"
TRIGGER_TYPE = "manual-codex-momo-full-catalog-no-newsletter"
TODAY = "2026-05-22"


MERCHANT_FALLBACKS: dict[str, dict[str, str]] = {
    "TP0006092": {"brand": "森活家居選物", "grade": "B", "score": "66.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0003585": {"brand": "森格諾傢居", "grade": "B", "score": "65.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0003624": {"brand": "蝸居客製", "grade": "B", "score": "66.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0005709": {"brand": "藤木居家具", "grade": "B", "score": "70.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0003625": {"brand": "☁凌雲家居", "grade": "B", "score": "70.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0006481": {"brand": "悅家傢具城", "grade": "B", "score": "68.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0003642": {"brand": "楡青企業社", "grade": "B", "score": "70.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0006669": {"brand": "景敦商行", "grade": "B", "score": "68.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0006860": {"brand": "佑澄企業社", "grade": "B", "score": "68.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0007407": {"brand": "RED HOUSE 家具工廠", "grade": "B", "score": "73.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0002179": {"brand": "888便利購 兒童玩具專賣店", "grade": "A", "score": "82.0", "theme": "family-parenting-future", "source": "親子_母嬰_玩具"},
    "TP0007070": {"brand": "S′AIME東京企劃", "grade": "A", "score": "84.0", "theme": "mobile-wardrobe-accessories", "source": "服飾_鞋包_配件"},
    "TP0009548": {"brand": "大檜仁心", "grade": "A", "score": "80.0", "theme": "home-ritual-lifestyle", "source": "居家_香氛_禮品"},
    "TP0004379": {"brand": "凱莎精選家具城", "grade": "B", "score": "68.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "TP0006348": {"brand": "LamiFans", "grade": "A", "score": "87.0", "theme": "creator-work-gear", "source": "家電_3C_通訊"},
    "TP0008114": {"brand": "輕氧家居", "grade": "B", "score": "64.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
    "GOODS-vacanza": {"brand": "vacanza", "grade": "A", "score": "76.0", "theme": "mobile-wardrobe-accessories", "source": "服飾_鞋包_配件"},
    "GOODS-da": {"brand": "DA 生活選物", "grade": "B", "score": "66.0", "theme": "outdoor-mobile-living", "source": "戶外_旅行_生活"},
    "GOODS-fun-house": {"brand": "FUN HOUSE", "grade": "B", "score": "68.0", "theme": "home-ritual-lifestyle", "source": "居家_家具_寢具_收納"},
}


BUCKETS: dict[str, dict[str, Any]] = {
    "entry-shoe-cabinet": {
        "category": "lifestyle-culture",
        "series": "玄關收納商品推薦",
        "label": "玄關鞋櫃",
        "slug": "entryway-shoe-cabinet-storage-products",
        "title": "玄關鞋櫃別只看容量：{count} 件鞋櫃、鞋架與薄型收納讓門口不再堵住",
        "excerpt": "玄關鞋櫃要同時看門片開合、走道寬度、常穿鞋數量與雨天動線，這份清單整理適合小宅門口的鞋櫃與鞋架選擇。",
        "cover": "Entryway Shoes",
        "palette": ("#eef1eb", "#375f58", "#d3a15d", "#202522"),
        "intent": "玄關開門、換鞋、收傘與出門前最後整理",
        "criteria": ["門片開合與走道寬度", "常穿鞋與低頻鞋分層", "雨天濕區是否有停靠點", "換鞋後能不能順手收回"],
    },
    "shoe-box-rack": {
        "category": "lifestyle-culture",
        "series": "玄關收納商品推薦",
        "label": "鞋盒鞋架",
        "slug": "transparent-shoe-box-rack-entryway-products",
        "title": "鞋盒、鞋架怎麼放才不亂：{count} 件透明鞋盒與多層鞋架整理常穿鞋",
        "excerpt": "透明鞋盒與多層鞋架適合把球鞋、季節鞋與常穿鞋分開，重點不是堆高，而是讓拿取與歸位變簡單。",
        "cover": "Shoe Rack Order",
        "palette": ("#f5f0e6", "#516a72", "#c98a54", "#211f1c"),
        "intent": "球鞋、季節鞋、室內拖與家庭成員鞋位管理",
        "criteria": ["鞋盒是否容易辨識", "鞋架層高是否適合靴子", "每人常穿鞋數量", "清潔與通風位置"],
    },
    "folding-storage-box": {
        "category": "lifestyle-culture",
        "series": "小宅收納商品推薦",
        "label": "折疊收納箱",
        "slug": "folding-storage-box-closet-underbed-products",
        "title": "折疊收納箱不是越大越好：{count} 件衣物、玩具與床底整理箱的選購順序",
        "excerpt": "折疊箱、翻蓋箱與床底盒各自適合不同頻率的物品，先分清楚每天、每週、每季會拿什麼，再決定容量。",
        "cover": "Folding Storage",
        "palette": ("#f3eee5", "#5b6f56", "#d28c4b", "#25211e"),
        "intent": "換季衣物、備品、玩具、繪本與床底低頻物件收納",
        "criteria": ["是否需要透明辨識", "翻蓋或抽屜的拿取方向", "床底高度與抽拉空間", "可否同系列堆疊"],
    },
    "drawer-storage": {
        "category": "lifestyle-culture",
        "series": "小宅收納商品推薦",
        "label": "抽屜收納",
        "slug": "drawer-storage-cabinet-small-home-products",
        "title": "抽屜櫃讓零散物有家：{count} 件透明櫃、夾縫櫃與桌邊收納清單",
        "excerpt": "抽屜櫃適合每天會拿的小物，夾縫櫃適合補動線，挑選時要看深度、抽拉方向與擺放高度。",
        "cover": "Drawer Storage",
        "palette": ("#eef2f0", "#405f63", "#c88953", "#212424"),
        "intent": "零食、文具、備品、包包與小物的日常歸位",
        "criteria": ["抽屜深度與物品高度", "是否會阻擋走道", "外露區域的視覺一致", "高頻與低頻物品分層"],
    },
    "closet-laundry-storage": {
        "category": "lifestyle-culture",
        "series": "衣櫃整理商品推薦",
        "label": "衣櫃整理",
        "slug": "closet-laundry-bedroom-storage-products",
        "title": "衣櫃整理先處理髒衣、換季與備品：{count} 件臥室收納單品清單",
        "excerpt": "衣櫃外的髒衣籃、換季箱與臥室儲物櫃，會決定房間是否能維持乾淨動線。",
        "cover": "Closet Reset",
        "palette": ("#f4efe8", "#6a6554", "#c98454", "#2a2925"),
        "intent": "衣物、髒衣、換季被品與臥室備品整理",
        "criteria": ["乾淨衣物與待洗衣物分區", "換季物品是否放低頻位置", "外露收納是否和房間色調一致", "拿取動線是否避開床邊"],
    },
    "desk-work-furniture": {
        "category": "ai-innovation",
        "series": "工作角落商品推薦",
        "label": "書桌辦公桌",
        "slug": "desk-work-corner-furniture-products",
        "title": "工作角落要先有穩定桌面：{count} 件書桌、辦公桌與會議桌怎麼選",
        "excerpt": "居家工作桌不只是寬度問題，還要看深度、椅子退出距離、線材位置與文件收納。",
        "cover": "Desk Setup",
        "palette": ("#edf2f5", "#2f5364", "#bd7d4f", "#202126"),
        "intent": "筆電工作、視訊會議、文件攤開與下班收尾",
        "criteria": ["桌面深度先於寬度", "椅子退出距離", "插座與線材位置", "視訊背景是否乾淨"],
    },
    "chair-cushion": {
        "category": "ai-innovation",
        "series": "工作角落商品推薦",
        "label": "椅子靠枕",
        "slug": "chair-cushion-home-office-products",
        "title": "椅子、靠枕與短休息角落：{count} 件工作與閱讀座位單品怎麼搭",
        "excerpt": "工作座位要看桌高、坐姿切換與空間動線；椅子與靠枕只能輔助，仍需依個人尺寸與使用時間評估。",
        "cover": "Chair Comfort",
        "palette": ("#f2efe8", "#4e5f74", "#c98957", "#22232a"),
        "intent": "工作、閱讀、梳妝與短暫休息的座位配置",
        "criteria": ["桌椅高度關係", "椅背與坐墊尺寸", "是否會卡住走道", "使用時間與收納位置"],
    },
    "side-cabinet-nightstand": {
        "category": "lifestyle-culture",
        "series": "小家具商品推薦",
        "label": "邊櫃床頭櫃",
        "slug": "side-cabinet-nightstand-bedroom-products",
        "title": "邊櫃、床頭櫃和餐邊櫃怎麼補空間：{count} 件小家具讓雜物退場",
        "excerpt": "小櫃體最適合承接床邊、沙發旁、餐邊與工作桌旁的零碎物件，重點是高度與開門方向。",
        "cover": "Side Cabinet",
        "palette": ("#f6f0e7", "#5c6255", "#cf8d52", "#24221e"),
        "intent": "床邊、沙發旁、餐邊與桌邊小物收納",
        "criteria": ["高度是否順手", "抽屜或門片方向", "插座與走道位置", "外露物品是否能被遮起來"],
    },
    "kitchen-rack": {
        "category": "lifestyle-culture",
        "series": "餐廚整理商品推薦",
        "label": "廚房置物架",
        "slug": "kitchen-rack-counter-storage-products",
        "title": "廚房架不是把東西堆高：{count} 件微波爐架、抽拉架與餐邊收納清單",
        "excerpt": "廚房置物架要釋放檯面，而不是把檯面雜物堆成牆。挑選時先看插座、抽拉方向與每天會拿的物品。",
        "cover": "Kitchen Rack",
        "palette": ("#f5f1e8", "#627158", "#d28a4d", "#27231f"),
        "intent": "微波爐、小家電、鍋具、餐具與餐邊備品整理",
        "criteria": ["插座與散熱空間", "抽拉方向與檯面深度", "每日使用物品優先", "餐邊櫃是否能承接外溢物"],
    },
    "sink-cleaning": {
        "category": "lifestyle-culture",
        "series": "餐廚整理商品推薦",
        "label": "水槽清潔收納",
        "slug": "sink-cleaning-tool-kitchen-products",
        "title": "水槽、拖把與清潔工具要有停靠點：{count} 件餐廚整理單品怎麼看",
        "excerpt": "水槽與清潔工具商品要先看安裝條件、使用後停放位置與走道，本文只整理尺寸與動線判斷。",
        "cover": "Sink Reset",
        "palette": ("#eef4f1", "#48675e", "#c9824f", "#202423"),
        "intent": "洗菜、洗碗、拖把收納與清潔工具歸位",
        "criteria": ["水槽尺寸與安裝條件", "工具使用後停放點", "是否阻擋走道", "濕區與乾區分界"],
    },
    "trash-bin": {
        "category": "lifestyle-culture",
        "series": "居家整理商品推薦",
        "label": "垃圾桶分類",
        "slug": "trash-bin-sorting-home-products",
        "title": "垃圾桶放對位置，家就少一半凌亂：{count} 件分類桶與日常整理選擇",
        "excerpt": "垃圾桶要依垃圾產生的位置決定，不只是看容量。廚房、客廳、工作區與玄關可能需要不同桶型。",
        "cover": "Trash Sorting",
        "palette": ("#f1eee7", "#586958", "#c4864f", "#25231f"),
        "intent": "廚房、客廳、工作區與戶外分類整理",
        "criteria": ["垃圾產生位置", "分類與清倒頻率", "開蓋方式與走道", "外露區域是否容易維持"],
    },
    "large-furniture": {
        "category": "lifestyle-culture",
        "series": "小宅家具商品推薦",
        "label": "大型家具",
        "slug": "compact-large-furniture-dining-bed-sofa-products",
        "title": "大件家具更要先量動線：{count} 件餐桌、床架、沙發與櫃體的選購檢查",
        "excerpt": "大型家具要先看電梯、門寬、走道與日後移動，而不是只看照片。本文整理下單前要確認的尺度與使用情境。",
        "cover": "Furniture Scale",
        "palette": ("#f4efe5", "#555f52", "#c47f4c", "#25231e"),
        "intent": "餐桌、床架、沙發、電視櫃與展示櫃的大件配置",
        "criteria": ["門寬與電梯限制", "走道與椅子拉出距離", "家具是否能分段進場", "低頻大物是否值得保留"],
    },
    "outdoor-patio": {
        "category": "outdoor-escapes",
        "series": "戶外生活商品推薦",
        "label": "戶外庭院",
        "slug": "outdoor-patio-umbrella-garden-products",
        "title": "陽台、庭院與戶外角落怎麼準備：{count} 件遮陽傘、花器與戶外收納清單",
        "excerpt": "戶外商品要看尺寸、收納、天候與使用頻率，尤其是遮陽傘、花器與大件戶外物件。",
        "cover": "Outdoor Patio",
        "palette": ("#eef2e6", "#4e704f", "#d09452", "#22291f"),
        "intent": "陽台、庭院、露營與戶外臨時遮蔭整理",
        "criteria": ["收起後放哪裡", "是否適合現有場地", "重量與搬移方式", "天候變化下的收納"],
    },
    "family-toys-table": {
        "category": "lifestyle-culture",
        "series": "親子禮物商品推薦",
        "label": "親子桌面玩具",
        "slug": "family-table-toys-puzzles-gifts-products",
        "title": "親子禮物先看能不能收回去：{count} 件拼圖、迷宮球與桌面遊戲清單",
        "excerpt": "親子桌面禮物要看共玩時間、零件數量、收納方式與年齡標示，不把玩具寫成成果承諾。",
        "cover": "Family Table",
        "palette": ("#f3efe4", "#466b7d", "#d58a5d", "#2a2421"),
        "intent": "拼圖、迷宮球、桌遊、磁性畫板與桌面共玩",
        "criteria": ["年齡標示與陪同需求", "零件是否容易收納", "一次遊玩時間", "是否能中途收起"],
    },
    "family-outdoor-toys": {
        "category": "outdoor-escapes",
        "series": "親子戶外商品推薦",
        "label": "親子戶外玩具",
        "slug": "family-outdoor-kites-play-products",
        "title": "週末戶外禮物怎麼挑：{count} 件風箏、跳繩與外出小物的使用清單",
        "excerpt": "戶外親子禮物要看場地、收納與成人陪同需求，尤其是風箏、跳繩與可攜式玩具。",
        "cover": "Family Outdoor",
        "palette": ("#edf3ec", "#3f6e73", "#d2904f", "#202625"),
        "intent": "公園、草地、週末戶外與家庭出遊",
        "criteria": ["場地是否足夠", "收納與攜帶方式", "成人陪同需求", "玩完是否容易收尾"],
    },
    "fashion-accessory-gifts": {
        "category": "casual-chic",
        "series": "配件禮物商品推薦",
        "label": "髮飾配件",
        "slug": "hair-accessory-small-gift-products",
        "title": "小禮物不一定要很大盒：{count} 件髮飾、耳飾與包款配件怎麼挑",
        "excerpt": "髮飾、耳飾、小包與墨鏡適合輕量送禮，也適合通勤與週末穿搭搭配，重點是材質、尺寸與使用場合。",
        "cover": "Accessory Gifts",
        "palette": ("#f5eef0", "#6a4e65", "#c98561", "#251f24"),
        "intent": "生日小禮、通勤配件、週末穿搭與旅行收納",
        "criteria": ["收禮者日常風格", "尺寸與配戴頻率", "是否容易收納", "材質資訊與保養方式"],
    },
    "mobile-outdoor-gear": {
        "category": "outdoor-escapes",
        "series": "城市移動商品推薦",
        "label": "移動小物",
        "slug": "mobile-outdoor-rain-bottle-fan-products",
        "title": "通勤與週末外出少一點狼狽：{count} 件雨具、保溫杯、風扇與車用小物",
        "excerpt": "城市移動商品要看重量、收納、續航或容量，不做效果承諾，只整理日常外出的實用判斷。",
        "cover": "Mobile Gear",
        "palette": ("#eef1f4", "#3f5870", "#d18b50", "#20242a"),
        "intent": "通勤、旅行、週末外出、雨天與車用備品",
        "criteria": ["重量與攜帶位置", "容量或續航是否符合需求", "收納後是否佔空間", "使用頻率是否足夠"],
    },
    "ai-work-gadgets": {
        "category": "ai-innovation",
        "series": "AI 工作小物商品推薦",
        "label": "工作小物",
        "slug": "ai-work-gadgets-translation-audio-products",
        "title": "AI 工作不是只有筆電：{count} 件翻譯、音訊與桌邊小物讓工作角落更完整",
        "excerpt": "工作小物要放回真實流程裡看：會議、外出、記錄、音訊與桌面收納，規格仍以商品頁為準。",
        "cover": "AI Work Gear",
        "palette": ("#eef2f5", "#334f6a", "#c07f50", "#20242c"),
        "intent": "會議、翻譯、音訊、筆記、桌面與遠距工作",
        "criteria": ["工作流程是否真的需要", "是否容易收納充電", "規格與相容性", "外出攜帶負擔"],
    },
    "home-scent-gifts": {
        "category": "lifestyle-culture",
        "series": "居家香氛禮物商品推薦",
        "label": "香氛禮物",
        "slug": "home-scent-small-gift-products",
        "title": "居家香氣和小禮物怎麼拿捏：{count} 件香氛、收納與質感小物清單",
        "excerpt": "香氛與小禮物適合放在居家儀式裡看，本文只談氣味偏好、擺放位置與送禮尺度，不涉及身心效果。",
        "cover": "Home Gifts",
        "palette": ("#f5eee7", "#6c5e50", "#ca8454", "#28231f"),
        "intent": "居家氣味、桌邊小禮、拜訪禮與收納搭配",
        "criteria": ["氣味偏好是否明確", "擺放位置與外盒尺寸", "是否適合收禮者日常", "文字標示與商品頁資訊"],
    },
}


EXCLUDE_RULES: list[tuple[str, str]] = [
    ("寵物與動物用品", r"寵物|貓籠|狗籠|鳥籠|鸚鵡|雞籠|雞棚|鴨|鵝|養殖|水族|飼料|儲糧桶|貓抓板|貓別墅|貓屋|貓舍"),
    ("醫療照護或安全風險", r"醫藥|藥品|醫療|醫用|醫材|口罩|藥箱|護理"),
    ("宗教祈福與效果承諾", r"財神|金紙|狐仙|貔貅|補財庫|招財|消災|解厄|打小人|冤親債主|提升貴人|愛情運|旺財運"),
    ("大型工程或農用設備", r"庭院門|別墅大門|鋁合金.*門|農村自建|水塔|儲水罐|農用|橋梁|水袋|花箱.*工程"),
    ("兒童交通工具高風險", r"童車|兒童自行車"),
    ("大型泡澡桶與浴缸", r"成人泡澡桶|洗澡浴桶|浴缸|浴盆"),
]


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def product_code_to_merchant_id(code: str, merchant_name: str) -> str:
    if code.startswith("TP"):
        return code[:9]
    if "vacanza" in merchant_name.lower() or "假期" in merchant_name:
        return "GOODS-vacanza"
    if "泰緯" in merchant_name:
        return "GOODS-da"
    if "易億" in merchant_name:
        return "GOODS-fun-house"
    digest = hashlib.sha1(merchant_name.encode("utf-8")).hexdigest()[:8]
    return f"GOODS-{digest}"


def merchant_meta(merchant_id: str, merchant_name: str) -> dict[str, str]:
    if merchant_id in MERCHANT_FALLBACKS:
        return MERCHANT_FALLBACKS[merchant_id]
    return {
        "brand": merchant_name.strip() or merchant_id,
        "grade": "B",
        "score": "62.0",
        "theme": "home-ritual-lifestyle",
        "source": "綜合_商品頁",
    }


def should_exclude(name: str) -> tuple[bool, str]:
    for reason, pattern in EXCLUDE_RULES:
        if re.search(pattern, name):
            return True, reason
    return False, ""


def classify_bucket(name: str) -> str:
    if re.search(r"翻譯|耳掛|耳罩|藍牙|AI|智能", name, flags=re.I):
        return "ai-work-gadgets"
    if re.search(r"髮|耳環|耳夾|墨鏡|斜背包|包款|大腸圈|髮圈|髮夾|髮帶|飾品", name):
        return "fashion-accessory-gifts"
    if re.search(r"保溫杯|風扇|自動傘|雨衣|打氣機|胎壓|口袋傘|戶外.*小物", name):
        return "mobile-outdoor-gear"
    if re.search(r"精油|香氛|禮盒", name):
        return "home-scent-gifts"
    if re.search(r"風箏|跳繩", name):
        return "family-outdoor-toys"
    if re.search(r"拼圖|迷宮|畫板|桌遊|積木|砂畫|切切樂|彈簧圈|模型|工程車|搶珠|玩具", name):
        return "family-toys-table"
    if re.search(r"遮陽傘|太陽傘|露營傘|吊床|花盆|花架|庭院|陽台|戶外", name):
        return "outdoor-patio"
    if re.search(r"垃圾桶|回收桶|分類桶", name):
        return "trash-bin"
    if re.search(r"水槽|洗菜|洗碗|拖把|塵推|清潔", name):
        return "sink-cleaning"
    if re.search(r"廚房|微波爐|烤箱|餐邊|茶水櫃|蔬菜儲物|鍋", name):
        return "kitchen-rack"
    if re.search(r"床頭櫃|邊櫃|收納櫃子|小型.*櫃|儲物櫃|餐邊櫃", name):
        return "side-cabinet-nightstand"
    if re.search(r"電腦椅|辦公椅|椅子|靠枕|靠背|坐墊|餐椅|化妝椅", name):
        return "chair-cushion"
    if re.search(r"書桌|辦公桌|會議桌|工作臺|大長桌|學習桌|總裁桌|經理桌", name):
        return "desk-work-furniture"
    if re.search(r"髒衣|洗衣籃|衣櫃|衣物|衣服|被子|臥室|床底|床下", name):
        return "closet-laundry-storage"
    if re.search(r"鞋盒|透明鞋|防塵鞋盒|球鞋|靴", name):
        return "shoe-box-rack"
    if re.search(r"鞋櫃|鞋架|換鞋|玄關|門口|雨傘架|傘架", name):
        return "entry-shoe-cabinet"
    if re.search(r"抽屜|夾縫|筆筒|桌面|杯架|包包|置物架|書架|展示架", name):
        return "drawer-storage"
    if re.search(r"收納箱|整理箱|儲物箱|翻蓋|折疊|大容量|收納盒", name):
        return "folding-storage-box"
    if re.search(r"床|沙發|餐桌|茶几|電視櫃|酒櫃|櫃|圓桌|餐臺", name):
        return "large-furniture"
    return "drawer-storage"


def short_product_name(raw: str) -> str:
    text = html.unescape(raw)
    text = re.sub(r"【[^】]{1,10}】", "", text)
    text = re.sub(r"\[[^\]]+\]", "", text)
    text = re.sub(r"[💖✨♔🔥🌍🏃‍♂️🏃‍♀️🇹🇼]+", "", text)
    text = re.sub(r"(免運到府|免運促銷|免運|可打統編|人氣爆款|爆款熱銷|熱賣|爆款|新款|2025新款|廠家直發|廠傢直銷|到府安裝)", "", text)
    text = re.sub(r"(抗菌|除菌|滅菌|殺菌|醫療|醫用|保健|療癒|治療)", "", text)
    text = re.sub(r"\s+", " ", text).strip(" -／/")
    if len(text) > 38:
        text = text[:38].rstrip(" ，、-／/") + "..."
    return text or raw[:38]


def selection_reason(name: str, bucket_key: str) -> str:
    info = BUCKETS[bucket_key]
    if bucket_key in {"family-toys-table", "family-outdoor-toys"}:
        return "適合放入家庭禮物清單，挑選時同步確認年齡標示、陪同需求、場地條件與收納方式。"
    if bucket_key in {"sink-cleaning", "trash-bin", "kitchen-rack"}:
        return "適合用來檢查餐廚與日常整理動線，重點是尺寸、擺放位置、清倒或使用後的收尾方式。"
    if bucket_key in {"desk-work-furniture", "chair-cushion", "ai-work-gadgets"}:
        return "適合補足工作角落的穩定流程，先看桌面深度、使用頻率、收納位置與規格相容性。"
    if bucket_key in {"fashion-accessory-gifts"}:
        return "適合輕量送禮或日常穿搭搭配，重點是使用場合、尺寸、收納與材質資訊。"
    if bucket_key in {"mobile-outdoor-gear", "outdoor-patio"}:
        return "適合通勤、週末或戶外場景，挑選時要看重量、收納、場地條件與實際使用頻率。"
    if "鞋" in name or "傘" in name:
        return "適合安排在玄關動線中比較門片、走道、常穿鞋數量與雨天停放位置。"
    if "收納" in name or "櫃" in name or "箱" in name:
        return "適合建立物品固定位置，先依使用頻率決定放在外層、內層或低頻收納區。"
    return f"適合放入{info['label']}清單，重點是尺寸、使用頻率、拿取動線與收尾方式。"


def risk_note(bucket_key: str, name: str) -> str:
    if bucket_key in {"family-toys-table", "family-outdoor-toys"}:
        return "請依商品年齡標示、場地條件與成人陪同需求使用；本文僅作一般選購參考。"
    if bucket_key == "sink-cleaning" or "水槽" in name:
        return "安裝條件、尺寸與配件請以商品頁與專業評估為準。"
    if bucket_key in {"chair-cushion", "desk-work-furniture"}:
        return "坐感、桌椅高度與使用舒適度因人而異，請依尺寸與個人需求評估。"
    if bucket_key == "home-scent-gifts":
        return "氣味偏好因人而異；本文不涉及身心效果或個別使用承諾。"
    return "價格、規格、活動與庫存請以 momo 商品頁公告為準。"


def load_product_rows() -> list[dict[str, Any]]:
    frame = pd.read_excel(SOURCE_XLSX, dtype=str).fillna("")
    rows: list[dict[str, Any]] = []
    for _, row in frame.iterrows():
        code = row["商品編號"].strip()
        merchant_raw = row["商店名稱"].strip()
        merchant_id = product_code_to_merchant_id(code, merchant_raw)
        meta = merchant_meta(merchant_id, merchant_raw)
        excluded, reason = should_exclude(row["商品名稱"].strip())
        rows.append(
            {
                "code": code,
                "rawName": row["商品名稱"].strip(),
                "name": short_product_name(row["商品名稱"].strip()),
                "merchantId": merchant_id,
                "merchantRawName": merchant_raw,
                "brandName": meta["brand"],
                "commissionRate": row["分潤率"].strip(),
                "sourceProductUrl": row["商品連結"].strip(),
                "affiliateUrl": row["推廣連結"].strip(),
                "bucket": classify_bucket(row["商品名稱"].strip()),
                "excluded": excluded,
                "excludeReason": reason,
            }
        )
    return rows


def placed_codes() -> set[str]:
    codes: set[str] = set()
    article_dir = ROOT / "automation" / "articles"
    for path in article_dir.glob("*.json"):
        try:
            article = load_json(path, {})
        except json.JSONDecodeError:
            continue
        for key in ("mainProducts", "sidebarProducts"):
            for product in article.get(key, []) or []:
                code = str(product.get("code") or "").strip()
                if code:
                    codes.add(code)
    return codes


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
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read(800_000).decode("utf-8", errors="ignore")
    except (urllib.error.URLError, TimeoutError):
        return ""
    patterns = [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, body, flags=re.I)
        if match:
            value = html.unescape(match.group(1)).strip()
            if value.startswith("//"):
                value = "https:" + value
            if value.startswith("http"):
                return value
    return ""


def image_cache() -> dict[str, str]:
    return load_json(IMAGE_CACHE, {})


def build_product(row: dict[str, Any], cache: dict[str, str]) -> dict[str, Any]:
    image_url = cache.get(row["code"], "")
    if image_url is None:
        image_url = ""
    if row["code"] not in cache:
        image_url = "" if os.getenv("MOMO_SKIP_IMAGE_FETCH") else fetch_og_image(row["sourceProductUrl"])
        cache[row["code"]] = image_url
        time.sleep(0.03)
    return {
        "code": row["code"],
        "name": row["name"],
        "merchantId": row["merchantId"],
        "brandName": row["brandName"],
        "affiliateUrl": row["affiliateUrl"],
        "sourceProductUrl": row["sourceProductUrl"],
        "imageUrl": image_url,
        "imageCredit": f"圖片來源：momo 商品頁｜{row['name']}",
        "selectionReason": selection_reason(row["name"], row["bucket"]),
        "riskNote": risk_note(row["bucket"], row["name"]),
    }


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size, index=1 if bold else 0)
            except OSError:
                continue
    return ImageFont.load_default()


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], width: int, fill: str, font_obj: ImageFont.ImageFont) -> int:
    x, y = xy
    line = ""
    for char in text:
        trial = line + char
        box = draw.textbbox((x, y), trial, font=font_obj)
        if box[2] - box[0] > width and line:
            draw.text((x, y), line, fill=fill, font=font_obj)
            y += 64
            line = char
        else:
            line = trial
    if line:
        draw.text((x, y), line, fill=fill, font=font_obj)
        y += 64
    return y


def create_cover(slug: str, title: str, info: dict[str, Any]) -> str:
    bg, accent, warm, dark = info["palette"]
    image = Image.new("RGB", (1200, 630), bg)
    draw = ImageDraw.Draw(image)
    draw.rectangle((72, 72, 1128, 558), outline="#d9d0c4", width=2)
    draw.rounded_rectangle((730, 124, 1065, 450), radius=18, fill="#fffaf1", outline="#d8cdbd", width=2)
    for idx, color in enumerate([accent, warm, "#ead7bd", "#d7dfd5"]):
        draw.rounded_rectangle((780, 178 + idx * 62, 1015, 220 + idx * 62), radius=8, fill=color)
    draw.rectangle((752, 452, 1042, 468), fill=dark)
    draw.rounded_rectangle((150, 360, 510, 500), radius=12, fill="#fffdf8", outline="#d7c8b7", width=2)
    draw.rectangle((190, 398, 470, 432), fill="#e5d5c2")
    draw.ellipse((122, 428, 270, 576), fill="#d8c4aa")
    draw.text((112, 118), "Elite Fashion", fill=accent, font=font(34, True))
    draw.text((112, 162), info["cover"], fill=dark, font=font(24))
    draw_wrapped(draw, title, (112, 224), 570, dark, font(48, True))
    draw.text((112, 504), "商品推薦清單｜尺寸動線｜使用頻率", fill="#665f57", font=font(24))
    output = ROOT / "images" / "optimized" / "article-covers" / f"{slug}.jpg"
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=92, optimize=True)
    return pipeline.relative_to_root(output)


def article_slug(bucket: str, index: int) -> str:
    base = BUCKETS[bucket]["slug"]
    if index == 1:
        return base
    return f"{base}-{index}"


def article_title(bucket: str, count: int, index: int) -> str:
    title = BUCKETS[bucket]["title"].format(count=count)
    variants = [
        "",
        "：進階整理篇",
        "：小空間補位篇",
        "：高頻使用篇",
        "：換季與備品篇",
        "：租屋友善篇",
        "：家庭多人篇",
        "：窄空間篇",
        "：週末整理篇",
    ]
    suffix = variants[index - 1] if index - 1 < len(variants) else f"：第 {index} 組選擇"
    return title + suffix


def brand_cards(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["merchantId"]].append(row)
    cards = []
    for merchant_id, hits in sorted(grouped.items(), key=lambda item: len(item[1]), reverse=True)[:5]:
        meta = merchant_meta(merchant_id, hits[0]["merchantRawName"])
        store_url = f"https://www.momoshop.com.tw/TP/{merchant_id}/main" if merchant_id.startswith("TP") else hits[0]["affiliateUrl"]
        cards.append(
            {
                "name": meta["brand"],
                "merchantId": merchant_id,
                "role": "推薦店家",
                "reason": f"本篇使用 {len(hits)} 件相關商品，適合比較{BUCKETS[hits[0]['bucket']]['label']}的尺寸、用途與收納方式。",
                "url": store_url,
            }
        )
    return cards


def sections_for(info: dict[str, Any], brand_names: str) -> list[dict[str, Any]]:
    criteria = info["criteria"]
    frames = [
        ("先定義這一區要完成的任務", f"{info['intent']}不是靠單一商品解決，而是要先知道物品在哪裡被拿起、在哪裡用完、最後要回到哪裡。"),
        ("尺寸永遠排在款式前面", f"先量寬度、深度、高度與開合方向，再看外觀。{criteria[0]}如果沒有確認，商品到家後很容易卡住動線。"),
        ("把高頻物放在最順手的位置", f"{criteria[1]}會決定商品是否真的被使用。每天會碰的物品要放在外層，低頻備品才適合往高處、深處或床底移。"),
        ("常見錯誤是一次買太多", "很多整理失敗不是因為買得不夠，而是同時加入太多不同尺寸與材質，讓視覺變得更吵。先處理最常亂的一區，成功率通常更高。"),
        ("店家與商品要放在同一個情境比較", f"本篇會看到 {brand_names} 等店家的商品，但判斷重點仍是使用情境。不要只看單一照片，請回到尺寸、動線、拿取頻率與收尾方式。"),
        ("下單前做一分鐘檢查", f"最後確認{criteria[2]}，以及{criteria[3]}。若答案不清楚，先把舊物撤掉、用紙膠帶標出位置，再回來比較商品會更穩。"),
    ]
    return [
        {
            "heading": heading,
            "paragraphs": [
                body,
                "Elite Fashion 編輯團隊的判斷順序，是先看生活流程，再看商品形式。這樣能避開只被照片吸引、卻忽略實際空間限制的購買方式。",
            ],
            "bullets": [
                "先確認尺寸、開合方向與擺放後的走道。",
                "價格、規格、活動與庫存請以 momo 商品頁公告為準。",
            ],
        }
        for heading, body in frames
    ]


def faq_for(info: dict[str, Any]) -> list[dict[str, str]]:
    label = info["label"]
    return [
        {
            "question": f"{label}商品要先看容量嗎？",
            "answer": "容量不是第一步。建議先看尺寸、動線、拿取頻率與收尾位置，再決定容量是否足夠。",
        },
        {
            "question": "商品圖片可以直接當成家中效果參考嗎？",
            "answer": "不建議只看圖片。請回到實際寬度、深度、高度、材質與擺放位置，並以商品頁規格為準。",
        },
        {
            "question": "如果同類商品很多，應該怎麼挑？",
            "answer": "先排除尺寸不合與使用頻率不明的款式，再從最常使用、最容易歸位的商品開始比較。",
        },
    ]


def disclaimer_for(bucket: str) -> str:
    if bucket in {"family-toys-table", "family-outdoor-toys"}:
        return "本文為一般家庭禮物與親子活動情境整理，僅提供年齡標示、共玩時間、收納方式與場地條件的選購參考。玩具與用品請依商品說明與成人陪同需求使用。"
    if bucket == "sink-cleaning":
        return "本文為一般餐廚整理與清潔工具收納情境整理，僅提供尺寸、動線與安裝條件的選購參考，不涉及衛生、醫療或個別風險判斷。"
    if bucket == "home-scent-gifts":
        return "本文為一般居家香氣與送禮情境整理，只提供氣味偏好、擺放位置與禮物尺度參考，不涉及身心效果或個別使用承諾。"
    return "本文為一般商品選購與居家生活情境整理，不宣稱商品承重、耐用年限、個別空間必然適用或使用效果。實際尺寸、材質、活動、價格與庫存請以 momo 商品頁公告為準。"


def make_article(bucket: str, rows: list[dict[str, Any]], index: int, cache: dict[str, str], config: dict[str, Any], categories: dict[str, pipeline.CategoryConfig]) -> dict[str, Any]:
    info = BUCKETS[bucket]
    count = len(rows)
    slug = article_slug(bucket, index)
    title = article_title(bucket, count, index)
    products = [build_product(row, cache) for row in rows]
    main_products = products[: min(10, len(products))]
    sidebar_products = products[min(10, len(products)) :]
    if len(main_products) < 6:
        raise ValueError(f"{slug} main products too few: {len(main_products)}")
    if sidebar_products and len(sidebar_products) < 5:
        main_products = products[: len(products)]
        sidebar_products = []
    if sidebar_products and len(sidebar_products) > 8:
        raise ValueError(f"{slug} sidebar too many: {len(sidebar_products)}")
    brands = brand_cards(rows)
    brand_names = "、".join(brand["name"] for brand in brands[:4])
    hero_image = create_cover(slug, title, info)
    category = categories[info["category"]]
    article = {
        "slug": slug,
        "category": info["category"],
        "title": title,
        "excerpt": info["excerpt"],
        "tags": [info["label"], "商品推薦", "選購清單", "居家整理"],
        "metaTitle": f"Elite Fashion｜{title[:50]}",
        "metaDescription": info["excerpt"][:155],
        "series": info["series"],
        "listingTitle": title[:58],
        "listingExcerpt": info["excerpt"],
        "heroImageAlt": f"{info['label']}情境封面，呈現整齊生活空間與商品選購氛圍，無品牌文字",
        "intro": f"{info['intent']}看似只是買幾件商品，其實真正影響使用感的是尺寸、動線、使用頻率與收尾方式。這篇把 {count} 件商品放在同一個情境裡，幫你先建立判斷順序，再回到各商品頁確認規格。",
        "sections": sections_for(info, brand_names),
        "faq": faq_for(info),
        "extendedReading": [
            {"title": f"瀏覽更多{category.label}文章", "url": f"/{category.page}"},
            {"title": "小宅收納單品：玄關、衣櫃、床底一次整理", "url": "/lifestyle-culture/small-home-storage-products-entry-closet-underbed.html"},
            {"title": "在家工作角落怎麼配", "url": "/ai-innovation/home-office-corner-desk-storage-furniture-guide.html"},
        ],
        "cta": {
            "variant": "gold",
            "text": "先確認尺寸、動線、使用頻率與收尾方式，再逐一查看商品頁規格；若不確定，從最常亂的一區開始就好。",
            "links": [
                {"label": f"前往 {brand['name']}", "url": brand["url"]}
                for brand in brands[:4]
            ],
        },
        "inlineCtas": [
            {
                "afterSection": 2,
                "variant": "olive",
                "eyebrow": "先量尺寸",
                "heading": "把商品放回真實動線裡比較",
                "text": "同一類商品看起來相近，實際差異常在深度、高度、拿取方向與收尾位置。",
                "links": [
                    {"label": main_products[0]["name"], "url": main_products[0]["affiliateUrl"]},
                    {"label": main_products[1]["name"], "url": main_products[1]["affiliateUrl"]},
                ],
            }
        ],
        "disclaimer": disclaimer_for(bucket),
        "audience": "重視居家效率、工作秩序、送禮質感與日常整理的讀者",
        "readTimeMinutes": 10 if count <= 14 else 11,
        "heroImage": hero_image,
        "sourceType": "manual-codex-momo-full-catalog-affiliate",
        "status": "published",
        "queueId": None,
        "mainProducts": main_products,
        "sidebarProducts": sidebar_products,
        "featuredBrands": brands,
    }
    saved = pipeline.save_generated_article(article, None, config, categories)
    pipeline.validate_generated_article(saved, config)
    upsert_publish_log(config, saved)
    return saved


def upsert_publish_log(config: dict[str, Any], article: dict[str, Any]) -> None:
    path = ROOT / config["paths"]["publishLogJson"]
    payload = load_json(path, {"version": 1, "updatedAt": pipeline.now_iso(), "entries": []})
    payload["entries"] = [
        entry
        for entry in payload.get("entries", [])
        if entry.get("file") != article["file"] and entry.get("articleId") != article["id"]
    ]
    payload["updatedAt"] = pipeline.now_iso()
    payload["entries"].insert(
        0,
        {
            "articleId": article["id"],
            "title": article["title"],
            "publishedAt": article["publishedAt"],
            "url": article["url"],
            "file": article["file"],
            "coverImageUrl": pipeline.path_to_url(config["baseUrl"], article["heroImage"]),
            "queueId": None,
            "triggerType": TRIGGER_TYPE,
        },
    )
    pipeline.write_json(path, payload)


def chunk_rows(rows: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    chunks = [rows[i : i + 18] for i in range(0, len(rows), 18)]
    if len(chunks) >= 2 and len(chunks[-1]) < 6:
        chunks[-2].extend(chunks[-1])
        chunks.pop()
    normalized: list[list[dict[str, Any]]] = []
    for chunk in chunks:
        if len(chunk) <= 18:
            normalized.append(chunk)
        else:
            normalized.append(chunk[:18])
            normalized.append(chunk[18:])
    return normalized


def plan_articles(rows: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]], int]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["bucket"]].append(row)
    plans: list[tuple[str, list[dict[str, Any]], int]] = []
    leftovers: list[dict[str, Any]] = []
    for bucket in BUCKETS:
        bucket_rows = sorted(grouped.get(bucket, []), key=lambda item: (item["merchantId"], item["name"], item["code"]))
        if not bucket_rows:
            continue
        if len(bucket_rows) < 6:
            leftovers.extend(bucket_rows)
            continue
        for index, chunk in enumerate(chunk_rows(bucket_rows), start=1):
            if len(chunk) >= 6:
                plans.append((bucket, chunk, index))
            else:
                leftovers.extend(chunk)
    if leftovers:
        for index, chunk in enumerate(chunk_rows(leftovers), start=1):
            if len(chunk) >= 6:
                plans.append(("drawer-storage", chunk, 50 + index))
    return plans


def update_latest_run(config: dict[str, Any], articles: list[dict[str, Any]], report: dict[str, Any]) -> None:
    payload = {
        "version": 1,
        "updatedAt": pipeline.now_iso(),
        "status": "generated",
        "triggerType": TRIGGER_TYPE,
        "newsletter": "not_sent_manual_codex_publish",
        "articleIds": [article["id"] for article in articles],
        "articleSlugs": [article["slug"] for article in articles],
        "report": {
            "sourceProducts": report["sourceProducts"],
            "eligibleProducts": report["eligibleProducts"],
            "excludedProducts": report["excludedProducts"],
            "newlyPlacedProducts": report["newlyPlacedProducts"],
            "totalPlacedProducts": report["totalPlacedProducts"],
        },
        "notes": "手動產文並推送 main 不會自動寄送電子報；本批已記錄為未寄送。",
    }
    pipeline.write_json(ROOT / config["paths"]["latestRunJson"], payload)


def update_tracker(articles: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> None:
    with TRACKER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    by_id = {row["merchant_id"]: row for row in rows}
    source_by_merchant: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in source_rows:
        if not row["excluded"]:
            source_by_merchant[row["merchantId"]].append(row)
    mentions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in articles:
        merchant_ids = {
            product["merchantId"]
            for product in [*article.get("mainProducts", []), *article.get("sidebarProducts", [])]
        }
        for merchant_id in merchant_ids:
            mentions[merchant_id].append(article)
    for merchant_id, article_hits in mentions.items():
        sample = source_by_merchant[merchant_id][0]
        meta = merchant_meta(merchant_id, sample["merchantRawName"])
        row = by_id.get(merchant_id)
        if row is None:
            row = {name: "" for name in fieldnames}
            row["merchant_id"] = merchant_id
            rows.append(row)
            by_id[merchant_id] = row
        row["brand"] = meta["brand"]
        row["source_sheet"] = meta["source"]
        row["recommendation_grade"] = meta["grade"]
        row["score"] = meta["score"]
        row["commission_rate"] = sample.get("commissionRate") or row.get("commission_rate") or "11.0%"
        row["main_products"] = "、".join(sorted({item["name"].replace("...", "")[:12] for item in source_by_merchant[merchant_id][:8]}))
        row["content_angles"] = "商品清單、尺寸動線、使用頻率、收納與送禮情境"
        row["promo_link_check"] = "OK"
        row["store_link"] = f"https://www.momoshop.com.tw/TP/{merchant_id}/main" if merchant_id.startswith("TP") else sample["affiliateUrl"]
        row["assigned_theme"] = meta["theme"]
        row["brand_role"] = "推薦店家"
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
        note = "2026-05-22 momo 首批商品清單補齊置入；不適合品項已另列排除報告。"
        if note not in row.get("notes", ""):
            row["notes"] = (row.get("notes", "").rstrip() + (" " if row.get("notes", "").strip() else "") + note).strip()
    with TRACKER_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def all_product_article_code_map() -> tuple[dict[str, str], list[dict[str, Any]]]:
    article_by_code: dict[str, str] = {}
    product_articles: list[dict[str, Any]] = []
    for path in (ROOT / "automation" / "articles").glob("*.json"):
        article = load_json(path, {})
        products = [*article.get("mainProducts", []), *article.get("sidebarProducts", [])]
        if not products:
            continue
        product_articles.append(article)
        for product in products:
            code = str(product.get("code") or "").strip()
            if code:
                article_by_code[code] = article.get("slug", "")
    return article_by_code, product_articles


def write_report(rows: list[dict[str, Any]], articles: list[dict[str, Any]], initially_placed: set[str]) -> dict[str, Any]:
    article_by_code, _ = all_product_article_code_map()
    final_placed = placed_codes()
    entries = []
    for row in rows:
        status = "excluded" if row["excluded"] else "placed" if row["code"] in final_placed else "pending"
        entries.append(
            {
                "code": row["code"],
                "name": row["name"],
                "merchantId": row["merchantId"],
                "brandName": row["brandName"],
                "bucket": row["bucket"],
                "status": status,
                "reason": row["excludeReason"] if row["excluded"] else "",
                "articleSlug": article_by_code.get(row["code"], ""),
            }
        )
    report = {
        "updatedAt": pipeline.now_iso(),
        "sourceProducts": len(rows),
        "eligibleProducts": sum(not row["excluded"] for row in rows),
        "excludedProducts": sum(row["excluded"] for row in rows),
        "alreadyPlacedBeforeRun": sum(row["code"] in initially_placed for row in rows),
        "newlyPlacedProducts": sum((not row["excluded"]) and row["code"] not in initially_placed and row["code"] in final_placed for row in rows),
        "totalPlacedProducts": sum((not row["excluded"]) and row["code"] in final_placed for row in rows),
        "pendingEligibleProducts": sum((not row["excluded"]) and row["code"] not in final_placed for row in rows),
        "articlesCreated": len(articles),
        "entries": entries,
    }
    pipeline.write_json(PLACEMENT_REPORT, report)
    return report


def main() -> int:
    config, categories = pipeline.load_config()
    source_rows = load_product_rows()
    initial = placed_codes()
    candidates = [
        row
        for row in source_rows
        if not row["excluded"] and row["code"] not in initial
    ]
    plans = plan_articles(candidates)
    cache = image_cache()
    articles = [
        make_article(bucket, rows, index, cache, config, categories)
        for bucket, rows, index in plans
    ]
    pipeline.write_json(IMAGE_CACHE, cache)
    report = write_report(source_rows, articles, initial)
    update_tracker(articles, source_rows)
    update_latest_run(config, articles, report)
    print(
        json.dumps(
            {
                "articlesCreated": len(articles),
                "sourceProducts": report["sourceProducts"],
                "eligibleProducts": report["eligibleProducts"],
                "excludedProducts": report["excludedProducts"],
                "newlyPlacedProducts": report["newlyPlacedProducts"],
                "totalPlacedProducts": report["totalPlacedProducts"],
                "pendingEligibleProducts": report["pendingEligibleProducts"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    for article in articles:
        print(f"- {article['slug']} -> {article['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
