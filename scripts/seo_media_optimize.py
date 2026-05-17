#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
from collections import defaultdict
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://tw.elitefasion.com"
ARTICLES_INDEX = ROOT / "data" / "articles-index.json"
WIDTH_SOCIAL = 1200
HEIGHT_SOCIAL = 630
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}

SOCIAL_IMAGE_SOURCES = {
    "images/og-main.jpg": "images/generated/fashion-1.png",
    "images/og-casual-chic.jpg": "images/generated/casual/travel-wear.png",
    "images/og-ai-innovation.jpg": "images/generated/ai/creative-sovereignty.png",
    "images/og-wellness-movement.jpg": "images/generated/wellness-1.png",
    "images/og-lifestyle-culture.jpg": "images/generated/fashion-1.png",
    "images/og-outdoor-escapes.jpg": "images/generated/outdoor-1.png",
    "images/og-runway-trends.jpg": "images/generated/runway/color-trends.png",
    "images/og-designer-perspective.jpg": "images/generated/designer/ai-design.png",
    "images/og-spring-summer.jpg": "images/generated/casual/travel-wear.png",
}

PAGE_SOCIAL_IMAGES = {
    "index.html": "images/og-main.jpg",
    "about.html": "images/og-main.jpg",
    "contact.html": "images/og-main.jpg",
    "all-articles.html": "images/og-main.jpg",
    "search.html": "images/og-main.jpg",
    "ai-innovation.html": "images/og-ai-innovation.jpg",
    "ai-work-reset-45.html": "images/og-ai-innovation.jpg",
    "casual-chic.html": "images/og-casual-chic.jpg",
    "spring-summer-capsule-wardrobe.html": "images/og-casual-chic.jpg",
    "body-rhythm-reset.html": "images/og-wellness-movement.jpg",
    "wellness-movement.html": "images/og-wellness-movement.jpg",
    "mature-life-reset.html": "images/og-lifestyle-culture.jpg",
    "lifestyle-culture.html": "images/og-lifestyle-culture.jpg",
    "outdoor-escapes.html": "images/og-outdoor-escapes.jpg",
    "runway-trends.html": "images/og-runway-trends.jpg",
    "trend-translation-2026.html": "images/og-runway-trends.jpg",
    "designer-perspective.html": "images/og-designer-perspective.jpg",
    "spring-summer-2026.html": "images/og-spring-summer.jpg",
}

COLLECTION_PAGE_NAMES = {
    "ai-innovation.html": "人工智能",
    "ai-work-reset-45.html": "45+ AI 工作重整",
    "casual-chic.html": "休閒時尚",
    "body-rhythm-reset.html": "熟齡健康恢復與身體節奏",
    "wellness-movement.html": "健康恢復",
    "mature-life-reset.html": "熟齡人生重整",
    "lifestyle-culture.html": "生活品味",
    "outdoor-escapes.html": "戶外生活",
    "runway-trends.html": "秀場趨勢",
    "trend-translation-2026.html": "2026 春夏趨勢轉譯",
    "designer-perspective.html": "設計師視角",
    "spring-summer-2026.html": "2026 春夏熟齡生活企劃",
    "spring-summer-capsule-wardrobe.html": "春夏旅行膠囊衣櫥",
    "all-articles.html": "所有文章列表",
    "search.html": "站內搜尋",
}

WEB_PAGE_SCHEMA_TYPES = {
    "about.html": "AboutPage",
    "contact.html": "ContactPage",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_articles() -> dict[str, dict[str, Any]]:
    payload = json.loads(ARTICLES_INDEX.read_text(encoding="utf-8"))
    return {
        str(item.get("file") or item.get("relativeUrl")): item
        for item in payload.get("items", [])
    }


def public_url(path: str) -> str:
    return f"{BASE_URL}/{path.lstrip('/')}"


def canonical_for(page_rel: str) -> str:
    if page_rel == "index.html":
        return f"{BASE_URL}/"
    return public_url(page_rel)


def normalize_local_ref(ref: str, page_rel: str, *, site_absolute_as_root: bool = True) -> str:
    value = html.unescape(ref).strip().strip("\"'")
    value = value.split("#", 1)[0].split("?", 1)[0]
    for base in (f"{BASE_URL}/", "https://tw.elitefashion.com/"):
        if value.startswith(base):
            value = value.removeprefix(base)
            return value.lstrip("/") if site_absolute_as_root else value
    if value.startswith(("http://", "https://", "data:")):
        return value
    if value.startswith("/"):
        return value.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(page_rel), value))


def is_noindex(content: str, page_rel: str) -> bool:
    if page_rel == "404.html":
        return True
    match = re.search(
        r"<meta[^>]+name=[\"']robots[\"'][^>]+content=[\"']([^\"']*)",
        content,
        flags=re.I,
    )
    return bool(match and "noindex" in match.group(1).lower())


def compact_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def strip_tags(value: str) -> str:
    value = re.sub(r"<script.*?</script>", " ", value, flags=re.S | re.I)
    value = re.sub(r"<style.*?</style>", " ", value, flags=re.S | re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return compact_text(value)


def get_title(content: str) -> str:
    match = re.search(r"<title>(.*?)</title>", content, flags=re.S | re.I)
    return compact_text(match.group(1)) if match else ""


def get_meta(content: str, name: str) -> str:
    patterns = [
        rf"<meta\s+[^>]*(?:name|property)=[\"']{re.escape(name)}[\"'][^>]*content=[\"']([^\"']*)",
        rf"<meta\s+[^>]*content=[\"']([^\"']*)[\"'][^>]*(?:name|property)=[\"']{re.escape(name)}[\"']",
    ]
    for pattern in patterns:
        match = re.search(pattern, content, flags=re.I | re.S)
        if match:
            return compact_text(match.group(1))
    return ""


def get_description(content: str) -> str:
    return get_meta(content, "description")


def get_h1(content: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", content, flags=re.S | re.I)
    return strip_tags(match.group(1)) if match else ""


def get_published_time(content: str, article: dict[str, Any]) -> str:
    for key in ("article:published_time", "datePublished"):
        value = get_meta(content, key)
        if value:
            return value
    time_match = re.search(r"<time[^>]+datetime=[\"']([^\"']+)", content, flags=re.I)
    if time_match:
        return compact_text(time_match.group(1))
    return str(article.get("publishedAt") or "")


def set_or_insert_meta(content: str, name: str, value: str, *, attr: str | None = None) -> str:
    attr = attr or ("property" if name.startswith(("og:", "article:")) else "name")
    escaped_name = re.escape(name)
    tag = f'    <meta {attr}="{name}" content="{html.escape(value, quote=True)}">'
    patterns = [
        re.compile(
            rf"(<meta\s+[^>]*(?:name|property)=[\"']{escaped_name}[\"'][^>]*content=[\"'])([^\"']*)([\"'][^>]*>)",
            flags=re.I | re.S,
        ),
        re.compile(
            rf"(<meta\s+[^>]*content=[\"'])([^\"']*)([\"'][^>]*(?:name|property)=[\"']{escaped_name}[\"'][^>]*>)",
            flags=re.I | re.S,
        ),
    ]
    for pattern in patterns:
        if pattern.search(content):
            return pattern.sub(rf"\g<1>{html.escape(value, quote=True)}\g<3>", content, count=1)
    head_end = content.lower().find("</head>")
    if head_end < 0:
        return content
    return content[:head_end] + tag + "\n" + content[head_end:]


def ensure_canonical(content: str, url: str) -> str:
    tag = f'    <link rel="canonical" href="{html.escape(url, quote=True)}">'
    pattern = re.compile(r"<link\s+[^>]*rel=[\"']canonical[\"'][^>]*>", flags=re.I | re.S)
    if pattern.search(content):
        return pattern.sub(tag, content, count=1)
    head_end = content.lower().find("</head>")
    return content[:head_end] + tag + "\n" + content[head_end:] if head_end >= 0 else content


def ensure_json_ld(content: str, payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    block = f'    <script type="application/ld+json">\n{serialized}\n    </script>\n'
    head_end = content.lower().find("</head>")
    return content[:head_end] + block + content[head_end:] if head_end >= 0 else content


def has_json_ld(content: str) -> bool:
    return "application/ld+json" in content.lower()


def local_image_refs(content: str, page_rel: str) -> set[str]:
    refs: set[str] = set()
    patterns = [
        r"<img[^>]+src=[\"']([^\"']+)",
        r"<source[^>]+srcset=[\"']([^\"']+)",
        r"<meta[^>]+(?:property|name)=[\"'](?:og:image|twitter:image)[\"'][^>]+content=[\"']([^\"']+)",
        r"<meta[^>]+content=[\"']([^\"']+)[\"'][^>]+(?:property|name)=[\"'](?:og:image|twitter:image)[\"']",
        r"url\([\"']?([^\"')]+)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, content, flags=re.I):
            raw = match.group(1)
            parts = [item.strip().split()[0] for item in raw.split(",")] if "," in raw else [raw]
            for part in parts:
                normalized = normalize_local_ref(part, page_rel)
                if normalized.startswith(("http://", "https://", "data:")):
                    continue
                if Path(normalized).suffix.lower() in IMAGE_EXTENSIONS:
                    refs.add(normalized)
    return refs


def image_dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def flatten(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGB", "L"):
        return image.convert("RGB")
    background = Image.new("RGB", image.size, (255, 255, 255))
    if "A" in image.getbands():
        background.paste(image, mask=image.getchannel("A"))
    else:
        background.paste(image)
    return background


def center_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    image = flatten(image)
    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def save_jpeg(path: Path, image: Image.Image, quality: int = 82) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="JPEG", quality=quality, optimize=True, progressive=True)


def save_webp(path: Path, image: Image.Image, quality: int = 82) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="WEBP", quality=quality, method=6)


def resize_max(image: Image.Image, *, max_width: int | None = None, max_long: int | None = None) -> Image.Image:
    image = flatten(image)
    if max_width is not None and image.width > max_width:
        scale = max_width / image.width
    elif max_long is not None and max(image.size) > max_long:
        scale = max_long / max(image.size)
    else:
        scale = 1.0
    if scale >= 1:
        return image
    return image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )


def make_social_images() -> list[str]:
    written: list[str] = []
    for target, source in SOCIAL_IMAGE_SOURCES.items():
        source_path = ROOT / source
        target_path = ROOT / target
        if not source_path.exists():
            continue
        with Image.open(source_path) as image:
            card = center_crop(image, WIDTH_SOCIAL, HEIGHT_SOCIAL)
        before = target_path.read_bytes() if target_path.exists() else None
        save_jpeg(target_path, card, quality=84)
        if before != target_path.read_bytes():
            written.append(target)
    return written


def rewrite_refs_in_content(content: str, replacements: dict[str, str], page_rel: str) -> str:
    def replace_ref(raw: str) -> str:
        if raw.startswith(("http://", "https://", "data:")):
            normalized = normalize_local_ref(raw, page_rel)
            if normalized in replacements and raw.startswith(BASE_URL):
                return public_url(replacements[normalized])
            return raw
        normalized = normalize_local_ref(raw, page_rel)
        replacement = replacements.get(normalized)
        if not replacement:
            return raw
        prefix = ""
        suffix = ""
        if "?" in raw:
            suffix = "?" + raw.split("?", 1)[1]
        if raw.startswith("/"):
            return "/" + replacement + suffix
        page_dir = posixpath.dirname(page_rel)
        if page_dir:
            return posixpath.relpath(replacement, page_dir) + suffix
        return replacement + suffix

    def src_repl(match: re.Match[str]) -> str:
        return f'{match.group(1)}{replace_ref(match.group(2))}{match.group(3)}'

    content = re.sub(r"(<img[^>]+src=[\"'])([^\"']+)([\"'])", src_repl, content, flags=re.I)
    content = re.sub(r"(<source[^>]+srcset=[\"'])([^\"']+)([\"'])", src_repl, content, flags=re.I)

    def url_repl(match: re.Match[str]) -> str:
        quote = match.group(1) or ""
        return f"url({quote}{replace_ref(match.group(2))}{quote})"

    return re.sub(r"url\(([\"']?)([^\"')]+)\1\)", url_repl, content, flags=re.I)


def collect_referenced_images() -> dict[str, set[str]]:
    by_image: dict[str, set[str]] = defaultdict(set)
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        page_rel = rel(path)
        content = path.read_text(encoding="utf-8", errors="ignore")
        for ref in local_image_refs(content, page_rel):
            if (ROOT / ref).exists():
                by_image[ref].add(page_rel)
    return by_image


def optimize_referenced_images() -> dict[str, Any]:
    by_image = collect_referenced_images()
    replacements: dict[str, str] = {}
    optimized: list[dict[str, Any]] = []

    for image_rel, pages in sorted(by_image.items()):
        path = ROOT / image_rel
        suffix = path.suffix.lower()
        size = path.stat().st_size
        if image_rel.startswith("images/generated/") and suffix == ".png" and size > 300 * 1024:
            target_rel = str(path.with_suffix(".webp").relative_to(ROOT)).replace(os.sep, "/")
            with Image.open(path) as image:
                output = resize_max(image, max_long=900)
            save_webp(ROOT / target_rel, output, quality=82)
            replacements[image_rel] = target_rel
            optimized.append(
                {
                    "source": image_rel,
                    "target": target_rel,
                    "originalKB": round(size / 1024, 1),
                    "newKB": round((ROOT / target_rel).stat().st_size / 1024, 1),
                    "pages": sorted(pages),
                }
            )
        elif image_rel.startswith("images/crossbody-bag/") and suffix in {".jpg", ".jpeg"} and size > 400 * 1024:
            before = size
            with Image.open(path) as image:
                output = resize_max(image, max_long=1600)
            save_jpeg(path, output, quality=82)
            optimized.append(
                {
                    "source": image_rel,
                    "target": image_rel,
                    "originalKB": round(before / 1024, 1),
                    "newKB": round(path.stat().st_size / 1024, 1),
                    "pages": sorted(pages),
                }
            )
        elif image_rel.startswith("images/generated/ai/chatgpt-image-2-prompts-") and suffix in {".jpg", ".jpeg"} and size > 300 * 1024:
            before = size
            with Image.open(path) as image:
                output = resize_max(image, max_width=1400)
            save_jpeg(path, output, quality=82)
            optimized.append(
                {
                    "source": image_rel,
                    "target": image_rel,
                    "originalKB": round(before / 1024, 1),
                    "newKB": round(path.stat().st_size / 1024, 1),
                    "pages": sorted(pages),
                }
            )

    if replacements:
        for path in ROOT.rglob("*.html"):
            if ".git" in path.parts:
                continue
            page_rel = rel(path)
            content = path.read_text(encoding="utf-8")
            updated = rewrite_refs_in_content(content, replacements, page_rel)
            if updated != content:
                path.write_text(updated, encoding="utf-8")

    return {"optimized": optimized, "replacements": replacements}


def article_json_ld(article: dict[str, Any], page_rel: str, title: str, description: str, image_url: str) -> dict[str, Any]:
    published = str(article.get("publishedAt") or "")
    payload: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article.get("title") or title,
        "description": article.get("metaDescription") or description,
        "image": image_url,
        "datePublished": published,
        "author": {"@type": "Organization", "name": "Elite Fashion Editorial Team"},
        "publisher": {
            "@type": "Organization",
            "name": "Elite Fashion",
            "logo": {"@type": "ImageObject", "url": public_url("images/logo.jpg")},
        },
        "mainEntityOfPage": canonical_for(page_rel),
        "inLanguage": "zh-TW",
    }
    if article.get("categoryLabel"):
        payload["articleSection"] = article["categoryLabel"]
    if article.get("tags"):
        payload["keywords"] = ", ".join(str(tag) for tag in article["tags"])
    if published:
        payload["dateModified"] = published
    return payload


def collection_json_ld(page_rel: str, title: str, description: str) -> dict[str, Any]:
    name = COLLECTION_PAGE_NAMES.get(page_rel, re.sub(r"\s+\|\s+Elite Fashion.*$", "", title))
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": name,
        "description": description,
        "url": canonical_for(page_rel),
        "inLanguage": "zh-TW",
        "isPartOf": {"@type": "WebSite", "name": "Elite Fashion", "url": BASE_URL},
    }


def web_page_json_ld(page_rel: str, title: str, description: str) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": WEB_PAGE_SCHEMA_TYPES.get(page_rel, "WebPage"),
        "name": re.sub(r"\s+\|\s+Elite Fashion.*$", "", title),
        "description": description,
        "url": canonical_for(page_rel),
        "inLanguage": "zh-TW",
        "isPartOf": {"@type": "WebSite", "name": "Elite Fashion", "url": BASE_URL},
        "publisher": {"@type": "Organization", "name": "Elite Fashion", "url": BASE_URL},
    }


def breadcrumb_json_ld(page_rel: str, title: str) -> dict[str, Any]:
    items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "首頁",
            "item": f"{BASE_URL}/",
        }
    ]
    label = COLLECTION_PAGE_NAMES.get(page_rel) or re.sub(r"\s+\|\s+Elite Fashion.*$", "", title)
    if page_rel != "index.html":
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": label,
                "item": canonical_for(page_rel),
            }
        )
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def ensure_meta_for_pages() -> dict[str, Any]:
    articles = load_articles()
    changed: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        page_rel = rel(path)
        content = path.read_text(encoding="utf-8")
        if is_noindex(content, page_rel):
            continue

        original = content
        article = articles.get(page_rel)
        title = get_title(content)
        description = get_description(content)
        h1 = get_h1(content)
        clean_title = re.sub(r"\s+\|\s+Elite Fashion.*$", "", title)

        if article:
            description = article.get("metaDescription") or article.get("excerpt") or description
            clean_title = article.get("metaTitle") or article.get("title") or clean_title
            og_image_rel = str(article.get("heroImage") or "")
        else:
            og_image_rel = PAGE_SOCIAL_IMAGES.get(page_rel, "images/og-main.jpg")

        og_image_url = public_url(og_image_rel)
        page_type = "article" if article else "website"
        if page_rel == "search.html":
            page_type = "website"

        content = ensure_canonical(content, canonical_for(page_rel))
        content = set_or_insert_meta(content, "og:type", page_type, attr="property")
        content = set_or_insert_meta(content, "og:url", canonical_for(page_rel), attr="property")
        content = set_or_insert_meta(content, "og:locale", "zh_TW", attr="property")
        content = set_or_insert_meta(content, "og:title", clean_title or h1 or title, attr="property")
        content = set_or_insert_meta(content, "og:description", description, attr="property")
        content = set_or_insert_meta(content, "og:image", og_image_url, attr="property")
        if article:
            published = get_published_time(content, article)
            if published:
                content = set_or_insert_meta(content, "article:published_time", published, attr="property")
        content = set_or_insert_meta(content, "twitter:card", "summary_large_image")
        content = set_or_insert_meta(content, "twitter:title", clean_title or h1 or title)
        content = set_or_insert_meta(content, "twitter:description", description)
        content = set_or_insert_meta(content, "twitter:image", og_image_url)

        if not has_json_ld(content):
            if article:
                content = ensure_json_ld(
                    content,
                    article_json_ld(article, page_rel, clean_title or title, description, og_image_url),
                )
            elif page_rel in COLLECTION_PAGE_NAMES:
                content = ensure_json_ld(content, collection_json_ld(page_rel, clean_title or title, description))
                content = ensure_json_ld(content, breadcrumb_json_ld(page_rel, clean_title or title))
            elif page_rel in WEB_PAGE_SCHEMA_TYPES:
                content = ensure_json_ld(content, web_page_json_ld(page_rel, clean_title or title, description))
                content = ensure_json_ld(content, breadcrumb_json_ld(page_rel, clean_title or title))

        if content != original:
            path.write_text(content, encoding="utf-8")
            changed.append(page_rel)

    return {"changedPages": changed}


def missing_local_image_refs() -> dict[str, list[str]]:
    missing: dict[str, set[str]] = defaultdict(set)
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        page_rel = rel(path)
        content = path.read_text(encoding="utf-8", errors="ignore")
        for ref in local_image_refs(content, page_rel):
            if ref.startswith(("http://", "https://", "data:")):
                continue
            if not (ROOT / ref).exists():
                missing[ref].add(page_rel)
    return {key: sorted(value) for key, value in sorted(missing.items())}


def audit() -> dict[str, Any]:
    articles = load_articles()
    image_refs = collect_referenced_images()
    image_rows = []
    for image_rel, pages in image_refs.items():
        path = ROOT / image_rel
        if not path.exists():
            continue
        try:
            width, height = image_dimensions(path)
        except Exception:
            width, height = None, None
        image_rows.append(
            {
                "file": image_rel,
                "kb": round(path.stat().st_size / 1024, 1),
                "width": width,
                "height": height,
                "pages": sorted(pages),
            }
        )
    large = sorted([row for row in image_rows if row["kb"] > 300], key=lambda row: -row["kb"])

    meta_missing: dict[str, list[str]] = defaultdict(list)
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        page_rel = rel(path)
        content = path.read_text(encoding="utf-8", errors="ignore")
        if is_noindex(content, page_rel):
            continue
        checks = {
            "title": bool(get_title(content)),
            "description": bool(get_description(content)),
            "canonical": bool(re.search(r"<link[^>]+rel=[\"']canonical[\"']", content, flags=re.I)),
            "og_type": bool(get_meta(content, "og:type")),
            "og_title": bool(get_meta(content, "og:title")),
            "og_description": bool(get_meta(content, "og:description")),
            "og_image": bool(get_meta(content, "og:image")),
            "twitter_card": bool(get_meta(content, "twitter:card")),
            "json_ld": has_json_ld(content),
        }
        for key, ok in checks.items():
            if not ok:
                meta_missing[key].append(page_rel)

    article_missing_json_ld = [
        page_rel
        for page_rel in articles
        if not is_noindex((ROOT / page_rel).read_text(encoding="utf-8", errors="ignore"), page_rel)
        and not has_json_ld((ROOT / page_rel).read_text(encoding="utf-8", errors="ignore"))
    ]
    return {
        "referencedImages": len(image_rows),
        "referencedImagesOver300KB": len(large),
        "largeReferencedImages": large[:80],
        "missingLocalImageRefs": missing_local_image_refs(),
        "metaMissingCounts": {key: len(value) for key, value in sorted(meta_missing.items())},
        "metaMissingSamples": {key: value[:20] for key, value in sorted(meta_missing.items()) if value},
        "articlePagesMissingJsonLd": len(article_missing_json_ld),
    }


def run_apply() -> dict[str, Any]:
    social = make_social_images()
    images = optimize_referenced_images()
    meta = ensure_meta_for_pages()
    return {"socialImages": social, "images": images, "meta": meta, "audit": audit()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["apply", "audit"])
    args = parser.parse_args()
    result = run_apply() if args.command == "apply" else audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
