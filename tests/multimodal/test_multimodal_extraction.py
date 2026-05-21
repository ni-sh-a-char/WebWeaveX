from pathlib import Path

from core.multimodal.universal_multimodal_extraction_engine import (
    extract_multimodal,
)
from core.layout.layout_detection_engine import detect_layout_blocks
from core.tables.table_extraction_engine import extract_tables
from core.vision.form_extraction_engine import extract_forms
from core.vision.ui_component_detection_engine import detect_ui_components
from core.vision.chart_detection_engine import detect_charts
from core.ir.multimodal_ir import compile_multimodal_ir


def test_multimodal_pipeline():
    result = extract_multimodal("tests/data/test_image.png")

    assert "multimodal_ir" in result
    assert result["bounded"] is True


def test_layout_and_table_pipeline():
    layout = detect_layout_blocks([
        {"bbox": [0, 0, 10, 10], "text": "a | b | c"},
        {"bbox": [0, 20, 10, 10], "text": "email"},
        {"bbox": [0, 40, 10, 10], "text": "submit"},
        {"bbox": [0, 60, 10, 10], "text": "revenue growth"},
    ])

    tables = extract_tables(layout)
    forms = extract_forms(layout)
    ui = detect_ui_components(layout)
    charts = detect_charts(layout)
    ir = compile_multimodal_ir(layout, tables, forms, charts, ui)

    assert len(tables["tables"]) == 1
    assert any(f["field"] == "email" for f in forms["forms"])
    assert any(c["type"] == "button" for c in ui["components"])
    assert charts["charts"][0]["detected"] is True
    assert ir["ir"] == "multimodal"


def test_multimodal_missing_file():
    result = extract_multimodal("tests/data/missing_image.png")

    assert "multimodal_ir" in result
    assert result["ocr"]["available"] is False
