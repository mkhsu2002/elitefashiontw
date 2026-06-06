#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Any
from xml.dom import minidom


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://tw.elitefasion.com"
SITE_NAME = "Elite Fashion"
EDITORIAL_TEAM = "Elite Fashion 編輯團隊"
TODAY = "2026-06-05"

EXCLUDED_HTML = {
    "404.html",
}

NON_ARTICLE_TOP_LEVEL = {
    "about.html",
    "all-articles.html",
    "ai-innovation.html",
    "casual-chic.html",
    "contact.html",
    "designer-perspective.html",
    "editorial-policy.html",
    "high-performance.html",
    "index.html",
    "lifestyle-culture.html",
    "outdoor-escapes.html",
    "runway-trends.html",
    "search.html",
    "wellness-movement.html",
}

CATEGORY_PAGES = {
    "ai-innovation": ("人工智能", "ai-innovation.html"),
    "runway-trends": ("秀場趨勢", "runway-trends.html"),
    "designer-perspective": ("設計師視角", "designer-perspective.html"),
    "casual-chic": ("休閒時尚", "casual-chic.html"),
    "wellness-movement": ("健康恢復", "wellness-movement.html"),
    "outdoor-escapes": ("戶外生活", "outdoor-escapes.html"),
    "lifestyle-culture": ("生活品味", "lifestyle-culture.html"),
}

try:
    from scripts.content_pipeline import LEGACY_LIFE_PROPOSALS_CATEGORY_OVERRIDES
except Exception:
    LEGACY_LIFE_PROPOSALS_CATEGORY_OVERRIDES = {}

try:
    from scripts.article_taxonomy import CORE_HUB_LINKS, enrich_article_record, hub_payload
except Exception:
    from article_taxonomy import CORE_HUB_LINKS, enrich_article_record, hub_payload


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def strip_tags(value: str) -> str:
    value = re.sub(r"<script.*?</script>", "", value, flags=re.I | re.S)
    value = re.sub(r"<style.*?</style>", "", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def extract_title(content: str) -> str:
    for pattern in [
        r"<h1[^>]*>(.*?)</h1>",
        r"<title[^>]*>(.*?)</title>",
    ]:
        match = re.search(pattern, content, flags=re.I | re.S)
        if match:
            title = strip_tags(match.group(1))
            return re.sub(r"\s+[-|]\s+Elite Fashion.*$", "", title).strip()
    return SITE_NAME


def extract_meta(content: str, name: str, *, attr: str = "name") -> str:
    match = re.search(
        rf'<meta[^>]+{attr}=["\']{re.escape(name)}["\'][^>]+content=["\']([^"\']*)["\']',
        content,
        flags=re.I,
    )
    return html.unescape(match.group(1)).strip() if match else ""


def extract_first_paragraph(content: str) -> str:
    match = re.search(r"<p[^>]*>(.*?)</p>", content, flags=re.I | re.S)
    return strip_tags(match.group(1)) if match else ""


def has_noindex(content: str) -> bool:
    robots = extract_meta(content, "robots").lower()
    return "noindex" in robots


def rel_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def extensionless_path(relative_path: str) -> str:
    relative_path = relative_path.lstrip("/")
    if relative_path == "index.html":
        return ""
    if relative_path.endswith(".html"):
        return relative_path[:-5]
    return relative_path


def canonical_url(relative_path: str) -> str:
    path = extensionless_path(relative_path)
    return f"{BASE_URL}/{path}" if path else f"{BASE_URL}/"


def display_href(relative_path: str, *, from_root: bool = True) -> str:
    path = extensionless_path(relative_path)
    if not path:
        return "/" if from_root else "../"
    return f"/{path}" if from_root else path


def local_href_to_extensionless(value: str) -> str:
    if value.startswith(("mailto:", "tel:", "#", "javascript:", "data:")):
        return value
    if value.startswith(("http://", "https://")):
        if value.startswith(BASE_URL + "/") and ".html" in value:
            return re.sub(r"\.html(?=([?#]|$))", "", value)
        return value
    if value in {"index", "/index"}:
        return "/"
    if value.endswith("/index"):
        return value[: -len("index")]
    value = re.sub(r"(^|/)index\.html(?=([?#]|$))", r"\1", value)
    return re.sub(r"\.html(?=([?#]|$))", "", value)


def normalize_local_hrefs(content: str) -> str:
    def repl(match: re.Match[str]) -> str:
        quote = match.group(1)
        href = match.group(2)
        return f'href={quote}{html.escape(local_href_to_extensionless(html.unescape(href)), quote=True)}{quote}'

    content = re.sub(r'href=(["\'])([^"\']+?\.html(?:[?#][^"\']*)?)\1', repl, content, flags=re.I)
    content = re.sub(r'href=(["\'])(/?(?:\.\./)*index)\1', repl, content, flags=re.I)
    return re.sub(rf"{re.escape(BASE_URL)}/([^\"'<>\s]+?)\.html\b", rf"{BASE_URL}/\1", content)


def classify_page(path: Path) -> tuple[str, str, str]:
    relative = rel_path(path)
    if path.name == "index.html":
        return "home", "首頁", ""
    if path.parent == ROOT:
        for key, (label, page) in CATEGORY_PAGES.items():
            if path.name == page:
                return "category", label, key
        if path.name in {
            "mature-life-reset.html",
            "body-rhythm-reset.html",
            "ai-work-reset-45.html",
            "commute-style-reset.html",
            "outdoor-travel-reset.html",
        }:
            return "hub", extract_title(path.read_text(encoding="utf-8", errors="ignore")), ""
        if path.name in NON_ARTICLE_TOP_LEVEL:
            return "page", extract_title(path.read_text(encoding="utf-8", errors="ignore")), ""
        return "article", "特輯", "special-features"
    category_key = path.parent.name
    if category_key in CATEGORY_PAGES:
        return "article", CATEGORY_PAGES[category_key][0], category_key
    if category_key == "life-proposals":
        mapped = LEGACY_LIFE_PROPOSALS_CATEGORY_OVERRIDES.get(path.name, "lifestyle-culture")
        if mapped in CATEGORY_PAGES:
            return "article", CATEGORY_PAGES[mapped][0], mapped
        return "article", "生活品味", "lifestyle-culture"
    if category_key == "uap-ufo-declassified":
        return "article", "特輯", "special-features"
    return "article", category_key.replace("-", " ").title(), category_key


def extract_internal_links(content: str, page_path: Path, limit: int = 15) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    seen: set[str] = set()
    main_match = re.search(r"<main[^>]*>(.*?)</main>", content, flags=re.I | re.S)
    search_area = main_match.group(1) if main_match else content
    search_area = re.sub(r"<nav[^>]*>.*?</nav>", "", search_area, flags=re.I | re.S)
    search_area = re.sub(r"<footer[^>]*>.*?</footer>", "", search_area, flags=re.I | re.S)
    for match in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', search_area, flags=re.I | re.S):
        href = html.unescape(match.group(1)).strip()
        if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        text = strip_tags(match.group(2))
        if not text or len(text) < 2:
            continue
        normalized = local_href_to_extensionless(href.split("#", 1)[0].split("?", 1)[0])
        if normalized in seen:
            continue
        seen.add(normalized)
        url = urllib.parse.urljoin(canonical_url(rel_path(page_path)), normalized)
        links.append({"name": text[:90], "url": url})
        if len(links) >= limit:
            break
    return links


def breadcrumb_schema(
    page_path: Path,
    title: str,
    category_key: str,
    *,
    page_type: str = "",
    primary_hub: dict[str, str] | None = None,
) -> dict[str, Any]:
    items = [
        {"@type": "ListItem", "position": 1, "name": "首頁", "item": f"{BASE_URL}/"},
    ]
    if page_type == "article" and primary_hub:
        items.append(
            {
                "@type": "ListItem",
                "position": len(items) + 1,
                "name": primary_hub["title"],
                "item": canonical_url(primary_hub["file"]),
            }
        )
    elif category_key in CATEGORY_PAGES and page_path.name != CATEGORY_PAGES[category_key][1]:
        label, category_page = CATEGORY_PAGES[category_key]
        items.append(
            {
                "@type": "ListItem",
                "position": len(items) + 1,
                "name": label,
                "item": canonical_url(category_page),
            }
        )
    items.append(
        {
            "@type": "ListItem",
            "position": len(items) + 1,
            "name": title,
            "item": canonical_url(rel_path(page_path)),
        }
    )
    return {"@type": "BreadcrumbList", "itemListElement": items}


def maintenance_schema(page_path: Path, content: str) -> dict[str, Any]:
    relative = rel_path(page_path)
    url = canonical_url(relative)
    page_type, category_label, category_key = classify_page(page_path)
    title = extract_title(content)
    description = extract_meta(content, "description") or extract_first_paragraph(content) or title
    image = extract_meta(content, "og:image", attr="property") or f"{BASE_URL}/images/og-main.jpg"
    modified = datetime.fromtimestamp(page_path.stat().st_mtime, tz=timezone.utc).isoformat()
    taxonomy_record = enrich_article_record(
        {
            "file": relative,
            "relativeUrl": relative,
            "category": category_key,
            "categoryLabel": category_label,
            "title": title,
            "excerpt": description,
            "tags": [item.strip() for item in extract_meta(content, "keywords").split(",") if item.strip()],
        }
    )
    primary_hub = taxonomy_record.get("primaryHub") if page_type == "article" else None
    graph: list[dict[str, Any]] = [
        {
            "@type": "Organization",
            "@id": f"{BASE_URL}/#organization",
            "name": SITE_NAME,
            "url": f"{BASE_URL}/",
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/images/logo.jpg",
            },
            "sameAs": [
                "https://www.instagram.com/northpath.ca",
                "https://www.facebook.com/northpathca/",
            ],
        },
        {
            "@type": "WebSite",
            "@id": f"{BASE_URL}/#website",
            "name": SITE_NAME,
            "url": f"{BASE_URL}/",
            "inLanguage": "zh-TW",
            "publisher": {"@id": f"{BASE_URL}/#organization"},
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{BASE_URL}/search?q={{search_term_string}}",
                "query-input": "required name=search_term_string",
            },
        },
        breadcrumb_schema(page_path, title, category_key, page_type=page_type, primary_hub=primary_hub),
    ]
    if page_type == "article":
        article_schema = {
            "@type": "Article",
            "@id": f"{url}#article",
            "headline": title,
            "description": description,
            "image": image,
            "author": {"@id": f"{BASE_URL}/#organization"},
            "publisher": {"@id": f"{BASE_URL}/#organization"},
            "mainEntityOfPage": url,
            "dateModified": modified,
            "inLanguage": "zh-TW",
            "articleSection": taxonomy_record.get("topicCategoryLabel") or category_label,
            "about": [
                {"@type": "Thing", "name": category_label},
                {"@type": "Thing", "name": taxonomy_record.get("topicCategoryLabel") or category_label},
            ],
        }
        if primary_hub:
            article_schema["isPartOf"] = {"@id": f"{canonical_url(primary_hub['file'])}#webpage"}
        graph.append(article_schema)
    else:
        graph.append(
            {
                "@type": "CollectionPage" if page_type in {"category", "hub", "home"} else "WebPage",
                "@id": f"{url}#webpage",
                "name": title,
                "description": description,
                "url": url,
                "isPartOf": {"@id": f"{BASE_URL}/#website"},
                "publisher": {"@id": f"{BASE_URL}/#organization"},
                "dateModified": modified,
                "inLanguage": "zh-TW",
            }
        )
    item_links = extract_internal_links(content, page_path)
    if item_links:
        graph.append(
            {
                "@type": "ItemList",
                "@id": f"{url}#itemlist",
                "name": f"{title}延伸閱讀",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index,
                        "name": item["name"],
                        "url": item["url"],
                    }
                    for index, item in enumerate(item_links, start=1)
                ],
            }
        )
    faq_items = re.findall(
        r"<summary[^>]*>(.*?)</summary>\s*<p[^>]*>(.*?)</p>",
        content,
        flags=re.I | re.S,
    )
    if faq_items:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": strip_tags(question),
                        "acceptedAnswer": {"@type": "Answer", "text": strip_tags(answer)},
                    }
                    for question, answer in faq_items[:8]
                ],
            }
        )
    return {"@context": "https://schema.org", "@graph": graph}


def upsert_meta_url(content: str, attr: str, key: str, url: str) -> str:
    pattern = rf'<meta(?=[^>]+{attr}=["\']{re.escape(key)}["\'])[^>]*>'
    match = re.search(pattern, content, flags=re.I)
    if not match:
        return content
    tag = match.group(0)
    if re.search(r'content=["\'][^"\']*["\']', tag, flags=re.I):
        updated = re.sub(r'content=(["\'])([^"\']*)\1', f'content="{html.escape(url)}"', tag, count=1, flags=re.I)
    else:
        updated = tag[:-1] + f' content="{html.escape(url)}">'
    return content[: match.start()] + updated + content[match.end() :]


def upsert_head_seo(page_path: Path, content: str) -> str:
    relative = rel_path(page_path)
    url = canonical_url(relative)
    content = normalize_local_hrefs(content)
    content = re.sub(
        r'\s*<script[^>]+id=["\']site-seo-schema["\'][^>]*>.*?</script>',
        "",
        content,
        flags=re.I | re.S,
    )
    canonical_tag = f'<link rel="canonical" href="{html.escape(url)}">'
    if re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', content, flags=re.I):
        content = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>', canonical_tag, content, count=1, flags=re.I)
    else:
        content = content.replace("</head>", f"    {canonical_tag}\n</head>", 1)
    feed_tag = f'<link rel="alternate" type="application/rss+xml" title="{SITE_NAME} RSS" href="{BASE_URL}/feed.xml">'
    if "application/rss+xml" not in content:
        content = content.replace(canonical_tag, f"{canonical_tag}\n    {feed_tag}", 1)
    content = upsert_meta_url(content, "property", "og:url", url)
    content = upsert_meta_url(content, "name", "twitter:url", url)
    schema = json.dumps(maintenance_schema(page_path, content), ensure_ascii=False, separators=(",", ":"))
    schema_tag = f'    <script type="application/ld+json" id="site-seo-schema">{schema}</script>\n'
    content = content.replace("</head>", f"{schema_tag}</head>", 1)
    return content


def format_date_from_iso(value: str) -> str:
    if not value:
        return TODAY
    value = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except ValueError:
        return TODAY


def image_url(path: str) -> str:
    if path.startswith(("http://", "https://")):
        return path
    return f"{BASE_URL}/{path.lstrip('/')}"


HUBS: list[dict[str, Any]] = [
    {
        "file": "mature-life-reset.html",
        "category": "lifestyle-culture",
        "title": "人生重整與一人生活秩序",
        "description": "整理離婚、喪偶、返台、獨居、家庭對話與社交邊界之後，如何把生活重新放回可掌握的日常。",
        "image": "images/og-lifestyle-culture.jpg",
        "eyebrow": "生活品味策展",
        "intro": [
            "人生重整不是把過去全部推翻，也不是逼自己立刻變得強大。真正能留下來的重整，通常從很小的秩序開始：今天晚上睡哪裡、明天早上先處理哪一份文件、這一週要和誰保持距離、哪些訊息需要回覆，哪些可以先暫停。當生活發生轉折，最容易消耗人的不是單一事件本身，而是每件事都同時要求你做決定。Elite Fashion 編輯團隊把這個主題頁設計成一張可反覆回來查看的生活地圖，讓你不用在情緒最混亂時，還要從零開始整理方向。",
            "這裡收錄的文章不把一人生活寫成浪漫口號，也不把關係結束寫成單一勝利敘事。離婚、喪偶、返台、長期獨居、家庭記憶、社交圈重建與事業節奏，背後都有非常具體的現實任務。家中安全、銀行帳戶、保險文件、租屋或購屋、家人溝通、工作交接、生活採買與夜間情緒，都會在某個時刻變成需要處理的清單。與其期待自己一次完成，不如先把任務拆成會影響安全、現金流、睡眠、工作與人際邊界的幾個層級。",
            "我們建議先處理能降低風險的事，再處理能恢復尊嚴的事，最後才處理形象與風格。降低風險包含門鎖、緊急聯絡人、重要文件、付款紀錄、醫療與保險資訊；恢復尊嚴則包含固定作息、衣櫥整理、廚房與浴室的使用動線、能讓自己出門見人的基本照顧。當這些基礎穩住，社交、旅行、興趣、第二曲線與新的關係才不會只是逃離，而會成為真正可以選擇的生活。",
            "台灣情境裡還有幾個常被忽略的細節：住宅空間較小，收納與通行動線會很快影響心情；家庭與親友關係密集，界線需要說得柔和但清楚；返台或跨國生活者常同時面對戶籍、健保、銀行、語言與家人期待；高壓職場中的讀者，則可能外表仍然能工作，內在卻已經沒有餘裕。這些都不是靠一句正能量能解決的事，需要的是可執行的順序。",
            "閱讀這個 hub 時，可以先挑最貼近當下壓力的入口。如果你剛經歷關係或家庭轉折，先看文件、住居與社交邊界；如果你已經穩住基本生活，則可以往居家秩序、返台重啟、信任網絡與事業韌性延伸；如果你正在替家人或朋友尋找支援，也請把文章當作陪伴對話的提綱，而不是替對方下指令。真正好的支援，是讓人重新拿回決定權，而不是用另一套標準壓住她。",
            "這個主題的核心判斷是：先讓生活變得可預期，再讓人生重新變得開闊。可預期不是無聊，而是在混亂中保留一點能被自己掌握的節奏。當家裡的鑰匙、文件、衣服、食物、工作與人際回覆都有位置，心就比較容易騰出空間，去思考下一步想成為什麼樣的人。這也是 Elite Fashion 寫人生重整時最在意的地方：不是替讀者定義答案，而是提供一套足夠清楚、足夠溫柔、也足夠現實的排序方式。",
        ],
        "links": [
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
        "faq": [
            ("這個主題頁適合從哪一篇開始？", "先從最會影響安全、文件、住居與現金流的文章開始，再延伸到社交、職涯與居家秩序。"),
            ("如果現在只想先穩住情緒，需要一次讀完嗎？", "不需要。建議先選一篇最貼近當下困難的文章，做完一到兩個小動作，再回來看下一篇。"),
            ("文章會提供法律、醫療或投資建議嗎？", "不會。本站提供生活整理與決策順序，涉及法律、醫療、保險或投資時，仍應諮詢合格專業人員。"),
        ],
    },
    {
        "file": "body-rhythm-reset.html",
        "category": "wellness-movement",
        "title": "身體節奏與恢復生活指南",
        "description": "從睡眠、降溫、肌力、久坐伸展、旅行恢復與日常補給，整理能長期留下來的身體照顧順序。",
        "image": "images/og-wellness-movement.jpg",
        "eyebrow": "健康恢復策展",
        "intro": [
            "身體節奏的重整，最怕被做成另一個高壓計畫。當工作、家庭、旅行與居家任務都擠在同一天，很多人會把睡眠、伸展、補水、飲食與恢復放到最後，直到疲勞變成明顯卡關才回頭處理。這個 hub 的目的，是把身體照顧從抽象口號拉回日常順序：什麼先做，什麼可以晚一點，哪些用品只是輔助，哪些習慣才是真正影響生活品質的核心。",
            "Elite Fashion 編輯團隊觀察到，讀者最常遇到的不是不知道健康重要，而是不知道怎麼在忙碌生活裡安排。晚上太熱、久坐肩頸緊、出差後睡眠亂掉、家中照護用品沒有位置、低壓運動總是被取消、飲食補給被活動與庫存牽著走，這些問題都不是單靠意志力能解決。比較可靠的做法，是把身體訊號當成生活設計的一部分，讓環境、時間與物品配置一起幫你降低阻力。",
            "本頁的閱讀順序可以從睡眠與恢復開始。睡眠不是一天結束時才發生的事，白天咖啡因、晚餐時間、室內溫度、光線、工作收尾方式與床邊物品，都會影響夜間品質。若你常在季節轉換、旅行移動或高壓專案後覺得身體跟不上，先檢查睡眠與恢復窗口，比先追求更完整的運動菜單更實際。",
            "接著再看肌力、久坐與低門檻活動。行動力不是只屬於健身房，而是每天從椅子站起來、提東西、爬樓梯、走一段路、搬行李、整理家裡時會用到的能力。若把運動想成必須一次完成的大型任務，就很容易延後；若把它拆成十分鐘伸展、上下班步行、睡前放鬆與週末恢復，反而更容易持續。這也是本站寫身體照顧時最在意的取捨：先讓身體願意開始，再慢慢談強度。",
            "在台灣生活裡，身體節奏也會被天氣與居住空間影響。濕熱、冷氣、窄小浴室、通勤時間、辦公室久坐與連假移動，都會讓用品與習慣的選擇不同。涼感寢具、靠墊、按摩工具、耳塞、補水用品、簡單備餐或小型伸展角落，都不應只是商品清單，而要回到你家裡的使用位置、清潔方式與收納邊界。買得越多不一定越健康，真正能被反覆使用的才有意義。",
            "如果文章涉及食品、護具、照護、睡眠或身體不適，我們會保留必要的限制語氣。一般生活媒體不應承諾療效，也不應把用品寫成醫療替代方案。你可以把這些文章視為生活檢查表：先觀察、再調整環境與頻率，最後才決定是否需要添購或尋求專業協助。身體節奏不是追求完美，而是讓自己每天少一點硬撐，多一點可以恢復的空間。",
            "若只能先做一件事，請從最常重複發生的卡點開始。有人是睡前滑手機太久，有人是辦公椅與桌高不合，有人是出差後沒有恢復日，也有人是用品散在各處，真正使用時反而找不到。把卡點寫下來，再選對應文章，比一次追求完整健康計畫更容易成功。",
        ],
        "links": [
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
        "faq": [
            ("身體恢復應該先從運動還是睡眠開始？", "若已經長期疲勞，先穩住睡眠、補水、溫度與恢復窗口，再慢慢加入低門檻活動。"),
            ("文章裡的用品可以直接當健康建議嗎？", "不可以。用品只是生活配置參考，任何持續不適、用藥、復健或照護問題，都應諮詢合格專業人員。"),
            ("沒有時間運動怎麼辦？", "先把活動拆小，例如十分鐘伸展、走路、站立休息或睡前放鬆，讓身體先有可重複的節奏。"),
        ],
    },
    {
        "file": "ai-work-reset-45.html",
        "category": "ai-innovation",
        "title": "AI 工作重整與第二曲線",
        "description": "從辦公室協作、履歷整理、管理判斷、內容工作與副業測試，建立不暴露隱私也能提升效率的 AI 工作方法。",
        "image": "images/og-ai-innovation.jpg",
        "eyebrow": "人工智能策展",
        "intro": [
            "AI 工作重整最重要的不是追逐工具清單，而是重新分配你的注意力。每天的回信、摘要、簡報、會議整理、資料比對、履歷修改、客戶溝通與內容草稿，都有一部分可以交給工具先做粗稿；但判斷風險、理解人情、決定取捨、保護資料與承擔結果，仍然需要由人守住。這個 hub 的目標，是幫讀者把 AI 從流行話題放回真實工作流程，讓它成為降低摩擦的助手，而不是新的焦慮來源。",
            "很多人學 AI 的第一步卡在名詞太多：模型、提示、外掛、自動化、資料庫、助理、工作流，每一個字看似都需要重新學一門技術。Elite Fashion 編輯團隊的建議是，不要從工具開始，而要從任務開始。你可以先列出一週內最耗時的十件事，標記哪些是重複整理、哪些是需要判斷、哪些有隱私或商業敏感資訊。只有低風險、可檢查、可重做的任務，才適合先交給 AI 練習。",
            "這個主題頁分成三條路徑。第一條是辦公室效率：會議紀要、Email 草稿、簡報初稿、資料摘要與跨部門溝通。第二條是職涯價值：履歷、面試、管理者定位、第二曲線與專業經驗再包裝。第三條是小型副業與內容實驗：把多年經驗拆成受眾問題、服務原型、交付物與收費假設，用低成本方式測試市場，而不是一開始就投入過大的平台或課程。",
            "AI 的風險同樣需要被寫清楚。不要把公司內部資料、客戶個資、合約、未公開財務、醫療或付款資訊直接丟進不明工具；不要用 AI 產出的內容直接對外承諾；不要把工具回覆當作唯一事實來源。比較穩的工作方式，是讓 AI 提供草稿、框架、檢查清單與反方觀點，再由你回到來源、情境與責任邊界確認。效率真正提升，不是因為少看一次，而是因為你更快知道該看哪裡。",
            "對正在思考第二曲線的讀者來說，AI 的價值不只在於節省時間，也在於降低試錯成本。你可以用它整理自己的經驗資產，測試某個主題是否能寫成文章、顧問服務、工作坊、模板或社群內容；也可以用它模擬不同受眾會問什麼、反對什麼、願意為什麼付費。但最後能不能成立，仍然取決於你是否真的理解讀者的問題，是否能提供比通用整理更具體的判斷。",
            "本頁的閱讀順序是：先從 AI 入門與辦公室協作建立基本安全感，再看管理者導入、履歷面試與第二曲線，最後才看副業與工具選物。這樣安排，是為了避免把 AI 學習變成另一個囤積課程的行為。工具會改版，熱門平台會輪替，但清楚描述問題、拆解流程、檢查來源、保護資料與做出判斷的能力，會持續有效。這也是本站寫 AI 工作重整的核心標準。",
            "如果你正在團隊裡推動 AI，也可以把這個頁面當成共讀起點。先用文章討論哪些任務可交給工具協助，哪些資料不能輸入，哪些輸出需要二次確認，再決定是否導入更複雜的流程。當規則先講清楚，效率提升才不會變成新的管理風險。",
        ],
        "links": [
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
        "faq": [
            ("完全不懂技術，可以從這個主題開始嗎？", "可以。建議先從日常工作任務開始，而不是從工具名詞開始。"),
            ("AI 工具可以處理公司資料嗎？", "涉及個資、未公開商業資訊、合約、付款、醫療或客戶資料時，應遵守公司政策並避免輸入不明工具。"),
            ("要不要先買很多 AI 課程？", "不建議一開始大量購買。先用兩週小實驗確認自己真正需要改善的工作流程，再決定是否進階學習。"),
        ],
    },
    {
        "file": "commute-style-reset.html",
        "category": "casual-chic",
        "title": "通勤衣櫥與鞋包選物指南",
        "description": "把通勤、會議、週末、旅行與日常整理成可重複穿搭的衣櫥順序，降低每天出門前的決策疲勞。",
        "image": "images/og-casual-chic.jpg",
        "eyebrow": "休閒時尚策展",
        "intro": [
            "通勤衣櫥不是越多越好，而是每天出門前能不能快速做出不後悔的選擇。真正有用的衣櫥，會同時照顧早晨時間、辦公室溫度、會議正式度、鞋子舒適度、包包容量、天氣變化與下班後的行程。如果每一次搭配都像重新開一個專案，衣服再漂亮也會變成壓力。這個 hub 把通勤穿搭、鞋包、配件、旅行衣物與週末休閒整理成一套可重複使用的順序，幫你把風格變成生活效率的一部分。",
            "Elite Fashion 編輯團隊建議先建立核心輪廓，再補變化。核心輪廓包含三到五套可以應付常見工作日的搭配：一套正式會議、一套日常辦公、一套外出拜訪、一套週五或週末銜接、一套天氣不穩時的備案。每一套都要確認上衣、下身、外套、鞋子、包包與配件可以互相替換，而不是只在照片裡好看。當基本輪廓穩定，早晨就不需要重新發明自己。",
            "鞋包是通勤衣櫥裡最容易被低估的部分。鞋子決定一天能不能走路、站立與移動；包包決定電腦、雨傘、水瓶、補妝用品、文件與個人物品是否有位置。若只看外觀，很容易買到不適合日常節奏的單品。比較好的檢查方式，是先列出你每天真正攜帶的物品，再看包內分層、肩帶、重量、材質、開口安全感與雨天維護；鞋子則要回到通勤距離、地面材質、站立時間與腳型。",
            "台灣通勤情境還需要考慮濕熱、冷氣、午後雨、捷運與辦公室溫差。輕薄外套、可清潔材質、抗皺布料、能快速替換的鞋子與收納小包，通常比單季流行更能提升生活品質。這不代表衣櫥只能保守，而是要讓風格建立在真實動線上。當你知道哪一雙鞋可以走整天，哪一個包能放下工作物品，哪一件外套能處理冷氣，風格就會變得更從容。",
            "配件與妝髮的角色，是替基本衣櫥增加識別度，而不是製造更多負擔。耳環、皮帶、絲巾、髮飾、唇彩、眼鏡與小型包款，都可以讓同一套衣服在不同場合有不同表情。但它們必須有固定收納位置，也要能在早晨五分鐘內被找到。買配件前先問：它能搭配至少三套衣服嗎？它適合我的常見場合嗎？它需要額外照顧到我懶得使用嗎？",
            "這個主題頁的閱讀順序，是先看衣櫥架構與正式休閒的平衡，再看通勤鞋包、旅行衣物、配件與早晨整理。若你正在重新整理衣櫥，先不要急著淘汰或大量購買；把一週實際穿過、覺得舒服、被稱讚、或穿完很想立刻換掉的單品寫下來，通常比看更多穿搭圖更準確。衣櫥的目的不是證明你有多少選擇，而是讓每一天的你都比較容易出門。",
            "最後再回到預算分配。最常穿、最常走、最常背、最常被看到的單品，值得花較多時間比較；低頻場合或情緒型購物，則適合先用現有衣物替代。這樣做不會讓風格變保守，反而會讓每一次添購都更精準，也更符合自己的生活節奏。",
        ],
        "links": [
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
        "faq": [
            ("通勤衣櫥應該先買衣服、鞋子還是包包？", "先看你每天最卡的地方。若常覺得累，先看鞋；若常找不到東西，先看包；若每天搭配困難，再整理衣櫥輪廓。"),
            ("膠囊衣櫥會不會太無聊？", "不必。核心單品負責穩定，配件、色彩、鞋包與外套可以負責變化。"),
            ("可以照文章清單直接採買嗎？", "建議先用自己的工作日、通勤距離、辦公室溫度與常見場合檢查，再決定真正需要補哪一類。"),
        ],
    },
    {
        "file": "outdoor-travel-reset.html",
        "category": "outdoor-escapes",
        "title": "旅行與戶外移動準備指南",
        "description": "從週末出行、城市散步、登山、露營、機上睡眠與拍攝設備，整理更輕盈也更安全的移動順序。",
        "image": "images/og-outdoor-escapes.jpg",
        "eyebrow": "戶外生活策展",
        "intro": [
            "旅行與戶外移動的準備，不應只是把清單越寫越長。真正好的準備，是讓你出門後更自由，而不是被裝備、行李與不確定感綁住。週末城市散步、近郊登山、露營、長途飛行、家庭出遊、工作旅行與拍攝行程，需要的東西不同；若全部用同一份清單處理，不是帶太多，就是漏掉真正重要的細節。這個 hub 把戶外與旅行文章整理成一套出門前可檢查的順序。",
            "Elite Fashion 編輯團隊建議先分辨移動型態，再決定裝備。城市與通勤延伸行程重視鞋子、包包、雨具、行動電源與外套；登山與戶外重視路線、天氣、補水、防曬、保暖、照明與撤退計畫；長途飛行重視頸枕、耳塞、壓縮收納、睡眠節奏與抵達後恢復；拍攝或內容工作則要考慮手機、相機、備用電力、儲存與重量。裝備不是越專業越好，而是要符合你實際會走的路。",
            "安全感來自準備順序，而不是購買數量。出門前可以先確認四件事：目的地與天氣、交通與返回方式、身體狀態與同行者需求、必要用品與備案。若其中一件不清楚，就不適合只靠購物補足。特別是登山、露營、水邊活動或長途移動，裝備只能降低部分風險，不能替代路線判斷、時間管理與天候評估。",
            "台灣旅行與戶外情境很常遇到濕氣、午後雷陣雨、山區溫差、捷運與客運轉乘、狹小住宿空間、以及臨時改變行程。這些因素會影響鞋、外套、背包、收納袋、補水與電子設備的選擇。比起追求最完整清單，更實用的是建立一個可以依天氣和行程調整的模組：城市日用包、戶外半日包、過夜收納、機上睡眠包與拍攝補給包。每個模組只保留真正會使用的物品。",
            "旅行中的形象感，也不必和機能對立。好看的外套、舒適的鞋、整齊的收納與可快速整理的盥洗小包，都能讓移動變得更從容。關鍵是不要讓單品只服務照片，而要服務整段行程。若一件外套只能在拍照時好看，不能處理溫差與收納；若一雙鞋只適合室內，不能應付走路距離；若一個包沒有安全分層，再漂亮都可能在旅行中增加麻煩。",
            "閱讀這個主題頁時，可以先從即將發生的行程切入。週末出門看戶外與城市散步；準備長途飛行看機上睡眠與恢復；想提升旅行影像品質再看手機、相機與配件；要走山或露營則先看安全與路線。出門準備的核心不是把生活搬出去，而是知道哪些物品能讓你在陌生環境裡保持節奏。行李越清楚，旅途中越能把注意力留給風景、同行的人與自己的狀態。",
            "回家後也算旅程的一部分。濕衣物、鞋底、充電線、相機記憶卡、未用完的補給與盥洗用品，都需要有收尾位置。若每次旅行後都能快速清潔、補貨與歸位，下一次出門就不必重新整理一切；這種輕盈感，才是長期旅行生活真正值得追求的品質。",
        ],
        "links": [
            ("戶外生活分類總覽", "outdoor-escapes.html"),
            ("Horizon X 太空旅行頸枕", "outdoor-escapes/horizon-x-space-travel-neck-pillow.html"),
            ("豪華健行與戶外裝備", "outdoor-escapes/luxury-hiking.html"),
            ("台灣登山與路線準備", "outdoor-escapes/taiwan-hiking.html"),
            ("戶外裝備指南", "outdoor-escapes/gear-guide.html"),
            ("iPhone 與相機旅行拍攝", "outdoor-escapes/sony-vs-iphone.html"),
            ("全球數位遊牧城市", "lifestyle-culture/global-digital-nomad-hubs-2026.html"),
            ("精品旅宿與旅行美學", "lifestyle-culture/luxury-boutique-hotels.html"),
            ("冷泡茶與午後旅行補給", "lifestyle-culture/cold-brew-tea-gift-box-afternoon-guide.html"),
            ("親子出遊餐具與包袋", "lifestyle-culture/parent-child-outing-tableware-oral-care-maternity-bag.html"),
        ],
        "faq": [
            ("旅行準備最容易漏掉什麼？", "最容易漏掉的是返回方式、天氣備案、抵達後恢復，以及用品回家後的清潔收納。"),
            ("戶外裝備需要一次買齊嗎？", "不需要。先依行程風險與頻率補基本用品，再逐步升級常用裝備。"),
            ("拍攝設備和行李重量怎麼取捨？", "先確認這趟旅行的主要目的。如果不是拍攝任務，手機、穩定電力與簡單收納通常比多帶設備更實用。"),
        ],
    },
]


for hub in HUBS:
    hub["key"] = extensionless_path(hub["file"])
    hub["links"] = CORE_HUB_LINKS.get(hub["key"], hub["links"])[:12]


def render_nav(active: str = "") -> str:
    items = [
        ("首頁", "index.html"),
        ("人工智能", "ai-innovation.html"),
        ("秀場趨勢", "runway-trends.html"),
        ("設計師視角", "designer-perspective.html"),
        ("休閒時尚", "casual-chic.html"),
        ("健康恢復", "wellness-movement.html"),
        ("戶外生活", "outdoor-escapes.html"),
        ("生活品味", "lifestyle-culture.html"),
        ("搜尋", "search.html"),
        ("關於我們", "about.html"),
    ]
    links = "\n".join(
        f'                <li><a href="{("/" if url == "index.html" else extensionless_path(url))}"{" class=\"active\"" if url == active else ""}>{label}</a></li>'
        for label, url in items
    )
    return f"""    <nav class="navbar" role="navigation" aria-label="主導覽列">
        <div class="container">
            <div class="nav-brand"><a href="/" class="logo"><img src="images/logo.jpg" alt="Elite Fashion Logo"></a></div>
            <button class="mobile-menu-toggle" aria-label="開啟選單" aria-expanded="false"><span></span><span></span><span></span></button>
            <ul class="nav-menu">
{links}
            </ul>
        </div>
    </nav>"""


def render_footer() -> str:
    return """    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <h3>ELITE FASHION</h3>
                    <p>由 Elite Fashion 編輯團隊維護，整理時尚、科技、戶外與生活品味的可靠讀物。</p>
                </div>
                <div class="footer-links">
                    <div class="footer-column">
                        <h4>探索主題</h4>
                        <ul>
                            <li><a href="ai-innovation">人工智能</a></li>
                            <li><a href="runway-trends">秀場趨勢</a></li>
                            <li><a href="designer-perspective">設計師視角</a></li>
                            <li><a href="casual-chic">休閒時尚</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>生活方式</h4>
                        <ul>
                            <li><a href="wellness-movement">健康恢復</a></li>
                            <li><a href="outdoor-escapes">戶外生活</a></li>
                            <li><a href="lifestyle-culture">生活品味</a></li>
                            <li><a href="search">站內搜尋</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>關於與聯絡</h4>
                        <ul>
                            <li><a href="about">關於我們</a></li>
                            <li><a href="editorial-policy">編輯政策與更正說明</a></li>
                            <li><a href="contact">聯絡我們</a></li>
                            <li><a href="mailto:northpathca@gmail.com">northpathca@gmail.com</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 致力於定義精英生活藍圖。</p>
                <img src="images/footer-logo.jpg" alt="Elite Fashion" class="footer-logo">
            </div>
        </div>
    </footer>"""


def render_hub_page(hub: dict[str, Any]) -> str:
    title = hub["title"]
    relative = hub["file"]
    url = canonical_url(relative)
    image = image_url(hub["image"])
    links_html = "\n".join(
        f"""                <article class="hub-link-card">
                    <a href="{extensionless_path(path)}">
                        <span>{index:02d}</span>
                        <h3>{html.escape(label)}</h3>
                    </a>
                </article>"""
        for index, (label, path) in enumerate(hub["links"], start=1)
    )
    intro_html = "\n".join(f"                <p>{html.escape(paragraph)}</p>" for paragraph in hub["intro"])
    faq_html = "\n".join(
        f"""                <details class="faq-item">
                    <summary>{html.escape(question)}</summary>
                    <p>{html.escape(answer)}</p>
                </details>"""
        for question, answer in hub["faq"]
    )
    category_label, category_page = CATEGORY_PAGES[hub["category"]]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE_URL}/#organization",
                "name": SITE_NAME,
                "url": f"{BASE_URL}/",
                "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/images/logo.jpg"},
            },
            {
                "@type": "WebSite",
                "@id": f"{BASE_URL}/#website",
                "name": SITE_NAME,
                "url": f"{BASE_URL}/",
                "inLanguage": "zh-TW",
                "publisher": {"@id": f"{BASE_URL}/#organization"},
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{BASE_URL}/search?q={{search_term_string}}",
                    "query-input": "required name=search_term_string",
                },
            },
            {
                "@type": "CollectionPage",
                "@id": f"{url}#webpage",
                "name": title,
                "description": hub["description"],
                "url": url,
                "image": image,
                "dateModified": TODAY,
                "isPartOf": {"@id": f"{BASE_URL}/#website"},
                "publisher": {"@id": f"{BASE_URL}/#organization"},
                "inLanguage": "zh-TW",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "首頁", "item": f"{BASE_URL}/"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": category_label,
                        "item": canonical_url(category_page),
                    },
                    {"@type": "ListItem", "position": 3, "name": title, "item": url},
                ],
            },
            {
                "@type": "ItemList",
                "@id": f"{url}#itemlist",
                "name": f"{title}文章路徑",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index,
                        "name": label,
                        "url": canonical_url(path),
                    }
                    for index, (label, path) in enumerate(hub["links"], start=1)
                ],
            },
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in hub["faq"]
                ],
            },
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - Elite Fashion</title>
    <meta name="description" content="{html.escape(hub['description'])}">
    <meta property="og:locale" content="zh_TW">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{html.escape(title)} - Elite Fashion">
    <meta property="og:description" content="{html.escape(hub['description'])}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(title)} - Elite Fashion">
    <meta name="twitter:description" content="{html.escape(hub['description'])}">
    <meta name="twitter:image" content="{image}">
    <link rel="canonical" href="{url}">
    <link rel="alternate" type="application/rss+xml" title="Elite Fashion RSS" href="{BASE_URL}/feed.xml">
    <link rel="icon" type="image/svg+xml" href="images/favicon/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css?v=1.4">
    <script type="application/ld+json">{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
{render_nav(CATEGORY_PAGES[hub["category"]][1])}
    <header class="page-hero cornerstone-hero">
        <div class="container">
            <p class="cornerstone-eyebrow">{html.escape(hub["eyebrow"])}</p>
            <h1 class="page-hero-title">{html.escape(title)}</h1>
            <p class="page-hero-description">{html.escape(hub["description"])}</p>
            <p class="cornerstone-updated">更新日期：{TODAY}</p>
        </div>
    </header>

    <main>
        <section class="cornerstone-intro">
            <div class="container">
                <figure class="cornerstone-share-image">
                    <img src="{html.escape(hub["image"])}" alt="{html.escape(title)}可分享圖片" loading="lazy">
                    <figcaption>分享圖片：{html.escape(title)}</figcaption>
                </figure>
                <div class="cornerstone-prose">
{intro_html}
                </div>
            </div>
        </section>

        <section class="content-section cornerstone-links">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">文章路徑</h2>
                    <p class="section-subtitle">依照現在最需要處理的任務，選一篇開始即可。</p>
                </div>
                <div class="hub-link-grid">
{links_html}
                </div>
                <p class="cornerstone-category-link"><a href="{extensionless_path(category_page)}">回到{category_label}分類總覽 →</a></p>
            </div>
        </section>

        <section class="content-section cornerstone-faq">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">FAQ</h2>
                    <p class="section-subtitle">先確認閱讀順序，再進入文章細節。</p>
                </div>
{faq_html}
            </div>
        </section>
    </main>
{render_footer()}
    <script src="js/main.js"></script>
</body>
</html>
"""


def render_editorial_policy_page() -> str:
    title = "編輯政策與更正說明"
    description = "Elite Fashion 編輯團隊的內容準則、商業揭露、來源使用、健康與選物限制，以及讀者更正回報流程。"
    url = canonical_url("editorial-policy.html")
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": f"{BASE_URL}/#organization", "name": SITE_NAME, "url": f"{BASE_URL}/"},
            {"@type": "WebSite", "@id": f"{BASE_URL}/#website", "name": SITE_NAME, "url": f"{BASE_URL}/", "inLanguage": "zh-TW"},
            {
                "@type": "WebPage",
                "@id": f"{url}#webpage",
                "name": title,
                "description": description,
                "url": url,
                "dateModified": TODAY,
                "publisher": {"@id": f"{BASE_URL}/#organization"},
                "inLanguage": "zh-TW",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "首頁", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": title, "item": url},
                ],
            },
        ],
    }
    sections = [
        ("我們如何選題", "Elite Fashion 由編輯團隊以讀者的日常決策需求為核心選題，優先處理通勤、旅行、居家、身體節奏、工作效率、風格整理與生活轉折中會反覆遇到的問題。文章必須提供可執行的判斷順序，而不是只堆疊流行詞或商品清單。"),
        ("資料與來源使用", "內容會參考公開資訊、品牌或通路頁面、專業機構說明、編輯盤點與站內既有文章。涉及價格、庫存、活動、規格與配送條件時，讀者應以下單前實際商品頁或官方公告為準。"),
        ("選物與商業揭露", "部分文章含導購連結。若讀者透過部分連結前往選購，Elite Fashion 可能取得合作收益；但文章排序、取捨與提醒仍以編輯判斷、使用情境與限制說明為主。"),
        ("健康、照護與高風險主題", "涉及睡眠、食品、護具、照護、美容成分、身體不適或運動用品時，本站只提供一般生活整理與選購順序，不宣稱療效、醫療效果、減重、保健或抗老結果。個人狀況請諮詢合格專業人員。"),
        ("更正與讀者回報", "若你發現文章有錯字、連結失效、商品資訊過時、來源不清或需要補充限制，請透過聯絡頁回報，並附上文章網址與需更正的位置。編輯團隊會依影響程度檢視並更新頁面。"),
        ("更新日期與版本", "重要內容更新會盡可能在頁面保留更新日期。若只是修正錯字、標點、圖片 alt text 或不影響判斷的小型排版，可能不另行撰寫版本紀錄。"),
    ]
    section_html = "\n".join(
        f"""                <section class="policy-section">
                    <h2>{heading}</h2>
                    <p>{body}</p>
                </section>"""
        for heading, body in sections
    )
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Elite Fashion</title>
    <meta name="description" content="{description}">
    <meta property="og:locale" content="zh_TW">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title} - Elite Fashion">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{BASE_URL}/images/og-main.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} - Elite Fashion">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{BASE_URL}/images/og-main.jpg">
    <link rel="canonical" href="{url}">
    <link rel="alternate" type="application/rss+xml" title="Elite Fashion RSS" href="{BASE_URL}/feed.xml">
    <link rel="icon" type="image/svg+xml" href="images/favicon/favicon.svg">
    <link rel="stylesheet" href="css/styles.css?v=1.4">
    <script type="application/ld+json">{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
{render_nav()}
    <header class="page-hero cornerstone-hero">
        <div class="container">
            <p class="cornerstone-eyebrow">編輯團隊說明</p>
            <h1 class="page-hero-title">{title}</h1>
            <p class="page-hero-description">{description}</p>
            <p class="cornerstone-updated">更新日期：{TODAY}</p>
        </div>
    </header>
    <main class="content-section policy-page">
        <div class="container">
{section_html}
            <p class="cornerstone-category-link"><a href="contact">回報內容更正 →</a></p>
        </div>
    </main>
{render_footer()}
    <script src="js/main.js"></script>
</body>
</html>
"""


def write_hub_pages() -> None:
    for hub in HUBS:
        (ROOT / hub["file"]).write_text(render_hub_page(hub), encoding="utf-8")
    (ROOT / "editorial-policy.html").write_text(render_editorial_policy_page(), encoding="utf-8")


def inject_category_hub_blocks() -> None:
    by_category: dict[str, list[dict[str, Any]]] = {}
    for hub in HUBS:
        by_category.setdefault(hub["category"], []).append(hub)
    for category_key, hubs in by_category.items():
        _, category_page = CATEGORY_PAGES[category_key]
        path = ROOT / category_page
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        content = re.sub(
            r"\s*<!-- SEO-HUBS:START -->.*?<!-- SEO-HUBS:END -->",
            "",
            content,
            flags=re.I | re.S,
        )
        cards = "\n".join(
            f"""                <article class="article-card">
                    <a href="{extensionless_path(hub['file'])}" class="article-link">
                        <div class="article-image"><img src="{hub['image']}" alt="{html.escape(hub['title'])}主題圖片" loading="lazy"></div>
                        <div class="article-content">
                            <div class="article-meta"><span>Cornerstone Hub</span><span>更新日期：{TODAY}</span></div>
                            <h3 class="article-title">{html.escape(hub['title'])}</h3>
                            <p class="article-excerpt">{html.escape(hub['description'])}</p>
                            <span class="read-more-link">進入主題 →</span>
                        </div>
                    </a>
                </article>"""
            for hub in hubs
        )
        block = f"""
    <!-- SEO-HUBS:START -->
    <section class="content-section cornerstone-category-entry">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">主題深讀入口</h2>
                <p class="section-subtitle">先從完整策展頁掌握順序，再進入單篇文章。</p>
            </div>
            <div class="content-grid">
{cards}
            </div>
        </div>
    </section>
    <!-- SEO-HUBS:END -->
"""
        marker = '<section class="content-section">'
        if marker in content:
            content = content.replace(marker, block + "\n" + marker, 1)
        else:
            content = content.replace("</main>", block + "\n</main>", 1)
        path.write_text(content, encoding="utf-8")


def inject_category_archives() -> None:
    index_payload = load_json(ROOT / "data" / "articles-index.json", {"items": []})
    grouped: dict[str, list[dict[str, Any]]] = {key: [] for key in CATEGORY_PAGES}
    for item in index_payload.get("items", []):
        category = item.get("category")
        if category in grouped:
            grouped[category].append(item)
    for category_key, items in grouped.items():
        _, category_page = CATEGORY_PAGES[category_key]
        path = ROOT / category_page
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        content = re.sub(
            r"\s*<!-- SEO-CATEGORY-ARCHIVE:START -->.*?<!-- SEO-CATEGORY-ARCHIVE:END -->",
            "",
            content,
            flags=re.I | re.S,
        )
        links = "\n".join(
            f"""                    <li>
                        <a href="{extensionless_path(item.get('file') or item.get('relativeUrl') or '')}">
                            <span>{html.escape(' · '.join(part for part in [item.get('categoryLabel'), item.get('topicCategoryLabel')] if part))}</span>
                            {html.escape(item.get('title') or item.get('listingTitle') or 'Elite Fashion 文章')}
                        </a>
                    </li>"""
            for item in items
        )
        block = f"""
    <!-- SEO-CATEGORY-ARCHIVE:START -->
    <section class="content-section category-archive-section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">本分類完整文章索引</h2>
                <p class="section-subtitle">依更新時間整理，方便從主題分類頁直接進入所有相關文章。</p>
            </div>
            <ul class="category-archive-list">
{links}
            </ul>
        </div>
    </section>
    <!-- SEO-CATEGORY-ARCHIVE:END -->
"""
        footer_pos = content.find('<footer class="footer">')
        if footer_pos != -1:
            content = content[:footer_pos] + block + "\n" + content[footer_pos:]
        else:
            content = content.replace("</body>", block + "\n</body>", 1)
        path.write_text(content, encoding="utf-8")


def inject_article_cluster_links() -> None:
    index_payload = load_json(ROOT / "data" / "articles-index.json", {"items": []})
    for item in index_payload.get("items", []):
        record = enrich_article_record(dict(item))
        relative = record.get("file") or record.get("relativeUrl") or ""
        path = ROOT / str(relative)
        if not relative or not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        content = re.sub(
            r"\s*<!-- SEO-CLUSTER:START -->.*?<!-- SEO-CLUSTER:END -->",
            "",
            content,
            flags=re.I | re.S,
        )
        primary = record.get("primaryHub") or {}
        secondary = record.get("secondaryHubs") or []
        category_key = record.get("category")
        category_label, category_page = CATEGORY_PAGES.get(
            category_key,
            (record.get("categoryLabel") or "文章", "all-articles.html"),
        )
        core_links = CORE_HUB_LINKS.get(primary.get("key"), [])
        related_core = [
            (label, link_path)
            for label, link_path in core_links
            if link_path != relative and (ROOT / link_path).exists()
        ][:2]
        related_core_links = "\n".join(
            f'                <li><a href="/{extensionless_path(link_path)}">{html.escape(label)}</a></li>'
            for label, link_path in related_core
        )
        secondary_links = "\n".join(
            f'                <li><a href="{html.escape(hub["url"])}">{html.escape(hub["title"])}</a></li>'
            for hub in secondary
            if isinstance(hub, dict) and hub.get("url") and hub.get("title")
        )
        secondary_block = (
            f"""
            <h3>延伸主題</h3>
            <ul>
{secondary_links}
            </ul>"""
            if secondary_links
            else ""
        )
        block = f"""
        <!-- SEO-CLUSTER:START -->
        <section class="article-related seo-cluster-links" aria-label="主題延伸閱讀">
            <h2>主題延伸閱讀</h2>
            <p>這篇文章歸入 <a href="{html.escape(primary.get('url', '/all-articles'))}">{html.escape(primary.get('title', 'Elite Fashion 主題策展'))}</a>，可從同一條閱讀路徑繼續延伸。</p>
            <ul>
                <li><a href="{html.escape(primary.get('url', '/all-articles'))}">回到{html.escape(primary.get('title', 'Elite Fashion 主題策展'))}</a></li>
{related_core_links}
                <li><a href="/{extensionless_path(category_page)}">瀏覽更多{html.escape(category_label)}文章</a></li>
            </ul>{secondary_block}
        </section>
        <!-- SEO-CLUSTER:END -->
"""
        if "</main>" in content:
            content = content.replace("</main>", block + "\n    </main>", 1)
        elif '<footer class="footer">' in content:
            content = content.replace('<footer class="footer">', block + "\n    <footer class=\"footer\">", 1)
        path.write_text(content, encoding="utf-8")


def add_editorial_policy_to_footers() -> None:
    for page_path in ROOT.rglob("*.html"):
        if page_path.name in EXCLUDED_HTML:
            continue
        content = page_path.read_text(encoding="utf-8", errors="ignore")
        if "editorial-policy" in content:
            continue
        prefix = "../" if page_path.parent != ROOT else ""
        link = f'<li><a href="{prefix}editorial-policy">編輯政策與更正說明</a></li>'
        if "contact.html" in content:
            content = content.replace('<li><a href="contact.html">聯絡我們</a></li>', f"{link}\n                            <li><a href=\"contact.html\">聯絡我們</a></li>")
            content = content.replace('<li><a href="../contact.html">聯絡我們</a></li>', f"{link}\n                <li><a href=\"../contact.html\">聯絡我們</a></li>")
        elif "contact" in content and "<footer" in content:
            content = content.replace("</ul>", f"                            {link}\n                        </ul>", 1)
        page_path.write_text(content, encoding="utf-8")


def iter_indexable_html() -> list[Path]:
    pages = []
    for path in ROOT.rglob("*.html"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        if path.name in EXCLUDED_HTML:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        if has_noindex(content):
            continue
        pages.append(path)
    return sorted(pages, key=lambda item: rel_path(item))


def iter_maintainable_html() -> list[Path]:
    pages = []
    for path in ROOT.rglob("*.html"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        if path.name in EXCLUDED_HTML:
            continue
        pages.append(path)
    return sorted(pages, key=lambda item: rel_path(item))


def update_all_html() -> None:
    for page_path in iter_maintainable_html():
        content = page_path.read_text(encoding="utf-8")
        updated = upsert_head_seo(page_path, content)
        page_path.write_text(updated, encoding="utf-8")


def build_sitemap() -> None:
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for page_path in iter_indexable_html():
        relative = rel_path(page_path)
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = canonical_url(relative)
        lastmod = datetime.fromtimestamp(page_path.stat().st_mtime, tz=timezone.utc).date().isoformat()
        ET.SubElement(url, "lastmod").text = lastmod
        priority = "1.0" if page_path.name == "index.html" else "0.8" if page_path.parent == ROOT else "0.6"
        changefreq = "weekly" if page_path.parent == ROOT else "monthly"
        ET.SubElement(url, "changefreq").text = changefreq
        ET.SubElement(url, "priority").text = priority
    raw = ET.tostring(urlset, encoding="utf-8")
    pretty = minidom.parseString(raw).toprettyxml(indent="  ")
    (ROOT / "sitemap.xml").write_text(pretty, encoding="utf-8")


def build_feed() -> None:
    index = load_json(ROOT / "data" / "articles-index.json", {"items": []})
    items = index.get("items", [])[:50]
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = SITE_NAME
    ET.SubElement(channel, "link").text = f"{BASE_URL}/"
    ET.SubElement(channel, "description").text = "Elite Fashion 最新文章與主題策展"
    ET.SubElement(channel, "language").text = "zh-TW"
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(datetime.now(timezone.utc), usegmt=True)
    for record in items:
        item = ET.SubElement(channel, "item")
        relative = record.get("relativeUrl") or record.get("file") or ""
        if not relative:
            relative = re.sub(rf"^{re.escape(BASE_URL)}/", "", record.get("url", ""))
        url = canonical_url(relative)
        ET.SubElement(item, "title").text = record.get("title") or record.get("listingTitle") or "Elite Fashion 文章"
        ET.SubElement(item, "link").text = url
        ET.SubElement(item, "guid", isPermaLink="true").text = url
        ET.SubElement(item, "description").text = record.get("excerpt") or record.get("metaDescription") or ""
        published_date = format_date_from_iso(record.get("publishedAt", ""))
        dt = datetime.fromisoformat(f"{published_date}T00:00:00+00:00")
        ET.SubElement(item, "pubDate").text = format_datetime(dt, usegmt=True)
        ET.SubElement(item, "category").text = record.get("categoryLabel") or record.get("category") or "文章"
    raw = ET.tostring(rss, encoding="utf-8")
    pretty = minidom.parseString(raw).toprettyxml(indent="  ")
    (ROOT / "feed.xml").write_text(pretty, encoding="utf-8")
    shutil.copyfile(ROOT / "feed.xml", ROOT / "rss.xml")


def main() -> None:
    write_hub_pages()
    inject_category_hub_blocks()
    inject_category_archives()
    inject_article_cluster_links()
    add_editorial_policy_to_footers()
    update_all_html()
    build_sitemap()
    build_feed()
    print("SEO site maintenance complete.")


if __name__ == "__main__":
    main()
