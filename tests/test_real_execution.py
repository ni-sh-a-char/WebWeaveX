"""
test_real_execution.py

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

def test_real_execution():
    results = []
    hashes = []

    for inp in TEST_INPUTS:
        result = run({"input": inp})

        # Validate schema
        required_keys = ["human_readable", "structured_data", "ui_schema", "confidence", "source", "reconstructed_project", "version"]
        assert len(result) == 7
        for key in required_keys:
            assert key in result

        # No None values
        for v in result.values():
            assert v is not None

        # human_readable meaningful
        assert isinstance(result["human_readable"], str)
        assert len(result["human_readable"]) > 10

        # ui_schema has components
        assert "components" in result["ui_schema"]
        assert len(result["ui_schema"]["components"]) > 0

        # structured_data not empty
        print(f"Input: {inp}, structured_data: {result['structured_data']}")
        if inp == "todo app with login":
            print("Full result:", result)
        assert result["structured_data"]

        h = hashlib.sha256(str(result).encode()).hexdigest()
        hashes.append(h)
        results.append(result)

    # All hashes different
    assert len(set(hashes)) == len(hashes)

    return results

if __name__ == "__main__":
    results = test_real_execution()
    print("All tests passed!")
    print(json.dumps(results, indent=2))