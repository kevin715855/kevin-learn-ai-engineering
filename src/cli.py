import argparse
import logging
import sys
from .crawler import RoadmapCrawler
from .state import CrawlStateTracker
from .processor import RoadmapProcessor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    parser = argparse.ArgumentParser(description="Roadmap.sh AI Engineer Course Crawler")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Discover command
    subparsers.add_parser("discover", help="Discover course modules and lessons, and generate ROADMAP_DISCOVERY.md")

    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Crawl lessons and store raw data")
    crawl_parser.add_argument("--retry-failed", action="store_true", help="Retry previously failed lessons")
    crawl_parser.add_argument("--delay", type=float, default=0.2, help="Delay between requests in seconds")

    # Status command
    subparsers.add_parser("status", help="Show crawling progress status")

    # Retry failed command
    subparsers.add_parser("retry", help="Reset failed lessons to pending and crawl")

    # Process command
    subparsers.add_parser("process", help="Process raw lesson data into translated, normalized, and structured Markdown indexes")

    args = parser.parse_args()
    crawler = RoadmapCrawler()
    tracker = CrawlStateTracker()
    processor = RoadmapProcessor()

    if args.command == "discover":
        report = crawler.run_discovery()
        print(f"Discovery completed successfully! Discovered {report['total_modules']} modules and {report['total_lessons']} lessons.")
    elif args.command == "crawl":
        stats = crawler.run_crawl(retry_failed=getattr(args, "retry_failed", False), delay=getattr(args, "delay", 0.2))
        print(f"Crawl completed. Status summary: {stats}")
    elif args.command == "status":
        stats = tracker.get_stats()
        lessons = tracker.get_all_lessons()
        print(f"Total registered lessons: {len(lessons)}")
        print(f"Status breakdown: {stats}")
    elif args.command == "retry":
        stats = crawler.run_crawl(retry_failed=True)
        print(f"Retry completed. Status summary: {stats}")
    elif args.command == "process":
        report = processor.process_all()
        print(f"Processing completed! Processed {report['processed_lessons']} lessons across {report['total_modules']} modules. Malformed: {report['malformed_lessons']}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
