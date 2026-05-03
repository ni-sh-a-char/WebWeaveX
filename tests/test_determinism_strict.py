"""
test_determinism_strict.py

Test determinism: same input produces identical output.
"""

import json
import hashlib
from webweavex import run


def stable_hash(obj):
    """Create a stable hash of any JSON-serializable object."""
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


def test_same_input_multiple_times():
    """Test that same input produces identical output 5 times."""
    input_data = {"input": "calculator app"}
    results = []
    hashes = []

    for i in range(5):
        result = run(input_data)
        results.append(result)
        h = stable_hash(result)
        hashes.append(h)

    # All hashes should be identical
    if len(set(hashes)) != 1:
        raise ValueError(f"Non-deterministic: hashes differ {hashes}")

    return True


def test_different_inputs_different_outputs():
    """Test that different inputs produce different outputs."""
    inputs = [
        {"input": "calculator app"},
        {"input": "todo app"},
        {"input": "weather app"}
    ]

    hashes = []
    for inp in inputs:
        result = run(inp)
        h = stable_hash(result)
        hashes.append(h)

    # All hashes should be different
    if len(set(hashes)) != len(hashes):
        raise ValueError("Duplicate outputs for different inputs")

    return True


if __name__ == "__main__":
    test_same_input_multiple_times()
    print("Same input determinism: PASS")

    test_different_inputs_different_outputs()
    print("Different inputs differentiation: PASS")