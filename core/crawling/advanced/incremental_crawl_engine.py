from __future__ import annotations

def diff_crawl_states(previous: dict, current: dict):
    p=set(previous.get('visited',[])); c=set(current.get('visited',[]))
    return {"new_visited": sorted(c-p), "removed": sorted(p-c)}
