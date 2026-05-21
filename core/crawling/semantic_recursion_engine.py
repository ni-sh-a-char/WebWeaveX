from __future__ import annotations
from core.crawling.crawler_engine import crawl

def recursive_extract_v3(url: str, max_depth: int = 3, max_pages: int = 100):
    return crawl(url, max_depth=max_depth, max_pages=max_pages)
