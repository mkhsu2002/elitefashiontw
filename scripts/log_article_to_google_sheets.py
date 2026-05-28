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
from itertools import islice


ROOT = Path(__file__).resolve().parents[1]
PUBLISH_LOG_PATH = ROOT / "automation" / "publish-log.json"
GENERATED_ARTICLES_DIR = ROOT / "automation" / "articles"
SITE_CONFIG_PATH = ROOT / "automation" / "site-config.json"
ARTICLES_INDEX_PATH = ROOT / "data" / "articles-index.json"
AUTHENTICITY_LOG_PATH = ROOT / "automation" / "content-authenticity-log.json"
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
    "cover_image_url",
    "authenticity_audited",
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

    if getattr(worksheet, "col_count", len(HEADERS)) < len(HEADERS):
        worksheet.resize(cols=len(HEADERS))

    first_row = worksheet.row_values(1)
    if first_row[: len(HEADERS)] != HEADERS:
        worksheet.update(values=[HEADERS], range_name="A1")
    return worksheet


def load_article_detail(article_id: str) -> dict[str, Any]:
    article_path = GENERATED_ARTICLES_DIR / f"{article_id}.json"
    return load_json(article_path, {})


def load_articles_index_items() -> list[dict[str, Any]]:
    payload = load_json(ARTICLES_INDEX_PATH, {})
    items = payload.get("items", []) if isinstance(payload, dict) else []
    return [item for item in items if isinstance(item, dict)]


def path_to_url(base_url: str, relative_path: str) -> str:
    return f"{base_url.rstrip('/')}/{relative_path.lstrip('/')}"


def canonical_cover_image_url(image: str, site_config: dict[str, Any]) -> str:
    image = str(image or "").strip()
    if not image:
        return ""
    base_url = str(site_config.get("baseUrl", "") or "").rstrip("/")
    legacy_github_base = "https://mkhsu2002.github.io/elitefashiontw/"
    if image.startswith(legacy_github_base) and base_url:
        return path_to_url(base_url, image.replace(legacy_github_base, "", 1))
    if image.startswith(("http://", "https://")):
        return image
    if not base_url:
        return image.lstrip("/")
    return path_to_url(base_url, image)


def find_index_item(article_id: str, file_path: str) -> dict[str, Any]:
    for item in load_articles_index_items():
        if article_id and item.get("id") == article_id:
            return item
        if file_path and item.get("file") == file_path:
            return item
    return {}


def authenticity_log_entries() -> list[dict[str, Any]]:
    payload = load_json(AUTHENTICITY_LOG_PATH, {"entries": []})
    entries = payload.get("entries", []) if isinstance(payload, dict) else []
    return [entry for entry in entries if isinstance(entry, dict)]


def authenticity_audited_value(article_id: str, slug: str) -> str:
    for entry in authenticity_log_entries():
        if entry.get("publishReady") is not True:
            continue
        if article_id and entry.get("articleId") == article_id:
            return "yes"
        if slug and entry.get("slug") == slug:
            return "yes"
    return "no"


def build_sheet_entry(entry: dict[str, Any], site_config: dict[str, Any]) -> dict[str, str]:
    article_id = str(entry.get("articleId", "") or "")
    article_detail = load_article_detail(article_id)
    file_path = str(entry.get("file", "") or article_detail.get("file", ""))
    index_item = find_index_item(article_id, file_path)
    slug = str(article_detail.get("slug", "") or Path(file_path).stem)
    category = str(article_detail.get("category", "") or (Path(file_path).parts[0] if file_path else ""))
    series = str(article_detail.get("series", "") or "")
    provider = str(os.environ.get("CONTENT_MODEL_PROVIDER", "") or site_config.get("model", {}).get("provider", ""))
    model_name = str(os.environ.get("CONTENT_MODEL", "") or site_config.get("model", {}).get("defaultModel", ""))
    trigger_type = str(entry.get("triggerType", "") or "")
    notes = trigger_type if trigger_type else ""
    cover_image = str(
        entry.get("coverImageUrl", "")
        or article_detail.get("heroImage", "")
        or index_item.get("heroImage", "")
        or ""
    )

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
        "cover_image_url": canonical_cover_image_url(cover_image, site_config),
        "authenticity_audited": authenticity_audited_value(article_id, slug),
    }


def build_sheet_entry_from_index_item(item: dict[str, Any], site_config: dict[str, Any]) -> dict[str, str]:
    article_id = str(item.get("id", "") or "")
    file_path = str(item.get("file", "") or item.get("relativeUrl", "") or "")
    source_type = str(item.get("sourceType", "") or "")
    is_generated = source_type == "generated"
    queue_id = str(item.get("queueId", "") or "")
    trigger_type = "queue" if queue_id else ("generated-backfill" if is_generated else "legacy-backfill")

    return {
        "article_id": article_id,
        "slug": str(item.get("slug", "") or Path(file_path).stem),
        "title": str(item.get("title", "") or ""),
        "live_url": str(item.get("url", "") or ""),
        "path": file_path,
        "category": str(item.get("category", "") or ""),
        "series": str(item.get("series", "") or ""),
        "published_at": str(item.get("publishedAt", "") or ""),
        "queue_id": queue_id,
        "trigger_type": trigger_type,
        "provider": "",
        "model": "",
        "site_name": str(site_config.get("siteName", "Elite Fashion")),
        "site_url": str(site_config.get("baseUrl", "")),
        "status": str(item.get("status", "") or "published"),
        "notes": source_type or "legacy",
        "cover_image_url": canonical_cover_image_url(str(item.get("heroImage", "") or ""), site_config),
        "authenticity_audited": authenticity_audited_value(article_id, str(item.get("slug", "") or Path(file_path).stem)),
    }


def normalize_entry(entry: dict[str, Any]) -> list[str]:
    return [str(entry.get(header, "") or "") for header in HEADERS]


def chunk_rows(rows: list[list[str]], size: int = 50):
    iterator = iter(rows)
    while True:
        batch = list(islice(iterator, size))
        if not batch:
            return
        yield batch


def append_rows_chunked(worksheet, rows: list[list[str]], batch_size: int = 50) -> int:
    if not rows:
        return 0
    appended = 0
    for batch in chunk_rows(rows, size=batch_size):
        worksheet.append_rows(batch, value_input_option="RAW")
        appended += len(batch)
    return appended


def column_letter(index: int) -> str:
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def worksheet_rows_by_article_id(worksheet) -> dict[str, tuple[int, list[str]]]:
    values = worksheet.get_all_values()
    if not values:
        return {}
    headers = values[0]
    try:
        article_id_index = headers.index("article_id")
    except ValueError:
        article_id_index = 0

    rows: dict[str, tuple[int, list[str]]] = {}
    for row_number, row in enumerate(values[1:], start=2):
        article_id = row[article_id_index].strip() if len(row) > article_id_index else ""
        if article_id and article_id not in rows:
            rows[article_id] = (row_number, row)
    return rows


def update_cell_values(worksheet, updates: list[tuple[int, str, str]], batch_size: int = 50) -> int:
    if not updates:
        return 0
    updated = 0
    for batch in chunk_rows(updates, size=batch_size):
        worksheet.batch_update(
            [
                {"range": f"{column_letter(HEADERS.index(header) + 1)}{row_number}", "values": [[value]]}
                for row_number, header, value in batch
            ],
            value_input_option="RAW",
        )
        updated += len(batch)
    return updated


def upsert_sheet_entries(worksheet, rows: list[dict[str, str]]) -> tuple[int, int, int]:
    existing = worksheet_rows_by_article_id(worksheet)
    pending_rows: list[list[str]] = []
    pending_cell_updates: list[tuple[int, str, str]] = []
    skipped = 0

    for row in rows:
        article_id = str(row.get("article_id", "") or "")
        if not article_id:
            skipped += 1
            continue
        if article_id not in existing:
            pending_rows.append(normalize_entry(row))
            existing[article_id] = (-1, normalize_entry(row))
            continue

        row_number, existing_row = existing[article_id]
        changed = False
        for header in ("cover_image_url", "authenticity_audited"):
            column_index = HEADERS.index(header)
            desired = str(row.get(header, "") or "")
            current = existing_row[column_index].strip() if len(existing_row) > column_index else ""
            if row_number > 0 and desired and current != desired:
                pending_cell_updates.append((row_number, header, desired))
                changed = True
        if not changed:
            skipped += 1

    appended = append_rows_chunked(worksheet, pending_rows)
    updated = update_cell_values(worksheet, pending_cell_updates)
    return appended, updated, skipped


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

    appended, updated, _ = upsert_sheet_entries(worksheet, [row])
    if appended:
        return f"Logged article to Google Sheets: {article_id}"
    if updated:
        return f"Updated article metadata in Google Sheets: {article_id}"
    return f"Article already logged: {article_id}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Log content publish-log entry to Google Sheets.")
    parser.add_argument("--article-id", help="Specific articleId to sync. Defaults to latest entry.")
    parser.add_argument("--all", action="store_true", help="Sync all publish-log entries that are not yet in the worksheet.")
    parser.add_argument(
        "--all-site-articles",
        action="store_true",
        help="Sync all site articles from data/articles-index.json that are not yet in the worksheet.",
    )
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

    if args.all_site_articles:
        rows = [build_sheet_entry_from_index_item(item, site_config) for item in reversed(load_articles_index_items())]
        synced, updated, skipped = upsert_sheet_entries(worksheet, rows)
        print(f"Full-site backfill complete: synced={synced}, metadata_updated={updated}, skipped={skipped}")
        return 0

    if args.all:
        rows = [build_sheet_entry(entry, site_config) for entry in reversed(entries)]
        synced, updated, skipped = upsert_sheet_entries(worksheet, rows)
        print(f"Backfill complete: synced={synced}, metadata_updated={updated}, skipped={skipped}")
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
