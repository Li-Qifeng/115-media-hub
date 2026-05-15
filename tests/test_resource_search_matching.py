import unittest
from unittest.mock import patch

from app.core import search_telegram_channel_resource_items
from app.resource_identity import build_resource_search_match_info, sort_resource_search_items


class ResourceSearchMatchingTest(unittest.TestCase):
    def test_title_matches_rank_before_newer_description_matches(self):
        title_match = {
            "title": "光环 Halo S01 4K",
            "raw_text": "光环 Halo S01 4K\nhttps://example.com/halo",
            "published_at": "2024-01-01T00:00:00+00:00",
            "message_url": "https://t.me/s/demo/10",
        }
        description_match = {
            "title": "低智商犯罪 S01E13",
            "raw_text": "低智商犯罪 S01E13\n简介：主角带着光环一路破案。",
            "published_at": "2026-01-01T00:00:00+00:00",
            "message_url": "https://t.me/s/demo/20",
        }

        ordered = sort_resource_search_items(
            [
                {**description_match, "search_match": build_resource_search_match_info(description_match, "光环")},
                {**title_match, "search_match": build_resource_search_match_info(title_match, "光环")},
            ],
            "光环",
        )

        self.assertEqual(ordered[0]["title"], "光环 Halo S01 4K")

    def test_description_only_match_returns_explanatory_snippet(self):
        item = {
            "title": "低智商犯罪 S01E13",
            "raw_text": "低智商犯罪 S01E13\n简介：主角带着光环一路破案。",
        }

        match = build_resource_search_match_info(item, "光环")

        self.assertTrue(match["matched"])
        self.assertEqual(match["field"], "raw_text")
        self.assertIn("光环", match["snippet"])

    def test_channel_search_keeps_scanning_for_stronger_title_match(self):
        first_page = {
            "posts": [
                {
                    "title": "低智商犯罪 S01E13",
                    "raw_text": "低智商犯罪 S01E13\n简介：主角带着光环一路破案。",
                    "published_at": "2026-01-01T00:00:00+00:00",
                    "message_url": "https://t.me/s/demo/20",
                    "channel_name": "demo",
                    "link_type": "115share",
                    "link_url": "https://115.com/s/desc1",
                    "extra": {"source_post_id": "demo/20"},
                },
                {
                    "title": "另一条新资源",
                    "raw_text": "另一条新资源\n简介：也提到了光环。",
                    "published_at": "2026-01-01T00:01:00+00:00",
                    "message_url": "https://t.me/s/demo/19",
                    "channel_name": "demo",
                    "link_type": "115share",
                    "link_url": "https://115.com/s/desc2",
                    "extra": {"source_post_id": "demo/19"},
                },
            ],
            "next_before": "19",
            "has_more": True,
        }
        second_page = {
            "posts": [
                {
                    "title": "光环 Halo S01",
                    "raw_text": "光环 Halo S01\nhttps://115.com/s/halo",
                    "published_at": "2024-01-01T00:00:00+00:00",
                    "message_url": "https://t.me/s/demo/10",
                    "channel_name": "demo",
                    "link_type": "115share",
                    "link_url": "https://115.com/s/halo",
                    "extra": {"source_post_id": "demo/10"},
                }
            ],
            "next_before": "",
            "has_more": False,
        }

        def fake_fetch(*args, **kwargs):
            before = kwargs.get("before", "")
            return second_page if before else first_page

        with patch("app.core.fetch_telegram_channel_posts_page", side_effect=fake_fetch):
            result = search_telegram_channel_resource_items(
                {},
                {"channel_id": "demo", "name": "Demo"},
                "光环",
                limit_per_channel=2,
                max_pages=2,
                page_size=2,
            )

        self.assertEqual(result["pages_scanned"], 2)
        self.assertEqual(result["items"][0]["title"], "光环 Halo S01")


if __name__ == "__main__":
    unittest.main()
