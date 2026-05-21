from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from core.browser.html_semantic_extraction_engine import (
    extract_semantic_html,
)
from core.dom.dom_reconstruction_engine import reconstruct_dom
from core.extraction.semantic_content_extraction_engine import (
    extract_semantic_content,
)
from core.ir.browser_ir import compile_browser_ir
from core.documents.universal_document_extraction_engine import (
    extract_document_runtime,
)

MAX_HTML_FILE = 10_000_000


def extract_html_file(path: str) -> Dict[str, Any]:
    if not Path(path).is_file():
        return {
            "available": False,
            "reason": "file_not_found",
            "bounded": True,
        }

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read(MAX_HTML_FILE)

    semantic = extract_semantic_html(html)
    dom = reconstruct_dom(html)
    extraction = extract_semantic_content(html)

    browser_ir = compile_browser_ir(
        runtime={
            "available": True,
            "source": "file",
            "path": path,
            "title": semantic.get("title", ""),
            "html": html[:MAX_HTML_FILE],
            "bounded": True,
        },
        dom=dom,
        extraction=extraction,
        network={"requests": [], "bounded": True},
    )

    extracted_text = semantic.get("text", "")

    document_runtime = extract_document_runtime(
        extracted_text,
    )

    return {
        "available": True,
        "html": html[:MAX_HTML_FILE],
        "text": extracted_text[:5_000_000],
        "semantic": semantic,
        "dom": dom,
        "extraction": extraction,
        "browser_ir": browser_ir,
        "document_runtime": document_runtime,
        "bounded": True,
    }
