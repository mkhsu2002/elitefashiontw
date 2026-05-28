from __future__ import annotations

import unittest

from scripts.content_authenticity_audit import audit_article_record


def base_article(**overrides):
    article = {
        "id": "test-article",
        "slug": "test-article",
        "title": "居家收納的日常判斷",
        "category": "lifestyle-culture",
        "intro": "這是一篇一般生活文章，聚焦使用頻率與動線。",
        "markdownBody": "先看每天會碰到的物品，再決定收納位置。這不是測試結果，而是生活動線判斷。",
        "faq": [],
        "cta": {"label": "瀏覽更多", "url": "/lifestyle-culture.html", "text": "繼續閱讀。"},
    }
    article.update(overrides)
    return article


class ContentAuthenticityAuditTest(unittest.TestCase):
    def test_general_lifestyle_article_passes(self):
        review = audit_article_record(base_article())
        self.assertTrue(review["publishReady"])

    def test_unsourced_price_claim_fails(self):
        review = audit_article_record(
            base_article(markdownBody="這款商品目前只要 990 元，是近期最低價。")
        )
        self.assertFalse(review["publishReady"])
        self.assertTrue(any("價格" in item for item in review["requiredFixes"]))

    def test_unsourced_stock_claim_fails(self):
        review = audit_article_record(
            base_article(markdownBody="官方表示庫存有限，建議立刻下單。")
        )
        self.assertFalse(review["publishReady"])
        self.assertTrue(any("缺少可驗證依據" in item or "庫存" in item for item in review["requiredFixes"]))

    def test_ymyl_promise_without_disclaimer_fails(self):
        review = audit_article_record(
            base_article(
                category="wellness-movement",
                title="睡眠恢復指南",
                markdownBody="這個方法一定能改善失眠，並且保證讓身體恢復。",
            )
        )
        self.assertFalse(review["publishReady"])
        self.assertTrue(any("高風險" in item for item in review["requiredFixes"]))

    def test_affiliate_without_disclosure_or_rel_fails(self):
        article = base_article(
            mainProducts=[
                {
                    "name": "測試商品",
                    "affiliateUrl": "https://s.momoshop.com.tw/s/example",
                    "sourceProductUrl": "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=1",
                }
            ]
        )
        html = '<a href="https://s.momoshop.com.tw/s/example">前往商品</a>'
        review = audit_article_record(article, html_text=html)
        self.assertFalse(review["publishReady"])
        self.assertTrue(any("導購" in item for item in review["requiredFixes"]))

    def test_affiliate_with_disclosure_and_rel_passes(self):
        article = base_article(
            mainProducts=[
                {
                    "name": "測試商品",
                    "affiliateUrl": "https://s.momoshop.com.tw/s/example",
                    "sourceProductUrl": "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=1",
                }
            ]
        )
        html = (
            '<a href="https://s.momoshop.com.tw/s/example" '
            'rel="sponsored nofollow noopener noreferrer">前往商品</a>'
            "<section>導購揭露</section>"
        )
        review = audit_article_record(article, html_text=html)
        self.assertTrue(review["publishReady"])


if __name__ == "__main__":
    unittest.main()
