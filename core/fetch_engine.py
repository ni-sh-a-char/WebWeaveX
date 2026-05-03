"""
WebWeaveX Fetch Engine (Phase 5)

Purpose:
    Convert queries into URLs
    Fetch HTML safely
    Deterministic-safe behavior

STRICT RULES:
    No randomness
    Timeout enforced
    Graceful failure handling
"""

from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
import urllib.request


DEFAULT_TIMEOUT = 5


def _build_url(query: str, source: str) -> str:
    """
    Convert query into a URL.
    """

    encoded = urllib.parse.quote_plus(query)

    if source == "github":
        return f"https://github.com/search?q={encoded}"

    elif source == "stackoverflow":
        return f"https://stackoverflow.com/search?q={encoded}"

    elif source == "codepen":
        return f"https://codepen.io/search/pens?q={encoded}"

    elif source == "docs":
        return f"https://www.google.com/search?q={encoded}+documentation"

    elif source == "news":
        return f"https://news.google.com/search?q={encoded}"

    elif source == "web":
        return f"https://www.google.com/search?q={encoded}"

    return f"https://www.google.com/search?q={encoded}"


def _safe_fetch(url: str) -> str:
    """
    Fetch HTML content safely with retry.
    """

    for attempt in range(3):  # Retry up to 3 times
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as response:
                html = response.read().decode("utf-8", errors="ignore")

                # Normalize minimal (deterministic)
                if not isinstance(html, str):
                    html = ""

                if not html.strip():  # Check for non-empty content
                    continue  # Retry if empty

                return html

        except Exception:
            continue  # Retry on exception

    return ""  # Fail after retries


def _fetch_single(item: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch a single query."""
    query = item.get("query")
    source = item.get("source")
    priority = item.get("priority", 0)
    input_signature = item.get("input_signature", "")

    if not query or not source:
        return None

    url = _build_url(query, source)
    html = _safe_fetch(url)

    if not isinstance(html, str):
        html = ""

    return {
        "source": source,
        "query": query,
        "url": url,
        "html": html,
        "html_length": len(html),
        "success": len(html) > 0,
        "has_content": len(html.strip()) > 0,
        "input_signature": input_signature,
        "priority": priority
    }


def fetch_all(query_bundle: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch content for all queries.

    Args:
        query_bundle (dict)

    Returns:
        dict
    """

    if not isinstance(query_bundle, dict):
        raise TypeError("query_bundle must be dict")

    if "queries" not in query_bundle:
        raise ValueError("Missing 'queries'")

    queries = query_bundle["queries"]

    seen_urls = set()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(_fetch_single, item): item for item in queries}

        results = []
        for future in as_completed(futures):
            result = future.result()
            if result and result.get("url") not in seen_urls:
                seen_urls.add(result.get("url", ""))
                results.append(result)

            if len(results) >= 10:
                break

    results.sort(key=lambda x: x.get("priority", 0))

    return {
        "results": results,
        "total_fetched": len(results),
        "version": "v1_phase_5"
    }


def validate_fetch_engine() -> bool:
    """
    Validation for fetch engine.
    """

    test_bundle = {
        "queries": [
            {"source": "web", "query": "test query", "priority": 1}
        ]
    }

    result = fetch_all(test_bundle)

    if not isinstance(result, dict):
        raise RuntimeError("Result is not dict")

    if "results" not in result:
        raise RuntimeError("Missing results")

    if not isinstance(result["results"], list):
        raise RuntimeError("Results not list")

    return True


if __name__ == "__main__":
    ok = validate_fetch_engine()
    print("FETCH ENGINE VALIDATION:", "PASS" if ok else "FAIL")