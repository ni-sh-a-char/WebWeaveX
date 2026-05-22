from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".pptx": "pptx",
    ".xlsx": "xlsx",
    ".csv": "csv",
    ".json": "json",
    ".xml": "xml",
    ".html": "html",
    ".md": "markdown",
    ".txt": "text",
    ".py": "repository",
    ".js": "repository",
    ".ts": "repository",
    ".zip": "archive",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
}


def detect_input_type(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return "url"
    ext = Path(path).suffix.lower()
    return SUPPORTED_EXTENSIONS.get(ext, "unknown")


def ingest_input(path: str) -> Dict[str, Any]:
    input_type = detect_input_type(path)

    if input_type == "image":
        from core.multimodal.universal_multimodal_extraction_engine import (
            extract_multimodal,
        )

        multimodal = extract_multimodal(path)

        return {
            "path": path,
            "type": "image",
            "input_type": input_type,
            "supported": True,
            "multimodal": multimodal,
            "bounded": True,
        }

    return {
        "path": path,
        "input_type": input_type,
        "supported": input_type != "unknown",
        "bounded": True,
    }
