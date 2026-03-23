"""WebWeaveX Fetcher - Production-grade HTTP fetching with retries."""

import httpx
import time
from typing import Optional, Dict, Any

from .config import DEFAULT_CONFIG


class Fetcher:
    """HTTP fetcher with exponential backoff and retries."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        self.fetch_config = cfg.get("fetch", DEFAULT_CONFIG["fetch"])
        self.timeout = self.fetch_config.get("timeout", 10)
        self.retries = self.fetch_config.get("retries", 3)
        self.retry_delay = self.fetch_config.get("retry_delay", 1)
        self.retry_backoff = self.fetch_config.get("retry_backoff", 2)
        self.user_agent = self.fetch_config.get("user_agent", "WebWeaveX/1.0")
        self.follow_redirects = self.fetch_config.get("follow_redirects", True)
        self.max_redirects = self.fetch_config.get("max_redirects", 5)

    def fetch(self, url: str) -> str:
        """Fetch content from URL with exponential backoff retries."""
        headers = self._get_headers()
        last_error = None
        delay = self.retry_delay

        for attempt in range(self.retries):
            try:
                response = self._do_fetch(url, headers)
                return response
            except httpx.HTTPError as e:
                last_error = e
                if attempt < self.retries - 1:
                    time.sleep(delay)
                    delay *= self.retry_backoff
                continue
            except Exception as e:
                last_error = e
                break

        raise last_error or Exception(f"Failed to fetch {url}")

    def _get_headers(self) -> Dict[str, str]:
        """Get consistent headers for deterministic output."""
        return {
            "User-Agent": self.user_agent,
            "Accept-Language": self.fetch_config.get("accept_language", "en-US,en;q=0.9"),
            "Accept-Encoding": self.fetch_config.get("accept_encoding", "gzip, deflate"),
        }

    def _do_fetch(self, url: str, headers: Dict[str, str]) -> str:
        """Execute the HTTP fetch."""
        with httpx.Client(
            timeout=self.timeout,
            max_redirects=self.max_redirects,
            headers=headers,
        ) as client:
            response = client.get(url, follow_redirects=self.follow_redirects)
            response.raise_for_status()
            return response.text


class FetcherError(Exception):
    """Custom exception for fetcher errors."""
    pass
