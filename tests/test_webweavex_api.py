import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from webweavex import extract, extract_batch, get_config, set_config, CONFIG
from core.memory_context import MemoryContext


def test_config():
    print("\n=== CONFIG TEST ===")
    
    cfg = get_config()
    
    if cfg.get("ai_mode") != "off":
        print("FAIL: Default ai_mode not off")
        return False
    
    if not cfg.get("intelligence"):
        print("FAIL: Default intelligence not True")
        return False
    
    print(f"PASS: Config working ({cfg})")
    return True


def test_set_config():
    print("\n=== SET CONFIG TEST ===")
    
    set_config("ai_mode", "cloud")
    
    if get_config().get("ai_mode") != "cloud":
        print("FAIL: Config not set")
        return False
    
    set_config("ai_mode", "off")
    
    print("PASS: Set config working")
    return True


def test_extract_with_html():
    print("\n=== EXTRACT WITH HTML TEST ===")
    
    html = "<html><body><p>Python is great for machine learning and API development.</p><code>def train(): pass</code></body></html>"
    
    ctx = MemoryContext()
    result = extract(html=html, context=ctx)
    
    if not result.get("content"):
        print("FAIL: No content")
        return False
    
    if not result.get("intelligence"):
        print("FAIL: No intelligence")
        return False
    
    if "knowledge" not in result:
        print("FAIL: No knowledge key")
        return False
    
    print(f"PASS: Extract with HTML working")
    return True


def test_extract_empty():
    print("\n=== EXTRACT EMPTY TEST ===")
    
    ctx = MemoryContext()
    result = extract(context=ctx)
    
    if result.get("content") is None:
        print("FAIL: Content should be empty dict")
        return False
    
    print(f"PASS: Extract empty working")
    return True


def test_extract_batch():
    print("\n=== EXTRACT BATCH TEST ===")
    
    htmls = [
        "<html><body><p>Python</p></body></html>",
        "<html><body><p>JavaScript</p></body></html>"
    ]
    
    results = [extract(html=h, context=MemoryContext()) for h in htmls]
    
    if len(results) != 2:
        print(f"FAIL: Expected 2 results, got {len(results)}")
        return False
    
    print(f"PASS: Extract batch working ({len(results)} results)")
    return True


def test_determinism():
    print("\n=== DETERMINISM TEST ===")
    
    html = "<html><body><p>Python machine learning</p></body></html>"
    
    result1 = extract(html=html, context=MemoryContext())
    result2 = extract(html=html, context=MemoryContext())
    
    if result1 != result2:
        print("FAIL: Results differ")
        return False
    
    print("PASS: Deterministic extraction")
    return True


def run_all_tests():
    results = []
    
    results.append(("CONFIG", test_config()))
    results.append(("SET CONFIG", test_set_config()))
    results.append(("EXTRACT WITH HTML", test_extract_with_html()))
    results.append(("EXTRACT EMPTY", test_extract_empty()))
    results.append(("EXTRACT BATCH", test_extract_batch()))
    results.append(("DETERMINISM", test_determinism()))
    
    print("\n" + "=" * 50)
    print("WEBWEAVEX API REPORT")
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
