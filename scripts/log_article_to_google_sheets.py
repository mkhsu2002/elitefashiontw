#!/usr/bin/env python3
"""Sync content publish-log entries to Google Sheets.

Expected env vars:
- GOOGLE_SHEETS_SPREADSHEET_ID or GOOGLE_SHEET_ID
- GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON, GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON_BASE64,
  SERVICE_ACCOUNT_PATH, or GOOGLE_APPLICATION_CREDENTIALS
- GOOGLE_SHEETS_WORKSHEET_TITLE optional, default: Taiwan
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLISH_LOG_PATH = ROOT / "automation" / "publish-log.json"
GENERATED_ARTICLES_DIR = ROOT / "automation" / "articles"
SITE_CONFIG_PATH = ROOT / "automation" / "site-config.json"
DEFAULT_WORKSHEET = "Taiwan"
HEADERS = [
    "article_id",
    "slug",
    "title",
    "live_url",
    "path",
    "category",
    "series",
    "published_at",
    "queue_id",
    "trigger_type",
    "provider",
    "model",
    "site_name",
    "site_url",
    "status",
    "notes",
]


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def strict_mode() -> bool:
    return os.environ.get("CI_STRICT_GOOGLE_SHEETS", "").lower() == "true"


def load_service_account() -> dict[str, Any] | str | None:
    raw = os.environ.get("GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON")
    raw_b64 = os.environ.get("GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON_BASE64")
    service_account_path = os.environ.get("SERVICE_ACCOUNT_PATH") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if raw:
        return json.loads(raw)
    if raw_b64:
        return json.loads(base64.b64decode(raw_b64).decode("utf-8"))
    if service_account_path:
        return service_account_path
    return None


def client_from_env():
    try:
        import gspread
    except ModuleNotFoundError:
        if strict_mode():
            raise RuntimeError("gspread is not installed; cannot sync Google Sheets in strict mode.")
        print("gspread is not installed; skipping Google Sheets sync.")
        return None

    credentials = load_service_account()
    if credentials is None:
        if strict_mode():
            raise RuntimeError("Google Sheets credentials not configured in strict mode.")
        print("Google Sheets credentials not configured; skipping sync.")
        return None
    if isinstance(credentials, str):
        return gspread.service_account(filename=credentials)
    return gspread.service_account_from_dict(credentials)


def ensure_worksheet(spreadsheet, title: str):
    import gspread

    try:
        worksheet = spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=title, rows=1000, cols=len(HEADERS))

    first_row = worksheet.row_values(1)
    if first_row[: len(HEADERS)] != HEADERS:
        worksheet.update("A1", [HEADERS])
    return worksheet


def load_article_detail(article_id: str) -> dict[str, Any]:
    article_path = GENERATED_ARTICLES_DIR / f"{article_id}.json"
    return load_json(article_path, {})


def build_sheet_entry(entry: dict[str, Any], site_config: dict[str, Any]) -> dict[str, str]:
    article_id = str(entry.get("articleId", "") or "")
    article_detail = load_article_detail(article_id)
    file_path = str(entry.get("file", "") or article_detail.get("file", ""))
    slug = str(article_detail.get("slug", "") or Path(file_path).stem)
    category = str(article_detail.get("category", "") or (Path(file_path).parts[0] if file_path else ""))
    series = str(article_detail.get("series", "") or "")
    provider = str(os.environ.get("CONTENT_MODEL_PROVIDER", "") or site_config.get("model", {}).get("provider", ""))
    model_name = str(os.environ.get("CONTENT_MODEL", "") or site_config.get("model", {}).get("defaultModel", ""))
    trigger_type = str(entry.get("triggerType", "") or "")
    notes = trigger_type if trigger_type else ""

    return {
        "article_id": article_id,
        "slug": slug,
        "title": str(entry.get("title", "") or article_detail.get("title", "")),
        "live_url": str(entry.get("url", "") or article_detail.get("url", "")),
        "path": str(entry.get("file", "") or article_detail.get("file", "")),
        "category": category,
        "series": series,
        "published_at": str(entry.get("publishedAt", "") or article_detail.get("publishedAt", "")),
        "queue_id": str(entry.get("queueId", "") or article_detail.get("queueId", "")),
        "trigger_type": trigger_type,
        "provider": provider,
        "model": model_name,
        "site_name": str(site_config.get("siteName", "Elite Fashion")),
        "site_url": str(site_config.get("baseUrl", "")),
        "status": "published",
        "notes": notes,
    }


def normalize_entry(entry: dict[str, Any]) -> list[str]:
    return [str(entry.get(header, "") or "") for header in HEADERS]


def get_worksheet(site_config: dict[str, Any]):
    spreadsheet_id = os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID") or os.environ.get("GOOGLE_SHEET_ID")
    if not spreadsheet_id:
        if strict_mode():
            raise RuntimeError("Google Sheets spreadsheet ID not configured in strict mode.")
        print("Google Sheets spreadsheet ID not configured; skipping sync.")
        return None

    client = client_from_env()
    if client is None:
        return None

    worksheet_title = os.environ.get(
        "GOOGLE_SHEETS_WORKSHEET_TITLE",
        site_config.get("cloudLogging", {}).get("worksheetTitle", DEFAULT_WORKSHEET),
    )
    spreadsheet = client.open_by_key(spreadsheet_id)
    return ensure_worksheet(spreadsheet, worksheet_title)


def sync_entry(entry: dict[str, Any], site_config: dict[str, Any], worksheet=None) -> str:
    worksheet = worksheet or get_worksheet(site_config)
    if worksheet is None:
        return "Google Sheets sync skipped."

    row = build_sheet_entry(entry, site_config)
    article_id = row["article_id"]
    if not article_id:
        return "Latest entry has no article_id; skipped."

    existing_ids = worksheet.col_values(1)
    if article_id in existing_ids[1:]:
        return f"Article already logged: {article_id}"

    worksheet.append_row(normalize_entry(row), value_input_option="RAW")
    return f"Logged article to Google Sheets: {article_id}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Log content publish-log entry to Google Sheets.")
    parser.add_argument("--article-id", help="Specific articleId to sync. Defaults to latest entry.")
    parser.add_argument("--all", action="store_true", help="Sync all publish-log entries that are not yet in the worksheet.")
    args = parser.parse_args()

    publish_log = load_json(PUBLISH_LOG_PATH, {"entries": []})
    entries = publish_log.get("entries", [])
    if not entries:
        print("No publish-log entries found; nothing to sync.")
        return 0

    site_config = load_json(SITE_CONFIG_PATH, {})
    worksheet = get_worksheet(site_config)
    if worksheet is None:
        return 0

    if args.all:
        existing_ids = set(worksheet.col_values(1)[1:])
        synced = 0
        skipped = 0
        for entry in reversed(entries):
            article_id = str(entry.get("articleId", "") or "")
            if not article_id:
                skipped += 1
                continue
            if article_id in existing_ids:
                skipped += 1
                continue
            print(sync_entry(entry, site_config, worksheet=worksheet))
            existing_ids.add(article_id)
            synced += 1
        print(f"Backfill complete: synced={synced}, skipped={skipped}")
        return 0

    if args.article_id:
        entry = next((item for item in entries if item.get("articleId") == args.article_id), None)
        if entry is None:
            print(f"articleId not found in publish log: {args.article_id}")
            return 1
    else:
        entry = entries[0]

    print(sync_entry(entry, site_config, worksheet=worksheet))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
