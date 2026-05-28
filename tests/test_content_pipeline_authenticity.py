from __future__ import annotations

import unittest
from unittest.mock import patch

from scripts import content_pipeline as pipeline


class ContentPipelineAuthenticityTest(unittest.TestCase):
    def test_editorial_auditor_false_blocks_pipeline(self):
        base_review = {
            "articleId": "test-article",
            "slug": "test-article",
            "riskLevel": "low",
            "checkedAt": "2026-05-28T00:00:00Z",
            "publishReady": True,
            "claimChecks": [],
            "requiredFixes": [],
            "sourceEvidence": [],
            "reviewer": "automation",
        }
        config = {
            "paths": {
                "strategyFile": "automation/content-strategy.md",
                "reviewChecklistFile": "automation/editorial-review-checklist.md",
            },
            "model": {"apiKeySecretName": "CONTENT_MODEL_API_KEY"},
        }
        article = {"id": "test-article", "slug": "test-article", "title": "測試文章"}
        editorial_result = {
            "publishReady": False,
            "summary": "缺少來源。",
            "checks": [{"name": "真實性", "passed": False, "note": "缺少來源。"}],
            "requiredFixes": ["補上來源或移除宣稱。"],
        }

        with (
            patch.object(pipeline, "audit_article_for_publish", return_value=base_review),
            patch.object(pipeline, "run_editorial_model_audit", return_value=editorial_result),
            patch.object(pipeline, "upsert_audit_log"),
        ):
            with self.assertRaises(pipeline.PipelineError):
                pipeline.run_authenticity_review(article, config)


if __name__ == "__main__":
    unittest.main()
