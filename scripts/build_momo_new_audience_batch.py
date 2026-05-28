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
QUEUE_ID = "Q-0013"
GENERATED_IMAGE_DIR = Path("/Users/mkhsu/.codex/generated_images/019e6f48-25a3-70e3-af05-01a11108fe4d")


ARTICLES: list[dict[str, Any]] = [
    {
        "slug": "summer-airflow-fan-small-appliance-lighting",
        "title": "夏天前先整理家的空氣路線：循環扇、小家電與照明的舒適配置",
        "category": "lifestyle-culture",
        "audience": "家庭、小資租屋族、辦公室與季節家電需求者",
        "scene": "夏天真正難整理的不是只買一台電器，而是風從哪裡進、熱停在哪裡、燈光與桌面小家電會不會讓空間更擁擠。",
        "decision": "先看空氣動線，再看使用位置，最後才挑外型與品牌。循環扇、小家電與照明如果沒有一起想，很容易買到單品很漂亮、日常卻不好收的組合。",
        "items": ["循環扇", "小家電", "桌面電器", "照明"],
        "brands": ["TP0005764", "TP0006567", "TP0005409", "TP0005935"],
        "risk": "本文不承諾降溫、節電或健康效果；商品規格、活動、價格與庫存請以商品頁公告為準。",
        "cover": "ig_07378535d8e99728016a188471473c819b9750298790e603ad.png",
        "heroAlt": "明亮客廳裡的循環扇、小家電、桌燈與開窗採光配置",
    },
    {
        "slug": "rental-small-appliance-kitchen-desk-cleaning",
        "title": "租屋族小家電清單：廚房、桌面、清潔與季節電器先買哪些",
        "category": "lifestyle-culture",
        "audience": "家庭、小資租屋族、辦公室與季節家電需求者",
        "scene": "租屋生活最怕東西越買越多，插座不夠、收納不夠，最後每一台小家電都變成桌面壓力。",
        "decision": "先分出每天會用、每週會用、只在季節轉換時會用的物件，再決定廚房、桌面與清潔電器的優先順序。",
        "items": ["廚房小家電", "桌面電器", "清潔工具", "季節電器"],
        "brands": ["TP0005764", "TP0005409", "TP0006567", "TP0007559"],
        "risk": "本文為一般租屋採買情境整理，不宣稱商品耐用年限或個別空間必然適用。",
        "cover": "ig_07378535d8e99728016a1884b60c60819bbe65c0c8a8e6a6b9.png",
        "heroAlt": "租屋廚房與工作桌旁整理好的小家電、層架與清潔用品",
    },
    {
        "slug": "home-cooking-pan-tableware-tool-buying-order",
        "title": "自煮生活先買鍋還是餐具：日本鍋具、鐵鍋與餐桌工具的選購順序",
        "category": "lifestyle-culture",
        "audience": "自煮族、家庭料理、送禮與餐桌美學讀者",
        "scene": "自煮生活不一定要從一整套廚房開始。多數人更需要先判斷自己常煮什麼、幾個人吃、洗碗與收納能不能承受。",
        "decision": "鍋具先滿足烹調方式，餐具再回到上桌頻率；如果順序反過來，很容易擁有漂亮盤子，卻缺少真正好用的料理工具。",
        "items": ["日本鍋具", "台灣鐵鍋", "餐具", "杯壺與工具"],
        "brands": ["TP0001754", "TP0008921", "TP0000363", "TP0005971"],
        "risk": "商品材質、適用爐具、保養方式與庫存請以商品頁公告為準。",
        "cover": "ig_07378535d8e99728016a1884f1345c819b8b1393f7951d55a8.png",
        "heroAlt": "餐桌上的鍋具、鐵鍋、陶瓷餐具、木製餐具與新鮮食材",
    },
    {
        "slug": "office-afternoon-tea-drink-pantry-guide",
        "title": "下午三點不要只喝手搖：無糖茶、花草茶與辦公室飲品清單",
        "category": "lifestyle-culture",
        "audience": "辦公室、下午茶、家庭補貨與低負擔飲品讀者",
        "scene": "下午三點的飲品通常不是為了解渴而已，而是在會議與下一段工作之間，幫自己建立一個可以停十秒的節點。",
        "decision": "辦公室飲品可以先從無糖、好保存、不佔冰箱空間開始挑，再依口味、沖泡方式與共用情境慢慢補齊。",
        "items": ["無糖茶", "花草茶", "氣泡飲", "沖泡飲"],
        "brands": ["TP0008451", "TP0002361", "TP0000525", "TP0004250", "TP0004512"],
        "risk": "草本、酵素與機能飲品只作一般飲用情境整理，不宣稱保健、代謝或療效。",
        "cover": "ig_07378535d8e99728016a1885271238819b853cf69768aaace0.png",
        "heroAlt": "辦公室茶水角落裡的茶包、玻璃水壺、杯具、筆記本與城市窗景",
    },
    {
        "slug": "light-snack-cabinet-low-sugar-nuts-vegetarian",
        "title": "外食族的低負擔零食櫃：低醣點心、堅果、素食零嘴與沖泡飲",
        "category": "wellness-movement",
        "audience": "外食族、素食者、健身飲食、控糖或低醣關注者",
        "scene": "外食日很多的時候，最容易失控的不是正餐，而是下午、加班與回家前那段沒有準備的空白。",
        "decision": "零食櫃的重點不是把自己管得很嚴，而是先放入份量容易控制、保存穩定、口味不容易膩的選項。",
        "items": ["低醣點心", "堅果", "素食零嘴", "沖泡補給"],
        "brands": ["TP0006455", "TP0003486", "TP0002822", "TP0008420"],
        "risk": "本文不構成營養、醫療或個人化飲食建議；不得承諾控糖、減重、代謝或健康效果。",
        "cover": "ig_07378535d8e99728016a18855b6ee8819baa641451b03bd36e.png",
        "heroAlt": "辦公桌旁整理好的低負擔點心櫃、堅果、小點心、茶包與午餐袋",
    },
    {
        "slug": "home-scent-incense-cleaning-odor-zones",
        "title": "家裡的味道也需要整理：香氛、香品、清潔與除味用品怎麼分工",
        "category": "lifestyle-culture",
        "audience": "居家儀式、空間氣味、送禮、清潔除味讀者",
        "scene": "家裡的味道不該只靠一瓶香氛蓋過去。玄關、客廳、浴室與收納櫃的問題不同，需要先分辨來源。",
        "decision": "先清潔，再通風，最後才是香氛與香品。這個順序會讓空間更乾淨，也讓味道不必被堆得太重。",
        "items": ["香氛", "香品", "除味用品", "清潔小物"],
        "brands": ["TP0009664", "TP0002941", "TP0002661", "TP0004752", "TP0005358"],
        "risk": "本文不宣稱淨化、療癒、除菌或健康效果；香品使用需依空間通風與商品說明判斷。",
        "cover": "ig_07378535d8e99728016a188597c174819ba78c1babff19d36d.png",
        "heroAlt": "玄關與浴室旁的香氛、香品、毛巾、清潔用品與自然採光",
    },
    {
        "slug": "travel-luggage-front-open-carry-on-packing-system",
        "title": "出國前先整理箱包系統：前開式行李箱、登機箱與旅行收納",
        "category": "outdoor-escapes",
        "audience": "出差族、家庭旅行、自駕與戶外移動讀者",
        "scene": "行李箱不是越大越安心。真正讓出國前一晚變輕鬆的，是知道哪些東西要放外層、哪些東西不能臨時亂塞。",
        "decision": "先用旅程長度決定箱體，再用拿取頻率決定分層；前開、登機、收納袋與備用包各自負責不同任務。",
        "items": ["前開式行李箱", "登機箱", "旅行收納", "戶外小物"],
        "brands": ["TP0002546", "TP0005391", "TP0000151", "TP0000074"],
        "risk": "航空尺寸、重量與攜帶限制可能變動，實際出行前請以航空公司與官方公告為準。",
        "cover": "ig_07378535d8e99728016a1885c2f198819b98f3f960dde38587.png",
        "heroAlt": "陽光公寓地板上打開的行李箱、收納袋、旅行外套與小物",
    },
    {
        "slug": "first-pet-shopping-food-toy-cleaning-outing-order",
        "title": "第一次養寵物不要一次買太多：食品、玩具、清潔與外出用品順序",
        "category": "lifestyle-culture",
        "audience": "新手毛孩家庭、貓奴、爬蟲/水族、小寵主人",
        "scene": "第一次迎接寵物回家，很容易被可愛小物推著走，但真正重要的是先把吃、睡、清潔與外出這四件事安定下來。",
        "decision": "新手採買應該先少量、可替換、好清潔，再慢慢觀察寵物習慣。一次買滿通常不如保留調整空間。",
        "items": ["食品", "玩具", "清潔用品", "外出用品"],
        "brands": ["TP0008082", "TP0007661", "TP0000551", "TP0000823", "TP0000651", "TP0004035"],
        "risk": "本文為一般寵物用品採買情境整理，不構成獸醫、營養或健康建議；飲食與健康狀況請諮詢獸醫。",
        "cover": "ig_07378535d8e99728016a18863c0aa0819b96974fc1e832be06.png",
        "heroAlt": "乾淨居家角落中的寵物碗、玩具、牽繩、清潔用品、收納籃與小床",
    },
]


def load_tracker() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], list[str]]:
    with TRACKER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    return rows, {row["merchant_id"]: row for row in rows}, fieldnames


def merchant_card(row: dict[str, str], article_slug: str) -> dict[str, str]:
    brand = row["brand"].strip()
    products = row.get("main_products", "").strip()
    reason = row.get("content_angles", "").strip() or products
    promo = row.get("promo_link", "").strip()
    store = row.get("store_link", "").strip() or f"https://www.momoshop.com.tw/TP/{row['merchant_id']}/main"
    return {
        "name": f"{brand} 選物頁",
        "merchantId": row["merchant_id"],
        "brandName": brand,
        "affiliateUrl": promo or store,
        "sourceProductUrl": store,
        "imageCredit": f"圖片來源：momo 店家頁｜{brand}",
        "selectionReason": f"{reason}。本篇以使用情境、收納位置與商品頁資訊做比較，不寫成單一標準答案。",
        "riskNote": "價格、規格、活動與庫存請以 momo 商品頁公告為準。",
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


def build_sections(spec: dict[str, Any], brand_names: list[str]) -> list[dict[str, Any]]:
    item_text = "、".join(spec["items"])
    first_brands = "、".join(brand_names[:3])
    all_brands = "、".join(brand_names)
    return [
        {
            "heading": "先釐清真正要解決的生活問題",
            "paragraphs": [
                spec["scene"],
                f"Elite Fashion 編輯團隊會先把這題拆成「使用頻率、收納位置、維護成本」三個問題，而不是一開始就看品牌或外型。這樣做的好處，是讓 {item_text} 回到生活裡真正會出現的位置。",
                f"本篇會把 {first_brands} 等選項放在同一個情境裡比較。它們不是同一種答案，而是對應不同家庭、桌面、餐桌或出門節奏的補位方式。",
            ],
            "bullets": ["先寫下最常發生的使用情境。", "確認物品要放在哪裡、誰會使用、多久整理一次。"],
        },
        {
            "heading": "選購順序：先頻率，再空間，最後看風格",
            "paragraphs": [
                spec["decision"],
                "如果一件東西每天都會用，它應該被放在最容易拿的位置；如果只在週末或旅行前使用，就不該佔據最好的桌面或玄關位置。這個順序比單純追求完整清單更實用。",
                "風格仍然重要，只是它應該排在使用條件之後。顏色、材質與外觀要能接上既有空間，不要讓新物件變成另一個需要被整理的負擔。",
            ],
            "bullets": ["每日使用：優先看拿取與清潔。", "每週使用：優先看收納與搬動。", "偶爾使用：優先看體積與保存。"],
        },
        {
            "heading": "不同品牌適合放在不同位置比較",
            "paragraphs": [
                f"{all_brands} 可以被理解成不同的入口：有的適合先看大方向，有的適合補細節，有的適合當作同場景備選。編輯判斷會把它們放回使用情境，而不是把所有名字排成一張表。",
                "讀者在比較時，可以先問自己：這個品牌頁裡的商品，是補一個固定需求，還是只因為當下看起來吸引人？前者比較適合留下，後者可以先收藏，不急著下單。",
            ],
            "bullets": ["先看商品頁的尺寸、材質與使用限制。", "再看是否符合目前空間與使用頻率。"],
        },
        {
            "heading": "常見錯誤：一次買滿，反而失去調整空間",
            "paragraphs": [
                "很多採買失誤不是買錯品牌，而是買太早。還沒有確認動線、飲食習慣、出門頻率或寵物反應之前，一口氣買滿會讓後續調整變得麻煩。",
                "比較好的做法，是先買能解決核心問題的一到兩項，再用一週到一個月觀察是否真的被使用。若它能自然進入日常，再補上同情境的其他物件。",
                "這種慢一點的採買方式，對小宅、辦公室、餐桌、旅行與寵物用品都更友善，也比較符合本站希望建立的長期生活秩序。",
            ],
            "bullets": [],
        },
        {
            "heading": "下單前最後確認：商品頁、空間與使用者",
            "paragraphs": [
                "最後一步請回到商品頁確認規格、價格、活動與庫存。本文只提供情境與選購順序，不替任何即時資訊背書，也不把單一商品寫成唯一答案。",
                spec["risk"],
                "如果你正在替家人、孩子、寵物或有健康需求的人採買，請把安全、標示、使用限制與專業建議放在外觀之前。能被長期安心使用的物件，通常比一次買齊更值得。",
            ],
            "bullets": ["確認尺寸與擺放位置。", "確認清潔、保存或維護方式。", "確認是否需要專業建議或成人陪同。"],
        },
    ]


def build_article(spec: dict[str, Any], rows_by_merchant: dict[str, dict[str, str]], config: dict[str, Any], categories: dict[str, pipeline.CategoryConfig]) -> dict[str, Any]:
    brand_rows = [rows_by_merchant[mid] for mid in spec["brands"]]
    brand_names = [row["brand"] for row in brand_rows]
    cards = [merchant_card(row, spec["slug"]) for row in brand_rows]
    hero_image = prepare_cover(spec)
    category = categories[spec["category"]]
    disclaimer = spec["risk"]
    if spec["category"] == "wellness-movement" or "寵物" in spec["title"]:
        disclaimer = (
            f"{spec['risk']} 本文僅供一般生活資訊與選購情境參考，不構成醫療、營養、獸醫或個人化建議；"
            "若涉及健康、照護、飲食、受傷、疾病或寵物狀況，請先諮詢合格專業人員。"
        )
    article = {
        "slug": spec["slug"],
        "category": spec["category"],
        "title": spec["title"],
        "excerpt": f"從{spec['items'][0]}到{spec['items'][-1]}，整理適合台灣日常的採買順序、比較重點與常見錯誤。",
        "tags": [category.label, "生活採買", spec["items"][0], spec["items"][-1]],
        "metaTitle": f"Elite Fashion｜{spec['title'][:48]}",
        "metaDescription": f"{spec['title']}，以使用頻率、收納位置與商品頁資訊建立保守的比較順序。",
        "series": "新受眾生活採買指南",
        "listingTitle": spec["title"],
        "listingExcerpt": f"把{spec['items'][0]}、{spec['items'][-1]}與日常動線一起比較，避免一次買太多。",
        "heroImage": hero_image,
        "heroImageAlt": spec["heroAlt"],
        "intro": f"{spec['scene']} 本文不替讀者做衝動推薦，而是用使用頻率、收納位置與維護成本，整理一套更穩的採買順序。",
        "sections": build_sections(spec, brand_names),
        "faq": [
            {
                "question": "這篇文章會直接推薦單一品牌嗎？",
                "answer": "不會。本文會把不同品牌放回生活情境中比較，協助讀者判斷使用頻率、收納位置與商品頁資訊，而不是把單一品牌寫成唯一答案。",
            },
            {
                "question": "商品價格、活動或庫存可以以本文為準嗎？",
                "answer": "不可以。價格、活動、庫存、規格與配送條件都可能變動，請以下單前看到的商品頁或店家頁公告為準。",
            },
            {
                "question": "如果內容涉及健康、寵物或照護用品，應該怎麼判斷？",
                "answer": "請把本文視為一般生活採買整理，不要當成醫療、營養、獸醫或個人化建議；若有健康、照護或寵物狀況，應先詢問合格專業人員。",
            },
        ],
        "extendedReading": [
            {"title": f"瀏覽更多{category.label}文章", "url": f"/{category.page}"},
            {"title": "查看生活品味文章", "url": "/lifestyle-culture.html"},
            {"title": "查看站內搜尋", "url": "/search.html"},
        ],
        "cta": {
            "variant": "gold",
            "text": "下單前先確認商品頁資訊，再依你家的空間、使用頻率與維護方式慢慢比較。",
            "links": [{"label": f"查看 {row['brand']}", "url": row.get("promo_link") or row.get("store_link")} for row in brand_rows[:4]],
        },
        "inlineCtas": [
            {
                "afterSection": 2,
                "variant": "olive",
                "eyebrow": "先看情境，再看商品",
                "heading": "把常用物放在最容易回到原位的地方",
                "text": "好的採買不是一次買滿，而是讓每件物品都有固定位置、使用理由與收尾方式。",
                "links": [{"label": cards[0]["name"], "url": cards[0]["affiliateUrl"]}, {"label": cards[1]["name"], "url": cards[1]["affiliateUrl"]}],
            }
        ],
        "disclaimer": disclaimer,
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
                "role": "情境比較",
                "reason": row.get("content_angles") or row.get("main_products") or "可依商品頁資訊與使用情境比較。",
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
        note = "2026-05-28 momo 新受眾第一批生活採買文章已置入。"
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
    articles = [build_article(spec, rows_by_merchant, config, categories) for spec in ARTICLES]
    update_queue(articles, config)
    update_tracker(articles, tracker_rows, fieldnames)
    update_latest_run(config, articles)
    pipeline.rebuild_outputs(config, categories)
    strip_article_trailing_whitespace(articles)
    pipeline.verify_outputs(config, categories)
    print(f"Generated {len(articles)} Q-0013 momo new-audience articles:")
    for article in articles:
        print(f"- {article['slug']} -> {article['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
