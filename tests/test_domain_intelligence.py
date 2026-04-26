import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_engine import MEMORY
from core.domain_intelligence import (
    extract_domain, 
    detect_domain_type, 
    update_domain_learning, 
    get_domain_profile,
    set_domain_type
)
from core.config import CONFIG


def clear_memory_file():
    MEMORY.clear()
    MEMORY["deterministic_mode"] = True


def test_domain_detection():
    clear_memory_file()
    print("\n=== DOMAIN DETECTION TEST ===")
    
    tests = [
        ("https://example.com/docs/api", "documentation"),
        ("https://example.com/api/v1", "documentation"),
        ("https://example.com/blog/post", "blog"),
        ("https://example.com/article/123", "blog"),
        ("https://example.com/product/123", "ecommerce"),
        ("https://example.com/cart/checkout", "ecommerce"),
        ("https://example.com/forum/thread", "forum"),
        ("https://example.com/discussion/topic", "forum"),
        ("https://example.com/news/2024", "news"),
    ]
    
    for url, expected in tests:
        result = detect_domain_type(url)
        if result != expected:
            print(f"FAIL: {url} -> {result} (expected {expected})")
            return False
    
    print("PASS: Domain detection working")
    return True


def test_domain_extraction():
    clear_memory_file()
    print("\n=== DOMAIN EXTRACTION TEST ===")
    
    tests = [
        ("https://example.com/page", "example.com"),
        ("https://docs.example.com/api", "docs.example.com"),
        ("https://api.example.com/v1/ref", "api.example.com"),
    ]
    
    for url, expected in tests:
        result = extract_domain(url)
        if result != expected:
            print(f"FAIL: {url} -> {result} (expected {expected})")
            return False
    
    print("PASS: Domain extraction working")
    return True


def test_domain_tracking():
    clear_memory_file()
    MEMORY["deterministic_mode"] = False
    print("\n=== DOMAIN TRACKING TEST ===")
    
    update_domain_learning("example.com", 5.0, 0.1)
    profile = get_domain_profile("example.com")
    
    if profile.get("visits", 0) != 1:
        print(f"FAIL: visits not incremented")
        return False
    
    update_domain_learning("example.com", 3.0, 0.1)
    profile = get_domain_profile("example.com")
    
    if profile.get("visits", 0) != 2:
        print(f"FAIL: visits not incremented")
        return False
    
    print(f"PASS: Domain tracking working ({profile.get('visits')} visits)")
    return True


def test_domain_learning():
    clear_memory_file()
    MEMORY["deterministic_mode"] = False
    print("\n=== DOMAIN LEARNING TEST ===")
    
    update_domain_learning("example.com", 5.0, 0.1)
    profile = get_domain_profile("example.com")
    
    if profile.get("success_paths", 0) != 1:
        print(f"FAIL: success_paths not incremented")
        return False
    
    update_domain_learning("example.com", -1.0, -0.1)
    profile = get_domain_profile("example.com")
    
    if profile.get("failure_paths", 0) != 1:
        print(f"FAIL: failure_paths not incremented")
        return False
    
    print(f"PASS: Domain learning working")
    return True


def test_deterministic_safety():
    clear_memory_file()
    MEMORY["deterministic_mode"] = True
    print("\n=== DETERMINISTIC SAFETY TEST ===")
    
    update_domain_learning("example.com", 5.0, 0.1)
    profile = get_domain_profile("example.com")
    
    if profile.get("visits", 0) != 0:
        print(f"FAIL: updates in deterministic mode")
        return False
    
    print("PASS: Deterministic mode safe")
    return True


def test_domain_type():
    clear_memory_file()
    MEMORY["deterministic_mode"] = False
    print("\n=== DOMAIN TYPE TEST ===")
    
    set_domain_type("example.com", "documentation")
    profile = get_domain_profile("example.com")
    
    if profile.get("type") != "documentation":
        print(f"FAIL: domain type not set")
        return False
    
    print("PASS: Domain type set correctly")
    return True


def test_domain_scoring():
    clear_memory_file()
    MEMORY["deterministic_mode"] = False
    print("\n=== DOMAIN SCORING TEST ===")
    
    update_domain_learning("good-domain.com", 8.0, 0.1)
    update_domain_learning("good-domain.com", 7.0, 0.1)
    
    update_domain_learning("bad-domain.com", -2.0, -0.1)
    
    good_profile = get_domain_profile("good-domain.com")
    bad_profile = get_domain_profile("bad-domain.com")
    
    good_score = good_profile.get("success_paths", 0) - good_profile.get("failure_paths", 0)
    bad_score = bad_profile.get("success_paths", 0) - bad_profile.get("failure_paths", 0)
    
    if good_score <= bad_score:
        print(f"FAIL: domain scoring not working ({good_score} vs {bad_score})")
        return False
    
    print(f"PASS: Domain scoring working ({good_score} vs {bad_score})")
    return True


def run_all_tests():
    results = []
    
    results.append(("DOMAIN DETECTION", test_domain_detection()))
    results.append(("DOMAIN EXTRACTION", test_domain_extraction()))
    results.append(("DOMAIN TRACKING", test_domain_tracking()))
    results.append(("DOMAIN LEARNING", test_domain_learning()))
    results.append(("DETERMINISTIC SAFETY", test_deterministic_safety()))
    results.append(("DOMAIN TYPE", test_domain_type()))
    results.append(("DOMAIN SCORING", test_domain_scoring()))
    
    print("\n" + "=" * 50)
    print("DOMAIN INTELLIGENCE REPORT")
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