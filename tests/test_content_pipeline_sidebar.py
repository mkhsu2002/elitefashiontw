from __future__ import annotations

import unittest

from scripts import content_pipeline as pipeline


def product(index: int) -> dict[str, str]:
    return {
        "name": f"測試選物 {index}",
        "merchantId": f"TPTEST{index:04d}",
        "affiliateUrl": f"https://s.momoshop.com.tw/s/test-{index}",
        "selectionReason": "可作為同主題選物參考。",
    }


class ContentPipelineSidebarTest(unittest.TestCase):
    def test_sidebar_falls_back_to_main_products_when_empty(self):
        article = {"mainProducts": [product(index) for index in range(1, 5)], "sidebarProducts": []}

        html = pipeline.render_product_sidebar(article)

        self.assertEqual(html.count('class="product-card product-card-compact"'), 4)
        self.assertIn('rel="sponsored nofollow noopener noreferrer"', html)

    def test_sidebar_tops_up_from_main_products_when_sparse(self):
        article = {
            "mainProducts": [product(index) for index in range(1, 5)],
            "sidebarProducts": [product(5)],
        }

        products = pipeline.sidebar_products_for_article(article)

        self.assertEqual(len(products), 5)
        self.assertEqual(len({item["merchantId"] for item in products}), 5)

    def test_validate_blocks_missing_required_product_placement(self):
        article = {
            "markdownBody": "測試文章",
            "sections": [],
            "faq": [],
            "readTimeMinutes": 0,
            "mainProducts": [product(1), product(2), product(3)],
        }
        config = {
            "articleContract": {"requiredFields": []},
            "articleQuality": {
                "requireProductPlacement": True,
                "minProductPlacementItems": 4,
            },
        }

        with self.assertRaisesRegex(pipeline.PipelineError, "商品置入不足"):
            pipeline.validate_generated_article(article, config)

    def test_validate_allows_skipped_product_placement_with_reason(self):
        article = {
            "markdownBody": "測試文章",
            "sections": [],
            "faq": [],
            "readTimeMinutes": 0,
            "productPlacementSkippedReason": "純站務公告，沒有自然商品延伸。",
        }
        config = {
            "articleContract": {"requiredFields": []},
            "articleQuality": {
                "requireProductPlacement": True,
                "minProductPlacementItems": 4,
            },
        }

        pipeline.validate_generated_article(article, config)


if __name__ == "__main__":
    unittest.main()
