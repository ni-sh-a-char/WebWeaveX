#!/usr/bin/env python3
"""Cross-language comparison script."""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEST_OUTPUT_DIR = SCRIPT_DIR.parent.parent / 'test_output'
PYTHON_DIR = TEST_OUTPUT_DIR / 'python'
NODE_DIR = TEST_OUTPUT_DIR / 'node'
JAVA_DIR = TEST_OUTPUT_DIR / 'java'
KOTLIN_DIR = TEST_OUTPUT_DIR / 'kotlin'
DART_DIR = TEST_OUTPUT_DIR / 'dart'


def sort_dict_recursive(obj):
    """Recursively sort dictionary for comparison."""
    if isinstance(obj, dict):
        return {k: sort_dict_recursive(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        return [sort_dict_recursive(item) for item in obj]
    return obj


def compare_outputs(name, lang1="python", lang2="node"):
    """Compare outputs between two languages."""
    dir_map = {
        "python": PYTHON_DIR,
        "node": NODE_DIR,
        "java": JAVA_DIR,
        "kotlin": KOTLIN_DIR,
        "dart": DART_DIR
    }
    dir1 = dir_map.get(lang1, PYTHON_DIR)
    dir2 = dir_map.get(lang2, PYTHON_DIR)
    
    path1 = dir1 / f"{name}.json"
    path2 = dir2 / f"{name}.json"
    
    if not path1.exists():
        return False, f"{lang1.capitalize()} output not found: {path1}"
    
    if not path2.exists():
        return False, f"{lang2.capitalize()} output not found: {path2}"
    
    with open(path1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    
    with open(path2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    
    sorted1 = sort_dict_recursive(data1)
    sorted2 = sort_dict_recursive(data2)
    
    json1 = json.dumps(sorted1, indent=2, sort_keys=True)
    json2 = json.dumps(sorted2, indent=2, sort_keys=True)
    
    if json1 == json2:
        return True, "Match"
    
    diff_lines = []
    plines = json1.split('\n')
    nlines = json2.split('\n')
    
    max_lines = max(len(plines), len(nlines))
    for i in range(max_lines):
        p = plines[i] if i < len(plines) else "<missing>"
        n = nlines[i] if i < len(nlines) else "<missing>"
        if p != n:
            diff_lines.append(f"  Line {i+1}:")
            diff_lines.append(f"    {lang1.capitalize()}: {p}")
            diff_lines.append(f"    {lang2.capitalize()}: {n}")
            if len(diff_lines) >= 30:
                diff_lines.append("  ... (truncated)")
                break
    
    return False, "\n".join(diff_lines)


def main():
    """Run cross-language comparison."""
    print("=" * 60)
    print("Cross-Language Comparison")
    print("=" * 60)
    print()
    
    test_cases = [
        "basic",
        "url_email",
        "empty",
        "short",
        "numbers_only",
        "complex"
    ]
    
    languages = [
        ("python", "node"),
        ("python", "java"),
        ("python", "kotlin"),
        ("python", "dart"),
        ("node", "java"),
        ("node", "kotlin"),
        ("node", "dart"),
        ("java", "kotlin"),
        ("java", "dart"),
        ("kotlin", "dart"),
    ]
    
    all_passed = True
    total_tests = 0
    passed_tests = 0
    
    for lang1, lang2 in languages:
        print(f"\n--- {lang1.upper()} vs {lang2.upper()} ---")
        
        for name in test_cases:
            total_tests += 1
            passed, message = compare_outputs(name, lang1, lang2)
            status = "[PASS]" if passed else "[FAIL]"
            print(f"{status} {name}")
            if not passed:
                print(f"       {message}")
                all_passed = False
            else:
                passed_tests += 1
    
    print()
    print("=" * 60)
    if all_passed:
        print(f"FINAL RESULT: ALL TESTS PASSED ({passed_tests}/{total_tests})")
    else:
        print(f"FINAL RESULT: FAILED ({passed_tests}/{total_tests})")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
