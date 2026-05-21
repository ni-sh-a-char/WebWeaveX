from __future__ import annotations

import re


def extract_markdown(text: str) -> dict:
    src = text or ""
    headers = re.findall(r"^(#{1,6})\s+(.+)$", src, flags=re.MULTILINE)
    hierarchy = [{"level": len(h), "title": t.strip()} for h, t in headers]
    code_blocks = re.findall(r"```[\w-]*\n(.*?)```", src, flags=re.DOTALL)
    urls = sorted(set(re.findall(r"https?://[^\s\)]+", src)))
    return {
        "content": {"hierarchy": hierarchy, "urls": urls},
        "code": {"blocks": sorted([b.strip() for b in code_blocks if b.strip()])},
        "metadata": {"header_count": str(len(hierarchy))},
    }

