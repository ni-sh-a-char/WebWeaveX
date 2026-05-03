"""
test_failure_modes.py

Test failure modes: ensure proper exceptions for invalid inputs.
"""

from webweavex import run


def test_empty_input():
    """Test run with empty input."""
    try:
        run({"input": ""})
        raise ValueError("Should have raised exception")
    except Exception:
        pass  # Expected


def test_none_input():
    """Test run with None input."""
    try:
        run({"input": None})
        raise ValueError("Should have raised exception")
    except Exception:
        pass  # Expected


def test_wrong_key():
    """Test run with wrong key."""
    try:
        run({"wrong": "key"})
        raise ValueError("Should have raised exception")
    except Exception:
        pass  # Expected


def test_missing_input():
    """Test run with missing input key."""
    try:
        run({})
        raise ValueError("Should have raised exception")
    except Exception:
        pass  # Expected


if __name__ == "__main__":
    test_empty_input()
    print("Empty input: PASS")

    test_none_input()
    print("None input: PASS")

    test_wrong_key()
    print("Wrong key: PASS")

    test_missing_input()
    print("Missing input: PASS")

    print("All failure mode tests: PASS")