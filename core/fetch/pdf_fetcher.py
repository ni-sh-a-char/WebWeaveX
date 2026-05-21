from __future__ import annotations

import io
from typing import Dict

import requests
from pypdf import PdfReader

from core.fetch.base import FetchResponse


def fetch_pdf_sync(url: str, timeout: float = 15.0) -> Dict[str, object]:
    try:
        res = requests.get(url, timeout=timeout)
        res.raise_for_status()
        reader = PdfReader(io.BytesIO(res.content))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        return FetchResponse("pdf", url, res.status_code, "application/pdf", text, True, "", {"pages": str(len(reader.pages))}).to_dict()
    except Exception as exc:  # pragma: no cover
        return FetchResponse("pdf", url, 0, "application/pdf", "", False, str(exc), {}).to_dict()

