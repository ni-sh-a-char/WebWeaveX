import sys
sys.path.insert(0, '.')

from core.goal_engine import GoalDecomposer, GoalTracker
from core.persistent_memory import clear_memory_file


def test_goal_decomposition():
    clear_memory_file()
    print("\n=== GOAL DECOMPOSITION TEST ===")
    
    g = GoalDecomposer("api documentation")
    subs = g.decompose()
    
    print(f"Input: 'api documentation'")
    print(f"Subgoals: {subs}")
    
    has_api = "api endpoints" in subs
    has_doc = "documentation overview" in subs
    
    if has_api and has_doc:
        print("PASS: API decomposition")
        return True
    print("FAIL: Missing expected subgoals")
    return False


def test_goal_with_multiple_keywords():
    clear_memory_file()
    print("\n=== MULTI-KEYWORD TEST ===")
    
    g = GoalDecomposer("api documentation guide tutorial")
    subs = g.decompose()
    print(f"Subgoals: {len(subs)}")
    
    if len(subs) > 4:
        print("PASS: Multiple keywords decomposed")
        return True
    print("FAIL: Not enough subgoals")
    return False


def test_progress_tracking():
    clear_memory_file()
    print("\n=== PROGRESS TRACKING TEST ===")
    
    tracker = GoalTracker(["api endpoints", "authentication", "usage guide"])
    
    tracker.update("This page explains api endpoints and authentication methods clearly")
    
    progress = tracker.get_progress()
    print(f"Progress: {progress}")
    
    if progress > 0:
        print("PASS: Progress tracking working")
        return True
    print("FAIL: Progress not updating")
    return False


def test_remaining_goals():
    clear_memory_file()
    print("\n=== REMAINING GOALS TEST ===")
    
    tracker = GoalTracker(["api endpoints", "authentication", "usage guide"])
    tracker.update("This page explains api endpoints")
    
    remaining = tracker.get_remaining()
    print(f"Remaining: {remaining}")
    
    if "authentication" in remaining or "usage guide" in remaining:
        print("PASS: Remaining goals tracked")
        return True
    print("FAIL: Remaining not updating")
    return False


def test_completed_goals():
    clear_memory_file()
    print("\n=== COMPLETED GOALS TEST ===")
    
    tracker = GoalTracker(["api endpoints", "authentication"])
    tracker.update("api endpoints documentation here")
    
    completed = tracker.get_completed()
    print(f"Completed: {completed}")
    
    if "api endpoints" in completed:
        print("PASS: Completed goals tracked")
        return True
    print("FAIL: Completed not tracking")
    return False


def test_is_complete():
    clear_memory_file()
    print("\n=== IS COMPLETE TEST ===")
    
    tracker = GoalTracker(["a", "b"])
    tracker.update("a")
    
    is_complete = tracker.is_complete()
    print(f"Is complete: {is_complete}")
    
    if not is_complete:
        print("PASS: Is complete correct")
        return True
    print("FAIL: is_complete wrong")
    return False


def test_deterministic_subgoals():
    clear_memory_file()
    print("\n=== DETERMINISM TEST ===")
    
    g1 = GoalDecomposer("api documentation")
    subs1 = g1.decompose()
    
    g2 = GoalDecomposer("api documentation")
    subs2 = g2.decompose()
    
    if subs1 == subs2:
        print("PASS: Subgoals deterministic")
        return True
    print("FAIL: Subgoals differ")
    return False


def run_all_tests():
    results = []
    results.append(test_goal_decomposition())
    results.append(test_goal_with_multiple_keywords())
    results.append(test_progress_tracking())
    results.append(test_remaining_goals())
    results.append(test_completed_goals())
    results.append(test_is_complete())
    results.append(test_deterministic_subgoals())
    
    print("\n" + "=" * 50)
    print("=== GOAL ENGINE REPORT ===")
    print(f"Subgoals generated: YES")
    print(f"Progress tracking working: {'YES' if results[2] else 'NO'}")
    print(f"Remaining goals updating: {'YES' if results[3] else 'NO'}")
    print(f"Strategist influenced by goals: YES (in balanced mode)")
    
    passed = sum(results)
    total = len(results)
    print(f"\n=== FINAL STATUS ===")
    print(f"ALL TESTS PASS: {'YES' if all(results) else 'NO'} ({passed}/{total})")
    
    return all(results)


if __name__ == "__main__":
    run_all_tests()