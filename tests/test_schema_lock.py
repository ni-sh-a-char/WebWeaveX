import sys
sys.path.insert(0, '.')
from webweavex import extract


EXPECTED_KEYS = [
    "content",
    "intelligence",
    "knowledge",
    "ai",
    "meta",
    "knowledge_graph",
    "reconstructed_project"
]


def test_schema_keys():
    """Test that all expected keys are present."""
    r = extract("https://example.com")
    keys = sorted(r.keys())
    expected = sorted(EXPECTED_KEYS)
    assert keys == expected, f"Schema mismatch: {keys} != {expected}"


def test_schema_preserve():
    """Test schema is preserved across different inputs."""
    test_cases = [
        {"deterministic_mode": True},
        {"deterministic_mode": False},
        {"input_type": "code", "code": "def test(): return 1"}
    ]
    
    for opts in test_cases:
        r = extract("https://example.com", options=opts)
        keys = sorted(r.keys())
        expected = sorted(EXPECTED_KEYS)
        assert keys == expected, f"Schema mismatch for {opts}: {keys}"


if __name__ == "__main__":
    test_schema_keys()
    print("Schema lock test: PASS")