import json
import re


def normalize_text(text):
    if text is None:
        return None
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text if text else None


def normalize_data(data):
    title = normalize_text(data.get("title"))
    meta_description = normalize_text(data.get("meta_description"))
    
    headings = sorted([h.get("text") for h in data.get("headings", []) if h.get("text")])
    links = sorted([link.get("url") for link in data.get("links", []) if link.get("url")])
    code_blocks = sorted([cb.get("content") for cb in data.get("code_blocks", []) if cb.get("content")])
    embedded_json = sorted([ej.get("content") for ej in data.get("embedded_json", []) if ej.get("content")])
    
    return {
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "links": links,
        "code_blocks": code_blocks,
        "embedded_json": embedded_json
    }


def canonicalize(data):
    normalized = normalize_data(data)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))


def canonicalize_from_extracted(html, base_url):
    from .parser import extract_all
    data = extract_all(html, base_url)
    return canonicalize(data)