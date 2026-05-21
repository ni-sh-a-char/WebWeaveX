from __future__ import annotations

from typing import Any, Dict


def compile_multimodal_ir(
    layout: Dict[str, Any],
    tables: Dict[str, Any],
    forms: Dict[str, Any],
    charts: Dict[str, Any],
    ui: Dict[str, Any],
) -> Dict[str, Any]:
    blocks = layout.get("blocks", [])
    return {
        "ir": "multimodal",
        "semantic_blocks": blocks,
        "layout_tree": layout,
        "tables": tables,
        "charts": charts,
        "forms": forms,
        "navigation": [],
        "ui_components": ui,
        "layout": layout,
        "bounded": True,
    }
