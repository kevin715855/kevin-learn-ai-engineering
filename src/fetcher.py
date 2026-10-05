import urllib.request
import urllib.error
import logging
from typing import Tuple, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

logger = logging.getLogger(__name__)

def should_retry(exception):
    if isinstance(exception, urllib.error.HTTPError):
        return exception.code == 429 or (500 <= exception.code < 600)
    if isinstance(exception, (urllib.error.URLError, TimeoutError, ConnectionError)):
        return True
    return False

class ContentFetcher:
    def __init__(self, timeout: int = 30, max_retries: int = 3, backoff_factor: float = 2.0):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def fetch(self, url: str) -> Tuple[str, int, Dict[str, str]]:
        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=self.backoff_factor, min=1, max=60),
            retry=retry_if_exception(should_retry),
            before_sleep=lambda retry_state: logger.warning(
                "Retrying %s after error: %s (attempt %d)",
                url,
                retry_state.outcome.exception(),
                retry_state.attempt_number
            ),
            reraise=True
        )
        def _do_fetch():
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
                    logger.info("Fetched %s - Status: %d", url, status_code)
                    return content, status_code, headers
            except urllib.error.HTTPError as e:
                logger.error("HTTPError fetching %s: %d %s", url, e.code, e.reason)
                raise
            except Exception as e:
                logger.error("Error fetching %s: %s", url, e)
                raise

        return _do_fetch()
