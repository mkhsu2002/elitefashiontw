#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import http.client
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "automation" / "site-config.json"
TOP_LEVEL_NON_ARTICLE_PAGES = {
    "404.html",
    "about.html",
    "all-articles.html",
    "ai-innovation.html",
    "casual-chic.html",
    "contact.html",
    "designer-perspective.html",
    "high-performance.html",
    "index.html",
    "lifestyle-culture.html",
    "outdoor-escapes.html",
    "runway-trends.html",
    "search.html",
    "wellness-movement.html",
}
SPECIAL_ARTICLE_CATEGORY_MAP = {
    "crossbody-bag-style-guide.html": "casual-chic",
    "yoga-complete.html": "wellness-movement",
}
LEGACY_CATEGORY_LABELS = {
    "high-performance": "高效人生",
    "life-proposals": "人生提案",
    "special-features": "特輯",
}
MARKER_PREFIX = "AUTO-GENERATED"
CURATED_CATEGORY_IMAGE_POOLS = {
    "ai-innovation": [
        "images/generated/ai/creative-sovereignty.png",
        "images/generated/ai/customization.png",
        "images/generated/ai/ethics.png",
        "images/generated/ai/health-longevity.png",
        "images/generated/ai/outdoor-gear.png",
        "images/generated/ai/pet-care.png",
        "images/generated/ai/prediction.png",
        "images/generated/ai/saas-entrepreneur.png",
        "images/generated/ai/smart-home.png",
        "images/generated/ai/supply-chain.png",
        "images/generated/ai/systeme-promo.png",
        "images/generated/ai/virtual-idols.png",
        "images/generated/ai/wealth-fintech.png",
    ],
    "runway-trends": [
        "images/generated/runway/ai-couture-2026.png",
        "images/generated/runway/asymmetric.png",
        "images/generated/runway/color-trends.png",
        "images/generated/runway/digital-fabrics.png",
        "images/generated/runway/nft-fashion.png",
        "images/generated/runway/vintage-stocks.png",
    ],
    "designer-perspective": [
        "images/generated/designer/ai-design.png",
        "images/generated/designer/craftsmanship.png",
        "images/generated/designer/emotional-tailoring.png",
        "images/generated/designer/fashion-photography.png",
        "images/generated/designer/ipad-wacom.png",
        "images/generated/designer/masterclass-domestika.png",
        "images/generated/designer/stylist-power.png",
        "images/generated/designer/sustainability-pioneer.png",
    ],
    "casual-chic": [
        "images/generated/casual/capsule-wardrobe.png",
        "images/generated/casual/capsule.png",
        "images/generated/casual/denim.png",
        "images/generated/casual/office.png",
        "images/generated/casual/travel-wear.png",
    ],
    "wellness-movement": [
        "images/generated/wellness-1.png",
        "images/generated/wellness/ag1-huel.png",
        "images/generated/wellness/holographic.png",
        "images/generated/wellness/light-wear.png",
        "images/generated/wellness/neuro-yoga.png",
        "images/generated/wellness/recovery-tech.png",
    ],
    "outdoor-escapes": [
        "images/generated/outdoor-1.png",
        "images/generated/outdoor/gear-guide.png",
        "images/generated/outdoor/luxury-hiking.png",
        "images/generated/outdoor/sony-vs-iphone.png",
        "images/generated/outdoor/taiwan-hiking.png",
    ],
    "lifestyle-culture": [
        "images/generated/fashion-1.png",
        "images/generated/lifestyle/home-sanctuary.png",
        "images/generated/lifestyle/boutique-hotels.png",
        "images/generated/lifestyle/nomad.png",
        "images/generated/lifestyle/notion-obsidian.png",
        "images/generated/lifestyle/life-sovereignty.jpg",
        "images/generated/life-proposals/gray-divorce-new-chapter.png",
        "images/generated/life-proposals/finding-yourself-after-40.png",
        "images/generated/life-proposals/finding-your-tribe-midlife.png",
        "images/generated/life-proposals/social-energy-management.png",
        "images/generated/life-proposals/financial-independence-options.png",
        "images/generated/life-proposals/career-pivot-start-over.png",
        "images/generated/life-proposals/friendship-audit-outgrow.png",
    ],
}
ASSET_IDENTITY_CACHE: dict[str, str] = {}


@dataclass
class CategoryConfig:
    key: str
    label: str
    page: str
    directory: str
    cta_url: str
    placeholder_image: str


class PipelineError(RuntimeError):
    pass


def load_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        if default is None:
            raise FileNotFoundError(path)
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(text)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now_utc().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def iso_to_display(iso_value: str) -> str:
    if not iso_value:
        return ""
    raw = iso_value.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return iso_value
    return f"{dt.year}年{dt.month}月{dt.day}日"


def slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[「」『』（）()，、。！？：:／/]+", "-", normalized)
    normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    if not normalized:
        normalized = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
    ascii_candidate = re.sub(r"[^\x00-\x7F]+", "-", normalized)
    ascii_candidate = re.sub(r"-{2,}", "-", ascii_candidate).strip("-")
    return ascii_candidate or normalized[:60]


def strip_tags(content: str) -> str:
    content = re.sub(r"<script.*?</script>", "", content, flags=re.S | re.I)
    content = re.sub(r"<style.*?</style>", "", content, flags=re.S | re.I)
    content = re.sub(r"<[^>]+>", " ", content)
    content = html.unescape(content)
    return re.sub(r"\s+", " ", content).strip()


def extract_meta(content: str, key: str, *, property_mode: bool = False) -> str:
    attr = "property" if property_mode else "name"
    match = re.search(
        rf'<meta[^>]+{attr}="{re.escape(key)}"[^>]+content="([^"]*)"',
        content,
        flags=re.I,
    )
    return html.unescape(match.group(1)).strip() if match else ""


def extract_title_from_html(content: str) -> str:
    for pattern in [
        r'<h1[^>]*class="article-title"[^>]*>(.*?)</h1>',
        r"<h1[^>]*>(.*?)</h1>",
        r"<title>(.*?)</title>",
    ]:
        match = re.search(pattern, content, flags=re.S | re.I)
        if match:
            title = strip_tags(match.group(1))
            title = re.sub(r"\s+\|\s+Elite Fashion.*$", "", title)
            return title
    return ""


def extract_first_paragraph(content: str) -> str:
    match = re.search(r"<p[^>]*>(.*?)</p>", content, flags=re.S | re.I)
    return strip_tags(match.group(1)) if match else ""


def normalize_for_similarity(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\d{4}", "", value)
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", value)
    return value


def similarity_score(left: str, right: str) -> float:
    left_norm = normalize_for_similarity(left)
    right_norm = normalize_for_similarity(right)
    if not left_norm or not right_norm:
        return 0.0
    if left_norm == right_norm:
        return 1.0
    left_tokens = {left_norm[i : i + 2] for i in range(max(1, len(left_norm) - 1))}
    right_tokens = {right_norm[i : i + 2] for i in range(max(1, len(right_norm) - 1))}
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def is_duplicate_title(candidate: str, existing_titles: list[str], threshold: float = 0.72) -> bool:
    return any(similarity_score(candidate, title) >= threshold for title in existing_titles)


def relative_to_root(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def path_to_url(base_url: str, relative_path: str) -> str:
    return f"{base_url.rstrip('/')}/{relative_path.lstrip('/')}"


def url_to_relative(url_or_path: str) -> str:
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        parsed = urllib.parse.urlparse(url_or_path)
        return parsed.path.lstrip("/")
    return url_or_path.lstrip("/")


def normalize_site_asset_path(asset: str, base_url: str) -> str:
    if not asset:
        return ""
    if asset.startswith(base_url):
        return url_to_relative(asset)
    if asset.startswith("https://mkhsu2002.github.io/elitefashiontw/"):
        return asset.replace("https://mkhsu2002.github.io/elitefashiontw/", "")
    if asset.startswith("http://mkhsu2002.github.io/elitefashiontw/"):
        return asset.replace("http://mkhsu2002.github.io/elitefashiontw/", "")
    return asset


def normalize_external_url(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    if value.startswith(("http://", "https://")):
        return value
    return f"https://{value.lstrip('/')}"


def asset_exists(asset: str) -> bool:
    if not asset:
        return False
    if asset.startswith("http://") or asset.startswith("https://"):
        return True
    return (ROOT / asset.lstrip("/")).exists()


def asset_identity(asset: str) -> str:
    normalized = asset.lstrip("/")
    if not normalized:
        return ""
    if normalized.startswith(("http://", "https://")):
        return f"url:{normalized}"
    cached = ASSET_IDENTITY_CACHE.get(normalized)
    if cached:
        return cached
    path = ROOT / normalized
    if not path.exists():
        identity = f"path:{normalized}"
    else:
        identity = f"sha1:{hashlib.sha1(path.read_bytes()).hexdigest()}"
    ASSET_IDENTITY_CACHE[normalized] = identity
    return identity


def build_category_image_pool(category: CategoryConfig) -> list[str]:
    seen: set[str] = set()
    pool: list[str] = []
    for candidate in [category.placeholder_image, *CURATED_CATEGORY_IMAGE_POOLS.get(category.key, [])]:
        normalized = candidate.lstrip("/")
        identity = asset_identity(normalized)
        if not normalized or not identity or identity in seen or not asset_exists(normalized):
            continue
        seen.add(identity)
        pool.append(normalized)
    return pool


def hero_repeat_score(candidate: str, registry: list[dict[str, Any]], category_key: str) -> int:
    candidate_id = asset_identity(candidate)
    all_global = [asset_identity(item.get("heroImage", "").lstrip("/")) for item in registry if item.get("heroImage")]
    all_category = [
        asset_identity(item.get("heroImage", "").lstrip("/"))
        for item in registry
        if item.get("category") == category_key and item.get("heroImage")
    ]
    global_recent = [asset_identity(item.get("heroImage", "").lstrip("/")) for item in registry[:8] if item.get("heroImage")]
    category_recent = [
        asset_identity(item.get("heroImage", "").lstrip("/"))
        for item in registry
        if item.get("category") == category_key and item.get("heroImage")
    ][:6]
    score = all_global.count(candidate_id) * 4 + all_category.count(candidate_id) * 10
    score += global_recent.count(candidate_id) * 70 + category_recent.count(candidate_id) * 120
    if category_recent and candidate_id == category_recent[0]:
        score += 240
    if candidate_id in category_recent[:3]:
        score += 120
    if global_recent and candidate_id == global_recent[0]:
        score += 90
    return score


def recent_hero_blocklist(registry: list[dict[str, Any]], category_key: str) -> set[str]:
    global_recent = [asset_identity(item.get("heroImage", "").lstrip("/")) for item in registry[:3] if item.get("heroImage")]
    category_recent = [
        asset_identity(item.get("heroImage", "").lstrip("/"))
        for item in registry
        if item.get("category") == category_key and item.get("heroImage")
    ][:4]
    return {item for item in [*global_recent, *category_recent] if item}


def choose_balanced_hero_image(
    article: dict[str, Any],
    registry: list[dict[str, Any]],
    config: dict[str, Any],
    categories: dict[str, CategoryConfig],
) -> str:
    category = categories.get(article["category"])
    if not category:
        return article.get("heroImage", "")

    pool = build_category_image_pool(category)
    candidate = normalize_site_asset_path(article.get("heroImage", ""), config["baseUrl"]).lstrip("/")
    candidate_valid = asset_exists(candidate)
    blocked_recent = recent_hero_blocklist(registry, category.key)
    candidate_id = asset_identity(candidate)

    ranked_pool = [item for item in pool if asset_identity(item) not in blocked_recent] or pool

    if candidate_valid and candidate.startswith("http"):
        if candidate_id not in blocked_recent or not ranked_pool:
            return candidate
        return min(ranked_pool, key=lambda item: (hero_repeat_score(item, registry, category.key), item))

    if ranked_pool:
        best_pool_image = min(ranked_pool, key=lambda item: (hero_repeat_score(item, registry, category.key), item))
        best_score = hero_repeat_score(best_pool_image, registry, category.key)
        if not candidate_valid:
            return best_pool_image
        if candidate_id in blocked_recent and asset_identity(best_pool_image) != candidate_id:
            return best_pool_image
        candidate_score = hero_repeat_score(candidate, registry, category.key)
        if any(asset_identity(item) == candidate_id for item in ranked_pool) and candidate_score <= best_score:
            return candidate
        if candidate_score <= best_score and candidate_valid and candidate_id not in blocked_recent:
            return candidate
        return best_pool_image

    return candidate if candidate_valid else category.placeholder_image


def load_config() -> tuple[dict[str, Any], dict[str, CategoryConfig]]:
    config = load_json(CONFIG_PATH)
    categories = {
        entry["key"]: CategoryConfig(
            key=entry["key"],
            label=entry["label"],
            page=entry["page"],
            directory=entry["directory"],
            cta_url=entry["ctaUrl"],
            placeholder_image=entry["placeholderImage"],
        )
        for entry in config["categories"]
    }
    return config, categories


def detect_category(path: Path, categories: dict[str, CategoryConfig]) -> tuple[str, str]:
    if path.parent != ROOT:
        key = path.parent.name
        if key in categories:
            return key, categories[key].label
        return key, LEGACY_CATEGORY_LABELS.get(key, key.replace("-", " ").title())
    mapped = SPECIAL_ARTICLE_CATEGORY_MAP.get(path.name)
    if mapped and mapped in categories:
        return mapped, categories[mapped].label
    return "special-features", LEGACY_CATEGORY_LABELS["special-features"]


def estimate_read_time(content: str) -> int:
    cleaned = strip_tags(content)
    char_count = len(cleaned.replace(" ", ""))
    return max(4, round(char_count / 380))


def scan_legacy_articles(config: dict[str, Any], categories: dict[str, CategoryConfig]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    base_url = config["baseUrl"]
    for html_path in sorted(ROOT.rglob("*.html")):
        rel_path = relative_to_root(html_path)
        if rel_path.startswith(".git/"):
            continue
        if html_path.name in TOP_LEVEL_NON_ARTICLE_PAGES:
            continue
        content = html_path.read_text(encoding="utf-8")
        category_key, category_label = detect_category(html_path, categories)
        title = extract_title_from_html(content)
        description = extract_meta(content, "description") or extract_first_paragraph(content)
        meta_title = re.sub(r"\s+\|\s+Elite Fashion.*$", "", extract_title_from_html(content)) or title
        keywords = extract_meta(content, "keywords")
        tags = [item.strip() for item in keywords.split(",") if item.strip()]
        published = extract_meta(content, "article:published_time", property_mode=True)
        if not published:
            published = datetime.fromtimestamp(html_path.stat().st_mtime, tz=timezone.utc).replace(
                microsecond=0
            ).isoformat().replace("+00:00", "Z")
        hero_image = (
            extract_meta(content, "og:image", property_mode=True)
            or extract_meta(content, "twitter:image")
            or ""
        )
        hero_image = normalize_site_asset_path(hero_image, config["baseUrl"])
        listing_title = title
        listing_excerpt = description[:140]
        article_url = path_to_url(base_url, rel_path)
        record = {
            "id": f"legacy-{slugify(rel_path)}",
            "title": title,
            "slug": html_path.stem,
            "excerpt": description,
            "tags": tags,
            "metaTitle": meta_title[:80],
            "metaDescription": description[:180],
            "category": category_key,
            "categoryLabel": category_label,
            "series": category_label,
            "audience": "",
            "readTimeMinutes": estimate_read_time(content),
            "listingTitle": listing_title,
            "listingExcerpt": listing_excerpt,
            "markdownBody": "",
            "faq": [],
            "extendedReading": [],
            "cta": {
                "label": "瀏覽更多文章",
                "url": "/all-articles.html",
                "text": "繼續探索 Elite Fashion 的其他文章。",
            },
            "publishedAt": published,
            "publishedDateText": iso_to_display(published),
            "url": article_url,
            "relativeUrl": rel_path,
            "file": rel_path,
            "heroImage": hero_image,
            "sourceType": "legacy",
            "status": "published",
            "queueId": None,
        }
        records.append(record)
    return records


def load_generated_records(categories: dict[str, CategoryConfig], config: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    article_dir = ROOT / config["paths"]["generatedArticlesDir"]
    if not article_dir.exists():
        return records
    for metadata_path in sorted(article_dir.glob("*.json")):
        payload = load_json(metadata_path)
        payload["sourceType"] = "generated"
        payload["status"] = payload.get("status", "published")
        payload["queueId"] = payload.get("queueId")
        payload["relativeUrl"] = url_to_relative(payload["url"])
        category_key = payload["category"]
        payload["categoryLabel"] = categories[category_key].label if category_key in categories else category_key
        records.append(payload)
    return records


def build_registry(config: dict[str, Any], categories: dict[str, CategoryConfig]) -> list[dict[str, Any]]:
    generated = {record["file"]: record for record in load_generated_records(categories, config)}
    legacy = scan_legacy_articles(config, categories)
    records: list[dict[str, Any]] = []
    for record in legacy:
        if record["file"] in generated:
            continue
        records.append(record)
    records.extend(generated.values())
    records.sort(key=lambda item: item.get("publishedAt", ""), reverse=True)
    return records


def build_existing_title_context(
    registry: list[dict[str, Any]], *, topic: str, category: str | None = None, limit: int = 60
) -> list[str]:
    prioritized: list[tuple[float, str]] = []
    seen: set[str] = set()
    for index, record in enumerate(registry):
        title = record.get("title")
        if not title or title in seen:
            continue
        seen.add(title)
        score = 0.0
        if category and record.get("category") == category:
            score += 20
        score += similarity_score(topic, title) * 100
        score += max(0, 20 - min(index, 20))
        prioritized.append((score, title))
    prioritized.sort(key=lambda item: item[0], reverse=True)
    return [title for _, title in prioritized[:limit]]


def render_markdown_body(article: dict[str, Any]) -> str:
    lines = [f"# {article['title']}", "", article["intro"], ""]
    for section in article["sections"]:
        lines.append(f"## {section['heading']}")
        lines.append("")
        for paragraph in section.get("paragraphs", []):
            lines.append(paragraph)
            lines.append("")
        for bullet in section.get("bullets", []):
            lines.append(f"- {bullet}")
        if section.get("bullets"):
            lines.append("")
    if article.get("faq"):
        lines.append("## FAQ")
        lines.append("")
        for item in article["faq"]:
            lines.append(f"### {item['question']}")
            lines.append("")
            lines.append(item["answer"])
            lines.append("")
    if article.get("extendedReading"):
        lines.append("## 延伸閱讀")
        lines.append("")
        for item in article["extendedReading"]:
            lines.append(f"- [{item['title']}]({item['url']})")
        lines.append("")
    lines.append("## CTA")
    lines.append("")
    lines.append(article["cta"]["text"])
    lines.append("")
    lines.append(f"[{article['cta']['label']}]({article['cta']['url']})")
    lines.append("")
    if article.get("disclaimer"):
        lines.append("## 重要警語")
        lines.append("")
        lines.append(article["disclaimer"])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_paragraphs(paragraphs: list[str]) -> str:
    return "\n".join(f"            <p>{html.escape(item)}</p>" for item in paragraphs)


def render_bullets(bullets: list[str]) -> str:
    if not bullets:
        return ""
    items = "\n".join(f"                <li>{html.escape(item)}</li>" for item in bullets)
    return f"""
            <ul class="article-bullets">
{items}
            </ul>"""


def render_article_html(article: dict[str, Any], config: dict[str, Any], categories: dict[str, CategoryConfig]) -> str:
    category = categories.get(article["category"])
    category_label = category.label if category else article["category"]
    faq_items = "\n".join(
        f"""
            <details class="faq-item">
                <summary>{html.escape(item['question'])}</summary>
                <p>{html.escape(item['answer'])}</p>
            </details>"""
        for item in article["faq"]
    )
    extended_items = "\n".join(
        f'                <li><a href="{html.escape(item["url"])}">{html.escape(item["title"])}</a></li>'
        for item in article["extendedReading"]
    )
    section_html = "\n".join(
        f"""
        <section class="article-section">
            <h2>{html.escape(section['heading'])}</h2>
{render_paragraphs(section.get('paragraphs', []))}
{render_bullets(section.get('bullets', []))}
        </section>"""
        for section in article["sections"]
    )
    canonical = article["url"]
    hero_image = article["heroImage"]
    hero_image_url = hero_image
    if hero_image and not hero_image.startswith("http"):
        hero_image_url = path_to_url(config["baseUrl"], hero_image)
    hero_image_tag_src = hero_image if hero_image.startswith("http") else f"../{hero_image}"
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"],
                },
            }
            for item in article["faq"]
        ],
    }
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["metaDescription"],
        "datePublished": article["publishedAt"],
        "author": {"@type": "Organization", "name": config["siteName"]},
        "publisher": {"@type": "Organization", "name": config["siteName"]},
        "mainEntityOfPage": canonical,
        "image": hero_image_url,
    }
    disclaimer_html = ""
    if article.get("disclaimer"):
        disclaimer_html = f"""
        <section class="article-cta">
            <h2>重要警語</h2>
            <p>{html.escape(article['disclaimer'])}</p>
        </section>"""
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(article['metaTitle'])} | {html.escape(config['siteName'])}</title>
    <meta name="description" content="{html.escape(article['metaDescription'])}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{html.escape(article['metaTitle'])}">
    <meta property="og:description" content="{html.escape(article['metaDescription'])}">
    <meta property="og:url" content="{html.escape(canonical)}">
    <meta property="og:image" content="{html.escape(hero_image_url)}">
    <meta property="article:published_time" content="{html.escape(article['publishedAt'])}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="{html.escape(canonical)}">
    <link rel="stylesheet" href="../css/styles.css?v=1.2">
    <link rel="icon" type="image/svg+xml" href="../images/favicon/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        .article-container {{
            max-width: 860px;
            margin: 0 auto;
            padding: 72px 20px 88px;
            line-height: 1.9;
        }}
        .article-header {{
            text-align: center;
            margin-bottom: 36px;
        }}
        .article-title {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(2.2rem, 5vw, 3.6rem);
            line-height: 1.2;
            margin-bottom: 18px;
            color: #111;
        }}
        .article-subtitle {{
            max-width: 720px;
            margin: 0 auto 24px;
            color: #555;
            font-size: 1.15rem;
        }}
        .meta-box {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 14px 22px;
            font-size: 0.95rem;
            color: #666;
            padding: 14px 0;
            border-top: 1px solid #eee;
            border-bottom: 1px solid #eee;
            margin-bottom: 28px;
        }}
        .hero-img {{
            width: 100%;
            border-radius: 16px;
            margin-bottom: 34px;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.08);
        }}
        .article-section h2, .article-faq h2, .article-related h2, .article-cta h2 {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            margin: 3.4rem 0 1.2rem;
        }}
        .article-section p, .article-faq p, .article-cta p {{
            margin-bottom: 1.2rem;
            color: #2d2d2d;
            font-size: 1.08rem;
        }}
        .article-bullets {{
            margin: 0 0 1.2rem 1.2rem;
            color: #2d2d2d;
        }}
        .article-bullets li {{
            margin-bottom: 0.7rem;
        }}
        .faq-item {{
            border: 1px solid #e7dfcf;
            border-radius: 12px;
            padding: 16px 18px;
            margin-bottom: 12px;
            background: #fcfaf6;
        }}
        .faq-item summary {{
            font-weight: 600;
            cursor: pointer;
        }}
        .article-related ul {{
            padding-left: 1.2rem;
        }}
        .article-cta {{
            margin-top: 2.8rem;
            padding: 28px;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(197,160,89,0.14), rgba(17,17,17,0.04));
        }}
        .article-cta a {{
            display: inline-block;
            margin-top: 12px;
            padding: 12px 24px;
            background: #111;
            color: #fff;
            text-decoration: none;
            border-radius: 999px;
        }}
    </style>
    <script type="application/ld+json">{json.dumps(article_schema, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
</head>
<body>
    <nav class="navbar" role="navigation" aria-label="主導覽列">
        <div class="container">
            <div class="nav-brand">
                <a href="../index.html" class="logo"><img src="../images/logo.jpg" alt="Elite Fashion Logo"></a>
            </div>
            <button class="mobile-menu-toggle" aria-label="開啟選單" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <ul class="nav-menu">
                <li><a href="../index.html">首頁</a></li>
                <li><a href="../ai-innovation.html">人工智能</a></li>
                <li><a href="../runway-trends.html">秀場趨勢</a></li>
                <li><a href="../designer-perspective.html">設計師視角</a></li>
                <li><a href="../casual-chic.html">休閒時尚</a></li>
                <li><a href="../wellness-movement.html">瑜伽健身</a></li>
                <li><a href="../outdoor-escapes.html">戶外生活</a></li>
                <li><a href="../lifestyle-culture.html">生活品味</a></li>
                <li><a href="../all-articles.html">文章列表</a></li>
                <li><a href="../contact.html">聯絡我們</a></li>
            </ul>
        </div>
    </nav>

    <main class="article-container">
        <header class="article-header">
            <div class="meta-box">
                <span>發布日期：{html.escape(article['publishedDateText'])}</span>
                <span>分類：{html.escape(category_label)}</span>
                <span>閱讀時間：約 {article['readTimeMinutes']} 分鐘</span>
            </div>
            <h1 class="article-title">{html.escape(article['title'])}</h1>
            <p class="article-subtitle">{html.escape(article['excerpt'])}</p>
        </header>

        <img src="{html.escape(hero_image_tag_src)}" alt="{html.escape(article['title'])}" class="hero-img">

        {section_html}

        <section class="article-faq">
            <h2>FAQ</h2>
            {faq_items}
        </section>

        <section class="article-related">
            <h2>延伸閱讀</h2>
            <ul>
{extended_items}
            </ul>
        </section>

        <section class="article-cta">
            <h2>下一步建議</h2>
            <p>{html.escape(article['cta']['text'])}</p>
            <a href="{html.escape(article['cta']['url'])}">{html.escape(article['cta']['label'])}</a>
        </section>
{disclaimer_html}
    </main>

    <script src="../js/main.js"></script>
</body>
</html>
"""


def render_article_card(record: dict[str, Any]) -> str:
    rel_url = record.get("relativeUrl") or url_to_relative(record["url"])
    image = record.get("heroImage") or "images/generated/fashion-1.png"
    image_src = image if image.startswith("http") else image
    meta_left = record.get("series") or record.get("categoryLabel") or "精選文章"
    meta_right = record.get("publishedDateText") or iso_to_display(record.get("publishedAt", ""))
    title = record.get("listingTitle") or record.get("title") or "Elite Fashion 文章"
    excerpt = record.get("listingExcerpt") or record.get("excerpt") or ""
    return f"""
                <article class="article-card">
                    <a href="{html.escape(rel_url)}" class="article-link">
                        <div class="article-image">
                            <img src="{html.escape(image_src)}" alt="{html.escape(title)}" loading="lazy">
                        </div>
                        <div class="article-content">
                            <div class="article-meta">
                                <span>{html.escape(meta_left)}</span>
                                <span>{html.escape(meta_right)}</span>
                            </div>
                            <h3 class="article-title">{html.escape(title)}</h3>
                            <p class="article-excerpt">{html.escape(excerpt)}</p>
                            <span class="read-more-link">閱讀全文 →</span>
                        </div>
                    </a>
                </article>"""


def render_all_articles_page(config: dict[str, Any], categories: dict[str, CategoryConfig], registry: list[dict[str, Any]]) -> str:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in registry:
        grouped.setdefault(record["category"], []).append(record)
    sections = []
    ordered_keys = [key for key in categories if key in grouped]
    ordered_keys.extend(sorted(key for key in grouped if key not in categories))
    for key in ordered_keys:
        items = grouped.get(key, [])[:60]
        if not items:
            continue
        label = categories[key].label if key in categories else items[0].get("categoryLabel", key.replace("-", " ").title())
        links = "\n".join(
            f'                        <li class="article-item"><a href="{html.escape(item["relativeUrl"])}" class="article-link">{html.escape(item["listingTitle"])} <span class="article-arrow">→</span></a></li>'
            for item in items
        )
        sections.append(
            f"""
                    <section class="category-section" id="{html.escape(key)}">
                        <h2 class="category-title">{html.escape(label)}</h2>
                        <ul class="article-list">
{links}
                        </ul>
                    </section>"""
        )
    search_path = "search.html"
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>所有文章列表 | {html.escape(config['siteName'])}</title>
    <meta name="description" content="瀏覽 Elite Fashion 全站文章、系列主題與最新自動化內容更新。">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{html.escape(path_to_url(config['baseUrl'], 'all-articles.html'))}">
    <meta property="og:title" content="所有文章列表 | {html.escape(config['siteName'])}">
    <meta property="og:description" content="用分類與搜尋快速找到站內所有文章。">
    <link rel="canonical" href="{html.escape(path_to_url(config['baseUrl'], 'all-articles.html'))}">
    <link rel="stylesheet" href="css/styles.css?v=1.2">
    <link rel="icon" type="image/svg+xml" href="images/favicon/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        .page-header {{
            padding: 8rem 0 4rem;
            background: linear-gradient(180deg, #f8f5ef, #fff);
            text-align: center;
        }}
        .page-title {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(2.4rem, 4vw, 3.2rem);
            margin-bottom: 1rem;
        }}
        .page-subtitle {{
            max-width: 720px;
            margin: 0 auto 1.4rem;
            color: #555;
        }}
        .page-actions a {{
            display: inline-block;
            padding: 12px 22px;
            border-radius: 999px;
            background: #111;
            color: #fff;
            text-decoration: none;
        }}
        .articles-container {{
            padding: 4rem 0 5rem;
            max-width: 1040px;
            margin: 0 auto;
        }}
        .category-section {{
            margin-bottom: 3rem;
        }}
        .category-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            display: inline-block;
            margin-bottom: 1.4rem;
            border-bottom: 2px solid #C5A059;
            padding-bottom: 0.4rem;
        }}
        .article-list {{
            list-style: none;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
        }}
        .article-item {{
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06);
        }}
        .article-link {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            padding: 1.2rem 1.3rem;
            color: #222;
            text-decoration: none;
        }}
        .article-arrow {{
            color: #C5A059;
        }}
    </style>
</head>
<body>
    <nav class="navbar" role="navigation" aria-label="主導覽列">
        <div class="container">
            <div class="nav-brand">
                <a href="index.html" class="logo"><img src="images/logo.jpg" alt="Elite Fashion Logo"></a>
            </div>
            <button class="mobile-menu-toggle" aria-label="開啟選單" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <ul class="nav-menu">
                <li><a href="index.html">首頁</a></li>
                <li><a href="ai-innovation.html">人工智能</a></li>
                <li><a href="runway-trends.html">秀場趨勢</a></li>
                <li><a href="designer-perspective.html">設計師視角</a></li>
                <li><a href="casual-chic.html">休閒時尚</a></li>
                <li><a href="wellness-movement.html">瑜伽健身</a></li>
                <li><a href="outdoor-escapes.html">戶外生活</a></li>
                <li><a href="lifestyle-culture.html">生活品味</a></li>
                <li><a href="all-articles.html" class="active">文章列表</a></li>
                <li><a href="contact.html">聯絡我們</a></li>
            </ul>
        </div>
    </nav>

    <header class="page-header">
        <div class="container">
            <h1 class="page-title">所有文章列表</h1>
            <p class="page-subtitle">站內所有文章都會從同一份索引同步到這裡。若你想快速找主題，可直接使用站內搜尋。</p>
            <div class="page-actions"><a href="{search_path}">前往搜尋頁</a></div>
        </div>
    </header>

    <main class="container">
        <div class="articles-container">
{''.join(sections)}
        </div>
    </main>

    <script src="js/main.js"></script>
</body>
</html>
"""


def render_search_page(config: dict[str, Any]) -> str:
    search_index_url = "data/search-index.json"
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>站內搜尋 | {html.escape(config['siteName'])}</title>
    <meta name="description" content="搜尋 Elite Fashion 站內文章、FAQ 與系列主題。">
    <link rel="canonical" href="{html.escape(path_to_url(config['baseUrl'], 'search.html'))}">
    <link rel="stylesheet" href="css/styles.css?v=1.2">
    <link rel="icon" type="image/svg+xml" href="images/favicon/favicon.svg">
    <style>
        .search-shell {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 8rem 20px 4rem;
        }}
        .search-input {{
            width: 100%;
            padding: 16px 18px;
            border: 1px solid #d8d1c5;
            border-radius: 14px;
            font-size: 1rem;
        }}
        .search-results {{
            margin-top: 2rem;
            display: grid;
            gap: 1rem;
        }}
        .search-card {{
            padding: 1.4rem;
            border: 1px solid #eee;
            border-radius: 16px;
            background: #fff;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.04);
        }}
        .search-card a {{
            color: #111;
            text-decoration: none;
        }}
        .search-meta {{
            color: #666;
            font-size: 0.94rem;
            margin-bottom: 0.5rem;
        }}
        .search-empty {{
            color: #666;
        }}
    </style>
</head>
<body>
    <nav class="navbar" role="navigation" aria-label="主導覽列">
        <div class="container">
            <div class="nav-brand"><a href="index.html" class="logo"><img src="images/logo.jpg" alt="Elite Fashion Logo"></a></div>
            <button class="mobile-menu-toggle" aria-label="開啟選單" aria-expanded="false"><span></span><span></span><span></span></button>
            <ul class="nav-menu">
                <li><a href="index.html">首頁</a></li>
                <li><a href="all-articles.html">文章列表</a></li>
                <li><a href="search.html" class="active">搜尋</a></li>
                <li><a href="contact.html">聯絡我們</a></li>
            </ul>
        </div>
    </nav>

    <main class="search-shell">
        <h1>站內搜尋</h1>
        <p>搜尋文章標題、摘要、FAQ 與標籤。</p>
        <input id="search-input" class="search-input" type="search" placeholder="例如：Dify、客服、熟齡穿搭、AI 代理人">
        <div id="search-results" class="search-results"></div>
    </main>

    <script>
        const input = document.getElementById('search-input');
        const results = document.getElementById('search-results');

        function escapeHtml(value) {{
            return value
                .replaceAll('&', '&amp;')
                .replaceAll('<', '&lt;')
                .replaceAll('>', '&gt;')
                .replaceAll('"', '&quot;');
        }}

        function render(items, query) {{
            if (!query) {{
                results.innerHTML = '<p class="search-empty">輸入關鍵字後會在這裡顯示結果。</p>';
                return;
            }}
            if (!items.length) {{
                results.innerHTML = '<p class="search-empty">找不到符合結果，請換個關鍵字試試看。</p>';
                return;
            }}
            results.innerHTML = items.map((item) => `
                <article class="search-card">
                    <a href="${{item.relativeUrl}}">
                        <div class="search-meta">${{escapeHtml(item.categoryLabel)}} · ${{escapeHtml(item.publishedDateText || '')}}</div>
                        <h2>${{escapeHtml(item.title)}}</h2>
                        <p>${{escapeHtml(item.excerpt)}}</p>
                    </a>
                </article>
            `).join('');
        }}

        async function load() {{
            const response = await fetch('{search_index_url}', {{ cache: 'no-store' }});
            const items = await response.json();
            const params = new URLSearchParams(window.location.search);
            const initialQuery = params.get('q') || '';
            input.value = initialQuery;
            const apply = () => {{
                const query = input.value.trim().toLowerCase();
                const filtered = items.filter((item) => {{
                    const haystack = [item.title, item.excerpt, ...(item.tags || []), ...(item.faqQuestions || [])]
                        .join(' ')
                        .toLowerCase();
                    return haystack.includes(query);
                }});
                render(filtered.slice(0, 50), query);
            }};
            input.addEventListener('input', apply);
            apply();
        }}

        load().catch(() => {{
            results.innerHTML = '<p class="search-empty">搜尋索引載入失敗。</p>';
        }});
    </script>
    <script src="js/main.js"></script>
</body>
</html>
"""


def marker_block(key: str, content: str) -> str:
    return f"<!-- {MARKER_PREFIX}:START {key} -->\n{content}\n<!-- {MARKER_PREFIX}:END {key} -->"


def replace_marker_block(file_path: Path, key: str, replacement: str) -> None:
    original = file_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"<!-- {MARKER_PREFIX}:START {re.escape(key)} -->.*?<!-- {MARKER_PREFIX}:END {re.escape(key)} -->",
        flags=re.S,
    )
    block = marker_block(key, replacement)
    if pattern.search(original):
        updated = pattern.sub(block, original, count=1)
    else:
        raise PipelineError(f"{relative_to_root(file_path)} 缺少標記區塊：{key}")
    write_text(file_path, updated)


def build_front_listing(registry: list[dict[str, Any]], categories: dict[str, CategoryConfig]) -> dict[str, Any]:
    latest = registry[:12]
    by_category = {}
    for key, category in categories.items():
        by_category[key] = {
            "label": category.label,
            "items": [
                summarize_record(record)
                for record in registry
                if record["category"] == key
            ][:6],
        }
    return {
        "updatedAt": now_iso(),
        "latest": [summarize_record(record) for record in latest],
        "byCategory": by_category,
    }


def summarize_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["id"],
        "title": record["listingTitle"],
        "excerpt": record["listingExcerpt"],
        "category": record["category"],
        "categoryLabel": record["categoryLabel"],
        "series": record["series"],
        "publishedAt": record["publishedAt"],
        "publishedDateText": record.get("publishedDateText") or iso_to_display(record["publishedAt"]),
        "relativeUrl": record.get("relativeUrl") or url_to_relative(record["url"]),
        "heroImage": record.get("heroImage"),
        "tags": record.get("tags", []),
    }


def build_search_index(registry: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": record["id"],
            "title": record["listingTitle"],
            "excerpt": record["listingExcerpt"],
            "category": record["category"],
            "categoryLabel": record["categoryLabel"],
            "relativeUrl": record.get("relativeUrl") or url_to_relative(record["url"]),
            "publishedDateText": record.get("publishedDateText") or iso_to_display(record["publishedAt"]),
            "tags": record.get("tags", []),
            "faqQuestions": [item["question"] for item in record.get("faq", [])],
        }
        for record in registry
    ]


def render_queue_markdown(queue: dict[str, Any]) -> str:
    lines = ["# 主題 Queue", ""]
    if not queue["series"]:
        lines.extend(["目前沒有待處理的主題序列。", "", "## 使用方式", "", "- `加入主題序列：Dify AI，篇數：6，補充：偏台灣中小企業導入與實作`", "- `直接生成主題：AI 代理人怎麼落地到客服部門`", ""])
        return "\n".join(lines)
    for series in queue["series"]:
        lines.append(f"## {series['queueId']}｜{series['topic']}")
        lines.append("")
        lines.append(f"- 狀態：{series['status']}")
        lines.append(f"- 規劃篇數：{series['plannedCount']}")
        lines.append(f"- 補充方向：{series.get('direction') or '未提供'}")
        lines.append(f"- 建立時間：{series['createdAt']}")
        lines.append("")
        for item in series["items"]:
            suffix = ""
            if item.get("articleId"):
                suffix = f"｜文章 ID：{item['articleId']}｜檔案：{item.get('file', '')}"
            lines.append(
                f"{item['order']}. {item['title']}｜{item['status']}｜{item['targetReader']}｜{item['category']}{suffix}"
            )
        lines.append("")
    return "\n".join(lines)


def render_publish_log_markdown(log_payload: dict[str, Any]) -> str:
    lines = ["# 發文紀錄", ""]
    if not log_payload["entries"]:
        lines.append("目前尚無由自動化內容流水線發布的新文章。")
        lines.append("")
        return "\n".join(lines)
    for entry in log_payload["entries"]:
        lines.append(f"## {entry['publishedAt']}｜{entry['title']}")
        lines.append("")
        lines.append(f"- 文章 ID：{entry['articleId']}")
        lines.append(f"- URL：{entry['url']}")
        lines.append(f"- 檔案：{entry['file']}")
        lines.append(f"- 類型：{entry['triggerType']}")
        if entry.get("queueId"):
            lines.append(f"- Queue：{entry['queueId']}")
        lines.append("")
    return "\n".join(lines)


def rebuild_outputs(config: dict[str, Any], categories: dict[str, CategoryConfig]) -> list[dict[str, Any]]:
    registry = build_registry(config, categories)
    paths = config["paths"]
    articles_index_path = ROOT / paths["articlesIndexJson"]
    front_listing_path = ROOT / paths["frontListingJson"]
    search_index_path = ROOT / paths["searchIndexJson"]
    queue_json_path = ROOT / paths["queueJson"]
    publish_log_path = ROOT / paths["publishLogJson"]

    queue_payload = load_json(queue_json_path, default={"version": 1, "updatedAt": now_iso(), "nextQueueSequence": 1, "series": []})
    publish_log = load_json(publish_log_path, default={"version": 1, "updatedAt": now_iso(), "entries": []})

    articles_index_payload = {
        "updatedAt": now_iso(),
        "count": len(registry),
        "items": registry,
    }
    front_listing_payload = build_front_listing(registry, categories)
    search_index_payload = build_search_index(registry)

    write_json(articles_index_path, articles_index_payload)
    write_json(front_listing_path, front_listing_payload)
    write_json(search_index_path, search_index_payload)
    write_text(ROOT / paths["queueMarkdown"], render_queue_markdown(queue_payload))
    write_text(ROOT / paths["publishLogMarkdown"], render_publish_log_markdown(publish_log))
    write_text(ROOT / "all-articles.html", render_all_articles_page(config, categories, registry))
    write_text(ROOT / "search.html", render_search_page(config))

    latest_cards = "\n".join(render_article_card(record) for record in front_listing_payload["latest"][:6])
    replace_marker_block(ROOT / "index.html", "homepage-latest-articles", latest_cards)
    for key, category in categories.items():
        cards = "\n".join(render_article_card(record) for record in front_listing_payload["byCategory"][key]["items"])
        replace_marker_block(ROOT / category.page, f"category-{key}-latest", cards)

    subprocess.run([sys.executable, str(ROOT / "generate_sitemap.py")], cwd=ROOT, check=True)
    return registry


def choose_category_for_topic(topic: str, categories: dict[str, CategoryConfig]) -> str:
    topic_lower = topic.lower()
    mapping = [
        ("ai", "ai-innovation"),
        ("代理人", "ai-innovation"),
        ("客服", "ai-innovation"),
        ("世足", "outdoor-escapes"),
        ("世界盃", "outdoor-escapes"),
        ("足球", "outdoor-escapes"),
        ("職涯", "lifestyle-culture"),
        ("轉職", "lifestyle-culture"),
        ("第二曲線", "lifestyle-culture"),
        ("退休", "lifestyle-culture"),
        ("房地產", "lifestyle-culture"),
        ("房市", "lifestyle-culture"),
        ("地產", "lifestyle-culture"),
        ("房價", "lifestyle-culture"),
        ("閱讀", "lifestyle-culture"),
        ("居家", "lifestyle-culture"),
        ("紀錄", "lifestyle-culture"),
        ("秀場", "runway-trends"),
        ("時裝週", "runway-trends"),
        ("設計", "designer-perspective"),
        ("穿搭", "casual-chic"),
        ("衣櫥", "casual-chic"),
        ("鞋", "casual-chic"),
        ("包", "casual-chic"),
        ("瑜伽", "wellness-movement"),
        ("健康", "wellness-movement"),
        ("睡眠", "wellness-movement"),
        ("肌力", "wellness-movement"),
        ("更年期", "wellness-movement"),
        ("戶外", "outdoor-escapes"),
        ("旅行", "outdoor-escapes"),
        ("獨旅", "outdoor-escapes"),
        ("旅拍", "outdoor-escapes"),
        ("生活", "lifestyle-culture"),
        ("品味", "lifestyle-culture"),
    ]
    for keyword, category in mapping:
        if keyword in topic_lower:
            return category
    return "lifestyle-culture"


def extract_json_from_text(raw_text: str) -> Any:
    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$", "", raw_text)
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        match = re.search(r"(\{.*\}|\[.*\])", raw_text, flags=re.S)
        if match:
            return json.loads(match.group(1))
        raise


def get_model_runtime_config(config: dict[str, Any], *, planner: bool = False) -> dict[str, Any]:
    model_config = config["model"]
    provider = os.getenv(model_config.get("providerEnv", ""), model_config.get("provider", "openai-compatible"))
    endpoint = os.getenv(model_config.get("endpointEnv", ""), model_config["endpoint"])
    api_mode = os.getenv(model_config.get("apiModeEnv", ""), model_config.get("apiMode", "responses"))
    api_key = os.getenv(model_config["apiKeySecretName"])
    model_name = os.getenv(
        model_config["plannerModelEnv"] if planner else model_config["defaultModelEnv"]
    ) or (
        model_config["plannerModelFallback"] if planner else model_config["defaultModel"]
    )
    return {
        "provider": provider,
        "endpoint": endpoint,
        "apiMode": api_mode,
        "apiKey": api_key,
        "modelName": model_name,
    }


def get_title_context_limit(config: dict[str, Any], *, planner: bool = False) -> int:
    runtime = get_model_runtime_config(config, planner=planner)
    if runtime["provider"] == "nvidia":
        return 24 if planner else 18
    return 80 if planner else 60


def model_request(config: dict[str, Any], prompt_path: Path, payload: dict[str, Any], *, planner: bool = False) -> Any:
    runtime = get_model_runtime_config(config, planner=planner)
    api_key = runtime["apiKey"]
    if not api_key:
        raise PipelineError(f"缺少環境變數：{config['model']['apiKeySecretName']}")
    system_prompt = prompt_path.read_text(encoding="utf-8")
    user_payload = json.dumps(payload, ensure_ascii=False)
    if runtime["apiMode"] == "chat_completions":
        body = {
            "model": runtime["modelName"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_payload},
            ],
        }
    else:
        body = {
            "model": runtime["modelName"],
            "input": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_payload},
            ],
        }
    request = urllib.request.Request(
        runtime["endpoint"],
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    max_attempts = int(config["model"].get("maxAttempts", 3))
    retry_delay = float(config["model"].get("retryDelaySeconds", 4))
    parsed: dict[str, Any] | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=config["model"]["requestTimeoutSeconds"]) as response:
                parsed = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as error:
            details = error.read().decode("utf-8", errors="ignore")
            transient = error.code in {408, 409, 425, 429, 500, 502, 503, 504}
            if transient and attempt < max_attempts:
                time.sleep(retry_delay * attempt)
                continue
            raise PipelineError(f"模型 API 失敗：{error.code} {details}") from error
        except (
            http.client.RemoteDisconnected,
            urllib.error.URLError,
            TimeoutError,
            socket.timeout,
            ConnectionResetError,
        ) as error:
            if attempt < max_attempts:
                time.sleep(retry_delay * attempt)
                continue
            raise PipelineError(f"模型 API 連線失敗：{error}") from error
    if parsed is None:
        raise PipelineError("模型 API 沒有回傳有效內容。")
    output_text = ""
    if runtime["apiMode"] == "chat_completions":
        choices = parsed.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            content = message.get("content", "")
            if isinstance(content, str):
                output_text = content.strip()
            elif isinstance(content, list):
                parts: list[str] = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") in {"text", "output_text"}:
                        parts.append(item.get("text", ""))
                output_text = "\n".join(parts).strip()
    else:
        output_text = parsed.get("output_text")
        if not output_text:
            outputs = parsed.get("output", [])
            texts: list[str] = []
            for item in outputs:
                for chunk in item.get("content", []):
                    if chunk.get("type") in {"output_text", "text"}:
                        texts.append(chunk.get("text", ""))
            output_text = "\n".join(texts).strip()
    if not output_text:
        raise PipelineError("模型沒有回傳可解析文字")
    return extract_json_from_text(output_text)


def fallback_plan(topic: str, count: int, direction: str, existing_titles: list[str], categories: dict[str, CategoryConfig]) -> dict[str, Any]:
    category = choose_category_for_topic(topic, categories)
    templates = [
        "{topic} 入門：先釐清問題，再決定要不要開始",
        "{topic} 比較指南：哪些做法真的適合現在的你",
        "{topic} 情境拆解：把抽象概念放回日常生活與工作",
        "{topic} 決策順序：開始前最該先確認的 5 件事",
        "{topic} 常見誤區：很多人不是做不到，而是順序弄反了",
        "{topic} 實用版：如何在不過度用力的情況下開始",
        "{topic} 深入版：從單一靈感走向穩定習慣或流程",
        "{topic} 下一步：看完之後，最值得先做的是什麼",
    ]
    items = []
    for order in range(1, count + 1):
        title = templates[(order - 1) % len(templates)].format(topic=topic)
        if is_duplicate_title(title, existing_titles):
            title = f"{title}（實戰版 {order}）"
        items.append(
            {
                "order": order,
                "title": title,
                "angle": f"{direction or '以熟齡女性的生活與工作決策場景切入'}，聚焦第 {order} 篇的不同決策情境。",
                "targetReader": "想把抽象趨勢翻成自己可用下一步的台灣讀者",
                "series": f"{topic} 系列",
                "category": category,
                "ctaHint": "導向同系列下一篇或該分類主題頁",
            }
        )
    return {
        "seriesName": f"{topic} 系列",
        "category": category,
        "items": items,
    }


def fallback_article(brief: dict[str, Any], config: dict[str, Any], categories: dict[str, CategoryConfig], existing_titles: list[str]) -> dict[str, Any]:
    title = brief["title"]
    if is_duplicate_title(title, existing_titles):
        title = f"{title}：台灣企業的實作版"
    category_key = brief["category"]
    category = categories.get(category_key, categories["ai-innovation"])
    title_slug = slugify(brief.get("slug") or title)
    sections = [
        {
            "heading": "先把問題定義清楚，再談工具導入",
            "paragraphs": [
                f"{brief['topic']} 之所以容易失敗，往往不是工具不夠強，而是團隊沒有先對齊要解的核心問題。對台灣中小企業來說，真正需要先釐清的是：目前流程哪一段最耗時、最難交接、最常出錯。",
                "當主題進入執行階段，最實際的做法不是一次把所有流程自動化，而是挑出一條最容易驗證成效的路徑，先做小範圍試點，再決定要不要擴大。",
            ],
            "bullets": [
                "先盤點目前人工流程與交接點",
                "列出最容易量化的效益指標",
                "把試點範圍控制在單一部門或單一情境",
            ],
        },
        {
            "heading": "從台灣讀者熟悉的場景切入，才有落地可能",
            "paragraphs": [
                f"這篇主題適合從 {brief.get('direction') or '實際部門與工作流程'} 去理解，而不是只看國外抽象案例。若你的團隊規模不大，越需要把導入節奏拆成可以在一到兩週內觀察的動作。",
                "與其追求一次做到最完整，不如先設計一個低風險版本，觀察內容品質、回應時間、交接成本與實際採用率，再決定下一步。",
            ],
            "bullets": [
                "建立最小可行流程",
                "同步留下人工覆核機制",
                "每週回顧一次成效與失敗案例",
            ],
        },
        {
            "heading": "真正值得複製的，是流程而不是單一靈感",
            "paragraphs": [
                "當第一個場景跑順後，下一步才是把 SOP、FAQ、責任分工與驗證規則整理成團隊可持續維護的內容資產。",
                "如果沒有把資料來源、例外處理與更新節點定義清楚，再好的自動化也很容易在兩個月後失效。對內容團隊來說，可持續維護比短期爆量更重要。",
            ],
            "bullets": [
                "把常見問題整理成 FAQ",
                "保留例外處理與人工接手節點",
                "用同一份索引管理文章、搜尋與前台列表",
            ],
        },
    ]
    article = {
        "title": title,
        "slug": title_slug,
        "excerpt": brief["excerpt"],
        "tags": brief["tags"],
        "metaTitle": brief["metaTitle"],
        "metaDescription": brief["metaDescription"],
        "category": category_key,
        "series": brief.get("series") or category.label,
        "audience": brief.get("targetReader") or "對相關主題有導入需求的台灣讀者",
        "readTimeMinutes": 9,
        "listingTitle": title,
        "listingExcerpt": brief["excerpt"],
        "heroImage": category.placeholder_image,
        "intro": f"這篇文章聚焦 {brief['topic']}，不是談空泛趨勢，而是整理出台灣讀者真正能採取的做法、判斷順序與上線前應先確認的細節。",
        "sections": sections,
        "faq": [
            {
                "question": f"{brief['topic']} 一定要一次全面導入嗎？",
                "answer": "不需要。對大多數台灣中小企業來說，先用單一場景做試點，觀察成效與風險，再逐步擴大會更穩健。",
            },
            {
                "question": "怎麼避免導入後只剩表面自動化？",
                "answer": "關鍵不在工具，而在是否把流程、例外處理、人工覆核與績效指標一起定義清楚。沒有這些配套，自動化很容易停在示範階段。",
            },
        ],
        "extendedReading": [
            {
                "title": f"瀏覽更多{category.label}文章",
                "url": f"/{category.page}",
            },
            {
                "title": "查看所有文章列表",
                "url": "/all-articles.html",
            },
        ],
        "cta": {
            "label": f"查看更多{category.label}內容",
            "url": f"/{category.page}",
            "text": f"若你想繼續延伸這個主題，建議先從 {category.label} 分類頁往下看，找到最接近你目前決策階段的下一篇文章。",
        },
    }
    return article


def build_article_brief(item: dict[str, Any], categories: dict[str, CategoryConfig]) -> dict[str, Any]:
    category = categories[item["category"]]
    title = item["title"]
    return {
        "topic": item.get("topic") or title,
        "title": title,
        "slug": item.get("slug") or slugify(title),
        "excerpt": f"聚焦 {title}，從台灣讀者熟悉的情境拆解步驟、風險與下一步。",
        "tags": [category.label, item.get("topic") or title, "內容自動化"],
        "metaTitle": title[:36],
        "metaDescription": f"{title}，整理適用對象、導入步驟、風險與驗證方式，幫助讀者快速判斷下一步。",
        "category": item["category"],
        "series": item.get("series") or category.label,
        "direction": item.get("angle") or "",
        "targetReader": item.get("targetReader") or "台灣讀者",
        "ctaUrl": item.get("ctaUrl") or "",
        "ctaLabel": item.get("ctaLabel") or "",
        "ctaText": item.get("ctaText") or "",
        "disclaimerText": item.get("disclaimerText") or "",
    }


def parse_direct_topic_request(topic: str) -> dict[str, Any]:
    raw = topic.strip()
    cta_match = re.search(
        r"CTA\s*推薦(?:[^\n]*?\s)?(https?://\S+|[A-Za-z0-9.-]+\.[A-Za-z]{2,}\S*)",
        raw,
        flags=re.I,
    )
    cta_url = normalize_external_url(cta_match.group(1)) if cta_match else ""
    disclaimer_required = bool(re.search(r"文末加註必要的警語|必要的警語", raw))

    cleaned = raw
    if cta_match:
        cleaned = cleaned.replace(cta_match.group(0), "")
    cleaned = re.sub(r"^\s*直接生成主題[:：]\s*", "", cleaned)
    cleaned = re.sub(r"^\s*談論\s*", "", cleaned)
    cleaned = re.sub(r"[，,、]?\s*並(?=\s*[，,、]|$)", "", cleaned)
    cleaned = re.sub(r"(?:[，,、]?\s*並\s*)+$", "", cleaned).strip()
    cleaned = re.sub(r"[，,、]?\s*文末加註必要的警語", "", cleaned).strip()
    cleaned = re.sub(r"[，,、]\s*$", "", cleaned).strip()

    cta_label = "查看延伸閱讀"
    cta_text = "如果你想延伸閱讀這個主題，下一步可以直接前往我們推薦的專頁。"
    if "world-cup-2026" in cta_url:
        cta_label = "前往看更多 2026 世足賽整理"
        cta_text = "如果你想繼續追蹤 2026 世足賽的賽程、話題整理與延伸觀點，下一步最適合直接前往專門整理這個主題的頁面。"
    elif "insightestate.ca" in cta_url:
        cta_label = "前往洞悉地產權威論壇"
        cta_text = "如果你想進一步閱讀來自在地視角的加拿大房市觀察與生活圈分析，下一步最適合直接前往洞悉地產的繁體中文論壇。"
    elif "ai-survival-guide" in cta_url or "flypigai" in cta_url:
        cta_label = "前往查看 AI 生存指南"
        cta_text = "如果你想把這篇文章的觀念延伸成更完整的自學與工作規劃，下一步最適合直接前往完整的 AI 生存指南頁面。"

    disclaimer_text = ""
    if disclaimer_required:
        disclaimer_text = (
            "本文僅供一般資訊參考，不構成投資、稅務、法律、移民、貸款或購屋建議。"
            "加拿大各省、市場、稅制與身份限制差異很大，且可能隨政策調整而變動。"
            "在進行任何海外置產或資產配置前，請務必先向當地持牌仲介、律師、會計師與財務顧問確認最新規範與風險。"
        )

    return {
        "topic": cleaned,
        "ctaUrl": cta_url,
        "ctaLabel": cta_label if cta_url else "",
        "ctaText": cta_text if cta_url else "",
        "disclaimerText": disclaimer_text,
    }


def ensure_unique_slug(slug: str, registry: list[dict[str, Any]]) -> str:
    existing = {item["slug"] for item in registry}
    if slug not in existing:
        return slug
    suffix = 2
    while f"{slug}-{suffix}" in existing:
        suffix += 1
    return f"{slug}-{suffix}"


def apply_article_defaults(article: dict[str, Any], brief: dict[str, Any], categories: dict[str, CategoryConfig]) -> dict[str, Any]:
    category_key = article.get("category") or brief["category"]
    if category_key not in categories:
        category_key = brief["category"]
    category = categories[category_key]

    article["title"] = article.get("title") or brief["title"]
    article["slug"] = article.get("slug") or brief["slug"]
    article["excerpt"] = article.get("excerpt") or brief["excerpt"]
    article["tags"] = article.get("tags") or brief["tags"]
    article["metaTitle"] = article.get("metaTitle") or article["title"]
    article["metaDescription"] = article.get("metaDescription") or brief["metaDescription"]
    article["category"] = category_key
    article["series"] = article.get("series") or brief.get("series") or category.label
    article["audience"] = article.get("audience") or brief.get("targetReader") or "台灣讀者"
    article["listingTitle"] = article.get("listingTitle") or article["title"]
    article["listingExcerpt"] = article.get("listingExcerpt") or article["excerpt"]
    article["heroImage"] = article.get("heroImage") or category.placeholder_image
    article["intro"] = article.get("intro") or brief["excerpt"]
    article["sections"] = article.get("sections") or [
        {
            "heading": brief["title"],
            "paragraphs": [brief["excerpt"]],
            "bullets": [],
        }
    ]
    article["faq"] = article.get("faq") or []
    article["extendedReading"] = article.get("extendedReading") or [
        {"title": f"瀏覽更多{category.label}文章", "url": f"/{category.page}"}
    ]
    article["cta"] = article.get("cta") or {
        "label": f"查看更多{category.label}內容",
        "url": f"/{category.page}",
        "text": f"若你想延伸閱讀，建議先從 {category.label} 分類頁繼續往下看。",
    }
    if brief.get("ctaUrl"):
        article["cta"]["url"] = brief["ctaUrl"]
        if brief.get("ctaLabel"):
            article["cta"]["label"] = brief["ctaLabel"]
        if brief.get("ctaText"):
            article["cta"]["text"] = brief["ctaText"]
    if brief.get("disclaimerText"):
        article["disclaimer"] = brief["disclaimerText"]
    return article


def save_generated_article(article: dict[str, Any], queue_id: str | None, config: dict[str, Any], categories: dict[str, CategoryConfig]) -> dict[str, Any]:
    category = categories[article["category"]]
    published_at = now_iso()
    article_id = f"auto-{now_utc().strftime('%Y%m%d%H%M%S')}-{article['slug']}"
    relative_html_path = f"{category.directory}/{article['slug']}.html"
    article_url = path_to_url(config["baseUrl"], relative_html_path)
    article["id"] = article_id
    article["queueId"] = queue_id
    article["publishedAt"] = published_at
    article["publishedDateText"] = iso_to_display(published_at)
    article["url"] = article_url
    article["file"] = relative_html_path
    article["relativeUrl"] = relative_html_path
    article["status"] = "published"
    article["markdownBody"] = render_markdown_body(article)

    metadata_path = ROOT / config["paths"]["generatedArticlesDir"] / f"{article['slug']}.json"
    markdown_path = ROOT / config["paths"]["generatedArticlesDir"] / f"{article['slug']}.md"
    html_path = ROOT / relative_html_path

    write_json(metadata_path, article)
    write_text(markdown_path, article["markdownBody"])
    write_text(html_path, render_article_html(article, config, categories))
    return article


def update_queue_after_publish(queue_payload: dict[str, Any], queue_id: str, order: int, article: dict[str, Any]) -> None:
    for series in queue_payload["series"]:
        if series["queueId"] != queue_id:
            continue
        for item in series["items"]:
            if item["order"] == order:
                item["status"] = "published"
                item["articleId"] = article["id"]
                item["file"] = article["file"]
                item["publishedAt"] = article["publishedAt"]
                break
        if all(item["status"] == "published" for item in series["items"]):
            series["status"] = "completed"
        else:
            series["status"] = "in_progress"
        return
    raise PipelineError(f"找不到 queue item：{queue_id}#{order}")


def append_publish_log(config: dict[str, Any], article: dict[str, Any], *, trigger_type: str, queue_id: str | None) -> None:
    path = ROOT / config["paths"]["publishLogJson"]
    payload = load_json(path, default={"version": 1, "updatedAt": now_iso(), "entries": []})
    payload["updatedAt"] = now_iso()
    payload["entries"].insert(
        0,
        {
            "articleId": article["id"],
            "title": article["title"],
            "publishedAt": article["publishedAt"],
            "url": article["url"],
            "file": article["file"],
            "queueId": queue_id,
            "triggerType": trigger_type,
        },
    )
    write_json(path, payload)


def parse_instruction(instruction: str) -> dict[str, Any]:
    text = instruction.strip()
    queue_match = re.search(
        r"加入主題序列[:：]\s*(?P<topic>[^，,\n]+)\s*[，,]\s*篇數[:：]\s*(?P<count>\d+)\s*[，,]\s*補充[:：]\s*(?P<direction>.+)$",
        text,
    )
    if queue_match:
        return {
            "action": "enqueue",
            "topic": queue_match.group("topic").strip(),
            "count": int(queue_match.group("count")),
            "direction": queue_match.group("direction").strip(),
        }
    direct_match = re.search(r"直接生成主題[:：]\s*(?P<topic>.+)$", text)
    if direct_match:
        return {
            "action": "generate-now",
            "topic": direct_match.group("topic").strip(),
        }
    raise PipelineError("無法解析指令，請使用「加入主題序列：...」或「直接生成主題：...」格式。")


def enqueue_topic(config: dict[str, Any], categories: dict[str, CategoryConfig], topic: str, count: int, direction: str, *, fixture: bool = False) -> dict[str, Any]:
    queue_path = ROOT / config["paths"]["queueJson"]
    queue_payload = load_json(queue_path, default={"version": 1, "updatedAt": now_iso(), "nextQueueSequence": 1, "series": []})
    registry = build_registry(config, categories)
    existing_titles = [item["title"] for item in registry]
    title_context = build_existing_title_context(
        registry,
        topic=topic,
        category=choose_category_for_topic(topic, categories),
        limit=get_title_context_limit(config, planner=True),
    )
    if fixture or not os.getenv(config["model"]["apiKeySecretName"]):
        planned = fallback_plan(topic, count, direction, existing_titles, categories)
    else:
        planned = model_request(
            config,
            ROOT / "automation" / "prompts" / "series-planner.md",
            {
                "strategy": (ROOT / config["paths"]["strategyFile"]).read_text(encoding="utf-8"),
                "reviewChecklist": (ROOT / config["paths"]["reviewChecklistFile"]).read_text(encoding="utf-8"),
                "topic": topic,
                "count": count,
                "direction": direction,
                "existingTitles": title_context,
                "categories": [{key: value.label} for key, value in categories.items()],
            },
            planner=True,
        )
    queue_id = f"Q-{queue_payload['nextQueueSequence']:04d}"
    queue_payload["nextQueueSequence"] += 1
    queue_payload["updatedAt"] = now_iso()
    category_key = planned["category"] if planned["category"] in categories else choose_category_for_topic(topic, categories)
    series_entry = {
        "queueId": queue_id,
        "topic": topic,
        "direction": direction,
        "plannedCount": count,
        "status": "planned",
        "createdAt": now_iso(),
        "seriesName": planned.get("seriesName") or f"{topic} 系列",
        "items": [],
    }
    for index, item in enumerate(planned["items"][:count], start=1):
        title = item["title"]
        if is_duplicate_title(title, existing_titles):
            title = f"{title}（系列版 {index}）"
        series_entry["items"].append(
            {
                "order": index,
                "title": title,
                "angle": item.get("angle") or direction,
                "targetReader": item.get("targetReader") or "台灣讀者",
                "category": item.get("category") if item.get("category") in categories else category_key,
                "series": item.get("series") or series_entry["seriesName"],
                "ctaHint": item.get("ctaHint") or "導向系列下一篇",
                "status": "planned",
                "articleId": None,
                "file": None,
            }
        )
        existing_titles.append(title)
    queue_payload["series"].append(series_entry)
    write_json(queue_path, queue_payload)
    rebuild_outputs(config, categories)
    return {"queueId": queue_id, "topic": topic, "plannedCount": len(series_entry["items"])}


def get_next_queue_item(queue_payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]] | tuple[None, None]:
    for series in queue_payload["series"]:
        if series["status"] == "completed":
            continue
        for item in series["items"]:
            if item["status"] == "planned":
                return series, item
    return None, None


def candidate_title_from_angle(topic: str, angle: str) -> str:
    if "：" in angle or len(angle) >= 24 or topic in angle:
        return angle
    return f"{topic}：{angle}"


def compute_category_gap_scores(
    registry: list[dict[str, Any]], selection_rules: dict[str, Any], categories: dict[str, CategoryConfig]
) -> dict[str, float]:
    target_entries = selection_rules.get("targetShares", [])
    target_shares = {
        entry["category"]: entry["share"]
        for entry in target_entries
        if entry.get("category") in categories
    }
    lookback = selection_rules.get("categoryGapLookback", 36)
    recent_records = [item for item in registry if item["category"] in target_shares][:lookback]
    counts = Counter(item["category"] for item in recent_records)
    total = sum(counts.values()) or 1
    return {
        category: target_shares.get(category, 0.0) - (counts.get(category, 0) / total)
        for category in target_shares
    }


def get_fallback_item(config: dict[str, Any], categories: dict[str, CategoryConfig], registry: list[dict[str, Any]]) -> dict[str, Any]:
    backlog = load_json(ROOT / config["paths"]["topicBacklogFile"])
    existing_titles = [item["title"] for item in registry]
    recent_titles = existing_titles[:18]
    recent_categories = [item["category"] for item in registry[:9] if item.get("category") in categories]
    selection_rules = backlog.get("selectionRules", {})
    category_gaps = compute_category_gap_scores(registry, selection_rules, categories)
    business_weights = selection_rules.get("businessValueWeights", {})
    evergreen_weights = selection_rules.get("evergreenWeights", {})
    avoid_patterns = selection_rules.get("avoidTitlePatterns", [])

    ranked_candidates: list[tuple[float, dict[str, Any]]] = []
    for entry in backlog["fallbackTopics"]:
        category = entry["category"]
        if category not in categories:
            continue
        for angle in entry["angles"]:
            candidate_title = candidate_title_from_angle(entry["topic"], angle)
            if is_duplicate_title(candidate_title, existing_titles):
                continue
            score = float(entry.get("priority", 50))
            score += round(category_gaps.get(category, 0.0) * 100, 2)
            score += business_weights.get(entry.get("businessValue", "low"), 0)
            score += evergreen_weights.get(entry.get("evergreen", "low"), 0)
            if any(pattern in candidate_title for pattern in avoid_patterns):
                score -= 12
            if any(similarity_score(entry["topic"], title) >= 0.18 for title in recent_titles):
                score -= 28
            score -= recent_categories.count(category) * 5
            ranked_candidates.append(
                (
                    score,
                    {
                        "topic": entry["topic"],
                        "title": candidate_title,
                        "angle": entry.get("direction") or angle,
                        "targetReader": entry["audience"],
                        "category": category,
                        "series": entry["topic"],
                        "ctaHint": entry["ctaHint"],
                        "status": "planned",
                    },
                )
            )
    if ranked_candidates:
        ranked_candidates.sort(key=lambda item: item[0], reverse=True)
        return ranked_candidates[0][1]
    raise PipelineError("找不到可用的 fallback topic，請先補充 automation/topic-backlog.json")


def validate_generated_article(article: dict[str, Any], config: dict[str, Any]) -> None:
    missing = [
        field
        for field in config["articleContract"]["requiredFields"]
        if field not in article or article[field] in (None, "", [])
    ]
    if missing:
        raise PipelineError(f"文章資料缺少必要欄位：{', '.join(missing)}")


def generate_article_from_item(config: dict[str, Any], categories: dict[str, CategoryConfig], item: dict[str, Any], *, queue_id: str | None, trigger_type: str, fixture: bool = False) -> dict[str, Any]:
    registry = build_registry(config, categories)
    existing_titles = [record["title"] for record in registry]
    brief = build_article_brief(item, categories)
    title_context = build_existing_title_context(
        registry,
        topic=brief["title"],
        category=brief["category"],
        limit=get_title_context_limit(config, planner=False),
    )
    if fixture or not os.getenv(config["model"]["apiKeySecretName"]):
        article = fallback_article(brief, config, categories, existing_titles)
    else:
        article = model_request(
            config,
            ROOT / "automation" / "prompts" / "article-writer.md",
            {
                "strategy": (ROOT / config["paths"]["strategyFile"]).read_text(encoding="utf-8"),
                "reviewChecklist": (ROOT / config["paths"]["reviewChecklistFile"]).read_text(encoding="utf-8"),
                "brief": brief,
                "existingTitles": title_context,
                "categories": {key: value.label for key, value in categories.items()},
            },
            planner=False,
        )
    article = apply_article_defaults(article, brief, categories)
    article["heroImage"] = choose_balanced_hero_image(article, registry, config, categories)
    article["slug"] = ensure_unique_slug(slugify(article["slug"]), registry)
    saved = save_generated_article(article, queue_id, config, categories)
    validate_generated_article(saved, config)
    append_publish_log(config, saved, trigger_type=trigger_type, queue_id=queue_id)
    return saved


def verify_outputs(config: dict[str, Any], categories: dict[str, CategoryConfig], *, article_id: str | None = None) -> dict[str, Any]:
    paths = config["paths"]
    articles_index = load_json(ROOT / paths["articlesIndexJson"])
    front_listing = load_json(ROOT / paths["frontListingJson"])
    search_index = load_json(ROOT / paths["searchIndexJson"])
    publish_log = load_json(ROOT / paths["publishLogJson"])
    queue_payload = load_json(ROOT / paths["queueJson"])

    for path_key in ["articlesIndexJson", "frontListingJson", "searchIndexJson", "publishLogJson", "queueJson"]:
        path = ROOT / paths[path_key]
        if not path.exists():
            raise PipelineError(f"缺少必要檔案：{relative_to_root(path)}")

    ids = set()
    urls = set()
    files = set()
    for item in articles_index["items"]:
        if item["id"] in ids:
            raise PipelineError(f"重複 article id：{item['id']}")
        if item["url"] in urls:
            raise PipelineError(f"重複 article url：{item['url']}")
        if item["file"] in files:
            raise PipelineError(f"重複 article file：{item['file']}")
        ids.add(item["id"])
        urls.add(item["url"])
        files.add(item["file"])
        if not (ROOT / item["file"]).exists():
            raise PipelineError(f"文章檔不存在：{item['file']}")

    target_article = None
    if article_id:
        target_article = next((item for item in articles_index["items"] if item["id"] == article_id), None)
        if not target_article:
            raise PipelineError(f"找不到文章：{article_id}")
        if target_article["id"] not in {item["id"] for item in front_listing["latest"]} and not any(
            target_article["id"] == item["id"]
            for entry in front_listing["byCategory"].values()
            for item in entry["items"]
        ):
            raise PipelineError("前台列表資料未包含最新文章")
        if target_article["id"] not in {item["id"] for item in search_index}:
            raise PipelineError("搜尋索引未包含最新文章")
        if target_article["id"] not in {entry["articleId"] for entry in publish_log["entries"]}:
            raise PipelineError("發文紀錄未包含最新文章")

        relative_url = target_article["relativeUrl"]
        all_articles_content = (ROOT / "all-articles.html").read_text(encoding="utf-8")
        if relative_url not in all_articles_content:
            raise PipelineError("所有文章列表頁未包含最新文章連結")
        category_config = categories.get(target_article["category"])
        if category_config:
            category_content = (ROOT / category_config.page).read_text(encoding="utf-8")
            if relative_url not in category_content:
                raise PipelineError(f"{category_config.page} 未包含最新文章連結")
        home_content = (ROOT / "index.html").read_text(encoding="utf-8")
        if relative_url not in home_content:
            raise PipelineError("首頁最新文章區未包含最新文章連結")

    return {
        "articlesCount": articles_index["count"],
        "queueSeries": len(queue_payload["series"]),
        "verifiedArticleId": article_id,
    }


def command_sync(config: dict[str, Any], categories: dict[str, CategoryConfig]) -> None:
    rebuild_outputs(config, categories)
    latest_run_path = ROOT / config["paths"]["latestRunJson"]
    write_json(latest_run_path, {"status": "synced", "updatedAt": now_iso()})


def command_generate_now(config: dict[str, Any], categories: dict[str, CategoryConfig], topic: str, *, fixture: bool = False) -> dict[str, Any]:
    parsed = parse_direct_topic_request(topic)
    normalized_topic = parsed["topic"] or topic.strip()
    item = {
        "topic": normalized_topic,
        "title": normalized_topic,
        "angle": "直接生成單篇文章，不進 queue。",
        "targetReader": "對主題有立即搜尋需求的台灣讀者",
        "category": choose_category_for_topic(normalized_topic, categories),
        "series": normalized_topic,
        "ctaHint": "導向對應分類頁",
        "ctaUrl": parsed.get("ctaUrl") or "",
        "ctaLabel": parsed.get("ctaLabel") or "",
        "ctaText": parsed.get("ctaText") or "",
        "disclaimerText": parsed.get("disclaimerText") or "",
        "status": "planned",
    }
    article = generate_article_from_item(config, categories, item, queue_id=None, trigger_type="direct", fixture=fixture)
    rebuild_outputs(config, categories)
    verify_outputs(config, categories, article_id=article["id"])
    write_json(ROOT / config["paths"]["latestRunJson"], {"status": "generated", "updatedAt": now_iso(), "articleId": article["id"], "url": article["url"], "title": article["title"]})
    return article


def command_scheduled_run(config: dict[str, Any], categories: dict[str, CategoryConfig], *, fixture: bool = False) -> dict[str, Any]:
    queue_payload = load_json(ROOT / config["paths"]["queueJson"])
    registry = build_registry(config, categories)
    series, item = get_next_queue_item(queue_payload)
    queue_id = None
    order = None
    trigger_type = "fallback"
    if item:
        queue_id = series["queueId"]
        order = item["order"]
        item["topic"] = series["topic"]
        trigger_type = "queue"
    else:
        item = get_fallback_item(config, categories, registry)
    article = generate_article_from_item(config, categories, item, queue_id=queue_id, trigger_type=trigger_type, fixture=fixture)
    if queue_id is not None and order is not None:
        update_queue_after_publish(queue_payload, queue_id, order, article)
        queue_payload["updatedAt"] = now_iso()
        write_json(ROOT / config["paths"]["queueJson"], queue_payload)
    rebuild_outputs(config, categories)
    verify_outputs(config, categories, article_id=article["id"])
    write_json(
        ROOT / config["paths"]["latestRunJson"],
        {
            "status": "generated",
            "updatedAt": now_iso(),
            "articleId": article["id"],
            "url": article["url"],
            "title": article["title"],
            "queueId": queue_id,
            "triggerType": trigger_type,
        },
    )
    return article


def command_parse_instruction(config: dict[str, Any], categories: dict[str, CategoryConfig], instruction: str, *, fixture: bool = False) -> dict[str, Any]:
    parsed = parse_instruction(instruction)
    if parsed["action"] == "enqueue":
        result = enqueue_topic(
            config,
            categories,
            parsed["topic"],
            parsed["count"],
            parsed["direction"],
            fixture=fixture,
        )
        write_json(ROOT / config["paths"]["latestRunJson"], {"status": "queued", "updatedAt": now_iso(), **result})
        return result
    article = command_generate_now(config, categories, parsed["topic"], fixture=fixture)
    return {"articleId": article["id"], "url": article["url"], "title": article["title"]}


def wait_for_live(config: dict[str, Any], *, article_url: str | None = None, article_title: str | None = None, timeout_seconds: int = 1200) -> dict[str, Any]:
    latest_run = load_json(ROOT / config["paths"]["latestRunJson"], default={})
    article_url = article_url or latest_run.get("url")
    article_title = article_title or latest_run.get("title")
    if not article_url:
        raise PipelineError("沒有可檢查的文章 URL")
    deadline = time.time() + timeout_seconds
    last_status = "未開始"
    while time.time() < deadline:
        try:
            request = urllib.request.Request(
                article_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; EliteFashionContentBot/1.0; +https://tw.elitefasion.com)",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache",
                },
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                body = response.read().decode("utf-8", errors="ignore")
                if response.status == 200 and (not article_title or article_title in body):
                    result = {
                        "status": "live",
                        "checkedAt": now_iso(),
                        "url": article_url,
                    }
                    latest_run.update(result)
                    write_json(ROOT / config["paths"]["latestRunJson"], latest_run)
                    return result
                last_status = f"HTTP {response.status}，但內容尚未命中"
        except Exception as error:  # noqa: BLE001
            last_status = str(error)
        time.sleep(30)
    raise PipelineError(f"正式站在等待時間內仍未讀到文章：{article_url}｜最後狀態：{last_status}")


def send_notification(config: dict[str, Any], *, article_title: str | None = None, article_url: str | None = None) -> dict[str, Any]:
    latest_run = load_json(ROOT / config["paths"]["latestRunJson"], default={})
    article_title = article_title or latest_run.get("title")
    article_url = article_url or latest_run.get("url")
    api_key = os.getenv(config["notifications"]["providerSecretName"])
    from_email = os.getenv(config["notifications"]["fromEmailSecretName"])
    to_email = os.getenv(config["notifications"]["toEmailSecretName"])
    subject_prefix = config["notifications"].get("subjectPrefix", "")
    if not all([api_key, from_email, to_email, article_title, article_url]):
        raise PipelineError("通知設定不完整，請確認 RESEND API key、寄件與收件信箱，以及最新文章資料。")
    payload = {
        "from": from_email,
        "to": [to_email],
        "subject": f"{subject_prefix}文章已上線：{article_title}",
        "html": f"<p>{html.escape(article_title)}</p><p><a href=\"{html.escape(article_url)}\">{html.escape(article_url)}</a></p>",
    }
    request = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "EliteFashionContentPipeline/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="ignore")
        raise PipelineError(f"寄送通知失敗：{error.code} {details}") from error
    latest_run["notification"] = {"sentAt": now_iso(), "id": body.get("id")}
    write_json(ROOT / config["paths"]["latestRunJson"], latest_run)
    return {"status": "sent", "providerId": body.get("id")}


def main() -> int:
    config, categories = load_config()
    parser = argparse.ArgumentParser(description="Elite Fashion content pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("sync", help="Rebuild indices, pages, and logs")
    verify_parser = subparsers.add_parser("verify", help="Verify generated outputs")
    verify_parser.add_argument("--article-id", dest="article_id")

    command_parser = subparsers.add_parser("command", help="Parse natural language instruction")
    command_parser.add_argument("--instruction", required=True)
    command_parser.add_argument("--fixture", action="store_true")

    enqueue_parser = subparsers.add_parser("enqueue", help="Add topic series to queue")
    enqueue_parser.add_argument("--topic", required=True)
    enqueue_parser.add_argument("--count", required=True, type=int)
    enqueue_parser.add_argument("--direction", default="")
    enqueue_parser.add_argument("--fixture", action="store_true")

    direct_parser = subparsers.add_parser("generate-now", help="Generate one article immediately")
    direct_parser.add_argument("--topic", required=True)
    direct_parser.add_argument("--fixture", action="store_true")

    scheduled_parser = subparsers.add_parser("scheduled-run", help="Consume next queue item or fallback topic")
    scheduled_parser.add_argument("--fixture", action="store_true")

    live_parser = subparsers.add_parser("wait-for-live", help="Poll production URL until article is live")
    live_parser.add_argument("--article-url")
    live_parser.add_argument("--article-title")
    live_parser.add_argument("--timeout-seconds", type=int, default=1200)

    notify_parser = subparsers.add_parser("send-notification", help="Send email after production is live")
    notify_parser.add_argument("--article-title")
    notify_parser.add_argument("--article-url")

    args = parser.parse_args()

    try:
        if args.command == "sync":
            command_sync(config, categories)
            print(json.dumps({"status": "ok", "action": "sync"}, ensure_ascii=False))
        elif args.command == "verify":
            result = verify_outputs(config, categories, article_id=args.article_id)
            print(json.dumps({"status": "ok", **result}, ensure_ascii=False))
        elif args.command == "command":
            result = command_parse_instruction(config, categories, args.instruction, fixture=args.fixture)
            print(json.dumps({"status": "ok", **result}, ensure_ascii=False))
        elif args.command == "enqueue":
            result = enqueue_topic(
                config,
                categories,
                args.topic,
                args.count,
                args.direction,
                fixture=args.fixture,
            )
            print(json.dumps({"status": "ok", **result}, ensure_ascii=False))
        elif args.command == "generate-now":
            article = command_generate_now(config, categories, args.topic, fixture=args.fixture)
            print(json.dumps({"status": "ok", "articleId": article["id"], "url": article["url"]}, ensure_ascii=False))
        elif args.command == "scheduled-run":
            article = command_scheduled_run(config, categories, fixture=args.fixture)
            print(json.dumps({"status": "ok", "articleId": article["id"], "url": article["url"]}, ensure_ascii=False))
        elif args.command == "wait-for-live":
            result = wait_for_live(
                config,
                article_url=args.article_url,
                article_title=args.article_title,
                timeout_seconds=args.timeout_seconds,
            )
            print(json.dumps({"status": "ok", **result}, ensure_ascii=False))
        elif args.command == "send-notification":
            result = send_notification(config, article_title=args.article_title, article_url=args.article_url)
            print(json.dumps({"status": "ok", **result}, ensure_ascii=False))
        return 0
    except PipelineError as error:
        print(json.dumps({"status": "error", "message": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
