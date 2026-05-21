"""Repository cognition example."""

from webweavex import extract_repository

if __name__ == "__main__":
    result = extract_repository(".", semantic_runtime=False)
    print("bounded:", result.get("bounded", True))
