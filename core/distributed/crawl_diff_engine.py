from __future__ import annotations
def crawl_diff(a:list,b:list):
    sa=set(a or []); sb=set(b or []); return {"added":sorted(sb-sa),"removed":sorted(sa-sb)}
