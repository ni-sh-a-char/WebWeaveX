import sys

sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.memory_context import MemoryContext
from core.multi_agent import StrategistAgent
from core.context_schema import init_context
import json


REQUIRED_CONTEXT_KEYS = [
    "crawl",
    "knowledge",
    "learning",
    "agent",
    "meta",
]


def create_context():
    ctx = MemoryContext()
    init_context(ctx)
    ctx["meta"]["deterministic_mode"] = True
    return ctx


def test_determinism():
    crawler1 = WebCrawler()
    ctx1 = create_context()
    r1 = crawler1.crawl("https://example.com", depth=2, goal="test", use_multi_agent=True, context=ctx1)
    r1_json = json.dumps(r1, sort_keys=True)

    crawler2 = WebCrawler()
    ctx2 = create_context()
    r2 = crawler2.crawl("https://example.com", depth=2, goal="test", use_multi_agent=True, context=ctx2)
    r2_json = json.dumps(r2, sort_keys=True)

    print("\n=== DETERMINISM TEST ===")
    if r1_json == r2_json:
        print("PASS: Deterministic across runs")
        return True
    print("FAIL: Results differ")
    print(f"Run 1: {r1_json[:100]}...")
    print(f"Run 2: {r2_json[:100]}...")
    return False


def test_memory_integrity():
    crawler = WebCrawler()
    ctx = create_context()
    crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=ctx)

    print("\n=== CONTEXT INTEGRITY TEST ===")
    missing = [k for k in REQUIRED_CONTEXT_KEYS if k not in ctx]
    if not missing:
        print(f"PASS: All {len(REQUIRED_CONTEXT_KEYS)} keys present")
        return True
    print(f"FAIL: Missing keys: {missing}")
    return False


def test_cache_consistency():
    crawler = WebCrawler()
    r1 = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=create_context())
    score1 = r1[0].get("multi_agent", {}).get("analyzer", {}).get("decisions", [{}])[0].get("score")

    crawler2 = WebCrawler()
    r2 = crawler2.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=create_context())
    score2 = r2[0].get("multi_agent", {}).get("analyzer", {}).get("decisions", [{}])[0].get("score")

    print("\n=== CACHE CONSISTENCY TEST ===")
    if score1 == score2 and score1 is not None:
        print(f"PASS: Scores match ({score1})")
        return True
    print(f"FAIL: Scores differ: {score1} vs {score2}")
    return False


def test_preview_causality():
    print("\n=== PREVIEW CAUSALITY TEST ===")

    goal = "documentation"
    strategist = StrategistAgent(goal)

    candidates = [
        {"url": "https://a.com/docs", "score": 5},
        {"url": "https://a.com/blog", "score": 5},
    ]

    ctx1 = create_context()
    ctx1["crawl"]["link_previews"] = {
        "https://a.com/docs": "API documentation guide",
        "https://a.com/blog": "latest news updates",
    }
    result1 = strategist.decide_next([], list(candidates), avg_score=5, context=ctx1)
    urls1 = [url for _, url in result1]

    strategist2 = StrategistAgent(goal)
    ctx2 = create_context()
    ctx2["crawl"]["link_previews"] = {
        "https://a.com/docs": "random content",
        "https://a.com/blog": "documentation guide",
    }
    result2 = strategist2.decide_next([], list(candidates), avg_score=5, context=ctx2)
    urls2 = [url for _, url in result2]

    docs_first = urls1 and urls1[0].endswith("docs")
    blog_first = urls2 and urls2[0].endswith("blog")

    if docs_first and blog_first:
        print("PASS: Ranking flips with preview")
        return True
    print(f"FAIL: docs_first={docs_first}, blog_first={blog_first}")
    return False


def test_no_loop():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=3, goal="test", use_multi_agent=True, context=create_context())

    print("\n=== LOOP SAFETY TEST ===")
    urls = [r["url"] for r in results]
    unique = set(urls)

    if len(urls) == len(unique):
        print(f"PASS: No loops ({len(urls)} pages)")
        return True
    print(f"FAIL: Loop detected: {urls}")
    return False


def test_score_range():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=2, goal="test", use_multi_agent=True, context=create_context())

    print("\n=== SCORE RANGE TEST ===")
    decisions = results[0].get("multi_agent", {}).get("analyzer", {}).get("decisions", [])
    scores = [d.get("score", 0) for d in decisions if "score" in d]

    out_of_range = [s for s in scores if s < -5 or s > 20]
    if not out_of_range:
        print(f"PASS: Scores in range")
        return True
    print(f"FAIL: Out of range: {out_of_range}")
    return False


def test_multi_agent_structure():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=create_context())

    print("\n=== MULTI-AGENT STRUCTURE TEST ===")
    ma = results[0].get("multi_agent", {})

    has_all = all(k in ma for k in ["explorer", "analyzer", "strategist"])
    if has_all:
        print("PASS: All agents present")
        return True
    missing = [k for k in ["explorer", "analyzer", "strategist"] if k not in ma]
    print(f"FAIL: Missing: {missing}")
    return False


def test_decision_trace():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=create_context())

    print("\n=== DECISION TRACE TEST ===")
    decisions = results[0].get("multi_agent", {}).get("analyzer", {}).get("decisions", [])

    required = ["url", "score"]
    optional = ["url_score", "topic_score", "preview_score"]

    complete = 0
    for decision in decisions:
        has_req = all(k in decision for k in required)
        has_opt = any(k in decision for k in optional)
        if has_req and has_opt:
            complete += 1

    if complete > 0:
        print("PASS: Decision trace complete")
        return True
    print("FAIL: Missing trace fields")
    return False


def test_preview_in_explore_mode():
    print("\n=== PREVIEW IN EXPLORE MODE TEST ===")

    ctx = create_context()
    ctx["crawl"]["link_previews"] = {
        "https://a.com/docs": "documentation guide important",
        "https://a.com/other": "random content",
    }

    goal = "documentation"
    strategist = StrategistAgent(goal)
    candidates = [
        {"url": "https://a.com/docs", "score": 1},
        {"url": "https://a.com/other", "score": 1},
    ]

    result = strategist.decide_next([], list(candidates), avg_score=1.5, context=ctx)
    urls = [url for _, url in result]

    docs_first = urls and urls[0].endswith("docs")

    if docs_first:
        print("PASS: Explore mode deterministic ordering")
        return True
    print("FAIL: Explore mode ordering unexpected")
    return False


def test_immutability():
    import copy

    crawler = WebCrawler()
    ctx1 = create_context()
    crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=ctx1)
    snapshot1 = copy.deepcopy(ctx1.get_all())

    crawler2 = WebCrawler()
    ctx2 = create_context()
    crawler2.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=ctx2)
    snapshot2 = copy.deepcopy(ctx2.get_all())

    print("\n=== IMMUTABILITY TEST ===")
    if snapshot1 == snapshot2:
        print("PASS: Context deterministic and consistent")
        return True
    print("FAIL: Context mutated inconsistently")
    return False


def test_avg_score_correctness():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=2, goal="test", use_multi_agent=True, context=create_context())

    print("\n=== AVG SCORE TEST ===")

    ma = results[0].get("multi_agent", {})
    avg = ma.get("analyzer", {}).get("avg_score", None)

    if avg is not None:
        print(f"PASS: avg_score exists ({avg})")
        return True

    print("FAIL: avg_score missing")
    return False


def test_result_preservation():
    crawler = WebCrawler()

    results = crawler.crawl(
        "https://example.com",
        depth=3,
        goal="example",
        use_multi_agent=True,
        context=create_context(),
    )

    print("\n=== FINAL RESULT PRESERVATION TEST ===")

    if len(results) >= 1:
        print(f"PASS: Results preserved ({len(results)} pages)")
        return True

    print("FAIL: No results returned")
    return False


def run_all_tests():
    results = []
    results.append(test_determinism())
    results.append(test_memory_integrity())
    results.append(test_cache_consistency())
    results.append(test_preview_causality())
    results.append(test_no_loop())
    results.append(test_score_range())
    results.append(test_multi_agent_structure())
    results.append(test_decision_trace())
    results.append(test_preview_in_explore_mode())
    results.append(test_immutability())
    results.append(test_avg_score_correctness())
    results.append(test_result_preservation())

    print("\n" + "=" * 60)
    print("=== SYSTEM VALIDATION REPORT ===")
    passed = sum(results)
    total = len(results)
    print(f"TOTAL: {'PASS' if all(results) else 'FAIL'} ({passed}/{total})")
    return all(results)


if __name__ == "__main__":
    run_all_tests()
