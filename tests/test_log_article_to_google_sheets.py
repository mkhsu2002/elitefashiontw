from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import log_article_to_google_sheets as sheets


class GoogleSheetsArticleLogTest(unittest.TestCase):
    def test_authenticity_audited_value_reads_publish_ready_log(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "content-authenticity-log.json"
            log_path.write_text(
                json.dumps(
                    {
                        "entries": [
                            {
                                "articleId": "article-1",
                                "slug": "first-article",
                                "publishReady": True,
                            },
                            {
                                "articleId": "article-2",
                                "slug": "second-article",
                                "publishReady": False,
                            },
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch.object(sheets, "AUTHENTICITY_LOG_PATH", log_path):
                self.assertEqual(sheets.authenticity_audited_value("article-1", "first-article"), "yes")
                self.assertEqual(sheets.authenticity_audited_value("article-2", "second-article"), "no")
                self.assertEqual(sheets.authenticity_audited_value("", "first-article"), "yes")
                self.assertEqual(sheets.authenticity_audited_value("missing", "missing"), "no")


if __name__ == "__main__":
    unittest.main()
