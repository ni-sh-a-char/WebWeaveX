from __future__ import annotations

import unicodedata


def normalize_unicode(value: str) -> str:
    return unicodedata.normalize("NFC", value or "")
