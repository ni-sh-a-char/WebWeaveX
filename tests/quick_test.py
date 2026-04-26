import sys
sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.persistent_memory import clear_memory_file
from core.config import CONFIG


def test_determinism():
    clear_memory_file()
    CONFIG["deterministic_mode"] = True
    
    crawler1 = WebCrawler()
    r1 = crawler1.crawl("https://example.com", depth=1, goal="test", use_multi_agent=False)
    r1_urls = [x['url'] for x in r1]
    
    crawler2 = WebCrawler()
    r2 = crawler2.crawl("https://example.com", depth=1, goal="test", use_multi_agent=False)
    r2_urls = [x['url'] for x in r2]
    
    print("\n=== DETERMINISM TEST ===")
    print(f"Run 1: {r1_urls}")
    print(f"Run 2: {r2_urls}")
    
    if r1_urls == r2_urls:
        print("PASS: Deterministic")
        return True
    print("FAIL")
    return False


def test_memory():
    clear_memory_file()
    CONFIG["deterministic_mode"] = True
    
    crawler = WebCrawler()
    r = crawler.crawl("https://example.com", depth=2, goal="test", use_multi_agent=False)
    
    print("\n=== MEMORY TEST ===")
    print(f"Pages: {len(r)}")
    
    if len(r) > 1:
        print("PASS")
        return True
    print("FAIL")
    return False


def test_output():
    clear_memory_file()
    CONFIG["deterministic_mode"] = True
    
    crawler = WebCrawler()
    r = crawler.crawl("https://example.com", depth=1, goal="test", use_multi_agent=False)
    
    print("\n=== CONTRACT TEST ===")
    keys = list(r[0].keys())
    print(f"Keys: {keys}")
    
    required = ["url", "canonical", "encrypted", "timestamp", "detection", "adaptive", "profile", "unified", "knowledge", "memory", "agent"]
    missing = [k for k in required if k not in r[0]]
    
    if not missing:
        print("PASS")
        return True
    print(f"FAIL: {missing}")
    return False


def run_all():
    results = [test_determinism(), test_memory(), test_output()]
    print("\n" + "="*50)
    print(f"FINAL: {'PASS' if all(results) else 'FAIL'} ({sum(results)}/3)")


if __name__ == "__main__":
    run_all()