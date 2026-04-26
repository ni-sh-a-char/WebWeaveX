import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_engine import MEMORY, update_navigation_pattern
from core.domain_intelligence import (
    compute_exploration_priority,
    compute_pattern_score,
    get_domain_profile
)
from core.config import CONFIG


def clear_memory_file():
    MEMORY.clear()
    MEMORY["deterministic_mode"] = True
    MEMORY["navigation_patterns"] = {}


def test_compute_exploration_priority():
    clear_memory_file()
    print("\n=== COMPUTE EXPLORATION PRIORITY TEST ===")
    
    profile = {
        "visits": 5,
        "success_paths": 3,
        "failure_paths": 1,
        "quality_score": 0.5
    }
    
    priority = compute_exploration_priority(profile)
    
    if priority <= 0:
        print(f"FAIL: Priority should be positive ({priority})")
        return False
    
    empty_priority = compute_exploration_priority({})
    
    if empty_priority != 0:
        print(f"FAIL: Empty profile should be 0")
        return False
    
    print(f"PASS: Exploration priority working ({priority})")
    return True


def test_pattern_tracking():
    clear_memory_file()
    MEMORY["deterministic_mode"] = False
    print("\n=== PATTERN TRACKING TEST ===")
    
    path = ["https://a.com", "https://b.com", "https://c.com"]
    
    update_navigation_pattern(path, True)
    
    patterns = MEMORY.get("navigation_patterns", {})
    
    if not patterns:
        print("FAIL: Pattern not tracked")
        return False
    
    key = tuple(path[-3:])
    
    if key not in patterns:
        print("FAIL: Pattern key not found")
        return False
    
    if patterns[key].get("success", 0) != 1:
        print("FAIL: Success not recorded")
        return False
    
    print(f"PASS: Pattern tracking working")
    return True


def test_pattern_scoring():
    clear_memory_file()
    MEMORY["deterministic_mode"] = False
    print("\n=== PATTERN SCORING TEST ===")
    
    path = ["https://a.com", "https://b.com", "https://c.com"]
    key = tuple(path[-3:])
    
    MEMORY["navigation_patterns"] = {
        key: {"success": 5, "failure": 2}
    }
    
    score = compute_pattern_score(path)
    
    if score != 3:
        print(f"FAIL: Pattern score incorrect ({score})")
        return False
    
    short_path = ["https://a.com"]
    short_score = compute_pattern_score(short_path)
    
    if short_score != 0:
        print("FAIL: Short path should return 0")
        return False
    
    print(f"PASS: Pattern scoring working ({score})")
    return True


def test_deterministic_safety():
    clear_memory_file()
    MEMORY["deterministic_mode"] = True
    print("\n=== DETERMINISTIC SAFETY TEST ===")
    
    path = ["https://a.com", "https://b.com", "https://c.com"]
    
    update_navigation_pattern(path, True)
    
    patterns = MEMORY.get("navigation_patterns", {})
    
    if len(patterns) > 0:
        print("FAIL: Pattern updated in deterministic mode")
        return False
    
    print("PASS: Deterministic mode safe")
    return True


def test_exploration_priority_sorting():
    clear_memory_file()
    MEMORY["deterministic_mode"] = False
    print("\n=== EXPLORATION PRIORITY SORTING TEST ===")
    
    less_explored = {
        "visits": 1,
        "success_paths": 1,
        "failure_paths": 0,
        "quality_score": 0.5
    }
    
    more_explored = {
        "visits": 10,
        "success_paths": 5,
        "failure_paths": 2,
        "quality_score": 0.8
    }
    
    priority_less = compute_exploration_priority(less_explored)
    priority_more = compute_exploration_priority(more_explored)
    
    if priority_less <= priority_more:
        print(f"FAIL: Less explored should have higher priority ({priority_less} vs {priority_more})")
        return False
    
    print(f"PASS: Exploration priority sorting working ({priority_less} > {priority_more})")
    return True


def run_all_tests():
    results = []
    
    results.append(("COMPUTE EXPLORATION PRIORITY", test_compute_exploration_priority()))
    results.append(("PATTERN TRACKING", test_pattern_tracking()))
    results.append(("PATTERN SCORING", test_pattern_scoring()))
    results.append(("DETERMINISTIC SAFETY", test_deterministic_safety()))
    results.append(("EXPLORATION PRIORITY SORTING", test_exploration_priority_sorting()))
    
    print("\n" + "=" * 50)
    print("PATTERN INTELLIGENCE REPORT")
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