import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_context import MemoryContext
from core.context_schema import init_context
from core.crawler import WebCrawler
from core.self_evaluator import evaluate_performance
from core.strategy_evolution import evolve_strategy
from core.goal_engine import refine_goal
from core.meta_decision import decide_system_mode
from core.adaptive_memory import update_memory


def make_context():
    ctx = MemoryContext()
    init_context(ctx)
    return ctx


def test_metrics_change_over_time():
    print("\n=== METRICS EVOLUTION TEST ===")

    ctx = make_context()
    before = dict(ctx["meta"]["metrics"])

    crawler = WebCrawler()
    crawler.crawl("https://example.com", depth=2, goal="python api", use_multi_agent=True, context=ctx)

    after = dict(ctx["meta"]["metrics"])

    if before == after or not after:
        print("FAIL: Metrics did not evolve")
        return False

    print(f"PASS: Metrics updated {after}")
    return True


def test_weights_adapt_correctly():
    print("\n=== STRATEGY EVOLUTION TEST ===")

    ctx = make_context()
    ctx["meta"]["metrics"] = {
        "exploration_ratio": 0.2,
        "decision_quality": 0.3,
        "knowledge_growth": 2,
        "efficiency": 0.8,
    }

    before = dict(ctx["learning"]["weights"])
    evolve_strategy(ctx)
    after = dict(ctx["learning"]["weights"])

    if before == after:
        print("FAIL: Weights did not adapt")
        return False

    if round(sum(after.values()), 6) != 1.0:
        print(f"FAIL: Weights not normalized ({sum(after.values())})")
        return False

    print("PASS: Weights adapted and normalized")
    return True


def test_goal_evolves():
    print("\n=== GOAL REFINEMENT TEST ===")

    ctx = make_context()
    ctx["goal"] = "extract api docs"
    ctx["knowledge"]["entities"] = [
        {"type": "keyword", "value": "python"},
        {"type": "keyword", "value": "authentication"},
        {"type": "keyword", "value": "endpoint"},
    ]

    refine_goal(ctx)

    goal = ctx["goal"]
    if "python" not in goal or "authentication" not in goal:
        print(f"FAIL: Goal not refined correctly ({goal})")
        return False

    print(f"PASS: Goal refined ({goal})")
    return True


def test_system_mode_changes():
    print("\n=== META DECISION MODE TEST ===")

    ctx = make_context()

    ctx["meta"]["metrics"] = {"exploration_ratio": 0.2, "decision_quality": 0.7}
    m1 = decide_system_mode(ctx)

    ctx["meta"]["metrics"] = {"exploration_ratio": 0.8, "decision_quality": 0.9}
    m2 = decide_system_mode(ctx)

    if m1 != "explore" or m2 != "exploit":
        print(f"FAIL: Mode logic incorrect ({m1}, {m2})")
        return False

    print("PASS: Mode selection works")
    return True


def test_determinism_preserved():
    print("\n=== AUTONOMY DETERMINISM TEST ===")

    c1 = WebCrawler().crawl("https://example.com", depth=2, goal="python api", use_multi_agent=True, context=MemoryContext())
    c2 = WebCrawler().crawl("https://example.com", depth=2, goal="python api", use_multi_agent=True, context=MemoryContext())

    if json.dumps(c1, sort_keys=True) != json.dumps(c2, sort_keys=True):
        print("FAIL: Autonomous system is non-deterministic")
        return False

    print("PASS: Determinism preserved")
    return True


def run_all_tests():
    results = []
    results.append(("METRICS", test_metrics_change_over_time()))
    results.append(("WEIGHTS", test_weights_adapt_correctly()))
    results.append(("GOAL", test_goal_evolves()))
    results.append(("MODE", test_system_mode_changes()))
    results.append(("DETERMINISM", test_determinism_preserved()))

    print("\n" + "=" * 50)
    print("AUTONOMOUS EVOLUTION REPORT")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)
    for name, result in results:
        print(f"{name}: {'PASS' if result else 'FAIL'}")

    print(f"\nTOTAL: {'PASS' if passed == total else 'FAIL'} ({passed}/{total})")
    return passed == total


if __name__ == "__main__":
    run_all_tests()
