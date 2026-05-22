"""
WebWeaveX Extraction Engine (Phase 6)

Purpose:
    Convert raw HTML into structured content:
    - Clean text
    - Code blocks

STRICT RULES:
    - No randomness
    - No external dependencies
    - Deterministic output
    - Fail-safe behavior
"""

from typing import Dict, Any, List
import re


# ---------------------------
# CLEANING FUNCTIONS
# ---------------------------

def _remove_scripts(html: str) -> str:
    return re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)


def _remove_styles(html: str) -> str:
    return re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)


def _remove_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)


def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html)


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------
# TEXT EXTRACTION
# ---------------------------

def extract_text(html: str) -> str:
    if not html:
        return ""

    html = _remove_scripts(html)
    html = _remove_styles(html)
    html = _remove_comments(html)

    text = _strip_tags(html)
    text = _normalize_whitespace(text)

    return text


# ---------------------------
# CODE EXTRACTION
# ---------------------------

def _extract_pre_blocks(html: str) -> List[str]:
    blocks = re.findall(r"<pre.*?>(.*?)</pre>", html, flags=re.DOTALL | re.IGNORECASE)
    return [b.strip() for b in blocks if b.strip()]


def _extract_code_blocks(html: str) -> List[str]:
    blocks = re.findall(r"<code.*?>(.*?)</code>", html, flags=re.DOTALL | re.IGNORECASE)
    return [b.strip() for b in blocks if b.strip()]


def extract_code(html: str) -> List[Dict[str, Any]]:
    if not html:
        return []

    code_blocks = []

    pre_blocks = _extract_pre_blocks(html)
    code_blocks_raw = _extract_code_blocks(html)

    all_blocks = pre_blocks + code_blocks_raw

    for idx, block in enumerate(all_blocks):
        code_blocks.append({
            "id": idx,
            "content": block,
            "length": len(block),
        })

    return code_blocks


# ---------------------------
# MAIN EXTRACTION FUNCTION
# ---------------------------

def extract_content(html: str) -> Dict[str, Any]:
    if not isinstance(html, str):
        raise TypeError("html must be a string")

    if html.strip() == "":
        return {
            "text": "",
            "code": [],
            "metadata": {"empty": True}
        }

    text = extract_text(html)
    code = extract_code(html)

    return {
        "text": text,
        "code": code,
        "metadata": {
            "text_length": len(text),
            "code_blocks": len(code)
        }
    }


# ---------------------------
# VALIDATION
# ---------------------------

def validate_extraction_engine() -> bool:
    test_html = """
    <html>
        <body>
            <h1>Hello World</h1>
            <pre>def test(): return 1</pre>
            <script>var x = 1;</script>
        </body>
    </html>
    """

    result = extract_content(test_html)

    if not isinstance(result, dict):
        raise RuntimeError("Result is not dict")

    if "text" not in result:
        raise RuntimeError("Missing text")

    if "code" not in result:
        raise RuntimeError("Missing code")

    if len(result["code"]) == 0:
        raise RuntimeError("Code extraction failed")

    if "script" in result["text"].lower():
        raise RuntimeError("Script not removed")

    return True


class BaseExtractor:
    """Minimal extractor contract for site-specific extractors."""

    priority = 0

    def can_handle(self, url: str, html: str, metadata: Dict[str, Any]) -> bool:
        return False

    def extract(self, url: str, html: str, metadata: Dict[str, Any]) -> Dict[str, Any] | None:
        raise NotImplementedError


if __name__ == "__main__":
    ok = validate_extraction_engine()
    print("EXTRACTION ENGINE VALIDATION:", "PASS" if ok else "FAIL")