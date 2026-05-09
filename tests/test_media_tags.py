import unittest

from app.media_tags import media_tag_labels, remove_media_tags
from app.services.scraper import _build_scraper_target_path


class MediaTagParserTest(unittest.TestCase):
    def test_parse_requested_filename(self) -> None:
        name = "低智商犯罪.2026 - S01E01 - 第 1 集 - 2160p.WEB-DL.HDR10.HEVC.DDP 5.1.{tmdb-272432}.mkv"

        self.assertEqual(
            media_tag_labels(name),
            ["2160p", "WEB-DL", "HDR10", "HEVC", "DDP 5.1"],
        )

    def test_parse_common_release_tags(self) -> None:
        cases = {
            "Movie.2160p.WEB-DL.HDR10+.HEVC.TrueHD.7.1.Atmos.mkv": [
                "2160p",
                "WEB-DL",
                "HDR10+",
                "HEVC",
                "TrueHD 7.1",
                "Atmos",
            ],
            "Show.1080p.WEBRip.DoVi.H.265.EAC3.5.1.mkv": [
                "1080p",
                "WEBRip",
                "DV",
                "HEVC",
                "EAC3 5.1",
            ],
            "Film.1080p.BluRay.x264.DTS-HD.MA.5.1.mkv": [
                "1080p",
                "BluRay",
                "H.264",
                "DTS-HD MA 5.1",
            ],
            "Demo.2160p.REMUX.HLG.VP9.DD+5.1.mkv": [
                "2160p",
                "REMUX",
                "HLG",
                "VP9",
                "DDP 5.1",
            ],
        }

        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(media_tag_labels(name), expected)

    def test_remove_media_tags_for_title_cleaning(self) -> None:
        cleaned = remove_media_tags("Movie.2026.2160p.WEB-DL.HDR10+.HEVC.TrueHD.7.1.Atmos")

        self.assertNotIn("2160p", cleaned)
        self.assertNotIn("WEB-DL", cleaned)
        self.assertNotIn("HDR10", cleaned)
        self.assertNotIn("HEVC", cleaned)
        self.assertNotIn("TrueHD", cleaned)
        self.assertNotIn("Atmos", cleaned)

    def test_scraper_tv_target_keeps_media_tags_with_channels(self) -> None:
        name = "低智商犯罪.2026 - S01E01 - 第 1 集 - 2160p.WEB-DL.HDR10.HEVC.DDP 5.1.{tmdb-272432}.mkv"
        target_path, issue = _build_scraper_target_path(
            {"name": name, "path": name, "parent_path": ""},
            {"tmdb_id": 272432, "tmdb_media_type": "tv", "tmdb_title": "低智商犯罪", "tmdb_year": "2026"},
            {
                "title_language": "zh",
                "season": 1,
                "preserve_file_info": True,
                "preserve_tags": {
                    "resolution": True,
                    "source": True,
                    "dynamic_range": True,
                    "video": True,
                    "audio": True,
                },
                "organize_into_media_folder": False,
                "use_season_subfolder": False,
            },
        )

        self.assertEqual(issue, "")
        self.assertEqual(target_path, "低智商犯罪 (2026) - S01E01 [2160p WEB-DL HDR10 HEVC DDP 5.1].mkv")


if __name__ == "__main__":
    unittest.main()
