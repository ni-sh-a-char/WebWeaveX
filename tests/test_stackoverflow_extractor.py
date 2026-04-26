import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.extractor_engine import ExtractionEngine
from extractors.stackoverflow_extractor import StackOverflowExtractor
from extractors.github_extractor import GitHubExtractor
from extractors.generic_html_extractor import GenericHTMLExtractor


def test_detection():
    print("\n=== DETECTION TEST ===")
    
    extractor = StackOverflowExtractor()
    
    if extractor.can_handle("https://stackoverflow.com/questions/123", "", {}):
        print("PASS: StackOverflow URL detected")
        return True
    
    if not extractor.can_handle("https://example.com", "", {}):
        print("PASS: Non-StackOverflow URL not detected")
        return True
    
    print("FAIL: Detection broken")
    return False


def test_question_extraction():
    print("\n=== QUESTION EXTRACTION TEST ===")
    
    html = """
    <html><title>How to parse JSON in Python? - Stack Overflow</title>
    <div class="s-prose js-post-body"><p>I need to parse a JSON string in Python</p></div>
    </html>
    """
    
    extractor = StackOverflowExtractor()
    result = extractor.extract("https://stackoverflow.com/questions/123", html, {})
    
    if not result:
        print("FAIL: No result")
        return False
    
    if result.get("type") != "stackoverflow":
        print(f"FAIL: Wrong type ({result.get('type')})")
        return False
    
    text = result.get("text", "")
    if "json" not in text.lower() or "python" not in text.lower():
        print("FAIL: Question text not extracted")
        return False
    
    print("PASS: Question extraction working")
    return True


def test_answer_extraction():
    print("\n=== ANSWER EXTRACTION TEST ===")
    
    html = """
    <html><body>
    <div class="answer"><p>Use json.loads()</p></div>
    <div class="answer"><p>Use json.load()</p></div>
    </body></html>
    """
    
    extractor = StackOverflowExtractor()
    result = extractor.extract("https://stackoverflow.com/questions/123", html, {})
    
    if not result:
        print("FAIL: No result")
        return False
    
    answers = result.get("structured", {}).get("answers", [])
    if len(answers) < 2:
        print("FAIL: Answers not extracted")
        return False
    
    print(f"PASS: Answer extraction working ({len(answers)} answers)")
    return True


def test_code_extraction():
    print("\n=== CODE EXTRACTION TEST ===")
    
    html = """
    <html><body>
    <pre><code>import json
    data = json.loads(text)</code></pre>
    </body></html>
    """
    
    extractor = StackOverflowExtractor()
    result = extractor.extract("https://stackoverflow.com/questions/123", html, {})
    
    if not result:
        print("FAIL: No result")
        return False
    
    code = result.get("code", [])
    if len(code) < 1:
        print("FAIL: Code not extracted")
        return False
    
    print(f"PASS: Code extraction working ({len(code)} blocks)")
    return True


def test_deterministic():
    print("\n=== DETERMINISM TEST ===")
    
    html = "<html><title>Test - Stack Overflow</title><div class='answer'><p>Answer</p></div></html>"
    
    extractor = StackOverflowExtractor()
    
    result1 = extractor.extract("https://stackoverflow.com/questions/123", html, {})
    result2 = extractor.extract("https://stackoverflow.com/questions/123", html, {})
    
    if result1 != result2:
        print("FAIL: Results differ")
        return False
    
    print("PASS: Deterministic extraction")
    return True


def test_extractor_priority():
    print("\n=== EXTRACTOR PRIORITY TEST ===")
    
    engine = ExtractionEngine()
    engine.register(StackOverflowExtractor())
    engine.register(GitHubExtractor())
    engine.register(GenericHTMLExtractor())
    
    html = "<html><title>Test</title></html>"
    result = engine.extract("https://stackoverflow.com/questions/123", html, {})
    
    if result.get("type") != "stackoverflow":
        print(f"FAIL: Wrong type ({result.get('type')})")
        return False
    
    print(f"PASS: StackOverflow extractor has priority ({result.get('type')})")
    return True


def run_all_tests():
    results = []
    
    results.append(("DETECTION", test_detection()))
    results.append(("QUESTION EXTRACTION", test_question_extraction()))
    results.append(("ANSWER EXTRACTION", test_answer_extraction()))
    results.append(("CODE EXTRACTION", test_code_extraction()))
    results.append(("DETERMINISM", test_deterministic()))
    results.append(("EXTRACTOR PRIORITY", test_extractor_priority()))
    
    print("\n" + "=" * 50)
    print("STACKOVERFLOW EXTRACTOR REPORT")
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