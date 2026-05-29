#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_new_audience_batch_four as base


QUEUE_ID = "Q-0018"
TODAY = base.TODAY


ARTICLES: list[dict[str, Any]] = [
    {
        "slug": "elder-home-reading-care-vision-layout-supplies",
        "title": "長輩用品不只看功能：閱讀、照護、眼鏡與居家動線的準備順序",
        "category": "wellness-movement",
        "audience": "照護家庭、家庭旅行、閱讀與居家備品整理讀者",
        "items": ["閱讀用品", "照護備品", "眼鏡", "居家動線"],
        "brands": ["TP0005096", "TP0004194", "TP0009515", "TP0008981"],
        "cover": "ig_0612535e4e875d3d016a18ddcf903c819892f3ad3e8b68ccb7.png",
        "heroAlt": "明亮客廳中的閱讀椅、眼鏡、書本、居家備品籃與安全通行動線",
        "excerpt": "替長輩準備用品時，功能只是第一步；真正影響日常的是拿取高度、閱讀光線、備品位置與家人協作。",
        "intro": "替長輩準備用品，很容易先看功能：這個能不能支撐、那個是否好拿、眼鏡是不是清楚、備品是否齊全。但真正會影響每天使用的，往往是更細的事情：東西放在哪裡、誰會補、拿取時會不會擋路、閱讀光線夠不夠，以及家人能不能看懂同一套收納規則。",
        "decision": "先排居家動線，再補閱讀、眼鏡與照護備品",
        "sceneLine": "早晨閱讀、下午起身活動、睡前整理與家人臨時協助，是長輩用品最容易被真正使用到的四個時刻。",
        "priorityLine": "閱讀用品、眼鏡、常用備品和支撐用品要靠近固定座位，低頻備品則集中標示，不要讓每張桌面都堆滿用品。",
        "mistakeLine": "常見錯誤是看到功能多就下單，卻沒有確認高度、重量、清潔方式、字體標示與家中走道寬度。",
        "taiwanLine": "台灣住宅常見小客廳、窄走道與浴室濕氣，長輩用品要考慮拿取高度、防潮、照明和通行，不適合把備品分散在每個角落。",
        "maintenanceLine": "每週固定檢查閱讀位置、眼鏡收納、備品籃與坐墊或支撐用品狀態，若有破損、濕氣或拿取困難，就先調整位置再補新品。",
        "cautionLine": "涉及視力、身體不適、照護用品、醫材或復健需求時，請依商品標示並諮詢合格專業人員，不以一般選物文章替代醫療判斷。",
        "disclaimer": "本文為一般居家動線、閱讀用品、眼鏡與照護備品整理參考，不構成醫療、視力矯正、復健或照護處方；相關用品請依商品標示與專業建議選擇。",
        "brandReasons": {
            "TP0005096": "可從閱讀、書籍與保守型居家備品方向查看",
            "TP0004194": "適合查看醫材通路、照護用品與生活消耗品標示",
            "TP0009515": "可作為老花眼鏡、偏光太陽眼鏡與日常選鏡參考",
            "TP0008981": "適合補充枕頭、靠墊與居家支撐用品",
        },
    },
]


def update_queue(articles: list[dict[str, Any]], config: dict[str, Any]) -> None:
    path = base.ROOT / config["paths"]["queueJson"]
    queue = base.pipeline.load_json(path)
    by_slug = {article["slug"]: article for article in articles}
    series = next((item for item in queue["series"] if item.get("queueId") == QUEUE_ID), None)
    if series is None:
        series = {
            "queueId": QUEUE_ID,
            "topic": "長輩閱讀、照護備品與居家動線補齊",
            "direction": "補齊既定 momo 新受眾規劃中尚未發布的長輩用品題目；公開文章聚焦閱讀光線、眼鏡拿取、照護備品位置與家人協作，不使用療效或安全保證語氣。",
            "plannedCount": len(ARTICLES),
            "status": "planned",
            "source": "momo-ab-new-audience-roadmap",
            "createdAt": base.pipeline.now_iso(),
            "seriesName": "momo 新受眾規劃補齊",
            "items": [
                {
                    "order": index,
                    "slug": spec["slug"],
                    "title": spec["title"],
                    "targetReader": spec["audience"],
                    "category": spec["category"],
                    "status": "planned",
                }
                for index, spec in enumerate(ARTICLES, start=1)
            ],
        }
        queue["series"].append(series)
        queue["nextQueueSequence"] = max(int(queue.get("nextQueueSequence", 1)), 19)
    spec_by_slug = {spec["slug"]: spec for spec in ARTICLES}
    for index, item in enumerate(series["items"], start=1):
        spec = spec_by_slug.get(item.get("slug"), {})
        item.setdefault("order", index)
        if spec:
            item.setdefault("targetReader", spec["audience"])
            item.setdefault("category", spec["category"])
            item.setdefault("title", spec["title"])
        article = by_slug.get(item.get("slug"))
        if article:
            item["status"] = "published"
            item["articleId"] = article["id"]
            item["file"] = article["file"]
            item["publishedAt"] = article["publishedAt"]
    series["status"] = "completed" if all(item.get("status") == "published" for item in series["items"]) else "in_progress"
    queue["updatedAt"] = base.pipeline.now_iso()
    base.pipeline.write_json(path, queue)


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
        increment = 0
        for article in hits:
            if article["slug"] not in existing_slugs:
                existing_slugs.append(article["slug"])
                increment += 1
            if article["url"] not in existing_urls:
                existing_urls.append(article["url"])
        row["article_slug"] = ";".join(existing_slugs)
        row["live_url"] = ";".join(existing_urls)
        if increment:
            row["mention_count"] = str(int(row.get("mention_count") or 0) + increment)
        row["last_mentioned_at"] = TODAY
        note = "2026-05-28 momo 長輩用品閱讀照護與居家動線文章已置入。"
        if note not in row.get("notes", ""):
            row["notes"] = (row.get("notes", "").rstrip() + (" " if row.get("notes", "").strip() else "") + note).strip()
    with base.TRACKER_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(tracker_rows)


def main() -> int:
    base.QUEUE_ID = QUEUE_ID
    base.ARTICLES = ARTICLES
    base.update_queue = update_queue
    base.update_tracker = update_tracker
    return base.main()


if __name__ == "__main__":
    sys.exit(main())
