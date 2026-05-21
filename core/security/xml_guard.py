from __future__ import annotations
def safe_xml_size(size:int, limit:int=5_000_000):
    return size <= limit
