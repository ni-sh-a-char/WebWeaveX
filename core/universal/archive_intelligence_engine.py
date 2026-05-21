from __future__ import annotations


def extract_archive_intelligence(path_or_text: str):
    source = (path_or_text or "").lower()
    formats = []
    for ext in [".zip", ".tar", ".gz", ".tgz", ".rar", ".7z"]:
        if ext in source:
            formats.append(ext.lstrip("."))
    return {"archive_formats": sorted(set(formats)), "is_archive": bool(formats)}
