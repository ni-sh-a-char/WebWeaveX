"""Small Python sample for repository validation."""

import json
from pathlib import Path


def greet(name: str) -> str:
    return f"hello {name}"


if __name__ == "__main__":
    print(greet("webweavex"))
