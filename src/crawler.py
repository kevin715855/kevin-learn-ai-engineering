import logging
import time
from typing import Optional
from .state import CrawlStateTracker
from .discovery import DiscoveryEngine
from .fetcher import ContentFetcher
from .storage import RawStorage

logger = logging.getLogger(__name__)

class RoadmapCrawler:
    def __init__(self, db_path: str = "crawl_state.db", raw_dir: str = "raw_data", discovery_path: str = "ROADMAP_DISCOVERY.md"):
        self.state_tracker = CrawlStateTracker(db_path)
        self.discovery_engine = DiscoveryEngine(discovery_path)
        self.fetcher = ContentFetcher()
        self.storage = RawStorage(raw_dir)

    def run_discovery(self) -> dict:
        logger.info("Starting course discovery...")
        report = self.discovery_engine.discover()
        
        # Upsert all discovered lessons into state tracker
        for lesson in report["lessons"]:
            self.state_tracker.upsert_lesson(
                lesson_id=lesson["id"],
                slug=lesson["slug"],
                title=lesson["title"],
                module_id=lesson["module_id"],
                module_title=lesson["module_title"]
            )
        logger.info("Discovery complete. %d lessons registered in state tracker.", len(report["lessons"]))
        return report

    def crawl_lesson(self, lesson: dict) -> bool:
        lesson_id = lesson["id"]
        slug = lesson["slug"]
        url = lesson.get("download_url")

        if not url:
            # Construct fallback URL if missing
            url = f"https://raw.githubusercontent.com/nilbuild/developer-roadmap/master/roadmaps/ai-engineer/content/{slug}@{lesson_id}.md"

        logger.info("Crawling lesson [%s]: %s (%s)", lesson_id, lesson["title"], url)
        self.state_tracker.set_status(lesson_id, "FETCHING")

        try:
            content, status_code, headers = self.fetcher.fetch(url)
            file_path = self.storage.save_lesson_raw(
                lesson_id=lesson_id,
                slug=slug,
                content=content,
                status_code=status_code,
                headers=headers,
                download_url=url
            )
            self.state_tracker.set_status(lesson_id, "COMPLETED", error_message=None, raw_file_path=file_path)
            logger.info("Successfully crawled and stored lesson [%s]", lesson_id)
            return True
        except Exception as e:
            error_msg = str(e)
            logger.error("Failed to crawl lesson [%s] %s: %s", lesson_id, slug, error_msg)
            self.state_tracker.set_status(lesson_id, "FAILED", error_message=error_msg)
            return False

    def run_crawl(self, retry_failed: bool = False, delay: float = 0.5):
        if retry_failed:
            self.state_tracker.reset_failed()

        pending_lessons = self.state_tracker.get_pending_lessons()
        if not pending_lessons:
            logger.info("No pending lessons to crawl. Running discovery to ensure all items are registered...")
            self.run_discovery()
            pending_lessons = self.state_tracker.get_pending_lessons()

        logger.info("Found %d lessons to crawl.", len(pending_lessons))
        
        success_count = 0
        fail_count = 0

        for lesson in pending_lessons:
            success = self.crawl_lesson(lesson)
            if success:
                success_count += 1
            else:
                fail_count += 1
            if delay > 0:
                time.sleep(delay)

        stats = self.state_tracker.get_stats()
        logger.info("Crawling finished. Stats: %s (Success in run: %d, Failed in run: %d)", stats, success_count, fail_count)
        return stats
