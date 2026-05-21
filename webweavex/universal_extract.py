from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from core.ingestion.universal_ingestion_engine import (
    ingest_input,
)
from core.files.pdf_extraction_engine import (
    extract_pdf_text,
)
from core.files.docx_extraction_engine import (
    extract_docx_text,
)
from core.multimodal.universal_multimodal_extraction_engine import (
    extract_multimodal,
)
from core.archive.archive_extraction_engine import (
    extract_archive,
)
from core.files.html_file_extraction_engine import (
    extract_html_file,
)
from core.ir.media_ir import compile_media_ir
from core.repository.universal_repository_extraction_engine import (
    extract_repository as extract_repository_path,
)


def universal_extract(path: str) -> Dict[str, Any]:
    info = ingest_input(path)

    input_type = info["input_type"]

    if input_type == "pdf":
        payload = extract_pdf_text(path)
    elif input_type == "docx":
        payload = extract_docx_text(path)
    elif input_type == "image":
        multimodal = extract_multimodal(path)
        return {
            "ingestion": info,
            "extraction": multimodal,
            "multimodal_ir": multimodal.get("multimodal_ir", {}),
            "bounded": True,
        }
    elif input_type == "archive":
        payload = extract_archive(path)
    elif input_type == "html":
        payload = extract_html_file(path)
    elif input_type == "repository":
        root = path
        if Path(path).is_file():
            root = str(Path(path).parent)
        repo = extract_repository_path(root)
        return {
            "ingestion": info,
            "extraction": repo,
            "repository_ir": repo.get("repository_ir", {}),
            "bounded": True,
        }
    else:
        return {
            "unsupported": True,
            "input_type": input_type,
            "ingestion": info,
            "bounded": True,
        }

    return {
        "ingestion": info,
        "extraction": payload,
        "media_ir": compile_media_ir(payload),
        "bounded": True,
    }
