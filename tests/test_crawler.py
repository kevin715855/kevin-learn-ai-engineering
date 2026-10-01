import unittest
from unittest.mock import patch, MagicMock
import tempfile
import pathlib
import os

from src.state import CrawlStateTracker
from src.storage import RawStorage
from src.fetcher import ContentFetcher
from src.discovery import DiscoveryEngine
from src.crawler import RoadmapCrawler

class TestCrawlStateTracker(unittest.TestCase):
    def setUp(self):
        self.fd, self.db_path = tempfile.mkstemp()
        os.close(self.fd)
        self.tracker = CrawlStateTracker(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_upsert_and_status(self):
        self.tracker.upsert_lesson("123", "slug-1", "Lesson 1", "mod-1", "Module 1")
        lesson = self.tracker.get_lesson("123")
        self.assertIsNotNone(lesson)
        self.assertEqual(lesson["status"], "PENDING")
        self.assertEqual(lesson["title"], "Lesson 1")

        self.tracker.set_status("123", "COMPLETED", raw_file_path="/path/to/file")
        lesson = self.tracker.get_lesson("123")
        self.assertEqual(lesson["status"], "COMPLETED")
        self.assertEqual(lesson["raw_file_path"], "/path/to/file")

        stats = self.tracker.get_stats()
        self.assertEqual(stats["COMPLETED"], 1)

class TestRawStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = RawStorage(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_save_lesson_raw(self):
        path = self.storage.save_lesson_raw(
            lesson_id="abc",
            slug="test-slug",
            content="# Hello World",
            status_code=200,
            headers={"content-type": "text/markdown"},
            download_url="https://example.com/test.md"
        )
        self.assertTrue(os.path.exists(path))
        md_content = pathlib.Path(path).read_text(encoding="utf-8")
        self.assertEqual(md_content, "# Hello World")

        meta_path = pathlib.Path(self.temp_dir) / "lessons" / "test-slug@abc.json"
        self.assertTrue(meta_path.exists())

class TestContentFetcher(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_fetch_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.headers = {"Content-Type": "text/markdown"}
        mock_resp.read.return_value = b"# Content"
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        fetcher = ContentFetcher()
        content, status, headers = fetcher.fetch("https://example.com/test.md")
        self.assertEqual(content, "# Content")
        self.assertEqual(status, 200)

if __name__ == "__main__":
    unittest.main()
