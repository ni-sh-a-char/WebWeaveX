"""
test_full_system.py

Real functional testing for WebWeaveX pipeline.
"""

import hashlib
import json
from webweavex import run

# Test inputs
TEST_INPUTS = [
    "calculator app",
    "todo app with login",
    "weather dashboard India",
    "stock market analysis NIFTY 50",
    "chat websocket app",
    "AI trading bot",
    "portfolio website",
    "python REST API",
    "ML pipeline",
    "ecommerce system"
]

def test_full_system():
    results = []
    hashes = []

    for inp in TEST_INPUTS:
        try:
            result = run({"input": inp})
            print(f"Input: {inp}")
            print(f"Structured: {result.get('structured_data', {})}")
            print(f"Has input_signature: {'input_signature' in result.get('structured_data', {})}")
            # Validate schema
            required_keys = ["human_readable", "structured_data", "ui_schema", "confidence", "source", "reconstructed_project", "version"]
            for key in required_keys:
                if key not in result:
                    raise ValueError(f"Missing key: {key}")

            # Ensure no None values in structured_data
            structured = result["structured_data"]
            if any(v is None for v in structured.values()):
                raise ValueError("None values in structured_data")

            # Ensure meaningful outputs
            if not result["human_readable"] or len(result["human_readable"]) < 10:
                raise ValueError("Poor human_readable")

            if not structured or structured == {}:
                raise ValueError("Empty structured_data")

            ui = result["ui_schema"]
            if not ui.get("components"):
                raise ValueError("Empty ui_schema components")

            # Compute hash
            result_str = json.dumps(result, sort_keys=True)
            h = hashlib.sha256(result_str.encode()).hexdigest()
            hashes.append(h)
            print(f"Hash: {h}")

            results.append({
                "input": inp,
                "success": True,
                "hash": h
            })

        except Exception as e:
            results.append({
                "input": inp,
                "success": False,
                "error": str(e)
            })

    # Check all hashes differ
    if len(set(hashes)) != len(hashes):
        print("Hashes:", hashes)
        raise ValueError("Duplicate outputs detected")

    return results

if __name__ == "__main__":
    results = test_full_system()
    print(json.dumps(results, indent=2))
    print("\nAll integration tests: PASS")