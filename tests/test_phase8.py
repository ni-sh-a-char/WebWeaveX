import sys
sys.path.insert(0, '.')

from core.crawler import WebCrawler
from core.persistent_memory import clear_memory_file, load_memory
from core.memory_engine import MEMORY, reset_memory


def test_phase8():
    reset_memory()
    clear_memory_file()
    
    MEMORY["page_scores"] = {}
    
    crawler = WebCrawler()
    
    print("=== AUTONOMOUS INTELLIGENCE TEST ===")
    results = crawler.crawl("https://example.com", depth=3, goal="domain registry")
    
    print(f"\n=== PAGE SCORES ===")
    print(MEMORY.get("page_scores", {}))
    
    total_score = sum(MEMORY.get("page_scores", {}).values())
    print(f"\n=== TOTAL SCORE ===")
    print(total_score)
    
    print(f"\n=== SELECTED PATH ===")
    for r in results:
        score = r.get('agent', {}).get('page_score', 0) if r.get('agent') else 0
        print(f"  {r['url']} (score: {score})")
    
    print(f"\n=== STOP REASON ===")
    print(f"Pages crawled: {len(results)}")
    print(f"Agent decisions: {len(results[0].get('agent', {}).get('decisions', [])) if results else 0}")
    
    print(f"\n=== VALIDATION ===")
    
    if MEMORY.get("page_scores"):
        print("PASS: page_scores populated")
    else:
        print("FAIL: page_scores empty")
        return False
    
    if total_score > 0:
        print("PASS: total_score increasing")
    else:
        print("FAIL: no score")
        return False
    
    if len(results) > 1:
        print("PASS: multiple pages visited")
    else:
        print("FAIL: single page only")
        return False
    
    print("\n=== ALL PASSED ===")
    return True


if __name__ == "__main__":
    result = test_phase8()
    print(f"\nFINAL: {'PASS' if result else 'FAIL'}")