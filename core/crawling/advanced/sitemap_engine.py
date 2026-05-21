from __future__ import annotations
import re

def parse_sitemap(xml_text: str, max_urls: int = 5000):
    urls=sorted(set(re.findall(r"<loc>\s*(.*?)\s*</loc>", xml_text or '', flags=re.IGNORECASE)))
    return {"urls": urls[:max_urls]}
