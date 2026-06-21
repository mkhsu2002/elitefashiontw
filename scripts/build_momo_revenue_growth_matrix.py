#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACKER_CSV = ROOT / "automation" / "momo-brand-recommendation-tracker.csv"
OUT_DIR = ROOT / "automation" / "reports"
DATE_STAMP = "2026-06-21"
CSV_OUT = OUT_DIR / f"momo-affiliate-revenue-growth-matrix-{DATE_STAMP}.csv"
JSON_OUT = OUT_DIR / f"momo-affiliate-revenue-growth-matrix-{DATE_STAMP}.json"
MD_OUT = OUT_DIR / f"momo-affiliate-revenue-growth-plan-{DATE_STAMP}.md"

VALID_CATEGORIES = {
    "ai-innovation",
    "casual-chic",
    "lifestyle-culture",
    "outdoor-escapes",
    "wellness-movement",
}

BLOCKED_TITLE_TERMS = {
    "30+",
    "40+",
    "45+",
    "50+",
    "熟齡",
    "銀髮",
    "老人",
    "SEO",
    "GEO",
    "AEO",
    "品牌池",
    "矩陣",
    "批次",
    "分潤",
}


@dataclass(frozen=True)
class ArticleSpec:
    week: int
    slot: int
    cadence_type: str
    cluster: str
    category: str
    form: str
    title: str
    slug: str
    intent: str
    primary: tuple[str, ...]
    supporting: tuple[str, ...]
    internal_links: tuple[str, ...]
    cta_style: str
    risk_guardrail: str
    elite_judgment: str
    answer_summary: str


PILLARS: list[dict[str, str]] = [
    {
        "cluster": "通勤穿搭與移動包款",
        "category": "casual-chic",
        "slug": "commute-mobile-wardrobe-affiliate-hub",
        "title": "通勤、雨天與旅行鞋包配置主題頁",
        "purpose": "收束包款、防曬、雨具、鞋履與會議整理包文章，承接高購買意圖內鏈。",
    },
    {
        "cluster": "居家儀式與收納升級",
        "category": "lifestyle-culture",
        "slug": "home-ritual-storage-affiliate-hub",
        "title": "居家儀式、收納與清潔主題頁",
        "purpose": "收束香氛、燈光、床寢、收納、清潔與租屋改造文章。",
    },
    {
        "cluster": "AI 工作角落與創作者裝備",
        "category": "ai-innovation",
        "slug": "ai-work-creator-gear-affiliate-hub",
        "title": "AI 工作角落與創作者裝備主題頁",
        "purpose": "收束外接螢幕、筆電周邊、遠距工作包與手機拍攝裝備文章。",
    },
    {
        "cluster": "低壓恢復與身體支撐",
        "category": "wellness-movement",
        "slug": "recovery-support-affiliate-hub",
        "title": "睡眠、護具與居家恢復主題頁",
        "purpose": "收束睡前環境、耳塞、護具、按摩設備、伸展與低負擔補給文章。",
    },
    {
        "cluster": "辦公室補給與質感送禮",
        "category": "lifestyle-culture",
        "slug": "office-pantry-gifting-affiliate-hub",
        "title": "辦公室補給、咖啡茶與質感送禮主題頁",
        "purpose": "收束咖啡、茶、冷凍庫備餐、零食櫃、客戶禮與餐桌文章。",
    },
    {
        "cluster": "輕戶外與旅行準備",
        "category": "outdoor-escapes",
        "slug": "light-outdoor-travel-affiliate-hub",
        "title": "輕戶外、旅行與出門準備主題頁",
        "purpose": "收束露營、登山、防雨、防曬、行李箱與戶外餐食文章。",
    },
]


def s(*values: str) -> tuple[str, ...]:
    return tuple(values)


SPECS: list[ArticleSpec] = [
    ArticleSpec(1, 1, "高購買意圖導購文", "通勤穿搭與移動包款", "casual-chic", "buying-priority-guide", "通勤包不是越大越好：容量、肩帶、正式感與雨天備案怎麼選", "commute-bag-size-strap-formality-rain-backup", "通勤包選購", s("TP0007070", "TP0009277", "TP0004592"), s("TP0003240", "TP0003337", "TP0005684"), s("commute-bag-capacity-weight-strap-formality-guide", "rainy-workday-rain-boots-coat-umbrella-bag-materials"), "比較表後放三顆品牌 CTA", "不宣稱耐用、防水或容量足夠所有情境。", "先用每天帶的三件物品決定容量，再用肩帶與場合決定外型。", "通勤包應先看每天攜帶物、肩背負擔與正式場合，再補雨天材質備案。"),
    ArticleSpec(1, 2, "高購買意圖導購文", "通勤穿搭與移動包款", "casual-chic", "seasonal-checklist", "雨天上班不失控：抗風傘、雨鞋、雨衣與包款材質清單", "rainy-commute-umbrella-rain-shoes-bag-materials", "雨天通勤採買", s("TP0001609", "TP0005684", "TP0009277"), s("TP0005647", "TP0007070", "TP0005110"), s("rainy-workday-rain-boots-coat-umbrella-bag-materials", "spring-summer-commute-sun-protection-umbrella-light-bag"), "段落內雙 CTA 加文末品牌清單", "不保證防雨、防滑或抗風效果，規格回商品頁。", "把雨具分成抵達前、進門後、收納時三段，避免只買好看的傘。", "雨天通勤要同時處理防雨、收納與體面感，不能只看單一雨具。"),
    ArticleSpec(1, 3, "高購買意圖導購文", "AI 工作角落與創作者裝備", "ai-innovation", "use-case-guide", "手機不是只靠保護殼：車用、桌面、充電與 MagSafe 配件整理法", "phone-accessory-car-desk-charging-magsafe-system", "手機配件選購", s("TP0009476", "TP0000669", "TP0009160"), s("TP0007239", "TP0009130", "TP0002918"), s("phone-accessory-commute-car-charging-desk", "mobile-photography-cpl-rig-outdoor-creator-kit"), "商品卡分車用/桌面/外出三區", "不宣稱充電速度、相容性或安全認證，需回商品頁確認。", "先區分車上、辦公桌、旅行三個場景，再決定是否需要同一品牌系統。", "手機配件應按使用場景分層，而不是只看保護殼外觀。"),
    ArticleSpec(1, 4, "比較/選購順序文", "辦公室補給與質感送禮", "lifestyle-culture", "comparison-guide", "辦公室咖啡補給怎麼選：咖啡豆、濾掛、掛耳包與送禮盒", "office-coffee-beans-drip-bag-gift-box-guide", "辦公室咖啡", s("TP0000706", "TP0006151", "TP0009388"), s("TP0006698", "TP0009303", "TP0006348"), s("office-coffee-beans-drip-bags-workday-guide", "quality-gifting-coffee-tea-massage-umbrella-custom"), "比較表後放辦公室與送禮兩組 CTA", "不宣稱風味排名、獎項或即時價格。", "先看沖泡條件與共用情境，再決定豆、濾掛或禮盒。", "辦公室咖啡的選擇關鍵是沖泡門檻、保存方式與是否適合共享。"),
    ArticleSpec(1, 5, "AEO/GEO 答案型文章", "低壓恢復與身體支撐", "wellness-movement", "faq-hub", "睡前環境怎麼整理：耳塞、枕頭、燈光與香氛的低壓順序", "bedtime-environment-earplugs-pillow-light-scent-order", "睡前環境整理", s("TP0003593", "TP0001941", "TP0007295"), s("TP0002458", "TP0009548", "TP0009429"), s("bedtime-home-ritual-earplugs-pillow-scent-light", "home-stretch-corner-yoga-mat-light-scent"), "FAQ 前放低壓環境 CTA", "不承諾改善失眠、降噪效果或心理療效。", "先降低干擾，再補舒適物件；香氛只能放在清潔與通風之後。", "睡前環境應先處理聲音、光線與枕寢支撐，再考慮香氛。"),
    ArticleSpec(1, 6, "季節/情境文", "居家儀式與收納升級", "lifestyle-culture", "seasonal-checklist", "夏天前整理家的空氣路線：循環扇、小家電與照明怎麼配", "summer-airflow-fan-small-appliance-lighting-system", "夏季小家電", s("TP0006567", "TP0005764", "TP0007295"), s("TP0005935", "TP0007694", "TP0004799"), s("summer-airflow-fan-small-appliance-lighting", "living-room-work-corner-lighting-scent-storage"), "以使用位置分區 CTA", "不宣稱降溫、節電或健康效果。", "先判斷風從哪裡進、熱停在哪裡，再決定電器與燈光。", "夏季家電要和空氣動線、桌面位置與照明一起規劃。"),
    ArticleSpec(1, 7, "高購買意圖導購文", "輕戶外與旅行準備", "outdoor-escapes", "buying-priority-guide", "一日輕旅行包裡放什麼：防曬、充電、耳塞、雨具與小包", "day-trip-bag-sun-charging-earplug-rainwear-checklist", "一日旅行準備", s("TP0007070", "TP0009476", "TP0003593"), s("TP0000116", "TP0005684", "TP0009277"), s("day-trip-bag-essentials-sun-charging-rainwear", "travel-shoes-bag-lightweight-crossbody-rain-backup"), "清單中段放出門前 CTA", "不宣稱商品適合所有天氣或航空/交通限制。", "用拿取頻率決定包內位置，雨具與充電不要放在最深處。", "一日旅行的採買順序是防曬與電力先行，再補睡眠與雨天備案。"),
    ArticleSpec(1, 8, "品牌質感型雜誌文", "居家儀式與收納升級", "lifestyle-culture", "buy-better-longer-guide", "下班後的家要先安靜下來：香氛、燈光與收納的升級順序", "after-work-home-scent-light-storage-upgrade-order", "居家儀式", s("TP0002458", "TP0007295", "TP0005953"), s("TP0004627", "TP0009429", "TP0005162"), s("home-evening-scent-lighting-storage-ritual", "living-room-work-corner-lighting-scent-storage"), "克制品牌連結，文末集中 CTA", "不宣稱療癒、淨化或心理效果。", "先收掉視覺噪音，再談光線與味道，家才會真正安靜。", "下班後的居家升級應從收納與光線開始，香氛只負責最後一層情緒。"),
    ArticleSpec(1, 9, "比較/選購順序文", "AI 工作角落與創作者裝備", "ai-innovation", "comparison-guide", "第二螢幕怎麼選：外接螢幕、筆電、支架與資料備份的工作配置", "second-monitor-laptop-stand-backup-work-setup", "第二螢幕工作配置", s("TP0005967", "TP0002753", "TP0007010"), s("TP0000858", "TP0009476", "TP0006238"), s("second-monitor-laptop-desk-setup-ai-workflow", "ai-workflow-laptop-spec-warranty-monitor-backup"), "規格判斷表後放品牌 CTA", "不捏造效能測試、保固或相容性。", "先看工作視窗數量與攜帶需求，再談螢幕尺寸與筆電規格。", "第二螢幕的價值在於工作動線，而不是單純追求大尺寸。"),
    ArticleSpec(1, 10, "AEO/GEO 答案型文章", "辦公室補給與質感送禮", "lifestyle-culture", "faq-hub", "下午三點喝什麼：無糖茶、花草茶、氣泡飲與沖泡飲怎麼放辦公室", "office-afternoon-drinks-tea-sparkling-pantry-guide", "辦公室飲品", s("TP0005142", "TP0008786", "TP0000776"), s("TP0009026", "TP0001663", "TP0008341"), s("office-afternoon-tea-drink-pantry-guide", "office-drinks-sparkling-plant-milk-tea-coffee"), "FAQ 後放飲品補貨 CTA", "草本與酵素飲不得宣稱保健、代謝或療效。", "把飲品分成日常、共享、送禮與加班四種情境。", "辦公室飲品應以保存方式、糖度與共享便利性決定。"),
    ArticleSpec(2, 1, "高購買意圖導購文", "通勤穿搭與移動包款", "casual-chic", "buying-priority-guide", "會議前後的整理包：髮品、補妝、香氛與小包怎麼放", "meeting-grooming-hair-makeup-scent-small-bag-kit", "會議整理包", s("TP0007070", "TP0005448", "TP0008424"), s("TP0000439", "TP0002031", "TP0009277"), s("meeting-grooming-kit-hair-makeup-scent-small-bag", "home-nail-makeup-tools-beginner-storage"), "段落內小包與整理用品雙 CTA", "不宣稱美妝或髮品效果，成分與使用限制回商品頁。", "整理包的重點是會議前五分鐘能拿到，而不是把浴室搬進包裡。", "會議整理包應控制品項，先補儀容摩擦點，再看香氛與外觀。"),
    ArticleSpec(2, 2, "高購買意圖導購文", "輕戶外與旅行準備", "outdoor-escapes", "comparison-guide", "出國前先整理箱包系統：前開式行李箱、登機箱與收納袋", "travel-luggage-front-open-carry-on-packing-system-2", "行李箱收納", s("TP0002546", "TP0005391", "TP0000074"), s("TP0009277", "TP0005684", "TP0007070"), s("travel-luggage-front-open-carry-on-packing-system", "elder-travel-vision-reading-sunglasses-luggage"), "表格分短途/長途/出差 CTA", "航空尺寸與限制以官方公告為準。", "用旅程天數決定箱體，用拿取頻率決定前開或分層。", "行李箱系統要先看旅程與拿取頻率，再看外型與容量。"),
    ArticleSpec(2, 3, "比較/選購順序文", "居家儀式與收納升級", "lifestyle-culture", "buying-priority-guide", "小宅收納不是買更多盒子：玄關、衣櫃、書桌與清潔工具配置", "small-home-entry-closet-desk-cleaning-storage-order", "小宅收納", s("TP0005953", "TP0000922", "TP0006338"), s("TP0002948", "TP0007021", "TP0004627"), s("small-home-entry-closet-desk-cleaning-storage", "home-organization-cleaning-kitchen-storage-products"), "四區域商品 CTA", "不宣稱承重、防潮或適合所有坪數。", "先替物品安排停靠點，再買盒子；收納不是把東西藏起來。", "小宅收納的核心是動線與使用頻率，不是容器數量。"),
    ArticleSpec(2, 4, "高購買意圖導購文", "低壓恢復與身體支撐", "wellness-movement", "problem-solution-guide", "久坐工作日的腰背與膝蓋支撐：護具、坐墊、鞋包重量怎麼看", "workday-knee-back-support-cushion-bag-weight-guide", "久坐支撐用品", s("TP0003385", "TP0006750", "TP0002618"), s("TP0008160", "TP0009277", "TP0005953"), s("knee-back-support-brace-workday-guide", "chair-cushion-home-office-products"), "風險提醒後放護具 CTA", "不承諾矯正、治療、止痛或醫療效果。", "先看疼痛是否需要專業協助，再看日常支撐物是否只是減少摩擦。", "久坐支撐用品只能協助日常配置，不應取代專業診斷。"),
    ArticleSpec(2, 5, "AEO/GEO 答案型文章", "辦公室補給與質感送禮", "wellness-movement", "faq-hub", "外食日的零食櫃：低醣點心、堅果、素食零嘴與沖泡飲怎麼放", "office-snack-cabinet-low-sugar-nuts-vegetarian-drinks", "低負擔零食櫃", s("TP0006455", "TP0003486", "TP0002822"), s("TP0008420", "TP0000776", "TP0009026"), s("light-snack-cabinet-low-sugar-nuts-vegetarian", "office-home-snack-cabinet-nuts-tea-dessert"), "FAQ 後放零食櫃 CTA", "不得宣稱控糖、減重、代謝或保健效果。", "零食櫃不是自律象徵，而是替下午與加班預留可控選項。", "低負擔零食櫃應看份量、保存與口味疲乏，而不是健康標語。"),
    ArticleSpec(2, 6, "季節/情境文", "通勤穿搭與移動包款", "casual-chic", "seasonal-checklist", "春夏通勤防曬穿搭：防曬外套、抗風傘與輕量包怎麼不狼狽", "spring-summer-commute-sun-umbrella-light-bag-outfit", "春夏通勤防曬", s("TP0000116", "TP0005684", "TP0007070"), s("TP0001609", "TP0005647", "TP0009277"), s("spring-summer-commute-sun-protection-umbrella-light-bag", "weekend-light-outdoor-city-sun-jacket-shorts-small-bag"), "穿搭情境中段放 CTA", "不宣稱防曬效果或 UPF，規格需回商品頁。", "防曬穿搭要能從捷運、機車到會議室銜接。", "春夏通勤防曬要同時處理遮蔽、收納與正式感。"),
    ArticleSpec(2, 7, "高購買意圖導購文", "AI 工作角落與創作者裝備", "ai-innovation", "use-case-guide", "不露臉內容也需要設備順序：支架、燈光、濾鏡與收音怎麼買", "faceless-content-rig-light-filter-audio-buying-order", "內容拍攝設備", s("TP0002918", "TP0009335", "TP0001204"), s("TP0007295", "TP0005820", "TP0009476"), s("faceless-content-phone-rig-filter-light-audio", "mobile-photography-cpl-rig-outdoor-creator-kit"), "設備順序表後放 CTA", "不假裝實測，不承諾畫質或收音改善。", "先把固定、光線與聲音三件事穩住，再談濾鏡和風格。", "內容拍攝設備應先解決穩定度、光線與聲音，再補風格配件。"),
    ArticleSpec(2, 8, "品牌質感型雜誌文", "辦公室補給與質感送禮", "lifestyle-culture", "gift-guide", "質感送禮不必用力：咖啡、茶、按摩設備、雨傘與客製小物", "quality-gifting-coffee-tea-massage-umbrella-custom-goods", "質感送禮", s("TP0005142", "TP0006348", "TP0008485"), s("TP0009388", "TP0005684", "TP0009548"), s("quality-gifting-coffee-tea-massage-umbrella-custom", "cold-brew-tea-gift-box-afternoon-guide"), "文末分對象 CTA", "不承諾收禮反應、按摩或健康效果。", "送禮先看對方生活節奏，不要只看價格或包裝。", "質感送禮的關鍵是使用頻率與對方能否自然收下。"),
    ArticleSpec(2, 9, "比較/選購順序文", "居家儀式與收納升級", "lifestyle-culture", "comparison-guide", "浴室與廚房清潔怎麼分工：水垢、油污、除味與工具收納", "bathroom-kitchen-cleaning-scale-grease-odor-tool-storage", "居家清潔用品", s("TP0003487", "TP0007302", "TP0003749"), s("TP0005724", "TP0000922", "TP0002031"), s("home-cleaning-products-bathroom-kitchen-odor-guide", "sink-cleaning-tool-kitchen-products"), "分區比較表後放 CTA", "不宣稱抗菌、除菌或安全無毒，除非商品頁支持。", "先分污垢來源，再分清潔工具；香味不是清潔完成的證明。", "清潔用品要按髒污來源分工，不能用一瓶解決全屋。"),
    ArticleSpec(2, 10, "AEO/GEO 答案型文章", "輕戶外與旅行準備", "outdoor-escapes", "faq-hub", "新手登山先買什麼：排汗衣、雨衣褲、護膝與輕量收納順序", "beginner-hiking-shirt-rainwear-knee-support-storage-order", "登山新手裝備", s("TP0007424", "TP0003385", "TP0006750"), s("TP0000976", "TP0009177", "TP0000034"), s("beginner-hiking-gear-order-light-trail", "taiwan-hiking-routes-and-style"), "FAQ 後放裝備 CTA", "不宣稱安全保證或醫療防護。", "先買能應對氣候與路線風險的東西，再買風格小物。", "新手登山裝備要先處理天氣、支撐與收納，再談品牌完整度。"),
]


BASE_SPECS = list(SPECS)


MORE_TITLES: list[tuple[str, str, str, str, str, tuple[str, ...], tuple[str, ...]]] = [
    ("居家餐桌先買鍋還是杯盤：鍋具、餐具與收納工具的順序", "home-cooking-pan-tableware-storage-order", "辦公室補給與質感送禮", "lifestyle-culture", "comparison-guide", s("TP0001754", "TP0000363", "TP0005971"), s("TP0008921", "TP0003333", "TP0005142")),
    ("租屋小家電不要一次買滿：廚房、桌面、清潔與季節電器", "rental-small-appliance-kitchen-desk-cleaning-seasonal", "居家儀式與收納升級", "lifestyle-culture", "buying-priority-guide", s("TP0005764", "TP0006567", "TP0005935"), s("TP0007295", "TP0007694", "TP0000922")),
    ("旅行鞋包配置：好走鞋、輕量包、貼身小包與雨天備案", "travel-shoes-light-bag-crossbody-rain-backup-system", "通勤穿搭與移動包款", "casual-chic", "buying-priority-guide", s("TP0009277", "TP0007070", "TP0003634"), s("TP0005684", "TP0004592", "TP0003240")),
    ("客廳與工作角落照明：吸頂燈、桌燈、香氛與收納怎麼搭", "living-room-work-corner-lighting-scent-storage-system", "居家儀式與收納升級", "lifestyle-culture", "use-case-guide", s("TP0007295", "TP0004627", "TP0007694"), s("TP0004799", "TP0009429", "TP0005953")),
    ("AI 工作流需要什麼筆電周邊：螢幕、線材、保護貼與備份", "ai-workflow-laptop-monitor-cable-protection-backup", "AI 工作角落與創作者裝備", "ai-innovation", "comparison-guide", s("TP0002753", "TP0005967", "TP0006238"), s("TP0007010", "TP0000858", "TP0009476")),
    ("給家人的居家舒壓設備：按摩椅、按摩槍、護具與照護用品", "home-comfort-massage-device-brace-care-supplies-order", "低壓恢復與身體支撐", "wellness-movement", "buying-priority-guide", s("TP0008485", "TP0005698", "TP0009161"), s("TP0003385", "TP0006750", "TP0003894")),
    ("冷凍庫備餐清單：舒肥雞胸、地瓜、冷凍蔬菜與料理包", "freezer-meal-prep-chicken-sweet-potato-vegetables-pack", "辦公室補給與質感送禮", "wellness-movement", "seasonal-checklist", s("TP0005993", "TP0002665", "TP0001851"), s("TP0001794", "TP0000776", "TP0002736")),
    ("寵物友善居家清潔：除味、地板、洗衣與收納用品怎麼看", "pet-friendly-home-cleaning-floor-laundry-storage-order", "居家儀式與收納升級", "lifestyle-culture", "problem-solution-guide", s("TP0008976", "TP0009640", "TP0005724"), s("TP0003749", "TP0007478", "TP0000922")),
    ("日系露營風格入門：桌椅、爐具、杯具與收納小物順序", "japanese-camping-style-table-stove-cup-storage-order", "輕戶外與旅行準備", "outdoor-escapes", "buy-better-longer-guide", s("TP0007737", "TP0006752", "TP0003074"), s("TP0009177", "TP0009528", "TP0007424")),
    ("日常保養別堆太多：精華、面膜、身體保養與防曬怎麼排", "daily-skincare-essence-mask-body-sunscreen-order-2", "通勤穿搭與移動包款", "lifestyle-culture", "buying-priority-guide", s("TP0008453", "TP0001343", "TP0002583"), s("TP0008148", "TP0002458", "TP0005312")),
    ("頭皮與髮品整理：洗髮、染護、造型與按摩梳的選擇", "scalp-haircare-shampoo-color-styling-brush-choice", "通勤穿搭與移動包款", "lifestyle-culture", "comparison-guide", s("TP0005448", "TP0008576", "TP0004518"), s("TP0004416", "TP0005820", "TP0008424")),
    ("居家伸展角落：瑜珈墊、輔具、燈光與香氛的低壓配置", "home-stretch-yoga-mat-props-light-scent-corner", "低壓恢復與身體支撐", "wellness-movement", "use-case-guide", s("TP0009115", "TP0007295", "TP0002458"), s("TP0005953", "TP0004627", "TP0009429")),
    ("週末輕戶外穿搭：城市感、防曬外套、短褲與小包怎麼搭", "weekend-city-outdoor-sun-jacket-shorts-small-bag", "通勤穿搭與移動包款", "casual-chic", "seasonal-checklist", s("TP0007424", "TP0000116", "TP0009277"), s("TP0002198", "TP0003240", "TP0003634")),
    ("貓咪生活採買順序：貓砂、玩具、食品與清潔用品", "cat-living-litter-toys-food-cleaning-order", "居家儀式與收納升級", "lifestyle-culture", "buying-priority-guide", s("TP0000547", "TP0000351", "TP0008435"), s("TP0003220", "TP0007761", "TP0005724")),
    ("親子外出小物：餐具、口腔清潔、孕產穿搭與外出包", "parent-child-outing-tableware-oral-care-maternity-bag-kit", "輕戶外與旅行準備", "lifestyle-culture", "use-case-guide", s("TP0002712", "TP0002971", "TP0006972"), s("TP0000587", "TP0000319", "TP0007070")),
    ("辦公室飲品櫃：植物奶、茶包、咖啡與氣泡飲怎麼搭", "office-drink-cabinet-plant-milk-tea-coffee-sparkling", "辦公室補給與質感送禮", "lifestyle-culture", "comparison-guide", s("TP0000776", "TP0005142", "TP0006151"), s("TP0009026", "TP0001663", "TP0008341")),
    ("自駕與機車移動備案：行車紀錄、反光配件、雨具與充電", "road-scooter-dashcam-reflective-rain-charging-kit", "輕戶外與旅行準備", "outdoor-escapes", "seasonal-checklist", s("TP0001272", "TP0000034", "TP0001609"), s("TP0005110", "TP0009476", "TP0005684")),
    ("家庭禮物與益智玩具：積木、桌遊、拼圖與書店選物", "family-gift-blocks-board-games-puzzles-books", "辦公室補給與質感送禮", "lifestyle-culture", "gift-guide", s("TP0002179", "TP0002275", "TP0003052"), s("TP0002688", "TP0000319", "TP0002948")),
    ("防曬與雨具收納：玄關、通勤包與車廂裡各放什麼", "sun-rain-gear-entryway-commute-bag-scooter-storage", "通勤穿搭與移動包款", "casual-chic", "faq-hub", s("TP0000116", "TP0005684", "TP0001609"), s("TP0005647", "TP0005110", "TP0009277")),
    ("冷泡茶與茶禮盒：日常飲用、送禮與下午茶的不同判斷", "cold-brew-tea-gift-box-afternoon-decision", "辦公室補給與質感送禮", "lifestyle-culture", "gift-guide", s("TP0005142", "TP0007428", "TP0008786"), s("TP0003333", "TP0001441", "TP0006348")),
    ("遠距工作包清單：充電、耳機、簡報線材與移動收納", "remote-work-bag-charging-audio-presentation-storage", "AI 工作角落與創作者裝備", "ai-innovation", "use-case-guide", s("TP0009476", "TP0001204", "TP0005967"), s("TP0006348", "TP0002753", "TP0009277")),
    ("桌面線材怎麼整理：充電器、螢幕線、保護貼與備份小物", "desk-cable-charger-monitor-protection-backup-organizer", "AI 工作角落與創作者裝備", "ai-innovation", "buying-priority-guide", s("TP0009476", "TP0005967", "TP0006238"), s("TP0000669", "TP0007239", "TP0007010")),
    ("夏季低負擔日常：防曬、降噪睡眠、飲品與輕食補給", "summer-low-pressure-sun-sleep-drink-light-food", "低壓恢復與身體支撐", "wellness-movement", "seasonal-checklist", s("TP0000116", "TP0003593", "TP0009026"), s("TP0000776", "TP0002736", "TP0008341")),
    ("居家照護動線：沐浴、移位、收納與安全提醒怎麼看", "home-care-bathing-transfer-storage-safety-flow", "低壓恢復與身體支撐", "wellness-movement", "problem-solution-guide", s("TP0008844", "TP0005698", "TP0004949"), s("TP0009161", "TP0003894", "TP0005953")),
    ("香氛與身體保養送禮：精油、蠟燭、毛巾與生活小物", "scent-bodycare-gift-essential-oil-towel-goods", "居家儀式與收納升級", "lifestyle-culture", "gift-guide", s("TP0002458", "TP0009429", "TP0002031"), s("TP0009548", "TP0005162", "TP0007021")),
    ("居家美甲與彩妝工具：新手材料、刷具與收納怎麼買", "home-nail-makeup-tools-brush-storage-beginner", "通勤穿搭與移動包款", "casual-chic", "buying-priority-guide", s("TP0005240", "TP0008424", "TP0000439"), s("TP0000144", "TP0007932", "TP0003337")),
    ("飾品與皮件送禮：銀飾、戒指、皮夾與日常小包", "jewelry-leather-gift-ring-wallet-small-bag", "通勤穿搭與移動包款", "casual-chic", "gift-guide", s("TP0000144", "TP0007932", "TP0003337"), s("TP0007070", "TP0003240", "TP0006348")),
    ("男士通勤衣櫥：襯衫、長褲、外套與鞋包怎麼排", "mens-commute-shirt-trousers-jacket-shoes-wardrobe", "通勤穿搭與移動包款", "casual-chic", "buying-priority-guide", s("TP0003817", "TP0003665", "TP0003634"), s("TP0003240", "TP0009277", "TP0005684")),
    ("大尺碼工作與旅行穿搭：比例、舒適度、外套與包款", "plus-size-work-travel-outfit-jacket-bag-order", "通勤穿搭與移動包款", "casual-chic", "comparison-guide", s("TP0000405", "TP0000116", "TP0008908"), s("TP0002198", "TP0007070", "TP0009277")),
    ("露營咖啡與戶外餐食：手沖、濾掛、鍋具與冷凍食材", "camping-coffee-outdoor-meal-prep-cookware-food", "輕戶外與旅行準備", "outdoor-escapes", "buying-priority-guide", s("TP0009303", "TP0006151", "TP0005993"), s("TP0009388", "TP0006698", "TP0001794")),
    ("夜間移動安全感：反光配件、行車紀錄、雨具與降噪睡眠", "night-mobility-reflective-dashcam-rain-earplug-kit", "輕戶外與旅行準備", "outdoor-escapes", "seasonal-checklist", s("TP0000034", "TP0001272", "TP0003593"), s("TP0001609", "TP0003385", "TP0009476")),
    ("親子週末出門清單：防曬、餐具、玩具、雨具與收納袋", "family-weekend-outing-sun-tableware-toys-rain-storage", "輕戶外與旅行準備", "outdoor-escapes", "seasonal-checklist", s("TP0000116", "TP0002712", "TP0002179"), s("TP0005684", "TP0007070", "TP0002948")),
    ("第一次養寵物的購物順序：食品、玩具、清潔與外出用品", "first-pet-shopping-food-toy-cleaning-outing-order-2", "居家儀式與收納升級", "lifestyle-culture", "buying-priority-guide", s("TP0009203", "TP0002193", "TP0007478"), s("TP0005844", "TP0008435", "TP0005724")),
    ("水族與小寵補貨清單：飼料、清潔、棲地與收納", "aquarium-reptile-small-pet-food-cleaning-habitat-storage", "居家儀式與收納升級", "lifestyle-culture", "buying-priority-guide", s("TP0009226", "TP0007478", "TP0008435"), s("TP0005724", "TP0003749", "TP0000922")),
    ("寵物生日禮物：蛋糕、零食、玩具與清潔備案", "pet-birthday-gift-cake-snack-toy-cleaning", "辦公室補給與質感送禮", "lifestyle-culture", "gift-guide", s("TP0001817", "TP0002193", "TP0007478"), s("TP0009203", "TP0008435", "TP0005724")),
    ("辦公室點心櫃：堅果、甜點、茶飲與咖啡怎麼分層", "office-snack-cabinet-nuts-dessert-tea-coffee-layers", "辦公室補給與質感送禮", "lifestyle-culture", "buying-priority-guide", s("TP0003486", "TP0003278", "TP0005142"), s("TP0006151", "TP0009388", "TP0000776")),
    ("家庭餐桌週末補貨：冷凍食品、鍋具、餐具與茶點", "family-weekend-table-frozen-food-cookware-tableware-tea", "辦公室補給與質感送禮", "lifestyle-culture", "seasonal-checklist", s("TP0005993", "TP0001754", "TP0005971"), s("TP0003333", "TP0005142", "TP0000363")),
    ("早餐與冷凍麵食補貨：饅頭、地瓜、雞胸與沖泡飲", "breakfast-freezer-buns-sweet-potato-chicken-drinks", "辦公室補給與質感送禮", "wellness-movement", "buying-priority-guide", s("TP0004495", "TP0005993", "TP0002822"), s("TP0000776", "TP0002736", "TP0006455")),
    ("一人生活的餐具清單：杯盤、鍋具、咖啡茶與清潔收納", "solo-living-tableware-cookware-coffee-tea-cleaning-storage", "居家儀式與收納升級", "lifestyle-culture", "buying-priority-guide", s("TP0005971", "TP0001754", "TP0005142"), s("TP0000922", "TP0007302", "TP0009388")),
    ("玄關不是倉庫：鞋櫃、傘架、外出包與清潔工具怎麼分工", "entryway-shoe-cabinet-umbrella-bag-cleaning-tools", "居家儀式與收納升級", "lifestyle-culture", "comparison-guide", s("TP0005953", "TP0000922", "TP0006481"), s("TP0007407", "TP0005684", "TP0007070")),
    ("衣櫃與洗衣區整理：衣架、收納箱、毛巾與床寢備品", "closet-laundry-hanger-storage-towel-bedding-supplies", "居家儀式與收納升級", "lifestyle-culture", "buying-priority-guide", s("TP0005953", "TP0002031", "TP0002413"), s("TP0001106", "TP0007471", "TP0000922")),
    ("床邊櫃與睡前小物：耳塞、閱讀燈、香氛與床寢怎麼放", "nightstand-bedtime-earplug-reading-light-scent-bedding", "低壓恢復與身體支撐", "wellness-movement", "use-case-guide", s("TP0003593", "TP0007295", "TP0001941"), s("TP0002458", "TP0002413", "TP0001001")),
    ("夏季床寢怎麼換：天絲、棉被、保潔墊與涼被的順序", "summer-bedding-tencel-quilt-protector-cool-blanket-order", "低壓恢復與身體支撐", "wellness-movement", "seasonal-checklist", s("TP0002413", "TP0001106", "TP0007471"), s("TP0002795", "TP0003841", "TP0001941")),
    ("居家清潔工具牆：平板拖把、掃把、水槽清潔與垃圾桶", "home-cleaning-tool-wall-mop-broom-sink-trash-bin", "居家儀式與收納升級", "lifestyle-culture", "comparison-guide", s("TP0000922", "TP0003487", "TP0005724"), s("TP0005953", "TP0005709", "TP0007407")),
    ("租屋改造不動工：貼皮、燈光、收納與可移動家具", "rental-refresh-sticker-light-storage-movable-furniture", "居家儀式與收納升級", "lifestyle-culture", "buy-better-longer-guide", s("TP0009317", "TP0007295", "TP0005953"), s("TP0006338", "TP0007407", "TP0004627")),
    ("小陽台與庭院用品：遮陽、戶外椅、收納與植物照顧", "patio-balcony-shade-outdoor-chair-storage-plant-care", "輕戶外與旅行準備", "outdoor-escapes", "seasonal-checklist", s("TP0006752", "TP0003074", "TP0003894"), s("TP0005684", "TP0009177", "TP0005953")),
    ("游泳與戶外課前準備：泳鏡、防曬、毛巾與收納袋", "swimming-outdoor-class-goggles-sun-towel-storage-bag", "輕戶外與旅行準備", "outdoor-escapes", "faq-hub", s("TP0003976", "TP0000116", "TP0002031"), s("TP0007070", "TP0005684", "TP0002712")),
    ("城市週末拍攝包：手機支架、CPL、黑柔濾鏡與防曬外套", "city-weekend-photo-kit-phone-rig-cpl-filter-sun-jacket", "AI 工作角落與創作者裝備", "ai-innovation", "use-case-guide", s("TP0002918", "TP0009335", "TP0000116"), s("TP0009476", "TP0007424", "TP0005684")),
    ("手機車用配置：手機架、車充、線材、行車紀錄與雨天備案", "car-phone-setup-mount-charger-cable-dashcam-rain", "AI 工作角落與創作者裝備", "ai-innovation", "buying-priority-guide", s("TP0000092", "TP0009476", "TP0001272"), s("TP0000669", "TP0001609", "TP0005684")),
    ("簡報日的遠距設備：耳機、麥克風、螢幕與桌面光線", "presentation-day-remote-gear-headset-mic-monitor-light", "AI 工作角落與創作者裝備", "ai-innovation", "comparison-guide", s("TP0001204", "TP0007934", "TP0005967"), s("TP0007295", "TP0006348", "TP0009476")),
    ("高效率桌面別只買大桌：椅墊、靠枕、螢幕與收納順序", "efficient-desk-cushion-backrest-monitor-storage-order", "AI 工作角落與創作者裝備", "ai-innovation", "buying-priority-guide", s("TP0007407", "TP0006481", "TP0005967"), s("TP0006348", "TP0005953", "TP0007295")),
    ("工作角落的聲音整理：耳機、喇叭、降噪與會議收音", "work-corner-sound-headphones-speaker-noise-meeting-audio", "AI 工作角落與創作者裝備", "ai-innovation", "faq-hub", s("TP0001204", "TP0007934", "TP0006348"), s("TP0003593", "TP0005967", "TP0009476")),
    ("夏季辦公室冷氣備案：薄外套、熱飲、耳塞與桌面燈", "summer-office-ac-backup-light-jacket-hot-drink-earplug-lamp", "低壓恢復與身體支撐", "wellness-movement", "seasonal-checklist", s("TP0007424", "TP0005142", "TP0003593"), s("TP0007295", "TP0000116", "TP0002458")),
    ("長途移動恢復包：耳塞、護具、行李箱、茶包與防曬", "long-trip-recovery-kit-earplug-brace-luggage-tea-sun", "低壓恢復與身體支撐", "wellness-movement", "use-case-guide", s("TP0003593", "TP0003385", "TP0002546"), s("TP0005142", "TP0000116", "TP0005684")),
    ("長輩閱讀與照護角落：檯燈、眼鏡、收納與照護用品", "elder-reading-care-corner-lamp-glasses-storage-care-supplies", "低壓恢復與身體支撐", "wellness-movement", "problem-solution-guide", s("TP0007295", "TP0009515", "TP0005698"), s("TP0008844", "TP0005953", "TP0004949")),
    ("家庭浴室補貨：毛巾、清潔、口腔用品與收納動線", "family-bathroom-restock-towel-cleaning-oral-care-storage", "居家儀式與收納升級", "lifestyle-culture", "buying-priority-guide", s("TP0002031", "TP0005724", "TP0002971"), s("TP0000922", "TP0003487", "TP0007302")),
    ("咖啡茶與伴手禮桌：杯盤、茶點、香氛與客製小物", "coffee-tea-gift-table-tableware-snack-scent-custom", "辦公室補給與質感送禮", "lifestyle-culture", "gift-guide", s("TP0005971", "TP0003333", "TP0002458"), s("TP0006348", "TP0005142", "TP0009388")),
    ("週末家務重整：清潔、洗衣、床寢、補貨與出門包", "weekend-home-reset-cleaning-laundry-bedding-restock-bag", "居家儀式與收納升級", "lifestyle-culture", "seasonal-checklist", s("TP0000922", "TP0002031", "TP0002413"), s("TP0007070", "TP0005953", "TP0005724")),
    ("桌面下午茶儀式：咖啡杯、茶包、點心、香氛與閱讀燈", "desk-afternoon-ritual-coffee-cup-tea-snack-scent-lamp", "辦公室補給與質感送禮", "lifestyle-culture", "brand-editorial", s("TP0005971", "TP0005142", "TP0003278"), s("TP0009429", "TP0007295", "TP0006151")),
    ("旅行前一晚的採買檢查：行李箱、雨具、充電、睡眠與護具", "night-before-travel-luggage-rain-charging-sleep-brace-check", "輕戶外與旅行準備", "outdoor-escapes", "faq-hub", s("TP0002546", "TP0005684", "TP0009476"), s("TP0003593", "TP0003385", "TP0007070")),
]


def build_more_specs() -> list[ArticleSpec]:
    specs: list[ArticleSpec] = []
    for index, row in enumerate(MORE_TITLES, start=21):
        title, slug, cluster, category, form, primary, supporting = row
        week = ((index - 1) // 10) + 1
        slot = ((index - 1) % 10) + 1
        cadence = {
            1: "高購買意圖導購文",
            2: "比較/選購順序文",
            3: "AEO/GEO 答案型文章",
            4: "季節/情境文",
            5: "品牌質感型雜誌文",
        }[((slot - 1) % 5) + 1]
        intent = title.split("：", 1)[0]
        specs.append(
            ArticleSpec(
                week,
                slot,
                cadence,
                cluster,
                category,
                form,
                title,
                slug,
                intent,
                primary,
                supporting,
                s(slug.rsplit("-", 1)[0]),
                "依文章情境配置 2-3 組 CTA",
                "商品價格、規格、活動、庫存與限制均以商品頁公告為準；健康、寵物、照護、食品題不得承諾效果。",
                "先建立使用順序與常見錯誤，再讓商品成為讀者下一步的工具。",
                f"{intent}應先回到使用情境、頻率與限制，再比較品牌與商品。",
            )
        )
    return specs


def expand_to_80() -> list[ArticleSpec]:
    specs = BASE_SPECS + build_more_specs()
    if len(specs) != 80:
        raise SystemExit(f"Expected exactly 80 article specs, got {len(specs)}")
    return specs


def load_tracker() -> dict[str, dict[str, str]]:
    with TRACKER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["merchant_id"]: row for row in csv.DictReader(handle)}


def is_usable(row: dict[str, str]) -> bool:
    if row["coverage_status"] != "live":
        return False
    if row["recommendation_grade"] == "D":
        return False
    if "暫緩" in row["brand_role"] or "排除" in row["brand_role"]:
        return False
    if not row.get("promo_link", "").strip():
        return False
    return True


def row_for_csv(spec: ArticleSpec, tracker: dict[str, dict[str, str]]) -> dict[str, str]:
    brand_ids = list(spec.primary + spec.supporting)
    brands = [tracker[mid]["brand"] for mid in brand_ids]
    primary_brands = [tracker[mid]["brand"] for mid in spec.primary]
    support_brands = [tracker[mid]["brand"] for mid in spec.supporting]
    return {
        "week": str(spec.week),
        "weekly_slot": str(spec.slot),
        "cadence_type": spec.cadence_type,
        "cluster": spec.cluster,
        "category": spec.category,
        "article_form": spec.form,
        "title": spec.title,
        "slug": spec.slug,
        "search_intent": spec.intent,
        "primary_merchant_ids": ";".join(spec.primary),
        "primary_brands": ";".join(primary_brands),
        "supporting_merchant_ids": ";".join(spec.supporting),
        "supporting_brands": ";".join(support_brands),
        "all_brands": ";".join(brands),
        "internal_link_targets": ";".join(spec.internal_links),
        "cta_style": spec.cta_style,
        "risk_guardrail": spec.risk_guardrail,
        "elite_judgment": spec.elite_judgment,
        "answer_summary": spec.answer_summary,
        "status": "ready-to-brief",
    }


def validate(specs: list[ArticleSpec], tracker: dict[str, dict[str, str]]) -> None:
    errors: list[str] = []
    slugs = [spec.slug for spec in specs]
    for slug, count in Counter(slugs).items():
        if count > 1:
            errors.append(f"duplicate slug: {slug}")
    for spec in specs:
        if spec.category not in VALID_CATEGORIES:
            errors.append(f"{spec.slug}: invalid category {spec.category}")
        for term in BLOCKED_TITLE_TERMS:
            if term in spec.title:
                errors.append(f"{spec.slug}: blocked title term {term}")
        if not 3 <= len(spec.primary + spec.supporting) <= 7:
            errors.append(f"{spec.slug}: expected 3-7 brands")
        for merchant_id in spec.primary + spec.supporting:
            row = tracker.get(merchant_id)
            if not row:
                errors.append(f"{spec.slug}: missing merchant {merchant_id}")
            elif not is_usable(row):
                errors.append(
                    f"{spec.slug}: unusable merchant {merchant_id} "
                    f"({row['coverage_status']}/{row['recommendation_grade']}/{row['brand_role']})"
                )
    if errors:
        raise SystemExit("Matrix validation failed:\n" + "\n".join(errors))


def write_outputs(specs: list[ArticleSpec], tracker: dict[str, dict[str, str]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [row_for_csv(spec, tracker) for spec in specs]
    fieldnames = list(rows[0].keys())
    with CSV_OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    payload: dict[str, Any] = {
        "updatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "strategy": {
            "primaryGoal": "收益優先",
            "cadence": "每週 10 篇",
            "inventoryScope": "momo 為主",
            "oldContentScope": "輕量內鏈與 CTA 升級",
        },
        "pillars": PILLARS,
        "articles": rows,
    }
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    by_week: dict[int, list[dict[str, str]]] = defaultdict(list)
    by_cluster = Counter(row["cluster"] for row in rows)
    by_category = Counter(row["category"] for row in rows)
    brand_mentions = Counter()
    for spec in specs:
        for merchant_id in spec.primary + spec.supporting:
            brand_mentions[tracker[merchant_id]["brand"]] += 1
        by_week[spec.week].append(row_for_csv(spec, tracker))

    md: list[str] = [
        f"# momo 聯盟收益型內容矩陣（{DATE_STAMP}）",
        "",
        "## 執行口徑",
        "",
        "- 主目標：收益優先，但維持 Elite Fashion 編輯語氣與商品查證邊界。",
        "- 發文節奏：每週 10 篇，先規劃 8 週共 80 篇。",
        "- 商品來源：momo tracker 中 `coverage_status=live` 且有可用推廣連結的店家。",
        "- 舊文處理：每篇新文同步補 2 到 4 個舊文內鏈或相關閱讀，不大改舊文主體。",
        "- 前台限制：不得出現內部策略字眼；健康、照護、寵物、食品與美妝題不得承諾效果。",
        "",
        "## 旗艦頁規劃",
        "",
    ]
    for pillar in PILLARS:
        md.append(f"- `{pillar['slug']}`｜{pillar['title']}｜{pillar['category']}｜{pillar['purpose']}")
    md.extend(
        [
            "",
            "## 矩陣總覽",
            "",
            f"- 文章數：{len(rows)}",
            "- 分類分布：" + "、".join(f"{k} {v}" for k, v in sorted(by_category.items())),
            "- 主題分布：" + "、".join(f"{k} {v}" for k, v in sorted(by_cluster.items())),
            "- 最高品牌提及：" + "、".join(f"{brand} {count}" for brand, count in brand_mentions.most_common(12)),
            "",
            "## 週次清單",
            "",
        ]
    )
    for week in sorted(by_week):
        md.append(f"### Week {week}")
        md.append("")
        for row in by_week[week]:
            md.append(
                f"{row['weekly_slot']}. {row['title']}｜`{row['category']}`｜"
                f"{row['cadence_type']}｜主品牌：{row['primary_brands']}"
            )
        md.append("")
    md.extend(
        [
            "## 發布檢查",
            "",
            "- 每篇至少 2,200 個中文內容字元，含雜誌式導言、選購順序、比較表、FAQ、CTA 與導購揭露。",
            "- 所有導購連結需 `rel=\"sponsored nofollow\"`，且商品資訊存在於初始 HTML 可見內容。",
            "- 文章封面與 OG/Twitter 圖同一張 1200 x 630，alt 描述具體畫面。",
            "- 每週收尾更新 tracker 的 article_slug、live_url、mention_count、last_mentioned_at 與 notes。",
            "",
        ]
    )
    MD_OUT.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    tracker = load_tracker()
    specs = expand_to_80()
    validate(specs, tracker)
    write_outputs(specs, tracker)
    print(f"Wrote {CSV_OUT.relative_to(ROOT)}")
    print(f"Wrote {JSON_OUT.relative_to(ROOT)}")
    print(f"Wrote {MD_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
