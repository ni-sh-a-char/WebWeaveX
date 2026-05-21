from core.files.pdf_extraction_engine import extract_pdf_text
from core.files.docx_extraction_engine import extract_docx_text
from core.files.html_file_extraction_engine import extract_html_file


def test_pdf_includes_document_runtime():
    result = extract_pdf_text("missing.pdf")

    assert "document_runtime" in result
    assert result["document_runtime"]["document_ir"]["ir"] == "document_runtime"


def test_docx_includes_document_runtime():
    result = extract_docx_text("missing.docx")

    assert "document_runtime" in result


def test_html_includes_document_runtime(tmp_path):
    html_path = tmp_path / "doc.html"
    html_path.write_text(
        "<html><body><h1>Intro</h1><p>Hello [1]</p></body></html>",
        encoding="utf-8",
    )

    result = extract_html_file(str(html_path))

    assert result["available"] is True
    assert "document_runtime" in result
    assert result["document_runtime"]["citations"]["citations"]
