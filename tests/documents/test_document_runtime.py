from core.documents.universal_document_extraction_engine import (
    extract_document_runtime,
)


def test_document_runtime():
    text = """
# Intro

Hello world [1]

| Name | Age |
| John | 20 |

# References

Book A
"""

    result = extract_document_runtime(
        text,
    )

    assert "document_ir" in result

    assert (
        result["tables"]["tables"]
    )

    assert (
        result["citations"]["citations"]
    )


def test_document_runtime_ir_shape():
    result = extract_document_runtime("# Title\n\nBody")
    ir = result["document_ir"]

    assert ir["ir"] == "document_runtime"
    assert ir["document_structure"]["sections"]
    assert ir["hierarchy"]["hierarchy"]
    assert ir["knowledge_graph"]["nodes"]


def test_presentation_and_spreadsheet_hooks():
    result = extract_document_runtime(
        "sheet data",
        slides=[{"title": "Slide 1", "content": ["a"]}],
        workbook={"Sheet1": [["a", "b"]]},
    )

    assert result["slides"]["slides"][0]["title"] == "Slide 1"
    assert result["worksheets"]["worksheets"][0]["sheet"] == "Sheet1"
