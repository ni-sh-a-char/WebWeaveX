from __future__ import annotations

from typing import Any, Dict

from core.ocr.ocr_engine import extract_ocr
from core.layout.layout_detection_engine import (
    detect_layout_blocks,
)
from core.tables.table_extraction_engine import (
    extract_tables,
)
from core.vision.form_extraction_engine import (
    extract_forms,
)
from core.vision.chart_detection_engine import (
    detect_charts,
)
from core.vision.ui_component_detection_engine import (
    detect_ui_components,
)
from core.ir.multimodal_ir import (
    compile_multimodal_ir,
)


def extract_multimodal(
    path: str,
) -> Dict[str, Any]:
    ocr = extract_ocr(path)

    layout = detect_layout_blocks(
        ocr.get("regions", []),
    )

    tables = extract_tables(layout)

    forms = extract_forms(layout)

    charts = detect_charts(layout)

    ui = detect_ui_components(layout)

    multimodal_ir = compile_multimodal_ir(
        layout=layout,
        tables=tables,
        forms=forms,
        charts=charts,
        ui=ui,
    )

    return {
        "ocr": ocr,
        "layout": layout,
        "tables": tables,
        "forms": forms,
        "charts": charts,
        "ui": ui,
        "multimodal_ir": multimodal_ir,
        "bounded": True,
    }
