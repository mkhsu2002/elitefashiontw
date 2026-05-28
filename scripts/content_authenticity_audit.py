#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUTHENTICITY_LOG = ROOT / "automation" / "content-authenticity-log.json"
ARTICLES_INDEX = ROOT / "data" / "articles-index.json"
LATEST_RUN = ROOT / "automation" / "latest-run.json"
MOMO_TRACKER = ROOT / "automation" / "momo-brand-recommendation-tracker.csv"

AFFILIATE_HOSTS = (
    "https://www.icareushop.com.tw/",
    "https://s.momoshop.com.tw/",
    "https://www.momoshop.com.tw/",
    "https://m.momoshop.com.tw/",
)
YMYL_TERMS = (
    "健康",
    "醫療",
    "醫師",
    "護具",
    "保健",
    "長照",
    "懷孕",
    "孕",
    "症狀",
    "疾病",
    "治療",
    "療效",
    "減重",
    "法律",
    "法規",
    "律師",
    "保險",
    "投資",
    "ETF",
    "基金",
    "股票",
    "房地產",
    "買房",
    "貸款",
    "稅",
    "財務",
    "退休金",
)
UNSUPPORTED_SOURCE_PATTERNS = (
    r"研究指出",
    r"數據顯示",
    r"統計顯示",
    r"報告指出",
    r"官方表示",
    r"官方指出",
    r"專家建議",
    r"臨床(?:研究|實驗|證實)",
    r"最新研究",
)
SOURCE_EVIDENCE_TERMS = (
    "http://",
    "https://",
    "官方網站",
    "官方商品頁",
    "商品頁",
    "momo 商品頁",
    "公開資料",
    "衛福部",
    "健保署",
    "金管會",
    "內政部",
    "財政部",
    "勞動部",
    "FIFA",
    "NASA",
    "AARO",
    "FBI",
    "CIA",
    "McKinsey",
    "BoF",
)
PRICE_STOCK_PATTERNS = (
    r"(?:NT\$|新台幣|台幣)\s*[\d,]+",
    r"[\d,]+\s*元",
    r"[一二三四五六七八九十\d](?:\.\d)?\s*折",
    r"折扣(?:碼|價)?",
    r"限時(?:優惠|特價)",
    r"最低價",
    r"特價",
    r"庫存(?:剩|僅|有限|充足)",
    r"現貨",
    r"(?:排名第|第一名|TOP\s*\d|Top\s*\d)",
)
YMYL_PROMISE_PATTERNS = (
    r"保證",
    r"一定(?:能|會|可以)",
    r"必然",
    r"治癒",
    r"根治",
    r"治療",
    r"預防(?:疾病|失眠|疼痛|退化)",
    r"改善(?:失眠|疼痛|疾病|症狀|血壓|血糖)",
    r"降低(?:風險|死亡率)",
    r"穩賺",
    r"保本",
    r"報酬(?:保證|固定)",
    r"安全無虞",
)
DISCLAIMER_TERMS = (
    "不構成",
    "僅供一般資訊",
    "請諮詢",
    "合格專業",
    "依自身情況",
    "以商品頁公告為準",
    "以官方公告為準",
)
NEGATION_TERMS = ("不", "非", "未", "無", "避免", "不可", "不得", "不構成", "不保證", "不承諾")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strip_tags(raw: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", raw or ""))


def sentence_split(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[。！？!?；;])\s*", text) if part.strip()]


def compact(text: str, limit: int = 120) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else f"{text[:limit]}..."


def article_text(article: dict[str, Any], html_text: str = "") -> str:
    parts: list[str] = []
    for key in ("title", "excerpt", "metaTitle", "metaDescription", "intro", "markdownBody", "disclaimer"):
        value = article.get(key)
        if isinstance(value, str):
            parts.append(value)
    for section in article.get("sections") or []:
        parts.append(str(section.get("heading", "")))
        parts.extend(str(item) for item in section.get("paragraphs") or [])
        parts.extend(str(item) for item in section.get("bullets") or [])
    for item in article.get("faq") or []:
        parts.append(str(item.get("question", "")))
        parts.append(str(item.get("answer", "")))
    if html_text and not any(article.get(key) for key in ("markdownBody", "intro", "sections")):
        parts.append(strip_tags(html_text))
    return "\n".join(parts)


def is_affiliate_url(url: str) -> bool:
    return str(url).startswith(AFFILIATE_HOSTS)


def cta_links(cta: dict[str, Any]) -> list[dict[str, str]]:
    links = cta.get("links")
    if isinstance(links, list):
        return [
            {"label": str(item.get("label", "")), "url": str(item.get("url", ""))}
            for item in links
            if isinstance(item, dict)
        ]
    label = str(cta.get("label", ""))
    url = str(cta.get("url", ""))
    return [{"label": label, "url": url}] if label and url else []


def product_links(article: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    for key in ("mainProducts", "sidebarProducts"):
        for product in article.get(key) or []:
            if isinstance(product, dict):
                urls.extend(
                    str(product.get(url_key, "")).strip()
                    for url_key in ("affiliateUrl", "sourceProductUrl")
                    if product.get(url_key)
                )
    return urls


def has_affiliate(article: dict[str, Any], html_text: str) -> bool:
    urls = [link["url"] for link in cta_links(article.get("cta") or {})]
    urls.extend(product_links(article))
    urls.extend(re.findall(r'href=["\']([^"\']+)["\']', html_text or "", flags=re.I))
    return any(is_affiliate_url(url) for url in urls)


def risk_level(article: dict[str, Any], text: str, affiliate: bool) -> str:
    category = str(article.get("category", ""))
    if category == "wellness-movement" or any(term in text for term in YMYL_TERMS):
        return "high"
    if affiliate or any(re.search(pattern, text, flags=re.I) for pattern in UNSUPPORTED_SOURCE_PATTERNS):
        return "medium"
    return "low"


def sentence_has_source_evidence(sentence: str) -> bool:
    return any(term in sentence for term in SOURCE_EVIDENCE_TERMS)


def sentence_is_disclaimer(sentence: str) -> bool:
    return any(term in sentence for term in DISCLAIMER_TERMS)


def sentence_is_negated(sentence: str, match_start: int) -> bool:
    window = sentence[max(0, match_start - 24) : match_start + 12]
    return any(term in window for term in NEGATION_TERMS)


def load_momo_tracker() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    by_merchant: dict[str, dict[str, str]] = {}
    by_brand: dict[str, dict[str, str]] = {}
    if not MOMO_TRACKER.exists():
        return by_merchant, by_brand
    with MOMO_TRACKER.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            merchant_id = str(row.get("merchant_id", "")).strip()
            brand = str(row.get("brand", "")).strip()
            if merchant_id:
                by_merchant[merchant_id] = row
            if brand:
                by_brand[brand] = row
    return by_merchant, by_brand


def tracker_row_is_blocked(row: dict[str, str]) -> bool:
    joined = " ".join(
        str(row.get(key, ""))
        for key in ("coverage_status", "brand_role", "link_status", "recommendation_grade")
    )
    return "needs-verification" in joined or "paused" in joined


def audit_source_claims(text: str) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    fixes: list[str] = []
    patterns = [re.compile(pattern) for pattern in UNSUPPORTED_SOURCE_PATTERNS]
    for sentence in sentence_split(text):
        for pattern in patterns:
            if pattern.search(sentence) and not sentence_has_source_evidence(sentence):
                note = f"疑似來源宣稱缺少可驗證依據：{compact(sentence)}"
                checks.append({"name": "unsupported-source-claim", "passed": False, "note": note})
                fixes.append(note)
                break
    if not any(check["name"] == "unsupported-source-claim" for check in checks):
        checks.append({"name": "unsupported-source-claim", "passed": True, "note": "未發現無來源的研究、官方、數據或專家宣稱。"})
    return checks, fixes


def audit_price_stock_claims(text: str) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    fixes: list[str] = []
    patterns = [re.compile(pattern, flags=re.I) for pattern in PRICE_STOCK_PATTERNS]
    for sentence in sentence_split(text):
        if sentence_is_disclaimer(sentence):
            continue
        for pattern in patterns:
            if pattern.search(sentence) and not sentence_has_source_evidence(sentence):
                note = f"價格、折扣、庫存或排名宣稱缺少來源：{compact(sentence)}"
                checks.append({"name": "price-stock-claim", "passed": False, "note": note})
                fixes.append(note)
                break
    if not any(check["name"] == "price-stock-claim" for check in checks):
        checks.append({"name": "price-stock-claim", "passed": True, "note": "未發現未佐證的價格、折扣、庫存或排名宣稱。"})
    return checks, fixes


def audit_ymyl(text: str, current_risk: str) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    fixes: list[str] = []
    if current_risk != "high":
        checks.append({"name": "ymyl-risk", "passed": True, "note": "未判定為高風險 YMYL 題材。"})
        return checks, fixes

    has_disclaimer = any(term in text for term in DISCLAIMER_TERMS)
    if has_disclaimer:
        checks.append({"name": "ymyl-disclaimer", "passed": True, "note": "已出現保守表述或專業諮詢提醒。"})
    else:
        note = "高風險健康、法律、投資、保險、房地產或財務題材缺少保守提醒。"
        checks.append({"name": "ymyl-disclaimer", "passed": False, "note": note})
        fixes.append(note)

    patterns = [re.compile(pattern) for pattern in YMYL_PROMISE_PATTERNS]
    for sentence in sentence_split(text):
        for pattern in patterns:
            match = pattern.search(sentence)
            if match and not sentence_is_negated(sentence, match.start()):
                note = f"高風險題材出現保證式或療效/報酬宣稱：{compact(sentence)}"
                checks.append({"name": "ymyl-promise", "passed": False, "note": note})
                fixes.append(note)
                break
    if not any(check["name"] == "ymyl-promise" for check in checks):
        checks.append({"name": "ymyl-promise", "passed": True, "note": "未發現保證療效、報酬、安全或結果的表述。"})
    return checks, fixes


def audit_affiliate(article: dict[str, Any], html_text: str, affiliate: bool) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    fixes: list[str] = []
    if not affiliate:
        checks.append({"name": "affiliate-disclosure", "passed": True, "note": "未偵測到導購連結。"})
        return checks, fixes

    if "導購揭露" in html_text:
        checks.append({"name": "affiliate-disclosure", "passed": True, "note": "HTML 含可見導購揭露。"})
    else:
        note = "導購文章缺少可見導購揭露。"
        checks.append({"name": "affiliate-disclosure", "passed": False, "note": note})
        fixes.append(note)

    rel_failures: list[str] = []
    for tag in re.findall(r"<a\b[^>]*>", html_text or "", flags=re.I):
        href_match = re.search(r'href=["\']([^"\']+)["\']', tag, flags=re.I)
        if not href_match or not is_affiliate_url(href_match.group(1)):
            continue
        rel_match = re.search(r'rel=["\']([^"\']+)["\']', tag, flags=re.I)
        rel = rel_match.group(1).lower() if rel_match else ""
        if "sponsored" not in rel or "nofollow" not in rel:
            rel_failures.append(href_match.group(1))
    if rel_failures:
        note = f"導購連結缺少 sponsored nofollow：{', '.join(rel_failures[:3])}"
        checks.append({"name": "affiliate-rel", "passed": False, "note": note})
        fixes.append(note)
    else:
        checks.append({"name": "affiliate-rel", "passed": True, "note": "導購連結皆含 sponsored nofollow。"})

    missing_sources: list[str] = []
    for key in ("mainProducts", "sidebarProducts"):
        for product in article.get(key) or []:
            if not str(product.get("sourceProductUrl", "")).strip():
                missing_sources.append(str(product.get("name") or product.get("code") or "未命名商品"))
    if missing_sources:
        note = f"商品資料缺少 sourceProductUrl：{', '.join(missing_sources[:5])}"
        checks.append({"name": "product-source-url", "passed": False, "note": note})
        fixes.append(note)
    else:
        checks.append({"name": "product-source-url", "passed": True, "note": "商品資料皆有 sourceProductUrl，或本篇無商品卡。"})

    tracker_by_merchant, tracker_by_brand = load_momo_tracker()
    blocked: list[str] = []
    for key in ("mainProducts", "sidebarProducts", "featuredBrands"):
        for item in article.get(key) or []:
            merchant_id = str(item.get("merchantId", "")).strip()
            brand = str(item.get("brandName") or item.get("name") or "").strip()
            row = tracker_by_merchant.get(merchant_id) or tracker_by_brand.get(brand)
            if row and tracker_row_is_blocked(row):
                blocked.append(brand or merchant_id)
    if blocked:
        note = f"momo 追蹤表標示需查證或暫緩，不能強推薦：{', '.join(blocked[:5])}"
        checks.append({"name": "momo-tracker-status", "passed": False, "note": note})
        fixes.append(note)
    else:
        checks.append({"name": "momo-tracker-status", "passed": True, "note": "未使用需查證或暫緩的 momo 品牌作為推薦。"})

    return checks, fixes


def source_evidence(article: dict[str, Any], html_text: str) -> list[str]:
    evidence: list[str] = []
    for key in ("mainProducts", "sidebarProducts"):
        for product in article.get(key) or []:
            source_url = str(product.get("sourceProductUrl", "")).strip()
            if source_url:
                evidence.append(source_url)
    evidence.extend(re.findall(r"https?://[^\s\"'<>)]+", article.get("markdownBody", "")))
    evidence.extend(re.findall(r"https?://[^\s\"'<>)]+", html_text or ""))
    deduped: list[str] = []
    seen: set[str] = set()
    for item in evidence:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped[:20]


def audit_article_record(
    article: dict[str, Any],
    *,
    html_text: str = "",
    reviewer: str = "automation",
) -> dict[str, Any]:
    if not html_text and article.get("file"):
        html_path = ROOT / str(article["file"])
        if html_path.exists():
            html_text = html_path.read_text(encoding="utf-8")
    text = article_text(article, html_text)
    affiliate = has_affiliate(article, html_text)
    current_risk = risk_level(article, text, affiliate)

    claim_checks: list[dict[str, Any]] = []
    required_fixes: list[str] = []
    for check_group, fixes in (
        audit_source_claims(text),
        audit_price_stock_claims(text),
        audit_ymyl(text, current_risk),
        audit_affiliate(article, html_text, affiliate),
    ):
        claim_checks.extend(check_group)
        required_fixes.extend(fixes)

    publish_ready = not required_fixes
    return {
        "articleId": article.get("id", ""),
        "slug": article.get("slug", ""),
        "riskLevel": current_risk,
        "checkedAt": now_iso(),
        "publishReady": publish_ready,
        "claimChecks": claim_checks,
        "requiredFixes": required_fixes,
        "sourceEvidence": source_evidence(article, html_text),
        "reviewer": reviewer,
    }


def upsert_audit_log(review: dict[str, Any]) -> None:
    payload = load_json(AUTHENTICITY_LOG, default={"version": 1, "updatedAt": now_iso(), "entries": []})
    entries = [
        entry
        for entry in payload.get("entries", [])
        if not (
            entry.get("articleId") == review.get("articleId")
            and entry.get("slug") == review.get("slug")
        )
    ]
    entries.insert(0, review)
    payload["version"] = payload.get("version", 1)
    payload["updatedAt"] = now_iso()
    payload["entries"] = entries
    write_json(AUTHENTICITY_LOG, payload)


def audit_article_for_publish(article: dict[str, Any], *, reviewer: str = "automation", write_log: bool = True) -> dict[str, Any]:
    review = audit_article_record(article, reviewer=reviewer)
    if write_log:
        upsert_audit_log(review)
    if not review["publishReady"]:
        raise RuntimeError("文章真實性審核未通過：" + "；".join(review["requiredFixes"]))
    return review


def load_article_by_id(article_id: str) -> dict[str, Any]:
    index = load_json(ARTICLES_INDEX, default={"items": []})
    row = next((item for item in index.get("items", []) if item.get("id") == article_id), None)
    if not row:
        raise SystemExit(f"找不到 article id：{article_id}")
    metadata_path = ROOT / "automation" / "articles" / f"{row['slug']}.json"
    if metadata_path.exists():
        return load_json(metadata_path)
    return row


def load_article_by_slug(slug: str) -> dict[str, Any]:
    metadata_path = ROOT / "automation" / "articles" / f"{slug}.json"
    if metadata_path.exists():
        return load_json(metadata_path)
    index = load_json(ARTICLES_INDEX, default={"items": []})
    row = next((item for item in index.get("items", []) if item.get("slug") == slug), None)
    if not row:
        raise SystemExit(f"找不到 slug：{slug}")
    return row


def load_latest_article() -> dict[str, Any] | None:
    latest = load_json(LATEST_RUN, default={})
    if latest.get("status") != "generated":
        return None
    article_id = latest.get("articleId")
    if not article_id:
        return None
    return load_article_by_id(article_id)


def load_all_articles() -> list[dict[str, Any]]:
    index = load_json(ARTICLES_INDEX, default={"items": []})
    return [load_article_by_id(item["id"]) for item in index.get("items", []) if item.get("id")]


def run_cli() -> int:
    parser = argparse.ArgumentParser(description="Audit Elite Fashion article authenticity before publishing.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--latest", action="store_true", help="Audit latest generated article from automation/latest-run.json")
    target.add_argument("--article-id")
    target.add_argument("--slug")
    target.add_argument("--all", action="store_true")
    parser.add_argument("--no-write-log", action="store_true")
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args()

    if args.latest:
        latest_article = load_latest_article()
        if latest_article is None:
            print(json.dumps({"status": "skipped", "reason": "latest run is not a generated article"}, ensure_ascii=False))
            return 0
        articles = [latest_article]
    elif args.article_id:
        articles = [load_article_by_id(args.article_id)]
    elif args.slug:
        articles = [load_article_by_slug(args.slug)]
    else:
        articles = load_all_articles()

    reviews = []
    failed = []
    for article in articles:
        review = audit_article_record(article)
        reviews.append(review)
        if not args.no_write_log:
            upsert_audit_log(review)
        if not review["publishReady"]:
            failed.append(review)

    result = {
        "status": "ok" if not failed else "failed",
        "audited": len(reviews),
        "failed": len(failed),
        "reviews": [
            {
                "articleId": review["articleId"],
                "slug": review["slug"],
                "riskLevel": review["riskLevel"],
                "publishReady": review["publishReady"],
                "requiredFixes": review["requiredFixes"],
            }
            for review in reviews
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failed and not args.warn_only:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
