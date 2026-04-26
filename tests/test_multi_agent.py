import sys

sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.memory_context import MemoryContext
from core.multi_agent import StrategistAgent
from core.context_schema import init_context


def create_context():
    ctx = MemoryContext()
    init_context(ctx)
    ctx["meta"]["deterministic_mode"] = True
    return ctx


def test_multi_agent_exists():
    crawler = WebCrawler()
    ctx = create_context()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=ctx)

    print("\n=== MULTI AGENT TEST ===")

    has_multi_agent = bool(results) and "multi_agent" in results[0]
    print(f"Multi-agent key present: {has_multi_agent}")

    if has_multi_agent:
        ma = results[0]["multi_agent"]
        print(f"Explorer decisions: {len(ma.get('explorer', {}).get('decisions', []))}")
        print(f"Analyzer decisions: {len(ma.get('analyzer', {}).get('decisions', []))}")
        print(f"Strategist decisions: {len(ma.get('strategist', {}).get('decisions', []))}")

        if ma.get("explorer") and ma.get("analyzer") and ma.get("strategist"):
            print("PASS: All three agents exist")
            return True

    print("FAIL: Multi-agent not properly configured")
    return False


def test_determinism_with_multi_agent():
    crawler1 = WebCrawler()
    r1 = crawler1.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=create_context())
    r1_urls = [x["url"] for x in r1]

    crawler2 = WebCrawler()
    r2 = crawler2.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=create_context())
    r2_urls = [x["url"] for x in r2]

    print("\n=== DETERMINISM TEST ===")

    if r1_urls == r2_urls:
        print("PASS: Multi-agent deterministic")
        return True
    print("FAIL: Results differ")
    return False


def test_single_agent_still_works():
    crawler = WebCrawler()
    ctx = create_context()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=False, context=ctx)

    print("\n=== SINGLE AGENT TEST ===")

    if results and "agent" in results[0] and "multi_agent" not in results[0]:
        print("PASS: Single agent mode still works")
        return True
    print("FAIL: Single agent broken")
    return False


def test_output_contract():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True, context=create_context())

    print("\n=== OUTPUT CONTRACT TEST ===")
    required = [
        "url", "canonical", "encrypted", "timestamp", "detection", "adaptive",
        "profile", "unified", "knowledge", "memory", "agent", "multi_agent",
    ]
    missing = [k for k in required if k not in results[0]] if results else required

    if not missing:
        print("PASS: Contract satisfied")
        return True
    print(f"FAIL: Missing {missing}")
    return False


def test_multi_agent_hardening():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=3, goal="test docs api", use_multi_agent=True, context=create_context())

    print("\n=== MULTI AGENT HARDENING TEST ===")

    if not results:
        print("FAIL: No results")
        return False

    ma = results[0].get("multi_agent", {})

    explorer_valid = "selected_count" in ma.get("explorer", {})
    analyzer_valid = "avg_score" in ma.get("analyzer", {})
    strategist_valid = "mode" in ma.get("strategist", {})

    visited_urls = set()
    loop_safety = True
    for item in results:
        if item["url"] in visited_urls:
            loop_safety = False
            break
        visited_urls.add(item["url"])

    crawler1 = WebCrawler()
    r1 = crawler1.crawl("https://example.com", depth=3, goal="test", use_multi_agent=True, context=create_context())

    crawler2 = WebCrawler()
    r2 = crawler2.crawl("https://example.com", depth=3, goal="test", use_multi_agent=True, context=create_context())

    determinism = bool(r1 and r2) and r1[0]["url"] == r2[0]["url"]

    print(f"Explorer valid: {'YES' if explorer_valid else 'NO'}")
    print(f"Analyzer valid: {'YES' if analyzer_valid else 'NO'}")
    print(f"Strategist valid: {'YES' if strategist_valid else 'NO'}")
    print(f"Loop safety: {'PASS' if loop_safety else 'FAIL'}")
    print(f"Determinism: {'PASS' if determinism else 'FAIL'}")

    all_pass = explorer_valid and analyzer_valid and strategist_valid and loop_safety and determinism
    print(f"\nFINAL: {'PASS' if all_pass else 'FAIL'}")

    return all_pass


def test_semantic_influence():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=2, goal="test documentation api", use_multi_agent=True, context=create_context())

    print("\n=== SEMANTIC INFLUENCE TEST ===")

    if not results:
        print("FAIL: No results")
        return False

    ma = results[0].get("multi_agent", {})
    analyzer = ma.get("analyzer", {})
    decisions = analyzer.get("decisions", [])

    semantic_present = any("score" in d for d in decisions)
    print(f"Analyzer uses semantic scoring: {semantic_present}")

    mode_valid = ma.get("strategist", {}).get("mode") in ["explore", "balanced", "exploit"]
    print(f"Strategist mode valid: {mode_valid}")

    if semantic_present and mode_valid:
        print("PASS: Semantic layer active")
        return True
    print("FAIL: Semantic not integrated")
    return False


def test_preview_intelligence():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=2, goal="documentation guide api", use_multi_agent=True, context=create_context())

    print("\n=== PREVIEW INTELLIGENCE TEST ===")

    if not results:
        print("FAIL: No results")
        return False

    ma = results[0].get("multi_agent", {})
    mode = ma.get("strategist", {}).get("mode", "unknown")
    print(f"Strategist mode: {mode}")

    memory = results[0].get("memory", {})
    top_topics = memory.get("top_topics", [])
    print(f"Top topics extracted: {len(top_topics)}")

    if mode in ["explore", "balanced", "exploit"]:
        print("PASS: Preview intelligence active")
        return True
    print("FAIL: Preview not integrated")
    return False


def test_preview_priority():
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=2, goal="documentation", use_multi_agent=True, context=create_context())

    print("\n=== PREVIEW PRIORITY TEST ===")

    if not results:
        print("FAIL: No results")
        return False

    analyzer = results[0].get("multi_agent", {}).get("analyzer", {})
    decisions = analyzer.get("decisions", [])

    has_preview_score = any("preview_score" in d for d in decisions)
    has_scoring_breakdown = any("url_score" in d and "topic_score" in d for d in decisions)

    if has_preview_score and has_scoring_breakdown:
        print("PASS: Preview priority working")
        return True
    print("FAIL: Preview priority not working")
    return False


def test_preview_ranking_effect():
    print("\n=== PREVIEW RANKING EFFECT TEST ===")

    goal = "documentation"
    strategist = StrategistAgent(goal)
    ctx = create_context()

    candidates = [
        {"url": "https://a.com/docs", "score": 5},
        {"url": "https://a.com/blog", "score": 5},
    ]

    ctx["crawl"]["link_previews"] = {
        "https://a.com/docs": "API documentation guide",
        "https://a.com/blog": "latest news updates",
    }

    result = strategist.decide_next([], list(candidates), avg_score=5, context=ctx)
    urls_ranked = [url for _, url in result]

    docs_rank = urls_ranked.index("https://a.com/docs") if "https://a.com/docs" in urls_ranked else -1
    blog_rank = urls_ranked.index("https://a.com/blog") if "https://a.com/blog" in urls_ranked else -1
    test1_pass = docs_rank < blog_rank

    ctx2 = create_context()
    ctx2["crawl"]["link_previews"] = {
        "https://a.com/docs": "random content",
        "https://a.com/blog": "documentation guide",
    }

    strategist2 = StrategistAgent(goal)
    result2 = strategist2.decide_next([], list(candidates), avg_score=5, context=ctx2)
    urls_ranked2 = [url for _, url in result2]

    docs_rank2 = urls_ranked2.index("https://a.com/docs") if "https://a.com/docs" in urls_ranked2 else -1
    blog_rank2 = urls_ranked2.index("https://a.com/blog") if "https://a.com/blog" in urls_ranked2 else -1
    test2_pass = blog_rank2 < docs_rank2

    print(f"Test 1 (docs>blog): {'PASS' if test1_pass else 'FAIL'}")
    print(f"Test 2 (blog>docs): {'PASS' if test2_pass else 'FAIL'}")

    if test1_pass and test2_pass:
        print("PASS: Preview ranking definitively affects navigation")
        return True
    print("FAIL: Preview not affecting ranking")
    return False


def run_all_tests():
    results = []
    results.append(test_multi_agent_exists())
    results.append(test_determinism_with_multi_agent())
    results.append(test_single_agent_still_works())
    results.append(test_output_contract())
    results.append(test_multi_agent_hardening())
    results.append(test_semantic_influence())
    results.append(test_preview_intelligence())
    results.append(test_preview_priority())
    results.append(test_preview_ranking_effect())

    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"FINAL: {'PASS' if all(results) else 'FAIL'} ({passed}/{total})")
    return all(results)


if __name__ == "__main__":
    run_all_tests()
