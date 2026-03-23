#!/usr/bin/env python3
"""Export Python WebWeaveX outputs for cross-language comparison."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'implementations', 'python'))

from webweavex import WebWeaveX

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'test_output', 'python')
TEST_CASES_PATH = os.path.join(SCRIPT_DIR, '..', 'test_cases', 'test_cases.json')


def export_python_outputs():
    """Export Python outputs for all test cases."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(TEST_CASES_PATH, 'r') as f:
        test_cases = json.load(f)
    
    wx = WebWeaveX()
    
    print("Exporting Python outputs...")
    print("=" * 50)
    
    for tc in test_cases:
        name = tc['name']
        input_text = tc['input']
        
        print(f"Processing: {name}")
        
        result = wx.extract(input_text)
        output = result.to_dict()
        
        output_path = os.path.join(OUTPUT_DIR, f"{name}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, sort_keys=True, ensure_ascii=False)
        
        print(f"  Saved: {output_path}")
    
    print("=" * 50)
    print(f"Exported {len(test_cases)} test cases to {OUTPUT_DIR}")
    
    manifest_path = os.path.join(OUTPUT_DIR, 'manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump({'language': 'python', 'test_cases': [tc['name'] for tc in test_cases]}, f, indent=2)
    print(f"Manifest: {manifest_path}")


if __name__ == '__main__':
    export_python_outputs()
