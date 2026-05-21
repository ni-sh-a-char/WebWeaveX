from __future__ import annotations

from dataclasses import dataclass

MAX_DEPTH = 3
MAX_PAGES = 100
MAX_BYTES = 50_000_000


@dataclass
class CrawlBudget:
    max_depth: int = MAX_DEPTH
    max_pages: int = MAX_PAGES
    max_bytes: int = MAX_BYTES
    max_domain_visits: int = 50
    timeout_budget: float = 30.0
    pages: int = 0
    bytes_seen: int = 0

    def allow(self, depth: int, add_bytes: int = 0) -> bool:
        return depth <= self.max_depth and self.pages < self.max_pages and (self.bytes_seen + add_bytes) <= self.max_bytes

    def account(self, size: int):
        self.pages += 1
        self.bytes_seen += max(size, 0)

