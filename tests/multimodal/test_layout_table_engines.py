from core.layout.layout_detection_engine import detect_layout_blocks
from core.tables.table_extraction_engine import extract_tables


def test_detect_layout_blocks_bounded():
    layout = detect_layout_blocks([
        {"bbox": [0, 0, 1, 1], "text": "hello"},
    ])

    assert layout["bounded"] is True
    assert layout["blocks"][0]["id"] == "block_0"


def test_extract_tables_pipe_rows():
    layout = detect_layout_blocks([
        {"bbox": [0, 0, 1, 1], "text": "x | y"},
    ])
    tables = extract_tables(layout)

    assert tables["bounded"] is True
    assert tables["tables"][0]["rows"] == [["x", "y"]]
