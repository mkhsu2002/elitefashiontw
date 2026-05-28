#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

from content_authenticity_audit import audit_article_record


ROOT = Path(__file__).resolve().parents[1]
ARTICLES_INDEX = ROOT / "data" / "articles-index.json"
BATCH_1_SIZE = 21
BATCH_1_PRIORITY_SLUGS = (
    "camping-coffee-outdoor-meal-prep",
    "night-mobility-reflective-dashcam-support-sleep-kit",
    "scooter-commute-rain-gear-reflective-accessories",
    "eye-care-presbyopia",
    "solo-living-stabilization-taiwan-returnees",
    "solopreneur-daily-rhythm-outsourcing-strategy",
    "ai-health-longevity",
    "pregnancy-safe-exercise-guide",
    "post-divorce-first-6-steps",
    "return-divorce-restart-90-day-checklist",
    "中年未婚女性獨居評估與行動清單",
    "trust-network-women-entrepreneur",
    "ai-pet-care",
    "metro-vancouver-2026-investment-plan",
    "neobabylon-taiwan-sci-fi-story",
    "arsenal-mit-japan-stainless-scissors-project",
    "high-level-female-executive-post-divorce-social-reconstruction",
    "midlife-divorce-entrepreneur-priority",
    "rebuild-social-circle-after-returning-to-taiwan",
    "returning-taiwan-first-year-unmarried-women",
    "chatgpt-image-2-prompts-elite-women",
)
BATCH_1_PRIORITY_ORDER = {slug: index for index, slug in enumerate(BATCH_1_PRIORITY_SLUGS)}

HEALTH_TERMS = (
    "健康",
    "醫療",
    "醫師",
    "護具",
    "保健",
    "長照",
    "懷孕",
    "孕期",
    "症狀",
    "疾病",
    "治療",
    "療效",
    "睡眠",
    "按摩",
    "身體恢復",
    "熱感",
    "肌力",
    "瑜伽",
    "伸展",
    "照護",
    "飲水",
    "餵食",
    "毛孩",
    "失眠",
    "焦慮",
    "心悸",
    "關節",
    "骨骼",
    "血糖",
    "更年期",
    "牙齒",
    "視力",
    "體態",
    "呼吸法",
)
TEACHING_TERMS = (
    "教學",
    "課程",
    "學習",
    "提示詞",
    "指令",
    "入門",
    "新手",
    "實作",
    "導入",
    "工作流",
    "流程",
    "步驟",
    "怎麼開始",
    "如何建立",
    "如何使用",
    "清單",
    "檢查表",
)
THIRD_PARTY_TERMS = (
    "momo",
    "momoshop",
    "icareushop",
    "Petek",
    "ARSENAL",
    "Lululemon",
    "Ministry of Supply",
    "Systeme.io",
    "Systeme",
    "OpenAI",
    "ChatGPT",
    "Google",
    "FIFA",
    "World Cup",
    "NASA",
    "AARO",
    "FBI",
    "CIA",
    "McKinsey",
    "BoF",
    "BC 省",
    "加拿大",
    "溫哥華",
    "多倫多",
    "健保署",
    "衛福部",
    "金管會",
    "內政部",
    "財政部",
    "勞動部",
    "法院",
    "政府",
    "銀行",
    "保險公司",
    "醫院",
    "學校",
    "官方商品頁",
    "官方網站",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def article_for(item: dict[str, Any]) -> dict[str, Any]:
    metadata_path = ROOT / "automation" / "articles" / f"{item['slug']}.json"
    if metadata_path.exists():
        return load_json(metadata_path)
    return dict(item)


def article_html(item: dict[str, Any]) -> str:
    html_path = ROOT / str(item.get("file", ""))
    if html_path.exists():
        return html_path.read_text(encoding="utf-8", errors="ignore")
    return ""


def article_text(article: dict[str, Any]) -> str:
    keys = ("title", "excerpt", "metaTitle", "metaDescription", "intro", "markdownBody", "category", "series", "audience")
    return "\n".join(str(article.get(key, "") or "") for key in keys)


def external_urls(text: str, html_text: str) -> list[str]:
    urls = re.findall(r"https?://[^\s\"'<>)]+" , text + "\n" + html_text)
    return [
        url
        for url in urls
        if "elitefasion.com" not in url
        and "elitefashiontw" not in url
        and "schema.org" not in url
        and "w3.org" not in url
    ]


def score_entry(article: dict[str, Any], html_text: str, review: dict[str, Any]) -> tuple[int, str]:
    text = article_text(article)
    health_hits = [term for term in HEALTH_TERMS if term in text]
    teaching_hits = [term for term in TEACHING_TERMS if term in text]
    third_party_hits = [term for term in THIRD_PARTY_TERMS if term in text or term in html_text]
    product_fields = bool(article.get("mainProducts") or article.get("sidebarProducts") or article.get("featuredBrands"))
    urls = external_urls(text, html_text)
    if not (health_hits or teaching_hits):
        return 0, ""
    if not (third_party_hits or product_fields or urls):
        return 0, ""

    score = 0
    if review["riskLevel"] == "high":
        score += 3
    elif review["riskLevel"] == "medium":
        score += 2
    if review["requiredFixes"]:
        score += 3
    if product_fields or any("momoshop" in url or "icareushop" in url for url in urls):
        score += 2
    if health_hits:
        score += 2
    if any(term in text for term in ("醫療", "投資", "法律", "保險", "房地產", "政府", "療效", "保證", "專家", "研究指出", "數據顯示")):
        score += 1
    reasons = []
    if health_hits:
        reasons.append("health:" + ",".join(health_hits[:5]))
    if teaching_hits:
        reasons.append("teaching:" + ",".join(teaching_hits[:5]))
    if third_party_hits:
        reasons.append("third_party:" + ",".join(third_party_hits[:5]))
    elif urls:
        reasons.append("third_party:external-url")
    if product_fields:
        reasons.append("product_fields")
    if review["requiredFixes"]:
        reasons.append(f"required_fixes:{len(review['requiredFixes'])}")
    return score, " | ".join(reasons)


def is_batch_1_candidate(score: int, review: dict[str, Any], reasons: str) -> bool:
    return (
        score >= 9
        or (
            review["riskLevel"] == "high"
            and review["requiredFixes"]
            and ("product" in reasons or "health:" in reasons)
        )
    )


def later_batch_for(review: dict[str, Any], reasons: str) -> str:
    if review["riskLevel"] == "high" and "health:" in reasons:
        return "batch-2"
    if "product" in reasons or "momoshop" in reasons or "icareushop" in reasons:
        return "batch-3"
    return "batch-4"


def build_inventory() -> list[dict[str, Any]]:
    payload = load_json(ARTICLES_INDEX)
    rows: list[dict[str, Any]] = []
    for item in payload.get("items", []):
        article = article_for(item)
        html_text = article_html(item)
        review = audit_article_record(article, html_text=html_text)
        score, reasons = score_entry(article, html_text, review)
        if score <= 0:
            continue
        rows.append(
            {
                "slug": item["slug"],
                "title": item["title"],
                "category": item["category"],
                "public_url": item["url"],
                "riskLevel": review["riskLevel"],
                "current_audit_status": "pass" if review["publishReady"] else "fail",
                "required_fixes": len(review["requiredFixes"]),
                "score": score,
                "batch": "",
                "_batch_1_candidate": is_batch_1_candidate(score, review, reasons),
                "reasons": reasons,
            }
        )
    rows.sort(
        key=lambda row: (
            BATCH_1_PRIORITY_ORDER.get(row["slug"], len(BATCH_1_PRIORITY_ORDER)),
            -int(row["score"]),
            -int(row["required_fixes"]),
            row["category"],
            row["slug"],
        )
    )
    batch_1_remaining = BATCH_1_SIZE
    for row in rows:
        preferred_batch_1 = row["slug"] in BATCH_1_PRIORITY_ORDER
        scored_batch_1 = bool(row.pop("_batch_1_candidate"))
        if (preferred_batch_1 or scored_batch_1) and batch_1_remaining > 0:
            row["batch"] = "batch-1"
            batch_1_remaining -= 1
        else:
            row["batch"] = later_batch_for(
                {"riskLevel": row["riskLevel"], "requiredFixes": [None] * int(row["required_fixes"])},
                row["reasons"],
            )
    rows.sort(
        key=lambda row: (
            row["batch"],
            BATCH_1_PRIORITY_ORDER.get(row["slug"], len(BATCH_1_PRIORITY_ORDER)),
            -int(row["score"]),
            -int(row["required_fixes"]),
            row["category"],
            row["slug"],
        )
    )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Print high-risk content authenticity candidate inventory.")
    parser.add_argument("--format", choices=("csv", "json"), default="csv")
    parser.add_argument("--batch", help="Filter by batch id, for example batch-1.")
    args = parser.parse_args()

    rows = build_inventory()
    if args.batch:
        rows = [row for row in rows if row["batch"] == args.batch]

    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    writer = csv.DictWriter(sys.stdout, fieldnames=[
        "batch",
        "score",
        "riskLevel",
        "current_audit_status",
        "required_fixes",
        "category",
        "slug",
        "title",
        "public_url",
        "reasons",
    ])
    writer.writeheader()
    writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
