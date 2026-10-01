import urllib.request
import urllib.error
import time
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

class ContentFetcher:
    def __init__(self, timeout: int = 30, max_retries: int = 3, backoff_factor: float = 2.0):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def fetch(self, url: str) -> Tuple[str, int, Dict[str, str]]:
        attempt = 0
        last_error = None

        while attempt < self.max_retries:
            attempt += 1
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) RoadmapCrawler/1.0",
                        "Accept": "text/markdown,text/plain,*/*"
                    }
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    status_code = resp.status
                    headers = dict(resp.headers.items())
                    content = resp.read().decode("utf-8", errors="replace")
                    return content, status_code, headers
            except urllib.error.HTTPError as e:
                last_error = f"HTTPError {e.code}: {e.reason}"
                logger.warning("Attempt %d/%d failed for %s: %s", attempt, self.max_retries, url, last_error)
                if e.code in (404, 403):
                    # Do not retry on permanent client errors
                    break
            except Exception as e:
                last_error = f"{type(e).__name__}: {str(e)}"
                logger.warning("Attempt %d/%d failed for %s: %s", attempt, self.max_retries, url, last_error)

            if attempt < self.max_retries:
                sleep_time = self.backoff_factor ** attempt
                time.sleep(sleep_time)

        raise RuntimeError(f"Failed to fetch {url} after {attempt} attempts. Last error: {last_error}")
