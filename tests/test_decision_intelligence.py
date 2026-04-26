import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_context import MemoryContext
from core.context_schema import init_context
from core.multi_agent import intelligence_override, exploration_adjustment
from core.pattern_engine import apply_pattern_bias
from core.intelligence_engine import compute_cross_page_intelligence


def make_context():
    ctx = MemoryContext()
    init_context(ctx)
    ctx["meta"]["deterministic_mode"] = True
    ctx["goal"] = "python api documentation"
    return ctx


def test_override_triggers():
    print("\n=== OVERRIDE TRIGGER TEST ===")

    ctx = make_context()
    candidates = [
        {
            "url": "https://a.com/high",
            "score": 1.0,
            "intelligence": {
                "relevance": 0.9,
                "novelty": 0.8,
                "authority": 0.3,
                "composite_score": 0.91,
            },
        },
        {
            "url": "https://a.com/normal",
            "score": 9.0,
            "intelligence": {
                "relevance": 0.4,
                "novelty": 0.2,
                "authority": 0.2,
                "composite_score": 0.5,
            },
        },
    ]

    ordered = intelligence_override(ctx, candidates, "python api")

    if not ordered or ordered[0]["url"] != "https://a.com/high":
        print("FAIL: Override did not prioritize high intelligence candidate")
        return False

    if not ctx["intelligence"]["overrides"]:
        print("FAIL: Override tracking missing")
        return False

    print("PASS: Override trigger works")
    return True


def test_pattern_bias_works():
    print("\n=== PATTERN BIAS TEST ===")

    ctx = make_context()
    ctx["intelligence"]["patterns"] = {
        "high_value_patterns": [{"path": ["/docs/"], "avg_score": 3.0}],
        "dead_patterns": [{"path": ["/dead/"], "avg_score": -2.0}],
    }

    candidates = [
        {"url": "https://a.com/docs/page", "score": 1.0},
        {"url": "https://a.com/dead/page", "score": 1.0},
    ]

    updated = apply_pattern_bias(ctx, candidates)
    scores = {item["url"]: item["score"] for item in updated}

    if scores["https://a.com/docs/page"] <= scores["https://a.com/dead/page"]:
        print("FAIL: Pattern bias did not improve high-value candidate")
        return False

    print("PASS: Pattern bias works")
    return True


def test_cross_page_improves_ranking():
    print("\n=== CROSS-PAGE TEST ===")

    ctx = make_context()
    ctx["knowledge"]["topic_graph"] = {
        "python": ["https://a.com/docs", "https://a.com/api"],
        "api": ["https://a.com/api"],
    }
    ctx["knowledge"]["entities"] = [
        {"value": "python"},
        {"value": "api"},
        {"value": "documentation"},
    ]

    low = compute_cross_page_intelligence(ctx, "https://a.com/other", "gardening content")
    high = compute_cross_page_intelligence(ctx, "https://a.com/api", "python api documentation")

    if high <= low:
        print(f"FAIL: Cross-page intelligence not stronger for related page ({high} <= {low})")
        return False

    print("PASS: Cross-page intelligence improves related page score")
    return True


def test_deterministic_consistency():
    print("\n=== DECISION DETERMINISM TEST ===")

    ctx = make_context()
    ctx["crawl"]["path_history"] = ["https://a.com/docs"]

    candidates = [
        {"url": "https://b.com/a", "score": 1.0, "intelligence": {"relevance": 0.3, "novelty": 0.2, "authority": 0.2, "composite_score": 0.4}},
        {"url": "https://c.com/b", "score": 1.0, "intelligence": {"relevance": 0.3, "novelty": 0.2, "authority": 0.2, "composite_score": 0.4}},
    ]

    r1 = intelligence_override(ctx, exploration_adjustment(ctx, candidates), "goal")
    r2 = intelligence_override(ctx, exploration_adjustment(ctx, candidates), "goal")

    if r1 != r2:
        print("FAIL: Decision ordering not deterministic")
        return False

    print("PASS: Decision deterministic")
    return True


def run_all_tests():
    results = []
    results.append(("OVERRIDE", test_override_triggers()))
    results.append(("PATTERN", test_pattern_bias_works()))
    results.append(("CROSS_PAGE", test_cross_page_improves_ranking()))
    results.append(("DETERMINISM", test_deterministic_consistency()))

    print("\n" + "=" * 50)
    print("DECISION INTELLIGENCE REPORT")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        print(f"{name}: {'PASS' if result else 'FAIL'}")

    print(f"\nTOTAL: {'PASS' if passed == total else 'FAIL'} ({passed}/{total})")
    return passed == total


if __name__ == "__main__":
    run_all_tests()
