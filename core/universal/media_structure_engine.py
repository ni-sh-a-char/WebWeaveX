from __future__ import annotations


def extract_media_structure(text: str):
    source = (text or "").lower()
    media = []
    for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".webm", ".mp3", ".wav"]:
        if ext in source:
            media.append(ext.lstrip("."))
    return {"media_types": sorted(set(media)), "has_media": bool(media)}
