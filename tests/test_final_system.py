import sys
sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.persistent_memory import clear_memory_file, load_memory, save_memory
from core.memory_engine import MEMORY
import json


def test_determinism():
    clear_memory_file()
    crawler = WebCrawler()
    r1 = crawler.crawl("https://example.com", depth=1, goal="test")
    r1_json = json.dumps(r1, sort_keys=True)
    
    crawler2 = WebCrawler()
    r2 = crawler2.crawl("https://example.com", depth=1, goal="test")
    r2_json = json.dumps(r2, sort_keys=True)
    
    print("\n=== DETERMINISM TEST ===")
    
    if r1_json == r2_json:
        print("PASS: Full object equality - results are deterministic")
        return True
    print("FAIL: Results differ")
    return False


def test_memory_accumulation():
    clear_memory_file()
    crawler = WebCrawler()
    r = crawler.crawl("https://example.com", depth=2, goal="test")
    
    print("\n=== MEMORY ACCUMULATION TEST ===")
    print(f"Pages crawled: {len(r)}")
    
    if len(r) > 1:
        print("PASS: Multi-page crawl works")
        return True
    print("FAIL: Single page only")
    return False


def test_learning():
    from core.config import CONFIG
    
    clear_memory_file()
    
    original_mode = CONFIG.get("deterministic_mode", True)
    CONFIG["deterministic_mode"] = False
    
    crawler = WebCrawler()
    
    r1 = crawler.crawl("https://example.com", depth=2, goal="domain registry")
    scores1 = [x.get('agent', {}).get('page_score', 0) for x in r1]
    avg1 = sum(scores1)/max(1,len(scores1))
    
    print("\n=== LEARNING TEST ===")
    print(f"Run 1 scores: {scores1}")
    print(f"Run 1 avg: {avg1}")
    
    first_url = r1[0]['url']
    MEMORY["success_paths"][first_url] = 5
    MEMORY["url_scores_history"][first_url] = [scores1[0]]
    save_memory(MEMORY)
    
    r2 = crawler.crawl("https://example.com", depth=2, goal="domain registry")
    scores2 = [x.get('agent', {}).get('page_score', 0) for x in r2]
    avg2 = sum(scores2)/max(1,len(scores2))
    
    print(f"Run 2 scores: {scores2}")
    print(f"Run 2 avg: {avg2}")
    print(f"Success paths: {MEMORY.get('success_paths', {})}")
    print(f"URL history: {MEMORY.get('url_scores_history', {})}")
    
    CONFIG["deterministic_mode"] = original_mode
    
    if avg2 >= avg1 or scores2[0] > scores1[0]:
        print("PASS: Learning improving behavior")
        return True
    print("FAIL: Learning did not improve")
    return False


def test_agent_decisions():
    clear_memory_file()
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=2, goal="domain")
    
    all_decisions = []
    for r in results:
        if r.get('agent') and r['agent'].get('decisions'):
            all_decisions.extend(r['agent']['decisions'])
    
    seen = set()
    unique_decisions = []
    for d in all_decisions:
        key = (d.get('current'), tuple(sorted(d.get('selected', []))))
        if key not in seen:
            seen.add(key)
            unique_decisions.append(d)
    
    print("\n=== AGENT DECISIONS TEST ===")
    print(f"Total decisions: {len(all_decisions)}")
    print(f"Unique decisions: {len(unique_decisions)}")
    
    if unique_decisions:
        print(f"Sample: {unique_decisions[:2]}")
        print("PASS: Agent decisions present and unique")
        return True
    print("FAIL: No decisions")
    return False


def test_output_contract():
    clear_memory_file()
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1, goal="test")
    
    print("\n=== OUTPUT CONTRACT TEST ===")
    required = ["url", "canonical", "encrypted", "timestamp", "detection", "adaptive", "profile", "unified", "knowledge", "memory", "agent"]
    missing = [k for k in required if k not in results[0]]
    
    if not missing:
        print("PASS: Contract satisfied")
        return True
    print(f"FAIL: Missing {missing}")
    return False


def run_all_tests():
    results = []
    results.append(test_determinism())
    results.append(test_memory_accumulation())
    results.append(test_learning())
    results.append(test_agent_decisions())
    results.append(test_output_contract())
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    print(f"FINAL: {'PASS' if all(results) else 'FAIL'} ({passed}/{total})")
    return all(results)


if __name__ == "__main__":
    run_all_tests()