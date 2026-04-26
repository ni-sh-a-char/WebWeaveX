import sys
sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.persistent_memory import clear_memory_file
from core.memory_engine import MEMORY
from core.meta_learning import (
    update_strategy_performance, get_strategy_confidence, get_all_strategy_confidences,
    get_best_strategy, add_self_reflection, get_meta_learning_stats
)


def test_strategy_tracking_exists():
    clear_memory_file()
    print("\n=== STRATEGY TRACKING TEST ===")
    
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    perf = MEMORY.get("strategy_performance")
    
    if perf and "explore" in perf and "balanced" in perf and "exploit" in perf:
        print(f"PASS: Strategy tracking exists ({perf})")
        return True
    print("FAIL: Strategy tracking missing")
    return False


def test_confidence_valid():
    clear_memory_file()
    print("\n=== CONFIDENCE VALID TEST ===")
    
    conf = get_strategy_confidence("explore")
    
    if 0 <= conf <= 1:
        print(f"PASS: Confidence valid ({conf})")
        return True
    print(f"FAIL: Confidence invalid ({conf})")
    return False


def test_deterministic_mode_safe():
    clear_memory_file()
    print("\n=== DETERMINISTIC MODE SAFE TEST ===")
    
    crawler1 = WebCrawler()
    results1 = crawler1.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    perf1 = MEMORY.get("strategy_performance")
    
    crawler2 = WebCrawler()
    results2 = crawler2.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    perf2 = MEMORY.get("strategy_performance")
    
    if perf1 == perf2:
        print("PASS: Deterministic mode safe (no updates)")
        return True
    print("FAIL: Updates occurred in deterministic mode")
    return False


def test_all_confidences():
    clear_memory_file()
    print("\n=== ALL CONFIDENCES TEST ===")
    
    confidences = get_all_strategy_confidences()
    
    if all(0 <= confidences[k] <= 1 for k in confidences):
        print(f"PASS: All confidences valid ({confidences})")
        return True
    print(f"FAIL: Invalid confidences ({confidences})")
    return False


def test_meta_output():
    clear_memory_file()
    print("\n=== META OUTPUT TEST ===")
    
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    meta = results[0].get("meta")
    
    if meta is None:
        print("PASS: Meta None in deterministic mode")
        return True
    print("FAIL: Meta should be None in deterministic mode")
    return False


def test_best_strategy():
    clear_memory_file()
    print("\n=== BEST STRATEGY TEST ===")
    
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    stats = get_meta_learning_stats()
    best = stats.get("best_strategy")
    
    if best in ["explore", "balanced", "exploit"]:
        print(f"PASS: Best strategy valid ({best})")
        return True
    print(f"FAIL: Invalid best strategy ({best})")
    return False


def test_self_reflection():
    clear_memory_file()
    print("\n=== SELF REFLECTION TEST ===")
    
    add_self_reflection("Test reflection 1")
    add_self_reflection("Test reflection 2")
    
    reflections = MEMORY.get("self_reflection", [])
    
    if len(reflections) >= 2:
        print(f"PASS: Self reflection working ({len(reflections)} reflections)")
        return True
    print("FAIL: Self reflection not working")
    return False


def run_all_tests():
    results = []
    results.append(test_strategy_tracking_exists())
    results.append(test_confidence_valid())
    results.append(test_deterministic_mode_safe())
    results.append(test_all_confidences())
    results.append(test_meta_output())
    results.append(test_best_strategy())
    results.append(test_self_reflection())
    
    print("\n" + "=" * 60)
    print("=== META LEARNING VALIDATION ===")
    passed = sum(results)
    total = len(results)
    print(f"Total: {'PASS' if all(results) else 'FAIL'} ({passed}/{total})")
    
    return all(results)


if __name__ == "__main__":
    run_all_tests()