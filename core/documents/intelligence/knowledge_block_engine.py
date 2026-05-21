from __future__ import annotations

def extract_knowledge_blocks(text: str):
    lines=[ln.strip() for ln in (text or '').splitlines() if ln.strip()]
    blocks=[]
    buf=[]
    for ln in lines:
        buf.append(ln)
        if len(buf)>=8:
            blocks.append(' '.join(buf)); buf=[]
    if buf: blocks.append(' '.join(buf))
    return {"knowledge_blocks": blocks}
