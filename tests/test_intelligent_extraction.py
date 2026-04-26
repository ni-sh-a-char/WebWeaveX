import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.intelligent_extraction import build_intelligence
from core.memory_context import MemoryContext


def create_context():
    ctx = MemoryContext()
    ctx["deterministic_mode"] = True
    return ctx


def test_basic():
    ctx = create_context()
    print("\n=== BASIC TEST ===")
    
    content = {
        "text": "Visit https://example.com for Python docs. Check setup.py for config.",
        "code": ["def hello(): print('world')"],
        "structured": {"title": "Test"}
    }
    
    result = build_intelligence(content, context=ctx)
    
    if not result.get("summary"):
        print("FAIL: No summary")
        return False
    
    if not result.get("topics"):
        print("FAIL: No topics")
        return False
    
    if "python" not in result.get("code_insights", {}).get("languages", []):
        print("FAIL: Language not detected")
        return False
    
    print(f"PASS: Basic extraction working")
    return True


def test_determinism():
    ctx = create_context()
    print("\n=== DETERMINISM TEST ===")
    
    content = {
        "text": "Python programming is great for web development.",
        "code": ["def test(): pass"]
    }
    
    result1 = build_intelligence(content, context=ctx)
    result2 = build_intelligence(content, context=ctx)
    
    if result1 != result2:
        print("FAIL: Results differ")
        return False
    
    print("PASS: Deterministic extraction")
    return True


def test_code_insights():
    ctx = create_context()
    print("\n=== CODE INSIGHTS TEST ===")
    
    content = {
        "text": "Code with functions and classes",
        "code": [
            "def my_function(): pass",
            "function another() {}",
            "class MyClass {}"
        ]
    }
    
    result = build_intelligence(content, context=ctx)
    insights = result.get("code_insights", {})
    
    if insights.get("functions", 0) < 2:
        print(f"FAIL: Functions not detected ({insights})")
        return False
    
    if insights.get("classes", 0) < 1:
        print(f"FAIL: Classes not detected ({insights})")
        return False
    
    print(f"PASS: Code insights working ({insights})")
    return True


def test_importance():
    ctx = create_context()
    print("\n=== IMPORTANCE TEST ===")
    
    short_content = {"text": "Short", "code": []}
    long_content = {"text": "x " * 2000, "code": ["def x(): pass"]}
    
    short_result = build_intelligence(short_content, context=ctx)
    long_result = build_intelligence(long_content, context=ctx)
    
    if long_result.get("importance_score", 0) <= short_result.get("importance_score", 0):
        print("FAIL: Long content not scored higher")
        return False
    
    print(f"PASS: Importance scoring working")
    return True


def test_content_type():
    ctx = create_context()
    print("\n=== CONTENT TYPE TEST ===")
    
    content_code = {"text": "text", "code": ["def x(): pass"]}
    content_article = {"text": "a " * 2000, "code": []}
    content_structured = {"text": "text", "code": [], "structured": {"key": "value"}}
    content_short = {"text": "short", "code": []}
    
    result_code = build_intelligence(content_code, context=ctx)
    result_article = build_intelligence(content_article, context=ctx)
    result_structured = build_intelligence(content_structured, context=ctx)
    result_short = build_intelligence(content_short, context=ctx)
    
    if result_code.get("content_type") != "code":
        print(f"FAIL: code type wrong")
        return False
    
    if result_article.get("content_type") != "article":
        print(f"FAIL: article type wrong")
        return False
    
    if result_structured.get("content_type") != "structured":
        print(f"FAIL: structured type wrong")
        return False
    
    if result_short.get("content_type") != "short_text":
        print(f"FAIL: short_text type wrong")
        return False
    
    print("PASS: Content type detection working")
    return True


def test_capabilities():
    ctx = create_context()
    print("\n=== CAPABILITIES TEST ===")
    
    content = {
        "text": "This API is used to scrape web data and train ML models using neural networks.",
        "code": ["def train(): pass"]
    }
    
    result = build_intelligence(content, context=ctx)
    caps = result.get("capabilities", [])
    
    if not caps:
        print("FAIL: No capabilities detected")
        return False
    
    if "api_usage" not in caps and "web_scraping" not in caps:
        print(f"FAIL: Expected capability not found ({caps})")
        return False
    
    print(f"PASS: Capabilities working ({caps})")
    return True


def test_concepts():
    ctx = create_context()
    print("\n=== CONCEPTS TEST ===")
    
    content = {
        "text": "Python machine learning API using TensorFlow and docker containers."
    }
    
    result = build_intelligence(content, context=ctx)
    concepts = result.get("concepts", [])
    
    if not concepts:
        print("FAIL: No concepts detected")
        return False
    
    if "python" not in concepts:
        print("FAIL: python concept not found")
        return False
    
    print(f"PASS: Concepts working ({concepts})")
    return True


def test_confidence():
    ctx = create_context()
    print("\n=== CONFIDENCE TEST ===")
    
    empty_content = {"text": ""}
    full_content = {
        "text": "Python API for machine learning with tensorflow docker containers"
    }
    
    empty_result = build_intelligence(empty_content, context=ctx)
    full_result = build_intelligence(full_content, context=ctx)
    
    if "confidence" not in full_result:
        print("FAIL: Confidence missing")
        return False
    
    if full_result.get("confidence", 0) <= empty_result.get("confidence", 0):
        print("FAIL: Confidence not properly scored")
        return False
    
    print(f"PASS: Confidence working")
    return True


def test_relations():
    ctx = create_context()
    print("\n=== RELATIONS TEST ===")
    
    content = {
        "text": "api machine learning docker"
    }
    
    result = build_intelligence(content, context=ctx)
    relations = result.get("relations", [])
    
    if not isinstance(relations, list):
        print("FAIL: Relations not a list")
        return False
    
    print(f"PASS: Relations working ({len(relations)} relations)")
    return True


def test_schema_complete():
    ctx = create_context()
    print("\n=== SCHEMA COMPLETE TEST ===")
    
    content = {
        "text": "Python API machine learning",
        "code": ["def test(): pass"]
    }
    
    result = build_intelligence(content, context=ctx)
    required = ["summary", "topics", "entities", "concepts", "capabilities", "relations", "code_insights", "content_type", "importance_score", "confidence"]
    
    for key in required:
        if key not in result:
            print(f"FAIL: Missing {key}")
            return False
    
    print("PASS: Schema complete")
    return True


def run_all_tests():
    results = []
    
    results.append(("BASIC", test_basic()))
    results.append(("DETERMINISM", test_determinism()))
    results.append(("CODE INSIGHTS", test_code_insights()))
    results.append(("IMPORTANCE", test_importance()))
    results.append(("CONTENT TYPE", test_content_type()))
    results.append(("CAPABILITIES", test_capabilities()))
    results.append(("CONCEPTS", test_concepts()))
    results.append(("CONFIDENCE", test_confidence()))
    results.append(("RELATIONS", test_relations()))
    results.append(("SCHEMA COMPLETE", test_schema_complete()))
    
    print("\n" + "=" * 50)
    print("INTELLIGENT EXTRACTION REPORT")
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
