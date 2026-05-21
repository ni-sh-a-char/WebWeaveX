from __future__ import annotations

def inspect_archive(name_or_text: str):
    src = (name_or_text or '').lower()
    formats = [ext for ext in ['.zip','.tar','.tgz','.gz','.rar','.7z'] if ext in src]
    return {"is_archive": bool(formats), "formats": sorted(set(formats))}
