import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_context import MemoryContext
from core.context_schema import init_context
from core.intelligence_engine import compute_intelligence
from core.multi_agent import AnalyzerAgent


def make_context(goal="python api docs"):
    ctx = MemoryContext()
    init_context(ctx)
    ctx["goal"] = goal
    ctx["meta"]["deterministic_mode"] = True
    return ctx


def test_intelligence_determinism():
    print("\n=== INTELLIGENCE DETERMINISM TEST ===")

    ctx = make_context()
    content = {
        "text": "Python API documentation with endpoints and examples.",
        "code": ["def get_docs(): return True"],
        "structured": {"title": "Docs", "sections": ["API", "Examples"]},
    }

    i1 = compute_intelligence(ctx, "https://example.com/docs/api", content, {"source": "test"})
    i2 = compute_intelligence(ctx, "https://example.com/docs/api", content, {"source": "test"})

    if i1 != i2:
        print("FAIL: Intelligence output is not deterministic")
        return False

    print("PASS: Intelligence deterministic")
    return True


def test_intelligence_schema():
    print("\n=== INTELLIGENCE SCHEMA TEST ===")

    ctx = make_context()
    result = compute_intelligence(
        ctx,
        "https://example.com/docs",
        {"text": "API docs", "code": [], "structured": {}},
        {"source": "test"},
    )

    required = ["confidence", "relevance", "novelty", "authority", "semantic_score", "composite_score"]
    missing = [k for k in required if k not in result]
    if missing:
        print(f"FAIL: Missing keys {missing}")
        return False

    print("PASS: Schema complete")
    return True


def test_intelligence_improves_ranking():
    print("\n=== INTELLIGENCE RANKING TEST ===")

    ctx = make_context(goal="python api documentation")
    analyzer = AnalyzerAgent("python api documentation")

    ctx["crawl"]["link_previews"] = {
        "https://a.com/docs/api": "Python API documentation guide with examples",
        "https://a.com/random": "gardening travel and cooking",
    }

    s_docs = analyzer.score_page("https://a.com/docs/api", ctx, base_domain="a.com")
    s_random = analyzer.score_page("https://a.com/random", ctx, base_domain="a.com")

    if s_docs <= s_random:
        print(f"FAIL: Expected docs score > random score ({s_docs} <= {s_random})")
        return False

    print(f"PASS: Ranking improved ({s_docs} > {s_random})")
    return True


def run_all_tests():
    results = []
    results.append(("DETERMINISM", test_intelligence_determinism()))
    results.append(("SCHEMA", test_intelligence_schema()))
    results.append(("RANKING", test_intelligence_improves_ranking()))

    print("\n" + "=" * 50)
    print("INTELLIGENCE ENGINE REPORT")
    print("=" * 50)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        print(f"{name}: {'PASS' if result else 'FAIL'}")

    print(f"\nTOTAL: {'PASS' if passed == total else 'FAIL'} ({passed}/{total})")
    return passed == total


if __name__ == "__main__":
    run_all_tests()
