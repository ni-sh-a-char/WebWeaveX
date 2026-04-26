import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_context import MemoryContext
from core.context_schema import init_context
from core.knowledge_graph import (
    init_knowledge_graph,
    add_entity,
    add_relation,
    compute_knowledge_score,
    extract_and_add_entities,
    extract_and_add_relations
)


def create_context():
    ctx = MemoryContext()
    init_context(ctx)
    ctx["meta"]["deterministic_mode"] = True
    return ctx


def test_entity_extraction():
    ctx = create_context()
    ctx["meta"]["deterministic_mode"] = False
    print("\n=== ENTITY EXTRACTION TEST ===")
    
    text = "Visit https://example.com for Python docs. Contact dev@example.com for support. Check setup.py for configuration."
    
    entities = extract_and_add_entities(text, context=ctx)
    
    if not entities:
        print("FAIL: No entities extracted")
        return False
    
    entity_types = {e.get("type") for e in entities}
    
    if "url" not in entity_types:
        print("FAIL: URL not extracted")
        return False
    
    print(f"PASS: Entity extraction working ({len(entities)} entities)")
    return True


def test_entity_addition():
    ctx = create_context()
    ctx["meta"]["deterministic_mode"] = False
    print("\n=== ENTITY ADDITION TEST ===")
    
    entity = {"type": "url", "value": "https://test.com"}
    add_entity(entity, context=ctx)
    
    entities = ctx["knowledge"]["entities"]
    
    if not entities:
        print("FAIL: Entity not added")
        return False
    
    if entities[0].get("value") != "https://test.com":
        print("FAIL: Entity value mismatch")
        return False
    
    print("PASS: Entity addition working")
    return True


def test_relation_creation():
    ctx = create_context()
    ctx["meta"]["deterministic_mode"] = False
    print("\n=== RELATION CREATION TEST ===")
    
    add_relation("python", "api", "related", context=ctx)
    add_relation("python", "docs", "related", context=ctx)
    
    graph = ctx["knowledge"]["graph"]
    
    if "python" not in graph:
        print("FAIL: Relation not created")
        return False
    
    if len(graph["python"]) != 2:
        print("FAIL: Wrong number of relations")
        return False
    
    print("PASS: Relation creation working")
    return True


def test_knowledge_scoring():
    ctx = create_context()
    ctx["meta"]["deterministic_mode"] = False
    print("\n=== KNOWLEDGE SCORING TEST ===")
    
    entities = [
        {"type": "url", "value": "https://a.com"},
        {"type": "keyword", "value": "python"},
        {"type": "email", "value": "test@test.com"}
    ]
    
    knowledge_graph = {
        "python": [{"target": "api", "type": "related"}],
        "api": [{"target": "rest", "type": "related"}]
    }
    
    topic_graph = {
        "python": ["https://a.com"],
        "api": ["https://a.com"],
        "docs": ["https://a.com"]
    }
    
    score = compute_knowledge_score(
        entities, 
        knowledge_graph, 
        url="https://a.com/api/docs",
        topic_counts={"python": 2, "api": 1},
        topic_graph=topic_graph,
        context=ctx
    )
    
    if score <= 0:
        print(f"FAIL: Score should be positive ({score})")
        return False
    
    empty_score = compute_knowledge_score([], {}, url="", topic_counts=None, topic_graph=None, context=ctx)
    if empty_score != 0:
        print("FAIL: Empty URL should return 0")
        return False
    
    print(f"PASS: Knowledge scoring working ({score})")
    return True


def test_deterministic_safety():
    ctx = create_context()
    ctx["meta"]["deterministic_mode"] = True
    print("\n=== DETERMINISTIC SAFETY TEST ===")
    
    text = "https://example.com is a site with Python and APIs"
    extract_and_add_entities(text, context=ctx)
    
    entities = ctx["knowledge"]["entities"]
    
    if len(entities) > 0:
        print("FAIL: Entities added in deterministic mode")
        return False
    
    print("PASS: Deterministic mode safe")
    return True


def run_all_tests():
    results = []
    
    results.append(("ENTITY EXTRACTION", test_entity_extraction()))
    results.append(("ENTITY ADDITION", test_entity_addition()))
    results.append(("RELATION CREATION", test_relation_creation()))
    results.append(("KNOWLEDGE SCORING", test_knowledge_scoring()))
    results.append(("DETERMINISTIC SAFETY", test_deterministic_safety()))
    
    print("\n" + "=" * 50)
    print("KNOWLEDGE GRAPH REPORT")
    print("=" * 50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
    
    print(f"\nTOTAL: {'PASS' if passed == total else 'FAIL'} ({passed}/{total})")
    return passed == total


if __name__ == "__main__":
    run_all_tests()
