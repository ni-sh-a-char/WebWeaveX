from __future__ import annotations
from core.crawling.crawl_persistence_v3_engine import persist_crawl_state_v3

def checkpoint_crawl_v3(state: dict):
    return {"checkpoint": persist_crawl_state_v3(state)}
