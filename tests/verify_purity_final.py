"""
WebWeaveX Purity Validation Script

Purpose:
    Final validation of pure system compiler
    - No semantic maps
    - No keyword logic
    - Deterministic outputs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webweavex import run


def validate_purity():
    """Validate all purity requirements."""
    
    # Test 1: No semantic maps
    with open("core/semantic_engine.py") as f:
        content = f.read()
    
    if "ENTITY_PATTERN_MAP" in content or "ACTION_VERBS" in content:
        print("❌ FAILED: Semantic maps found")
        return False
    
    print("✅ PASSED: No semantic maps")
    
    # Test 2: Pure tokenization
    result = run({"input": "build api", "mode": "compiler"})
    sd = result.get("structured_data", {})
    semantics = sd.get("semantics", {})
    
    entities = semantics.get("entities", [])
    if not all(isinstance(e, dict) and "text" in e for e in entities):
        print("❌ FAILED: Entities not pure")
        return False
    
    print("✅ PASSED: Pure entities")
    
    # Test 3: Determinism
    r1 = run({"input": "test", "mode": "compiler"})
    r2 = run({"input": "test", "mode": "compiler"})
    
    if r1 != r2:
        print("❌ FAILED: Not deterministic")
        return False
    
    print("✅ PASSED: Deterministic")
    
    # Test 4: No forbidden types
    design = sd.get("system_design", {})
    if design.get("type") in ["execute", "simple"]:
        print("❌ FAILED: Forbidden types found")
        return False
    
    print("✅ PASSED: No forbidden types")
    
    print("\n🎉 ALL PURITY TESTS PASSED")
    return True


if __name__ == "__main__":
    validate_purity()