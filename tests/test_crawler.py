import unittest
from unittest.mock import patch, MagicMock
import tempfile
import pathlib
import os
import urllib.error

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

    def test_resumable_execution_skips_completed(self):
        self.tracker.upsert_lesson("123", "slug-1", "Lesson 1", "mod-1", "Module 1")
        self.tracker.upsert_lesson("456", "slug-2", "Lesson 2", "mod-1", "Module 1")
        
        # Mark lesson 1 as completed
        self.tracker.set_status("123", "COMPLETED", raw_file_path="/path/to/1")
        
        pending = self.tracker.get_pending_lessons()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["id"], "456")


class TestResumableCrawler(unittest.TestCase):
    @patch("src.crawler.DiscoveryEngine")
    @patch("src.crawler.ContentFetcher")
    @patch("src.crawler.RawStorage")
    def test_crawler_resumes_cleanly(self, mock_storage_cls, mock_fetcher_cls, mock_discovery_cls):
        fd, db_path = tempfile.mkstemp()
        os.close(fd)
        try:
            crawler = RoadmapCrawler(db_path=db_path)
            # Register two lessons: one COMPLETED, one PENDING
            crawler.state_tracker.upsert_lesson("l1", "lesson-1", "Lesson 1", "m1", "Mod 1")
            crawler.state_tracker.upsert_lesson("l2", "lesson-2", "Lesson 2", "m1", "Mod 1")
            crawler.state_tracker.set_status("l1", "COMPLETED", raw_file_path="/path/l1")

            mock_fetcher = mock_fetcher_cls.return_value
            mock_fetcher.fetch.return_value = ("# Lesson 2 content", 200, {})
            
            mock_storage = mock_storage_cls.return_value
            mock_storage.save_lesson_raw.return_value = "/path/l2"

            stats = crawler.run_crawl(delay=0)
            
            # Verify fetch was called only for l2, not l1 (completed lesson never re-fetched)
            self.assertEqual(mock_fetcher.fetch.call_count, 1)
            fetched_url = mock_fetcher.fetch.call_args[0][0]
            self.assertIn("lesson-2", fetched_url)

            l1_status = crawler.state_tracker.get_lesson("l1")
            l2_status = crawler.state_tracker.get_lesson("l2")
            self.assertEqual(l1_status["status"], "COMPLETED")
            self.assertEqual(l2_status["status"], "COMPLETED")
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)

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

    @patch("urllib.request.urlopen")
    def test_fetch_retry_on_500(self, mock_urlopen):
        err = urllib.error.HTTPError("https://example.com/test.md", 500, "Internal Server Error", {}, None)
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.headers = {"Content-Type": "text/markdown"}
        mock_resp.read.return_value = b"# Success After Retry"

        mock_manager = MagicMock()
        mock_manager.__enter__.return_value = mock_resp

        mock_urlopen.side_effect = [err, mock_manager]

        fetcher = ContentFetcher(max_retries=3, backoff_factor=0.01)
        content, status, headers = fetcher.fetch("https://example.com/test.md")
        self.assertEqual(content, "# Success After Retry")
        self.assertEqual(status, 200)
        self.assertEqual(mock_urlopen.call_count, 2)

    @patch("urllib.request.urlopen")
    def test_fetch_no_retry_on_404(self, mock_urlopen):
        err = urllib.error.HTTPError("https://example.com/test.md", 404, "Not Found", {}, None)
        mock_urlopen.side_effect = err

        fetcher = ContentFetcher(max_retries=3, backoff_factor=0.01)
        with self.assertRaises(urllib.error.HTTPError):
            fetcher.fetch("https://example.com/test.md")
        self.assertEqual(mock_urlopen.call_count, 1)

if __name__ == "__main__":
    unittest.main()
