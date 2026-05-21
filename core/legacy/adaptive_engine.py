"""
WebWeaveX Adaptive Engine (Phase 7)

Purpose:
    Self-healing extraction:
    - Detect low-value pages
    - Extract links
    - Fetch deeper content
    - Recover meaningful data

STRICT RULES:
    - Deterministic
    - No external libraries
    - Fail-safe
"""

from typing import Dict, Any, List
import re

from core.extraction_engine import extract_content
from core.fetch_engine import _safe_fetch


# ---------------------------
# SEARCH RESULT LINK EXTRACTION
# ---------------------------

def extract_search_links(html: str) -> List[str]:
    """
    Extract candidate URLs from search result pages.
    """

    if not html:
        return []

    links = re.findall(r'href=["\'](.*?)["\']', html, flags=re.IGNORECASE)

    cleaned = []

    for link in links:
        link = link.strip()

        if link.startswith("/url?q="):
            link = link.replace("/url?q=", "").split("&")[0]

        if not link.startswith("http"):
            continue

        link_lower = link.lower()

        if any(bad in link_lower for bad in [
            "google.com",
            "accounts.",
            "support.",
            "policies.",
            "preferences.",
            "javascript:",
            "#",
            "login",
            "signup",
            "ads"
        ]):
            continue

        cleaned.append(link)

    return sorted(set(cleaned))


def is_high_value_link(url: str) -> bool:
    """
    Check if link is high value.
    """

    if not isinstance(url, str):
        return False

    url_lower = url.lower()

    return any(k in url_lower for k in [
        "github.com",
        "stackoverflow.com",
        "medium.com",
        "dev.to",
        "docs",
        "tutorial",
        "guide",
        "article",
        "readme"
    ])


def filter_links_by_source(links: List[str], source: str) -> List[str]:
    """
    Filter links by source to get relevant content.
    """

    if not links:
        return []

    filtered = []

    for link in links:
        l = link.lower()

        if source == "github":
            if any(k in l for k in [
                "/blob/",
                "/tree/",
                "/commit/",
                "/issues",
                "/pull",
                "github.com/"
            ]):
                filtered.append(link)

        elif source == "stackoverflow":
            if any(k in l for k in [
                "/questions/",
                "/q/",
                "stackoverflow.com/"
            ]):
                filtered.append(link)

        else:
            filtered.append(link)

    if not filtered:
        return links

    return filtered


# ---------------------------
# LINK PRIORITIZATION
# ---------------------------

def prioritize_links(links: List[str], source: str) -> List[str]:
    """
    Prioritize links based on source relevance.
    """

    if not links:
        return []

    def score(link: str) -> int:
        link_lower = link.lower()
        s = 0

        if source in link_lower:
            s += 5

        if "github.com" in link_lower:
            s += 4

        if "stackoverflow.com" in link_lower:
            s += 3

        if "docs" in link_lower:
            s += 2

        return s

    return sorted(
        links,
        key=lambda x: (-score(x), x)
    )


# ---------------------------
# REAL PAGE FETCHING
# ---------------------------

def fetch_real_pages(html: str, source: str, max_pages: int = 3) -> List[Dict[str, Any]]:
    """
    Extract and fetch real content pages.
    """

    links = extract_search_links(html)

    links = filter_links_by_source(links, source)

    filtered = [l for l in links if is_high_value_link(l)]

    if not filtered:
        filtered = links  # fallback

    filtered = prioritize_links(filtered, source)

    results = []

    for link in filtered[:max_pages]:
        try:
            page_html = _safe_fetch(link)

            if not page_html:
                continue

            results.append({
                "url": link,
                "html": page_html
            })

        except Exception:
            continue

    return results


# ---------------------------
# LINK EXTRACTION
# ---------------------------

def extract_links(html: str) -> List[str]:
    if not html:
        return []

    links = re.findall(r'href=["\'](.*?)["\']', html, flags=re.IGNORECASE)

    clean_links = []
    for link in links:
        if link.startswith("http") and not any(
            bad in link.lower() for bad in ["login", "signup", "ads", "#"]
        ):
            clean_links.append(link)

    return sorted(set(clean_links))  # deduplicate + deterministic


# ---------------------------
# LOW VALUE DETECTION
# ---------------------------

GARBAGE_PATTERNS = [
    "click here if you are not redirected",
    "enable javascript",
    "human verification",
    "captcha",
    "access denied",
    "service unavailable",
    "checking your browser",
    "please wait",
    "redirecting"
]

def is_garbage_page(text: str) -> bool:
    if not text or len(text) < 50:
        return True
    text_lower = text.lower()
    for pattern in GARBAGE_PATTERNS:
        if pattern in text_lower:
            return True
    return False


def is_low_value(content: Dict[str, Any], url: str = "") -> bool:
    meta = content.get("metadata", {})
    text_len = meta.get("text_length", 0)
    code_blocks = meta.get("code_blocks", 0)

    url_lower = (url or "").lower()

    if any(k in url_lower for k in [
        "search?",
        "/search",
        "google.com",
        "bing.com"
    ]):
        return True

    text = content.get("text", "")
    if is_garbage_page(text):
        return True

    if code_blocks > 0:
        return False

    if text_len < 300:
        return True

    return False


# ---------------------------
# SELF-HEALING LOGIC
# ---------------------------

def recover_content(html: str, source: str = "", max_links: int = 3) -> Dict[str, Any]:
    """
    Try to recover useful content from deeper links.
    """
    max_links = min(max_links, 5)  # safety bound
    
    links = extract_links(html)

    if source == "github":
        links = [l for l in links if "github.com" in l]
    elif source == "stackoverflow":
        links = [l for l in links if "stackoverflow.com" in l]

    recovered = []

    for link in links[:max_links]:
        try:
            sub_html = _safe_fetch(link)

            if not sub_html:
                continue

            content = extract_content(sub_html)

            meta = content.get("metadata", {})
            text_len = meta.get("text_length", 0)
            code_blocks = meta.get("code_blocks", 0)

            if text_len > 200 or code_blocks > 0:
                recovered.append({
                    "url": link,
                    "content": content,
                    "score": len(content.get("text", "")) + len(content.get("code", [])) * 100
                })

        except Exception:
            continue

    return {
        "recovered": recovered,
        "recovered_count": len(recovered)
    }


# ---------------------------
# MAIN ADAPTIVE ENGINE
# ---------------------------

def adaptive_extract(fetch_results: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(fetch_results, dict):
        raise TypeError("fetch_results must be dict")

    if "results" not in fetch_results:
        raise ValueError("Missing results")

    final_results = []

    for item in fetch_results["results"]:
        html = item.get("html", "")

        base_content = extract_content(html)

        should_crawl = is_low_value(base_content, item.get("url", ""))

        if item.get("source") in ["github", "stackoverflow"]:
            should_crawl = True

        if should_crawl:
            real_pages = fetch_real_pages(html, item.get("source", ""))

            recovered = []

            for page in real_pages:
                try:
                    content = extract_content(page["html"])

                    meta = content.get("metadata", {})
                    text_len = meta.get("text_length", 0)
                    code_blocks = meta.get("code_blocks", 0)

                    if text_len > 200 or code_blocks > 0:
                        recovered.append({
                            "url": page["url"],
                            "content": content
                        })
                except Exception:
                    continue

            final_results.append({
                "source": item.get("source"),
                "url": item.get("url"),
                "query": item.get("query", ""),
                "base": base_content,
                "recovered": {
                    "recovered": recovered,
                    "recovered_count": len(recovered)
                },
                "input_signature": item.get("input_signature", "")
            })

        else:
            final_results.append({
                "source": item.get("source"),
                "url": item.get("url"),
                "query": item.get("query", ""),
                "base": base_content,
                "recovered": {
                    "recovered": [],
                    "recovered_count": 0
                },
                "input_signature": item.get("input_signature", "")
            })

    return {
        "adaptive_results": final_results,
        "total": len(final_results),
        "version": "v1_phase_10"
    }


# ---------------------------
# VALIDATION
# ---------------------------

def validate_adaptive_engine() -> bool:
    test_html = """
    <html>
        <body>
            <a href="https://example.com/page1">Link1</a>
            <pre>def x(): pass</pre>
        </body>
    </html>
    """

    result = adaptive_extract({
        "results": [{
            "source": "test",
            "url": "test",
            "html": test_html
        }]
    })

    if not isinstance(result, dict):
        raise RuntimeError("Invalid result")

    if "adaptive_results" not in result:
        raise RuntimeError("Missing adaptive_results")

    return True


if __name__ == "__main__":
    ok = validate_adaptive_engine()
    print("ADAPTIVE ENGINE VALIDATION:", "PASS" if ok else "FAIL")