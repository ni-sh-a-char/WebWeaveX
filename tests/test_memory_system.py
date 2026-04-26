import sys
sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.memory_engine import MEMORY, reset_memory


def run_memory_test():
    print("\n=== Initial Memory ===")
    print(MEMORY)
    
    crawler = WebCrawler()

    urls = [
        "https://example.com",
        "https://iana.org/domains/example",
        "https://example.com"
    ]

    results = []

    for url in urls:
        r = crawler.crawl(url, depth=1)
        results.append(r[0])
        print(f"\nAfter crawling {url}:")
        print("  visited_urls:", MEMORY.get("visited_urls", []))

    print("\n=== MEMORY SNAPSHOT ===")
    print(MEMORY)

    print("\n=== TOPIC COUNTS ===")
    print(MEMORY.get("topic_counts", {}))

    print("\n=== KNOWLEDGE GRAPH ===")
    print(MEMORY.get("knowledge_graph", {}))

    print("\n=== VALIDATION CHECKS ===")

    if len(MEMORY.get("visited_urls", [])) < 2:
        print("FAIL: visited_urls not accumulating")
        return False

    if not MEMORY.get("topic_counts"):
        print("FAIL: topic_counts empty")
        return False

    if not MEMORY.get("knowledge_graph"):
        print("FAIL: knowledge_graph empty")
        return False

    print("PASS: memory accumulation working")

    return True


def test_multi_depth_memory():
    reset_memory()
    crawler = WebCrawler()
    
    print("\n=== MULTI-DEPTH TEST ===")
    r = crawler.crawl("https://example.com", depth=2)
    
    print("Visited URLs count:", len(MEMORY.get("visited_urls", [])))
    print("Graph topics:", len(MEMORY.get("knowledge_graph", {})))
    print("Topic counts:", MEMORY.get("topic_counts", {}))
    
    if len(MEMORY.get("visited_urls", [])) > 1:
        print("PASS: multi-depth memory working")
        return True
    else:
        print("FAIL: multi-depth failed")
        return False


def test_determinism():
    reset_memory()
    crawler = WebCrawler()
    
    print("\n=== DETERMINISM TEST ===")
    r1 = crawler.crawl("https://example.com", depth=1)
    reset_memory()
    r2 = crawler.crawl("https://example.com", depth=1)
    
    mem1 = r1[0].get("memory", {})
    mem2 = r2[0].get("memory", {})
    
    if mem1 == mem2:
        print("PASS: determinism verified")
        return True
    else:
        print("FAIL: non-deterministic")
        return False


if __name__ == "__main__":
    results = []
    results.append(run_memory_test())
    results.append(test_multi_depth_memory())
    results.append(test_determinism())
    
    print("\nFINAL:", "PASS" if all(results) else "FAIL")