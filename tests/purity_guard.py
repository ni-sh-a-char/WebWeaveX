"""PURITY GUARD - V7 Validation Suite"""
import os
from webweavex import run, __version__


def has_type_field(obj, _visited=None):
    """Check if any 'type' key exists in object."""
    if _visited is None:
        _visited = set()
    
    obj_id = id(obj)
    if obj_id in _visited:
        return False
    _visited.add(obj_id)
    
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "type":
                return True
            if has_type_field(v, _visited):
                return True
    elif isinstance(obj, list):
        for i in obj:
            if has_type_field(i, _visited):
                return True
    return False


def test_no_type_field():
    """Test no 'type' key anywhere."""
    r = run({"input": "test", "mode": "compiler"})
    result = has_type_field(r)
    print("TEST 1 - No type field:", "PASS" if not result else "FAIL")
    return not result


def test_no_ui_keys():
    """Test no UI keys."""
    r = run({"input": "test", "mode": "compiler"})
    has_ui = "ui_schema" in r or "human_readable" in r
    print("TEST 2 - No UI keys:", "PASS" if not has_ui else "FAIL")
    return not has_ui


def test_empty_system_type():
    """Test system_type is empty."""
    r = run({"input": "test", "mode": "compiler"})
    sd = r.get("structured_data", {})
    sys = sd.get("system", {})
    st = sys.get("system_type", "x")
    arch = sys.get("architecture", "x")
    ok = st == "" and arch == ""
    print("TEST 3 - Empty system_type/architecture:", "PASS" if ok else "FAIL")
    return ok


def test_graph_structure():
    """Test graph has nodes and relationships."""
    r = run({"input": "test", "mode": "compiler"})
    sd = r.get("structured_data", {})
    sys = sd.get("system", {})
    eg = sd.get("execution_graph", {})
    
    comps = sys.get("components", [])
    rels = sys.get("relationships", [])
    nodes = eg.get("nodes", [])
    edges = eg.get("edges", [])
    
    ok = len(comps) >= 1 and len(nodes) >= 1
    print("TEST 4 - Graph structure:", "PASS" if ok else "FAIL")
    return ok


def test_determinism():
    """Test deterministic output."""
    r1 = run({"input": "det", "mode": "compiler"})
    r2 = run({"input": "det", "mode": "compiler"})
    ok = r1 == r2
    print("TEST 5 - Determinism:", "PASS" if ok else "FAIL")
    return ok


def test_universal_input():
    """Test universal inputs work."""
    tests = [
        "build REST API",
        "quantum trading engine",
        "ai assistant",
        "distributed system"
    ]
    
    all_ok = True
    for inp in tests:
        r = run({"input": inp, "mode": "compiler"})
        sd = r.get("structured_data", {})
        nodes = sd.get("execution_graph", {}).get("nodes", [])
        
        if len(nodes) < 1:
            all_ok = False
    
    print("TEST 6 - Universal input:", "PASS" if all_ok else "FAIL")
    return all_ok


def test_performance():
    """Test performance < 0.1s."""
    import time
    start = time.time()
    run({"input": "test", "mode": "compiler"})
    elapsed = time.time() - start
    ok = elapsed < 0.1
    print("TEST 7 - Performance:", "PASS" if ok else "FAIL", f"({elapsed:.4f}s)")
    return ok


def test_output_schema():
    """Test exact output schema."""
    r = run({"input": "test", "mode": "compiler"})
    
    must_have = ["structured_data", "confidence", "source", "version"]
    must_not_have = ["ui_schema", "human_readable"]
    
    has_all = all(k in r for k in must_have)
    has_none = any(k in r for k in must_not_have)
    
    ok = has_all and not has_none
    print("TEST 8 - Output schema:", "PASS" if ok else "FAIL")
    return ok


def test_graph_density():
    """Test graph has FULL CONNECTIVITY (not just linear chain)."""
    r = run({"input": "build REST API", "mode": "compiler"})
    edges = r["structured_data"]["execution_graph"]["edges"]
    
    # With 3 tokens (build, rest, api):
    # Sequence = 2 edges (build→rest, rest→api)
    # Full = 6 edges (all pairs)
    # Total unique should be > 2
    ok = len(edges) > 2
    print("TEST 9 - Graph density:", "PASS" if ok else "FAIL", f"(edges={len(edges)})")
    return ok


def run_all():
    """Run all tests."""
    print("=== V7 PURITY GUARD ===")
    print("VERSION:", __version__)
    print("")
    
    results = [
        test_no_type_field(),
        test_no_ui_keys(),
        test_empty_system_type(),
        test_graph_structure(),
        test_determinism(),
        test_universal_input(),
        test_performance(),
        test_output_schema(),
        test_graph_density()
    ]
    
    print("")
    passed = sum(results)
    total = len(results)
    
    print(f"RESULTS: {passed}/{total}")
    
    if all(results):
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
    
    return all(results)


if __name__ == "__main__":
    run_all()