from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from core.crypto.kaalka_hash_engine import compute_kaalka_hash, compute_kaalka_hash_payload

_UUID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
    re.IGNORECASE,
)
_TIMESTAMP_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b"
)
_EPOCH_MS_RE = re.compile(r"\b1[0-9]{12,13}\b")
_REACT_KEY_RE = re.compile(
    r'data-react(?:id|root|helmet|fiber|scroll|strictmode)?="[^"]*"',
    re.IGNORECASE,
)
_VUE_KEY_RE = re.compile(r'data-v-[a-z0-9]+="[^"]*"', re.IGNORECASE)
_ANGULAR_RE = re.compile(r'ng-version="[^"]*"|_ngcontent-[^=]+="[^"]*"', re.IGNORECASE)
_HYDRATION_RE = re.compile(
    r'data-(?:hydration|stale|server-rendered|reactroot|nextjs-scroll-focus|nuxt)(?:-id)?="[^"]*"',
    re.IGNORECASE,
)
_NONCE_RE = re.compile(
    r'(?:nonce|csp-nonce|data-nonce|integrity)="[^"]*"',
    re.IGNORECASE,
)
_DYNAMIC_ATTR_RE = re.compile(
    r'\s(?:data-(?:vm|gh|turbo|pjax|analytics|ga|gtm|session|request-id|view-component|'
    r'hydro-click|hovercard-url|octo-click|turbo-permanent|csrf|catalyst|random|app|'
    r'client|feature|testid|token)|'
    r'aria-(?:busy|live)="[^"]*"|'
    r'style="[^"]*")',
    re.IGNORECASE,
)
_CSRF_META_RE = re.compile(
    r'<meta[^>]+(?:csrf-token|authenticity-token|nonce)[^>]*>',
    re.IGNORECASE,
)
_SCRIPT_BLOB_RE = re.compile(
    r"<script[^>]*>.*?</script>",
    re.IGNORECASE | re.DOTALL,
)
_STYLE_BLOB_RE = re.compile(
    r"<style[^>]*>.*?</style>",
    re.IGNORECASE | re.DOTALL,
)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_BASE64_BLOB_RE = re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")
_SRCSET_RE = re.compile(r'srcset="[^"]*"', re.IGNORECASE)
_TAG_ATTR_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)((?:\s[^>]+)?)>")


def _normalize_attributes(attr_blob: str) -> str:
    if not attr_blob or not attr_blob.strip():
        return ""
    pairs: List[Tuple[str, str]] = []
    for match in re.finditer(
        r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+)))?',
        attr_blob,
    ):
        name = match.group(1).lower()
        value = match.group(2) or match.group(3) or match.group(4) or ""
        if name.startswith("on"):
            continue
        pairs.append((name, value))
    pairs.sort(key=lambda p: (p[0], p[1]))
    return " ".join(f'{n}="{v}"' if v else n for n, v in pairs)


def _compact_dom(html: str) -> str:
    text = _COMMENT_RE.sub("", html)
    text = re.sub(r">\s+<", "><", text)
    text = re.sub(r"\s+", " ", text)

    def _sort_tag(match: re.Match[str]) -> str:
        tag = match.group(1).lower()
        attrs = _normalize_attributes(match.group(2) or "")
        return f"<{tag}{(' ' + attrs) if attrs else ''}>"

    return _TAG_ATTR_RE.sub(_sort_tag, text).strip()


def stabilize_dom_html(html: str) -> Tuple[str, Dict[str, Any]]:
    """Normalize volatile DOM for deterministic Browser IR and replay."""
    original_len = len(html)
    text = html

    replacements: Dict[str, int] = {
        "uuids": 0,
        "timestamps": 0,
        "epoch_ms": 0,
        "react_keys": 0,
        "vue_keys": 0,
        "angular_keys": 0,
        "hydration": 0,
        "nonces": 0,
        "dynamic_attrs": 0,
        "script_blobs": 0,
        "style_blobs": 0,
        "base64_blobs": 0,
        "srcset": 0,
    }

    def _sub_count(pattern: re.Pattern[str], repl: str, key: str) -> None:
        nonlocal text
        text, n = pattern.subn(repl, text)
        replacements[key] = n

    _sub_count(_UUID_RE, "00000000-0000-4000-8000-000000000000", "uuids")
    _sub_count(_TIMESTAMP_RE, "1970-01-01T00:00:00Z", "timestamps")
    _sub_count(_EPOCH_MS_RE, "0", "epoch_ms")
    _sub_count(_REACT_KEY_RE, 'data-reactid="stable"', "react_keys")
    _sub_count(_VUE_KEY_RE, 'data-v-stable="1"', "vue_keys")
    _sub_count(_ANGULAR_RE, 'ng-version="stable"', "angular_keys")
    _sub_count(_HYDRATION_RE, 'data-hydration="stable"', "hydration")
    _sub_count(_NONCE_RE, 'nonce="stable"', "nonces")
    _sub_count(_DYNAMIC_ATTR_RE, "", "dynamic_attrs")
    _sub_count(_SCRIPT_BLOB_RE, "<script></script>", "script_blobs")
    _sub_count(_STYLE_BLOB_RE, "<style></style>", "style_blobs")
    _sub_count(_CSRF_META_RE, "<meta>", "dynamic_attrs")
    _sub_count(_BASE64_BLOB_RE, "BASE64STABLE", "base64_blobs")
    _sub_count(_SRCSET_RE, 'srcset="stable"', "srcset")

    text = _compact_dom(text)

    meta = {
        "original_bytes": original_len,
        "stabilized_bytes": len(text),
        "replacements": replacements,
        "stabilized_hash": compute_kaalka_hash(text[:1_000_000]),
        "bounded": True,
    }
    return text, meta


def compute_stable_dom_hash(html: str) -> str:
    """Canonical DOM hash after stabilization pipeline."""
    stable, _ = stabilize_dom_html(html)
    return compute_kaalka_hash(stable[:1_000_000])


def stabilize_extraction_payload(
    extraction: Dict[str, Any],
) -> Dict[str, Any]:
    """Strip volatile fields from semantic extraction dicts."""
    if not isinstance(extraction, dict):
        return {"bounded": True}
    stable = {
        k: v
        for k, v in sorted(extraction.items())
        if k
        not in (
            "timestamp",
            "fetched_at",
            "nonce",
            "request_id",
            "generated_at",
            "updated_at",
        )
    }
    links = stable.get("links", stable.get("anchors", []))
    if isinstance(links, list):

        def _link_key(item: Any) -> tuple:
            if isinstance(item, dict):
                return (
                    str(item.get("href", item.get("url", ""))),
                    str(item.get("text", "")),
                )
            return (str(item), "")

        stable["links"] = sorted(links, key=_link_key)
    stable["bounded"] = True
    return stable


def stable_browser_ir_fingerprint(
    url: str,
    title: str,
    dom_stabilization: Dict[str, Any],
    extraction: Dict[str, Any],
    authenticated: bool = False,
) -> str:
    """Deterministic browser IR identity from stabilized structural fields only."""
    return compute_kaalka_hash_payload(
        {
            "url": url,
            "title": title,
            "dom_hash": dom_stabilization.get("stabilized_hash", ""),
            "links": extraction.get("links", [])[:200],
            "authenticated": authenticated,
        }
    )
