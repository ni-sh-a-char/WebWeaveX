from __future__ import annotations

from typing import Any, Dict, List

MAX_BLOCKS = 10000


def detect_layout_blocks(
    ocr_regions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    blocks = []

    for idx, region in enumerate(ocr_regions[:MAX_BLOCKS]):
        blocks.append({
            "id": f"block_{idx}",
            "bbox": region.get("bbox"),
            "text": region.get("text", ""),
            "type": "text_block",
        })

    return {
        "blocks": blocks,
        "bounded": True,
    }
