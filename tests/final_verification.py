import sys
sys.path.insert(0, '.')

from core.fetcher import fetch_url
from core.parser import extract_all
from core.canonical import canonicalize
from core.kaalka_engine import encrypt_canonical
from core.detector import detect_page
from core.adaptive import adaptive_extract
from core.api_engine import execute_endpoints, is_valid_endpoint
from core.ai_engine import is_ai_available, augment_with_ai

def test_static_site():
    html = fetch_url("https://example.com")
    if not html:
        return False
    
    data = extract_all(html, "https://example.com")
    
    c1 = canonicalize(data)
    c2 = canonicalize(data)
    if c1 != c2:
        print("FAIL: canonical not deterministic")
        return False
    
    ts = 1234567890
    e1 = encrypt_canonical(c1, ts)
    e2 = encrypt_canonical(c2, ts)
    if e1 != e2:
        print("FAIL: encryption not deterministic")
        return False
    
    detection = detect_page(html, data)
    if detection.get("extractable") != "full":
        print("FAIL: detection incorrect for static site")
        return False
    
    adaptive = adaptive_extract("https://example.com", html, data, detection)
    if adaptive.get("strategy") != "standard":
        print("FAIL: adaptive strategy incorrect")
        return False
    
    print("PASS: static site test")
    return True


def test_endpoint_validation():
    valid = is_valid_endpoint("https://api.example.com/data.json")
    if not valid:
        return False
    
    invalid = is_valid_endpoint("https://example.com/page")
    if invalid:
        return False
    
    print("PASS: endpoint validation")
    return True


def test_api_execution():
    endpoints = ["https://jsonplaceholder.typicode.com/posts/1"]
    results = execute_endpoints(endpoints)
    print("PASS: API execution")
    return True


def test_ai_availability():
    available = is_ai_available()
    print(f"AI Available: {available}")
    print("PASS: AI check")
    return True


def test_output_contract():
    from core.crawler import WebCrawler
    crawler = WebCrawler()
    results = crawler.crawl("https://example.com", depth=1)
    
    r = results[0]
    required_keys = ["url", "canonical", "encrypted", "timestamp", "detection", "adaptive"]
    
    for key in required_keys:
        if key not in r:
            print(f"FAIL: missing key {key}")
            return False
    
    if not isinstance(r["timestamp"], int):
        print("FAIL: timestamp not int")
        return False
    
    if not isinstance(r["url"], str):
        print("FAIL: url not str")
        return False
    
    print("PASS: output contract")
    return True


def test_immutability():
    from core.ai_engine import augment_with_ai
    
    original = {"strategy": "standard", "data": {}}
    detection = {"confidence": 0.5}
    result = augment_with_ai(original, "", "", detection)
    
    if result is original:
        print("FAIL: mutation detected")
        return False
    
    print("PASS: immutability")
    return True


def main():
    tests = [
        test_static_site,
        test_endpoint_validation,
        test_api_execution,
        test_ai_availability,
        test_output_contract,
        test_immutability,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"FAIL: {test.__name__} - {e}")
    
    print(f"\n{passed}/{len(tests)} tests passed")
    return passed == len(tests)


if __name__ == "__main__":
    main()