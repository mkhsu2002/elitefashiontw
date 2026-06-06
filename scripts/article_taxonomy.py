#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Any


CORE_HUB_LINKS: dict[str, list[tuple[str, str]]] = {
    "mature-life-reset": [
        ("離婚後先做哪六件事", "lifestyle-culture/post-divorce-first-6-steps.html"),
        ("返台後的九十天生活清單", "lifestyle-culture/return-divorce-restart-90-day-checklist.html"),
        ("一人生活的居家安全與收納", "lifestyle-culture/solo-living-home-safety-organization-divorce.html"),
        ("高階女性的社交邊界重建", "lifestyle-culture/post-divorce-social-boundaries-highly-educated-women.html"),
        ("返台後的職涯與收入安排", "lifestyle-culture/divorcee-return-taiwan-career-income-plan.html"),
        ("高階主管喪偶後第一個月穩定計畫", "lifestyle-culture/executive-widowed-first-month-stability-plan.html"),
        ("長期一人生活的安全與資源配置", "lifestyle-culture/long-term-solo-living-home-safety-support-map.html"),
        ("家庭對話與跨國記憶整理", "lifestyle-culture/cross-border-memory-family-dialogue-forward.html"),
        ("創業者的長期韌性與自我照顧", "lifestyle-culture/entrepreneur-long-term-resilience-finance-community-selfcare.html"),
        ("重建社交圈與台灣生活節奏", "lifestyle-culture/rebuilding-social-circle-taiwan-returnee-women.html"),
    ],
    "body-rhythm-reset": [
        ("春夏睡眠與降溫順序", "wellness-movement/mature-women-spring-summer-cooling-sleep.html"),
        ("睡前儀式、耳塞、枕頭與光線", "wellness-movement/bedtime-home-ritual-earplugs-pillow-scent-light.html"),
        ("久坐辦公室的低門檻伸展", "wellness-movement/office-sitting-low-barrier-stretch-snack-pillow.html"),
        ("肌力與行動力基礎", "wellness-movement/sarcopenia-prevention.html"),
        ("旅行後的恢復科技與肩頸照顧", "wellness-movement/recovery-tech.html"),
        ("居家伸展角落與瑜伽墊配置", "wellness-movement/home-stretch-corner-yoga-mat-light-scent.html"),
        ("保守補給與日常飲食清單", "wellness-movement/conservative-supplement-vegetarian-job-tears-guide.html"),
        ("按摩、護具與送禮選物", "wellness-movement/home-comfort-massage-device-brace-gift-guide.html"),
        ("照護用品與居家動線", "wellness-movement/home-care-flow-bathing-transfer-storage-safety.html"),
        ("輕食零食與辦公補給", "wellness-movement/light-snack-cabinet-low-sugar-nuts-vegetarian.html"),
    ],
    "ai-work-reset-45": [
        ("不用寫程式的 AI 入門", "ai-innovation/ai-45.html"),
        ("辦公室 AI 生存指南", "ai-innovation/ai-survival-guide-mature-workers.html"),
        ("管理者如何導入 AI 工作流程", "life-proposals/ai-career-navigation-for-managers.html"),
        ("AI 與職涯第二曲線", "life-proposals/ai-second-curve-for-career-pivot.html"),
        ("用 AI 整理履歷與面試素材", "life-proposals/resume-refresh-modern.html"),
        ("專業經驗的小型 AI 副業測試", "life-proposals/ai-side-hustle-for-experts.html"),
        ("AI 工作角落與翻譯音訊工具", "ai-innovation/ai-work-gadgets-translation-audio-products.html"),
        ("手機配件、車用充電與工作桌", "ai-innovation/phone-accessory-commute-car-charging-desk.html"),
        ("創意主權與 AI 內容工作", "ai-innovation/ai-creative-sovereignty.html"),
        ("AI 倫理與奢侈品牌", "ai-innovation/ai-ethics-luxury.html"),
    ],
    "commute-style-reset": [
        ("春夏膠囊衣櫥", "spring-summer-capsule-wardrobe.html"),
        ("通勤襯衫、長褲、外套與鞋子", "casual-chic/mens-commute-shirt-trousers-jacket-shoes.html"),
        ("大尺碼正式休閒穿搭順序", "casual-chic/plus-size-office-travel-weekend-outfit-order.html"),
        ("旅行穿搭與行李衣物", "casual-chic/travel-wear.html"),
        ("膠囊衣櫥基礎", "casual-chic/capsule-wardrobe.html"),
        ("混合辦公風格", "casual-chic/hybrid-office-style-2026.html"),
        ("斜背包風格指南", "crossbody-bag-style-guide.html"),
        ("髮飾與小禮物配件", "casual-chic/hair-accessory-small-gift-products.html"),
        ("珠寶、皮件與小包送禮", "casual-chic/jewelry-leather-gift-ring-silver-wallet-small-bag.html"),
        ("早晨十分鐘儀容整理", "casual-chic/ten-minute-morning-grooming-lip-makeup-kit.html"),
    ],
    "outdoor-travel-reset": [
        ("背包舒適與重量配置", "outdoor-escapes/backpack-comfort-guide.html"),
        ("新手健行裝備順序", "outdoor-escapes/beginner-hiking-gear-order-light-trail.html"),
        ("一日出行包與天氣備案", "outdoor-escapes/day-trip-bag-essentials-sun-charging-rainwear.html"),
        ("前開式行李箱與收納系統", "outdoor-escapes/travel-luggage-front-open-carry-on-packing-system.html"),
        ("露營咖啡與戶外備餐", "outdoor-escapes/camping-coffee-outdoor-meal-prep.html"),
        ("iPhone 旅行 Vlog 裝備", "outdoor-escapes/iphone-travel-vlog-monitor.html"),
        ("戶外內容創作裝備", "outdoor-escapes/content-creation-gear.html"),
        ("全球旅行目的地準備", "outdoor-escapes/global-top-travel-destinations-2026.html"),
        ("太空旅行頸枕與機上睡眠", "outdoor-escapes/horizon-x-space-travel-neck-pillow.html"),
        ("雨天通勤與反光配件", "outdoor-escapes/scooter-commute-rain-gear-reflective-accessories.html"),
    ],
}

HUBS: dict[str, dict[str, str]] = {
    "mature-life-reset": {
        "title": "人生重整與一人生活秩序",
        "file": "mature-life-reset.html",
        "category": "lifestyle-culture",
    },
    "body-rhythm-reset": {
        "title": "身體節奏與恢復生活指南",
        "file": "body-rhythm-reset.html",
        "category": "wellness-movement",
    },
    "ai-work-reset-45": {
        "title": "AI 工作重整與第二曲線",
        "file": "ai-work-reset-45.html",
        "category": "ai-innovation",
    },
    "commute-style-reset": {
        "title": "通勤衣櫥與鞋包選物指南",
        "file": "commute-style-reset.html",
        "category": "casual-chic",
    },
    "outdoor-travel-reset": {
        "title": "旅行與戶外移動準備指南",
        "file": "outdoor-travel-reset.html",
        "category": "outdoor-escapes",
    },
}

PRIMARY_HUB_BY_CATEGORY = {
    "ai-innovation": "ai-work-reset-45",
    "wellness-movement": "body-rhythm-reset",
    "outdoor-escapes": "outdoor-travel-reset",
    "casual-chic": "commute-style-reset",
    "runway-trends": "commute-style-reset",
    "designer-perspective": "commute-style-reset",
    "lifestyle-culture": "mature-life-reset",
    "special-features": "mature-life-reset",
}

STABLE_TOPIC_CATEGORIES: dict[str, dict[str, Any]] = {
    "ai-workflow": {"label": "AI 工作流", "defaultHub": "ai-work-reset-45", "keywords": ["ai", "人工智能", "工作流", "automation", "自動化", "辦公"]},
    "creator-tools": {"label": "創作工具", "defaultHub": "ai-work-reset-45", "keywords": ["創作", "拍攝", "vlog", "內容", "相機", "手機攝影"]},
    "smart-living-tech": {"label": "智慧生活科技", "defaultHub": "ai-work-reset-45", "keywords": ["智慧", "smart", "gadgets", "充電", "螢幕", "筆電"]},
    "career-money": {"label": "職涯與金錢", "defaultHub": "mature-life-reset", "keywords": ["職涯", "履歷", "收入", "財務", "投資", "退休", "創業", "副業"]},
    "life-reset": {"label": "人生重整", "defaultHub": "mature-life-reset", "keywords": ["離婚", "喪偶", "返台", "獨居", "重建", "一人生活", "邊界"]},
    "relationships-family": {"label": "關係與家庭", "defaultHub": "mature-life-reset", "keywords": ["家庭", "親子", "伴侶", "家人", "社交", "友誼", "關係"]},
    "home-rituals": {"label": "居家儀式", "defaultHub": "mature-life-reset", "keywords": ["居家", "收納", "清潔", "廚房", "臥室", "香氛", "餐桌"]},
    "wardrobe-style": {"label": "衣櫥與穿搭", "defaultHub": "commute-style-reset", "keywords": ["衣櫥", "穿搭", "通勤", "外套", "襯衫", "長褲", "膠囊"]},
    "bags-shoes-accessories": {"label": "鞋包與配件", "defaultHub": "commute-style-reset", "keywords": ["包", "鞋", "皮件", "珠寶", "配件", "髮飾", "雨傘"]},
    "beauty-grooming": {"label": "妝髮與身體照護", "defaultHub": "commute-style-reset", "keywords": ["妝", "髮", "保養", "香水", "美容", "指甲", "肌膚"]},
    "runway-fashion": {"label": "秀場與流行", "defaultHub": "commute-style-reset", "keywords": ["秀場", "時裝週", "runway", "couture", "流行", "趨勢"]},
    "designer-craft": {"label": "設計與工藝", "defaultHub": "commute-style-reset", "keywords": ["設計師", "工藝", "品牌", "剪裁", "攝影師", "永續"]},
    "sleep-recovery": {"label": "睡眠與恢復", "defaultHub": "body-rhythm-reset", "keywords": ["睡", "恢復", "耳塞", "枕", "疲勞", "按摩"]},
    "movement-fitness": {"label": "活動與肌力", "defaultHub": "body-rhythm-reset", "keywords": ["運動", "瑜伽", "伸展", "肌力", "久坐", "健身"]},
    "food-nutrition": {"label": "飲食與補給", "defaultHub": "body-rhythm-reset", "keywords": ["飲食", "營養", "補給", "零食", "雞胸", "蔬菜", "茶"]},
    "care-support": {"label": "照護與輔具", "defaultHub": "body-rhythm-reset", "keywords": ["照護", "護具", "長照", "支撐", "護膝", "醫療"]},
    "travel-planning": {"label": "旅行準備", "defaultHub": "outdoor-travel-reset", "keywords": ["旅行", "行李", "機上", "旅宿", "出行", "目的地"]},
    "outdoor-gear": {"label": "戶外裝備", "defaultHub": "outdoor-travel-reset", "keywords": ["戶外", "登山", "健行", "露營", "背包", "雨具"]},
    "pet-family-life": {"label": "寵物與家庭日常", "defaultHub": "mature-life-reset", "keywords": ["寵物", "貓", "狗", "親子", "玩具", "家庭"]},
    "culture-hospitality": {"label": "文化與款待", "defaultHub": "mature-life-reset", "keywords": ["咖啡", "旅宿", "藝術", "閱讀", "米其林", "送禮", "款待"]},
}


def extensionless_path(relative_path: str) -> str:
    relative_path = relative_path.lstrip("/")
    if relative_path.endswith(".html"):
        return relative_path[:-5]
    return relative_path


def normalized_article_path(record: dict[str, Any]) -> str:
    value = record.get("file") or record.get("relativeUrl") or record.get("url") or ""
    value = str(value).split("?", 1)[0].split("#", 1)[0]
    value = re.sub(r"^https?://[^/]+/", "", value)
    if value and not value.endswith(".html"):
        value = f"{value}.html"
    return value.lstrip("/")


def hub_payload(key: str) -> dict[str, str]:
    hub = HUBS[key]
    return {
        "key": key,
        "title": hub["title"],
        "file": hub["file"],
        "url": f"/{extensionless_path(hub['file'])}",
        "category": hub["category"],
    }


def text_for_classification(record: dict[str, Any]) -> str:
    parts = [
        str(record.get("title") or ""),
        str(record.get("listingTitle") or ""),
        str(record.get("excerpt") or ""),
        str(record.get("metaDescription") or ""),
        " ".join(str(item) for item in record.get("tags") or []),
        normalized_article_path(record),
    ]
    return " ".join(parts).lower()


def classify_topic_category(record: dict[str, Any]) -> tuple[str, str]:
    text = text_for_classification(record)
    best_key = ""
    best_score = 0
    for key, topic in STABLE_TOPIC_CATEGORIES.items():
        score = sum(1 for keyword in topic["keywords"] if str(keyword).lower() in text)
        if score > best_score:
            best_key = key
            best_score = score
    if best_key:
        return best_key, STABLE_TOPIC_CATEGORIES[best_key]["label"]

    fallback_by_category = {
        "ai-innovation": "ai-workflow",
        "runway-trends": "runway-fashion",
        "designer-perspective": "designer-craft",
        "casual-chic": "wardrobe-style",
        "wellness-movement": "movement-fitness",
        "outdoor-escapes": "outdoor-gear",
        "lifestyle-culture": "home-rituals",
        "special-features": "culture-hospitality",
    }
    key = fallback_by_category.get(str(record.get("category") or ""), "home-rituals")
    return key, STABLE_TOPIC_CATEGORIES[key]["label"]


def core_hubs_for_article(path: str) -> list[str]:
    matches = []
    normalized = path.lstrip("/")
    for hub_key, links in CORE_HUB_LINKS.items():
        if any(link_path == normalized for _, link_path in links):
            matches.append(hub_key)
    return matches


def article_hub_keys(record: dict[str, Any]) -> tuple[str, list[str]]:
    path = normalized_article_path(record)
    core_matches = core_hubs_for_article(path)
    topic_key, _ = classify_topic_category(record)
    topic_default = STABLE_TOPIC_CATEGORIES[topic_key]["defaultHub"]
    category_default = PRIMARY_HUB_BY_CATEGORY.get(str(record.get("category") or ""), "mature-life-reset")
    primary = core_matches[0] if core_matches else topic_default or category_default
    secondary: list[str] = []
    for candidate in [*core_matches[1:], topic_default, category_default]:
        if candidate != primary and candidate in HUBS and candidate not in secondary:
            secondary.append(candidate)
        if len(secondary) >= 2:
            break
    return primary, secondary[:2]


def enrich_article_record(record: dict[str, Any]) -> dict[str, Any]:
    topic_key, topic_label = classify_topic_category(record)
    primary_key, secondary_keys = article_hub_keys({**record, "topicCategory": topic_key})
    record["topicCategory"] = topic_key
    record["topicCategoryLabel"] = topic_label
    record["primaryHub"] = hub_payload(primary_key)
    record["secondaryHubs"] = [hub_payload(key) for key in secondary_keys[:2]]
    return record


def validate_article_taxonomy(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not 16 <= len(STABLE_TOPIC_CATEGORIES) <= 24:
        errors.append(f"stable topic category count must be 16-24, got {len(STABLE_TOPIC_CATEGORIES)}")
    for hub_key, links in CORE_HUB_LINKS.items():
        if not 8 <= len(links) <= 12:
            errors.append(f"{hub_key} must expose 8-12 core articles, got {len(links)}")
    for record in records:
        identity = normalized_article_path(record) or str(record.get("id") or record.get("title") or "unknown")
        primary = record.get("primaryHub")
        secondary = record.get("secondaryHubs") or []
        if not isinstance(primary, dict) or primary.get("key") not in HUBS:
            errors.append(f"{identity} missing valid primaryHub")
        if len(secondary) > 2:
            errors.append(f"{identity} has more than 2 secondaryHubs")
        seen_secondary = [item.get("key") for item in secondary if isinstance(item, dict)]
        if len(seen_secondary) != len(set(seen_secondary)):
            errors.append(f"{identity} has duplicate secondaryHubs")
        if primary and primary.get("key") in seen_secondary:
            errors.append(f"{identity} primaryHub repeats in secondaryHubs")
        if record.get("topicCategory") not in STABLE_TOPIC_CATEGORIES:
            errors.append(f"{identity} has invalid topicCategory")
    return errors
