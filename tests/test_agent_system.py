import sys
sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.persistent_memory import clear_memory_file, load_memory
from core.memory_engine import MEMORY


def test_agent_system():
    clear_memory_file()
    MEMORY.clear()
    MEMORY.update({
        "visited_urls": [],
        "entities": [],
        "topic_counts": {},
        "knowledge_graph": {},
        "agent_decisions": []
    })
    
    crawler = WebCrawler()
    
    print("=== AGENT CRAWL TEST ===")
    results = crawler.crawl("https://example.com", depth=3, goal="find content")
    
    print(f"Pages crawled: {len(results)}")
    
    print("\n=== URLs VISITED ===")
    for r in results:
        print(f"  - {r['url']}")
    
    print("\n=== AGENT DECISIONS (from results) ===")
    all_decisions = []
    for r in results:
        if r.get('agent') and r['agent'].get('decisions'):
            decisions = r['agent']['decisions']
            all_decisions.extend(decisions)
            for d in decisions:
                print(f"  {d}")
    
    print("\n=== MEMORY STATE ===")
    print(f"Visited URLs: {len(MEMORY.get('visited_urls', []))}")
    print(f"Topics: {len(MEMORY.get('topic_counts', {}))}")
    print(f"Graph: {len(MEMORY.get('knowledge_graph', {}))}")
    
    print("\n=== VALIDATION ===")
    if len(results) > 1:
        print("PASS: Multiple pages crawled")
    else:
        print("FAIL: Not enough pages")
        return False
    
    if len(all_decisions) > 0:
        print("PASS: Agent made decisions")
    else:
        print("FAIL: No agent decisions")
        return False
    
    if len(MEMORY.get("visited_urls", [])) > 1:
        print("PASS: Memory accumulating")
    else:
        print("FAIL: Memory not working")
        return False
    
    print("\n=== QUERY TEST ===")
    from core.persistent_memory import query_memory
    q = query_memory("example")
    print(f"Query topics found: {len(q.get('topics_found', []))}")
    print(f"Query entities found: {len(q.get('entities_found', []))}")
    print(f"Query URLs found: {len(q.get('urls_found', []))}")
    
    return True


if __name__ == "__main__":
    result = test_agent_system()
    print("\nFINAL:", "PASS" if result else "FAIL")