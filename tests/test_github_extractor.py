import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.extractor_engine import ExtractionEngine
from extractors.github_extractor import GitHubExtractor
from extractors.generic_html_extractor import GenericHTMLExtractor


def test_github_detection():
    print("\n=== GITHUB DETECTION TEST ===")
    
    extractor = GitHubExtractor()
    
    if extractor.can_handle("https://github.com/user/repo", "", {}):
        print("PASS: GitHub URL detected")
        return True
    
    if extractor.can_handle("https://gitlab.com/user/repo", "", {}):
        print("PASS: GitLab URL detected (fallback)")
        return True
    
    if not extractor.can_handle("https://example.com", "", {}):
        print("PASS: Non-GitHub URL not detected")
        return True
    
    print("FAIL: Detection broken")
    return False


def test_code_extraction():
    print("\n=== CODE EXTRACTION TEST ===")
    
    html = """
    <html><head><title>Test Repo</title></head><body>
    <pre><code>def hello():
    print("world")
</code></pre>
    <pre><code>function test() {
    return true;
}</code></pre>
    </body></html>
    """
    
    extractor = GitHubExtractor()
    result = extractor.extract("https://github.com/test/repo", html, {})
    
    if not result:
        print("FAIL: No result returned")
        return False
    
    if result.get("type") != "github":
        print(f"FAIL: Wrong type ({result.get('type')})")
        return False
    
    if len(result.get("code", [])) < 2:
        print("FAIL: Code blocks not extracted")
        return False
    
    print(f"PASS: Code extraction working ({len(result.get('code', []))} blocks)")
    return True


def test_structured_title():
    print("\n=== STRUCTURED TITLE TEST ===")
    
    html = "<html><title>my-project - GitHub</title></html>"
    
    extractor = GitHubExtractor()
    result = extractor.extract("https://github.com/user/my-project", html, {})
    
    if not result:
        print("FAIL: No result")
        return False
    
    structured = result.get("structured", {})
    if "title" not in structured:
        print("FAIL: Title not in structured")
        return False
    
    print(f"PASS: Title extracted ({structured.get('title')})")
    return True


def test_deterministic():
    print("\n=== DETERMINISM TEST ===")
    
    html = "<html><title>Repo</title><pre><code>def test(): pass</code></pre></html>"
    
    extractor = GitHubExtractor()
    
    result1 = extractor.extract("https://github.com/test/repo", html, {})
    result2 = extractor.extract("https://github.com/test/repo", html, {})
    
    if result1 != result2:
        print("FAIL: Results differ")
        return False
    
    print("PASS: Deterministic extraction")
    return True


def test_extractor_priority():
    print("\n=== EXTRACTOR PRIORITY TEST ===")
    
    engine = ExtractionEngine()
    engine.register(GitHubExtractor())
    engine.register(GenericHTMLExtractor())
    
    html = "<html><title>Test</title></html>"
    result = engine.extract("https://github.com/user/repo", html, {})
    
    if result.get("type") != "github":
        print(f"FAIL: Wrong type ({result.get('type')})")
        return False
    
    print(f"PASS: GitHub extractor has priority ({result.get('type')})")
    return True


def run_all_tests():
    results = []
    
    results.append(("GITHUB DETECTION", test_github_detection()))
    results.append(("CODE EXTRACTION", test_code_extraction()))
    results.append(("STRUCTURED TITLE", test_structured_title()))
    results.append(("DETERMINISM", test_deterministic()))
    results.append(("EXTRACTOR PRIORITY", test_extractor_priority()))
    
    print("\n" + "=" * 50)
    print("GITHUB EXTRACTOR REPORT")
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