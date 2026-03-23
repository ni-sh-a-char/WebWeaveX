"""Test runner for WebWeaveX cross-language verification."""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "implementations", "python"))

from webweavex import WebWeaveX
from webweavex.entities import EntityEngine
from webweavex.chunker import Chunker
from webweavex.cleaner import Cleaner
from webweavex.graph import GraphEngine


def run_entity_tests():
    """Run entity extraction tests."""
    print("Running entity extraction tests...")
    
    test_cases = [
        {
            "name": "email_extraction",
            "input": "Contact support@example.com or sales@example.org",
            "expected_entities": 2,
            "types": ["email"]
        },
        {
            "name": "url_extraction",
            "input": "Visit https://example.com and http://test.org",
            "expected_entities": 2,
            "types": ["url"]
        },
        {
            "name": "mixed_entities",
            "input": "Email test@test.com at https://example.com or call 123-456-7890",
            "expected_entities": 3,
            "types": ["email", "url", "number"]
        },
        {
            "name": "phone_extraction",
            "input": "Call us at +1-555-123-4567",
            "expected_entities": 1,
            "types": ["phone"]
        }
    ]
    
    engine = EntityEngine()
    results = []
    
    for case in test_cases:
        entities = engine.extract(case["input"])
        result = {
            "test": case["name"],
            "input": case["input"],
            "entities": [e.to_dict() for e in entities],
            "count": len(entities),
            "passed": len(entities) >= case["expected_entities"]
        }
        results.append(result)
        print(f"  {case['name']}: {'PASS' if result['passed'] else 'FAIL'}")
    
    return results


def run_cleaner_tests():
    """Run cleaner tests."""
    print("Running cleaner tests...")
    
    test_cases = [
        {
            "name": "whitespace_normalization",
            "input": "Hello    World\n\n  Test  ",
            "check": lambda r: "  " not in r and "\n\n" not in r
        },
        {
            "name": "strip",
            "input": "   Hello   ",
            "check": lambda r: r.strip() == r
        }
    ]
    
    cleaner = Cleaner()
    results = []
    
    for case in test_cases:
        result = cleaner.clean(case["input"])
        passed = case["check"](result)
        results.append({
            "test": case["name"],
            "input": case["input"],
            "output": result,
            "passed": passed
        })
        print(f"  {case['name']}: {'PASS' if passed else 'FAIL'}")
    
    return results


def run_chunker_tests():
    """Run chunker tests."""
    print("Running chunker tests...")
    
    test_cases = [
        {
            "name": "basic_chunking",
            "input": "A" * 1000,
            "check": lambda c: len(c) > 1
        },
        {
            "name": "metadata",
            "input": "Hello World Test",
            "check": lambda c: c[0].index == 0 and c[0].start == 0
        }
    ]
    
    chunker = Chunker()
    results = []
    
    for case in test_cases:
        chunks = chunker.chunk(case["input"])
        passed = case["check"](chunks)
        results.append({
            "test": case["name"],
            "input": case["input"][:50] + "...",
            "chunk_count": len(chunks),
            "passed": passed
        })
        print(f"  {case['name']}: {'PASS' if passed else 'FAIL'}")
    
    return results


def run_graph_tests():
    """Run graph tests."""
    print("Running graph tests...")
    
    from webweavex.schema import Entity
    
    test_cases = [
        {
            "name": "empty_graph",
            "entities": [],
            "check": lambda r: len(r.nodes) == 0 and len(r.edges) == 0
        },
        {
            "name": "basic_graph",
            "entities": [
                Entity(type="email", value="test@test.com"),
                Entity(type="url", value="https://example.com")
            ],
            "check": lambda r: len(r.nodes) == 2
        }
    ]
    
    engine = GraphEngine()
    results = []
    
    for case in test_cases:
        graph = engine.build(case["entities"])
        passed = case["check"](graph)
        results.append({
            "test": case["name"],
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "passed": passed
        })
        print(f"  {case['name']}: {'PASS' if passed else 'FAIL'}")
    
    return results


def run_determinism_tests():
    """Run determinism tests."""
    print("Running determinism tests...")
    
    from webweavex.schema import Entity
    
    engine = EntityEngine()
    chunker = Chunker()
    graph_engine = GraphEngine()
    
    test_text = "test@test.com a@test.com b@test.com c@test.com"
    
    run1 = engine.extract(test_text)
    run2 = engine.extract(test_text)
    entities_match = [e.to_dict() for e in run1] == [e.to_dict() for e in run2]
    
    chunks1 = chunker.chunk("A" * 1000)
    chunks2 = chunker.chunk("A" * 1000)
    chunks_match = [c.to_dict() for c in chunks1] == [c.to_dict() for c in chunks2]
    
    entities = [
        Entity(type="email", value="c@test.com"),
        Entity(type="email", value="a@test.com"),
        Entity(type="email", value="b@test.com"),
    ]
    graph1 = graph_engine.build(entities)
    graph2 = graph_engine.build(entities)
    graph_match = graph1.to_json() == graph2.to_json()
    
    print(f"  entity_determinism: {'PASS' if entities_match else 'FAIL'}")
    print(f"  chunk_determinism: {'PASS' if chunks_match else 'FAIL'}")
    print(f"  graph_determinism: {'PASS' if graph_match else 'FAIL'}")
    
    return [
        {"test": "entity_determinism", "passed": entities_match},
        {"test": "chunk_determinism", "passed": chunks_match},
        {"test": "graph_determinism", "passed": graph_match}
    ]


def generate_snapshot():
    """Generate test snapshot for cross-language verification."""
    print("Generating test snapshot...")
    
    from webweavex.schema import Entity
    
    engine = EntityEngine()
    chunker = Chunker()
    graph_engine = GraphEngine()
    
    test_text = "Contact support@example.com or visit https://example.com. Call 555-123-4567."
    
    entities = engine.extract(test_text)
    chunks = chunker.chunk(test_text)
    graph = graph_engine.build(entities)
    
    snapshot = {
        "version": "1.0",
        "test_text": test_text,
        "entities": [e.to_dict() for e in entities],
        "chunks": [c.to_dict() for c in chunks],
        "graph": graph.to_dict()
    }
    
    output_path = os.path.join(os.path.dirname(__file__), "..", "test_cases", "python_snapshot.json")
    with open(output_path, "w") as f:
        json.dump(snapshot, f, indent=2, sort_keys=True)
    
    print(f"  Snapshot saved to {output_path}")
    return snapshot


def main():
    """Run all tests."""
    print("=" * 50)
    print("WebWeaveX Test Runner")
    print("=" * 50)
    
    all_results = {
        "entity_tests": run_entity_tests(),
        "cleaner_tests": run_cleaner_tests(),
        "chunker_tests": run_chunker_tests(),
        "graph_tests": run_graph_tests(),
        "determinism_tests": run_determinism_tests()
    }
    
    all_passed = True
    for category, results in all_results.items():
        for result in results:
            if not result.get("passed", True):
                all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("All tests PASSED")
    else:
        print("Some tests FAILED")
    print("=" * 50)
    
    generate_snapshot()
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
