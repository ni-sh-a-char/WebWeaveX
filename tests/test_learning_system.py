import sys
sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.persistent_memory import clear_memory_file
from core.memory_engine import MEMORY
from core.learning_engine import get_learning_stats, get_adaptive_weights
from core.persistent_learning import load_learning_state


def test_learning_disabled_in_deterministic():
    clear_memory_file()
    print("\n=== LEARNING DISABLED TEST ===")
    
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    weights = get_adaptive_weights()
    initial_weights = tuple(weights.values())
    
    crawler2 = WebCrawler()
    results2 = crawler2.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    weights2 = get_adaptive_weights()
    final_weights = tuple(weights2.values())
    
    if initial_weights == final_weights:
        print("PASS: Weights stable in deterministic mode")
        return True
    print("FAIL: Weights changed in deterministic mode")
    return False


def test_weights_stability():
    clear_memory_file()
    print("\n=== WEIGHTS STABILITY TEST ===")
    
    weights = get_adaptive_weights()
    
    total = sum(weights.values())
    all_bounded = all(0.05 <= w <= 0.6 for w in weights.values())
    
    if all_bounded and abs(total - 1.0) < 0.01:
        print(f"PASS: Weights stable (total={round(total, 3)})")
        return True
    print(f"FAIL: Weights unstable (total={round(total, 3)}, bounded={all_bounded})")
    return False


def test_learning_stats():
    clear_memory_file()
    print("\n=== LEARNING STATS TEST ===")
    
    stats = get_learning_stats()
    
    has_keys = all(k in stats for k in ["success_paths", "failed_paths", "adaptive_weights", "confidence"])
    
    if has_keys:
        print(f"PASS: Stats complete ({stats})")
        return True
    print("FAIL: Stats incomplete")
    return False


def test_learning_version():
    clear_memory_file()
    print("\n=== LEARNING VERSION TEST ===")
    
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    version = MEMORY.get("learning_version")
    
    if version == "v1_phase18":
        print(f"PASS: Version correct ({version})")
        return True
    print(f"FAIL: Version wrong ({version})")
    return False


def test_path_history_tracking():
    clear_memory_file()
    print("\n=== PATH HISTORY TEST ===")
    
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=2, goal="test", use_multi_agent=True)
    
    history = MEMORY.get("path_history", [])
    
    if len(history) >= 1:
        print(f"PASS: Path history tracked ({len(history)} urls)")
        return True
    print("FAIL: Path history empty")
    return False


def test_learning_output():
    clear_memory_file()
    print("\n=== LEARNING OUTPUT TEST ===")
    
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=True)
    
    learning = results[0].get("learning")
    
    if learning is None:
        print("PASS: Learning None in deterministic mode")
        return True
    print("FAIL: Learning should be None in deterministic mode")
    return False


def run_all_tests():
    results = []
    results.append(test_learning_disabled_in_deterministic())
    results.append(test_weights_stability())
    results.append(test_learning_stats())
    results.append(test_learning_version())
    results.append(test_path_history_tracking())
    results.append(test_learning_output())
    
    print("\n" + "=" * 60)
    print("=== LEARNING SYSTEM VALIDATION ===")
    passed = sum(results)
    total = len(results)
    print(f"Total: {'PASS' if all(results) else 'FAIL'} ({passed}/{total})")
    
    return all(results)


if __name__ == "__main__":
    run_all_tests()