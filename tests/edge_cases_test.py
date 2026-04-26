import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.intelligent_extraction import build_intelligence
from core.memory_context import MemoryContext


def test_edge_cases():
    ctx = MemoryContext()
    ctx["deterministic_mode"] = True
    print("\n=== EDGE CASES TEST ===")
    
    tests = [
        {"name": "empty", "content": {}},
        {"name": "only_code", "content": {"code": ["def x(): pass"]}},
        {"name": "only_text", "content": {"text": "hello world"}},
        {"name": "large", "content": {"text": "word " * 2000}},
        {"name": "no_entities", "content": {"text": "hello world python"}},
        {"name": "no_topics", "content": {"text": "this that with from"}},
        {"name": "mixed", "content": {"text": "python javascript java go rust docker kubernetes ml ai"}},
    ]
    
    for t in tests:
        try:
            result = build_intelligence(t["content"], context=ctx)
            
            assert "summary" in result, f"{t['name']}: missing summary"
            assert "topics" in result, f"{t['name']}: missing topics"
            assert "entities" in result, f"{t['name']}: missing entities"
            assert "concepts" in result, f"{t['name']}: missing concepts"
            assert "capabilities" in result, f"{t['name']}: missing capabilities"
            assert "relations" in result, f"{t['name']}: missing relations"
            assert "code_insights" in result, f"{t['name']}: missing code_insights"
            assert "content_type" in result, f"{t['name']}: missing content_type"
            assert "importance_score" in result, f"{t['name']}: missing importance_score"
            assert "confidence" in result, f"{t['name']}: missing confidence"
            
            print(f"  {t['name']}: OK (type={result.get('content_type')})")
        except Exception as e:
            print(f"  {t['name']}: FAIL - {e}")
            return False
    
    print("PASS: All edge cases handled")
    return True


if __name__ == "__main__":
    test_edge_cases()
