from __future__ import annotations

from typing import Any, Dict

from core.crawling.crawl_budget_engine import CrawlBudget
from core.crawling.dedup_engine import canonical_url
from core.crawling.domain_policy_engine import allow_url
from core.crawling.queue_engine import DeterministicQueue
from core.crawling.traversal_engine import discover_links
from core.fetch.http_fetcher import fetch_sync


def crawl(seed_url: str, max_depth: int = 2, max_pages: int = 20, same_domain_only: bool = False) -> Dict[str, Any]:
    q = DeterministicQueue()
    seed = canonical_url(seed_url)
    q.enqueue(seed)
    depth_map = {seed: 0}
    budget = CrawlBudget(max_depth=max_depth, max_pages=max_pages)
    visited = []
    discovered = []
    while q.peek() and budget.pages < budget.max_pages:
        url = q.dequeue()
        depth = depth_map.get(url, 0)
        if not budget.allow(depth):
            continue
        fetched = fetch_sync(url)
        text = str(fetched.get("text", "") or "")
        budget.account(len(text.encode("utf-8", errors="ignore")))
        visited.append(url)
        if depth < max_depth:
            for link in discover_links(url, text):
                link = canonical_url(link)
                if allow_url(seed, link, same_domain_only=same_domain_only):
                    discovered.append(link)
                    if q.enqueue(link):
                        depth_map[link] = depth + 1
    return {
        "visited": sorted(set(visited)),
        "queued": sorted(set(q.items())),
        "discovered": sorted(set(discovered)),
        "depth_map": {k: depth_map[k] for k in sorted(depth_map.keys())},
    }

