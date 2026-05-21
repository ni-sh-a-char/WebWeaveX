from __future__ import annotations


def chunk_text(text: str, chunk_size: int = 4096):
    src = text or ""
    chunks = []
    order = []
    step = max(1, chunk_size)
    for i in range(0, len(src), step):
        cid = f"c{i // step:06d}"
        chunks.append({"id": cid, "text": src[i : i + step]})
        order.append(cid)
    return {"chunks": chunks, "chunk_order": order}

