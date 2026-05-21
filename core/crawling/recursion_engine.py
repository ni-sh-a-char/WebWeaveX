from __future__ import annotations

from core.crawling.crawl_budget_engine import CrawlBudget


def should_recurse(depth: int, budget: CrawlBudget) -> bool:
    return budget.allow(depth)

