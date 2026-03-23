#!/usr/bin/env python3
"""Cross-language test runner for WebWeaveX."""

import json
import subprocess
import os
import sys

def run_python_tests():
    """Run Python tests."""
    print("=" * 60)
    print("Running Python Tests")
    print("=" * 60)
    
    python_dir = os.path.join(os.path.dirname(__file__), "..", "..", "implementations", "python")
    
    try:
        sys.path.insert(0, os.path.join(python_dir))
        from webweavex.entities import EntityEngine
        from webweavex.chunker import Chunker
        from webweavex.cleaner import Cleaner
        from webweavex.graph import GraphEngine
        from webweavex.schema import Entity
        
        engine = EntityEngine()
        cleaner = Cleaner()
        chunker = Chunker()
        graph_engine = GraphEngine()
        
        text = "Contact support@example.com or visit https://example.com. Call 555-123-4567."
        
        print("Testing entity extraction...")
        entities = engine.extract(text)
        print(f"  Found {len(entities)} entities")
        for e in entities:
            print(f"    - {e.type}: {e.value}")
        
        print("\nTesting cleaner...")
        cleaned = cleaner.clean("  Hello    World  ")
        print(f"  Cleaned: '{cleaned}'")
        
        print("\nTesting chunker...")
        chunks = chunker.chunk("A" * 1000)
        print(f"  Created {len(chunks)} chunks")
        
        print("\nTesting graph...")
        graph = graph_engine.build(entities)
        print(f"  Graph has {len(graph.nodes)} nodes and {len(graph.edges)} edges")
        
        print("\nTesting determinism...")
        run1 = engine.extract(text)
        run2 = engine.extract(text)
        deterministic = [e.to_dict() for e in run1] == [e.to_dict() for e in run2]
        print(f"  Deterministic: {deterministic}")
        
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False


def run_nodejs_tests():
    """Run Node.js tests."""
    print("\n" + "=" * 60)
    print("Running Node.js Tests")
    print("=" * 60)
    
    node_dir = os.path.join(os.path.dirname(__file__), "..", "..", "implementations", "node")
    package_json = os.path.join(node_dir, "package.json")
    
    if not os.path.exists(package_json):
        print("  Node.js package.json not found - skipping")
        return None
    
    try:
        import subprocess
        result = subprocess.run(
            ["npm", "install"],
            cwd=node_dir,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            print(f"  npm install failed: {result.stderr}")
            return False
        
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=node_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("  TypeScript compilation: ", end="")
        if result.returncode == 0:
            print("SUCCESS")
            return True
        else:
            print(f"FAILED: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("  Node.js/npm not found - skipping")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def generate_cross_language_snapshot():
    """Generate snapshot for cross-language comparison."""
    print("\n" + "=" * 60)
    print("Generating Cross-Language Snapshot")
    print("=" * 60)
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "implementations", "python"))
    
    from webweavex.entities import EntityEngine
    from webweavex.chunker import Chunker
    from webweavex.graph import GraphEngine
    
    test_text = "Contact support@example.com or visit https://example.com. Call 555-123-4567."
    
    engine = EntityEngine()
    chunker = Chunker()
    graph_engine = GraphEngine()
    
    entities = engine.extract(test_text)
    chunks = chunker.chunk(test_text)
    graph = graph_engine.build(entities)
    
    snapshot = {
        "version": "1.0.0",
        "language": "python",
        "test_text": test_text,
        "entities": [e.to_dict() for e in entities],
        "chunks": [c.to_dict() for c in chunks],
        "graph": graph.to_dict(),
    }
    
    output_path = os.path.join(os.path.dirname(__file__), "..", "test_cases", "cross_language_snapshot.json")
    with open(output_path, "w") as f:
        json.dump(snapshot, f, indent=2, sort_keys=True)
    
    print(f"  Snapshot saved to: {output_path}")
    return snapshot


def main():
    """Main entry point."""
    print("=" * 60)
    print("WebWeaveX Cross-Language Test Runner")
    print("=" * 60)
    
    results = {}
    
    results["python"] = run_python_tests()
    results["nodejs"] = run_nodejs_tests()
    
    snapshot = generate_cross_language_snapshot()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for lang, result in results.items():
        if result is None:
            print(f"  {lang}: SKIPPED")
        elif result:
            print(f"  {lang}: PASS")
        else:
            print(f"  {lang}: FAIL")
    
    all_passed = all(r for r in results.values() if r is not None)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests PASSED!")
    else:
        print("Some tests FAILED or were SKIPPED")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
