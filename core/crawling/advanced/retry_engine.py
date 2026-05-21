from __future__ import annotations

def next_retry(attempt: int, max_retries: int = 3):
    return attempt + 1 if attempt < max_retries else -1
