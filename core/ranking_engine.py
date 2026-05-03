"""
WebWeaveX Ranking Engine (Phase 8)

Purpose:
    Rank extracted results based on quality and usefulness

STRICT RULES:
    Deterministic
    No external dependencies
    No randomness
"""

from typing import Dict, Any, List


# ---------------------------
# SCORING FUNCTIONS
# ---------------------------

def _score_text(content: Dict[str, Any]) -> int:
    if not isinstance(content, dict):
        return 0
    
    text_len = content.get("metadata", {}).get("text_length", 0)

    if text_len > 2000:
        return 5
    elif text_len > 1000:
        return 4
    elif text_len > 500:
        return 3
    elif text_len > 200:
        return 2
    elif text_len > 50:
        return 1
    return 0


def _score_code(content: Dict[str, Any]) -> int:
    if not isinstance(content, dict):
        return 0
    
    code_blocks = content.get("metadata", {}).get("code_blocks", 0)

    if code_blocks >= 3:
        return 5
    elif code_blocks == 2:
        return 4
    elif code_blocks == 1:
        return 3
    return 0


def _score_recovery(recovered: Dict[str, Any] | None) -> int:
    if not isinstance(recovered, dict):
        return 0
    
    count = recovered.get("recovered_count", 0)

    if count >= 3:
        return 5
    elif count == 2:
        return 3
    elif count == 1:
        return 1

    return 0


def _score_source(source: str, keywords: str = "") -> int:
    base = 0
    if source == "github":
        base = 5
    elif source == "stackoverflow":
        base = 4
    elif source == "codepen":
        base = 3
    elif source == "docs":
        base = 4
    elif source == "web":
        base = 2
    elif source == "news":
        base = 1

    keywords_lower = keywords.lower()
    if "code" in keywords_lower or "api" in keywords_lower:
        if source == "github":
            base += 2
    elif "error" in keywords_lower or "fix" in keywords_lower:
        if source == "stackoverflow":
            base += 2

    return min(base, 7)


# ---------------------------
# FINAL SCORE
# ---------------------------

def compute_score(item: Dict[str, Any], keywords: str = "") -> int:
    base = item.get("base", {})
    recovered = item.get("recovered")
    source = item.get("source", "")

    score = 0

    score += _score_text(base)
    score += _score_code(base)
    score += _score_recovery(recovered)
    score += _score_source(source, keywords)

    return min(score, 10)


# ---------------------------
# RANKING FUNCTION
# ---------------------------

def rank_results(adaptive_output: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(adaptive_output, dict):
        raise TypeError("adaptive_output must be dict")

    if "adaptive_results" not in adaptive_output:
        raise ValueError("Missing adaptive_results")

    if not isinstance(adaptive_output["adaptive_results"], list):
        raise TypeError("adaptive_results must be a list")

    ranked = []

    for item in adaptive_output["adaptive_results"]:
        if not isinstance(item, dict):
            continue

        keywords = item.get("query", "")
        score = compute_score(item, keywords)

        ranked.append({
            **item,
            "score": score
        })

    if not ranked:
        ranked.append({
            "source": "fallback",
            "url": "",
            "base": {"text": "fallback", "code": [], "metadata": {"text_length": 1, "code_blocks": 0}},
            "recovered": {"recovered": [], "recovered_count": 0},
            "input_signature": "",
            "score": 0
        })

    # Deterministic sorting
    ranked_sorted = sorted(
        ranked,
        key=lambda x: (
            -x["score"],
            x.get("source", ""),
            x.get("url", "")
        )
    )

    top_result = ranked_sorted[0] if ranked_sorted else {"source": "none", "url": "", "base": {"text": "", "code": [], "metadata": {"text_length": 0, "code_blocks": 0}}, "recovered": {"recovered": [], "recovered_count": 0}, "input_signature": ""}

    return {
        "ranked_results": ranked_sorted,
        "top_result": top_result,
        "total": len(ranked_sorted),
        "version": "v1_phase_8"
    }


# ---------------------------
# VALIDATION
# ---------------------------

def validate_ranking_engine() -> bool:
    test_input = {
        "adaptive_results": [
            {
                "source": "github",
                "url": "a",
                "base": {
                    "metadata": {"text_length": 1500, "code_blocks": 2}
                },
                "recovered": None
            },
            {
                "source": "web",
                "url": "b",
                "base": {
                    "metadata": {"text_length": 300, "code_blocks": 0}
                },
                "recovered": None
            }
        ]
    }

    result = rank_results(test_input)

    if not isinstance(result, dict):
        raise RuntimeError("Invalid output")

    if "ranked_results" not in result:
        raise RuntimeError("Missing ranked_results")

    if result["top_result"]["source"] != "github":
        raise RuntimeError("Ranking failed")

    return True


if __name__ == "__main__":
    ok = validate_ranking_engine()
    print("RANKING ENGINE VALIDATION:", "PASS" if ok else "FAIL")