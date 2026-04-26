import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.extractor_engine import ExtractionEngine, BaseExtractor
from extractors.generic_html_extractor import GenericHTMLExtractor


def clear_engine():
    engine = ExtractionEngine()
    engine.register(GenericHTMLExtractor())
    return engine


def test_basic_extraction():
    print("\n=== BASIC EXTRACTION TEST ===")
    
    engine = clear_engine()
    
    html = "<html><body><p>Hello World</p></body></html>"
    
    result = engine.extract("https://example.com", html, {})
    
    if not result:
        print("FAIL: No result returned")
        return False
    
    if result.get("type") != "generic_html":
        print(f"FAIL: Wrong type ({result.get('type')})")
        return False
    
    if not result.get("content", {}).get("text"):
        print("FAIL: No text extracted")
        return False
    
    print(f"PASS: Basic extraction working ({result.get('type')})")
    return True


def test_fallback():
    print("\n=== FALLBACK TEST ===")
    
    engine = clear_engine()
    
    result = engine.extract("https://example.com", "", {})
    
    if not result:
        print("FAIL: No fallback result")
        return False
    
    if result.get("metadata", {}).get("source") != "fallback":
        print("FAIL: Not fallback source")
        return False
    
    print(f"PASS: Fallback working (source={result.get('metadata', {}).get('source')})")
    return True


def test_determinism():
    print("\n=== DETERMINISM TEST ===")
    
    engine = clear_engine()
    
    html = "<html><body><p>Test content</p></body></html>"
    
    result1 = engine.extract("https://example.com", html, {})
    result2 = engine.extract("https://example.com", html, {})
    
    if result1 != result2:
        print("FAIL: Results differ")
        return False
    
    print("PASS: Deterministic extraction")
    return True


def test_empty_html():
    print("\n=== EMPTY HTML TEST ===")
    
    engine = clear_engine()
    
    result = engine.extract("https://example.com", None, {})
    
    if not result:
        print("FAIL: No result for None html")
        return False
    
    if result.get("metadata", {}).get("source") != "fallback":
        print("FAIL: Not fallback for None html")
        return False
    
    print("PASS: Empty HTML handled")
    return True


def test_output_schema():
    print("\n=== OUTPUT SCHEMA TEST ===")
    
    engine = clear_engine()
    
    html = "<html><body><p>Content</p></body></html>"
    result = engine.extract("https://example.com", html, {})
    
    required_keys = {"url", "type", "content", "metadata"}
    content_keys = {"text", "code", "structured"}
    
    if not required_keys.issubset(result.keys()):
        print(f"FAIL: Missing keys in result")
        return False
    
    if not content_keys.issubset(result.get("content", {}).keys()):
        print(f"FAIL: Missing keys in content")
        return False
    
    print("PASS: Output schema valid")
    return True


def test_extractor_priority():
    print("\n=== EXTRACTOR PRIORITY TEST ===")
    
    class DummyExtractor(BaseExtractor):
        def can_handle(self, url, html, metadata):
            return True
        
        def extract(self, url, html, metadata):
            return {"type": "dummy", "text": "dummy"}
    
    engine = ExtractionEngine()
    engine.register(DummyExtractor())
    engine.register(GenericHTMLExtractor())
    
    html = "<html><body><p>Hello</p></body></html>"
    
    result = engine.extract("https://example.com", html, {})
    
    if result.get("type") != "dummy":
        print(f"FAIL: Generic extractor overrode specific extractor (got {result.get('type')})")
        return False
    
    print("PASS: Extractor priority working")
    return True


def test_priority_system():
    print("\n=== PRIORITY SYSTEM TEST ===")
    
    class Low(BaseExtractor):
        priority = 1
        def can_handle(self, url, html, metadata): return True
        def extract(self, url, html, metadata): return {"type": "low"}
    
    class High(BaseExtractor):
        priority = 100
        def can_handle(self, url, html, metadata): return True
        def extract(self, url, html, metadata): return {"type": "high"}
    
    engine = ExtractionEngine()
    engine.register(Low())
    engine.register(High())
    
    result = engine.extract("https://example.com", "<html></html>", {})
    
    if result.get("type") != "high":
        print(f"FAIL: Priority broken (got {result.get('type')})")
        return False
    
    print("PASS: Priority working")
    return True


def run_all_tests():
    results = []
    
    results.append(("BASIC EXTRACTION", test_basic_extraction()))
    results.append(("FALLBACK", test_fallback()))
    results.append(("DETERMINISM", test_determinism()))
    results.append(("EMPTY HTML", test_empty_html()))
    results.append(("OUTPUT SCHEMA", test_output_schema()))
    results.append(("EXTRACTOR PRIORITY", test_extractor_priority()))
    results.append(("PRIORITY SYSTEM", test_priority_system()))
    
    print("\n" + "=" * 50)
    print("EXTRACTION ENGINE REPORT")
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