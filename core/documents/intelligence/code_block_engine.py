from __future__ import annotations
import re

def extract_code_blocks(text: str):
    blocks=[b.strip() for b in re.findall(r"```[\w-]*\n(.*?)```", text or '', flags=re.DOTALL) if b.strip()]
    return {"code_blocks": sorted(blocks)}
