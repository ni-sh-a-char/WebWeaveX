"""
WebWeaveX Cache Engine (Phase 14)

Purpose:
    - Deterministic hybrid cache
    - Memory + disk
    - Hash-based lookup
    - Integrity signature verification
"""

import os
import json
import hashlib
from typing import Dict, Any, Optional


_MEMORY_CACHE: Dict[str, dict] = {}

CACHE_DIR = "cache_store"


def generate_cache_signature(data: dict) -> str:
    """Generate SHA-256 signature for cache integrity."""
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()


def _ensure_cache_dir():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def generate_cache_key(user_input: str) -> str:
    if not isinstance(user_input, str):
        user_input = str(user_input)

    return hashlib.sha256(user_input.encode()).hexdigest()


def _get_cache_path(key: str) -> str:
    return os.path.join(CACHE_DIR, f"{key}.json")


def load_cache(key: str) -> Optional[dict]:
    import copy

    if key in _MEMORY_CACHE:
        return copy.deepcopy(_MEMORY_CACHE[key])

    _ensure_cache_dir()
    path = _get_cache_path(key)

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, dict):
                return None

            sig = data.get("_signature")
            if not sig:
                return None

            check_data = {k: v for k, v in data.items() if k != "_signature"}
            if sig != generate_cache_signature(check_data):
                return None

            required_keys = {
                "human_readable",
                "structured_data",
                "ui_schema",
                "confidence",
                "source",
                "reconstructed_project",
                "version"
            }

            if not all(k in data for k in required_keys):
                return None

            _MEMORY_CACHE[key] = data
            return data
    except Exception:
        return None


def should_cache(data: dict) -> bool:
    if not isinstance(data, dict):
        return False

    confidence = data.get("confidence", 0.0)

    if not isinstance(confidence, (int, float)):
        return False

    if confidence < 0.5:
        return False

    required_keys = {
        "human_readable",
        "structured_data",
        "ui_schema",
        "confidence",
        "source",
        "reconstructed_project",
        "version"
    }

    if not all(k in data for k in required_keys):
        return False

    return True


def save_cache(key: str, data: dict):
    if not isinstance(data, dict):
        return

    if not should_cache(data):
        return

    _ensure_cache_dir()
    path = _get_cache_path(key)

    try:
        import copy
        data_copy = copy.deepcopy(data)

        sig_data = {k: v for k, v in data_copy.items() if k != "_signature"}
        data_copy["_signature"] = generate_cache_signature(sig_data)

        temp_path = path + ".tmp"

        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data_copy, f, ensure_ascii=False, sort_keys=True)

        os.replace(temp_path, path)

        _MEMORY_CACHE[key] = copy.deepcopy(data_copy)
    except Exception:
        return


def clear_cache(key: str = None):
    if key:
        if key in _MEMORY_CACHE:
            del _MEMORY_CACHE[key]
        path = _get_cache_path(key)
        if os.path.exists(path):
            os.remove(path)
    else:
        _MEMORY_CACHE.clear()
        if os.path.exists(CACHE_DIR):
            import shutil
            shutil.rmtree(CACHE_DIR)


def validate_cache_engine() -> bool:
    test_input = "test_query"
    key = generate_cache_key(test_input)

    test_data = {
        "human_readable": "test",
        "structured_data": {"test": True},
        "ui_schema": {"type": "test"},
        "confidence": 0.8,
        "source": "test",
        "reconstructed_project": [],
        "version": "v1"
    }

    clear_cache(key)

    save_cache(key, test_data)
    loaded = load_cache(key)

    if not loaded:
        raise RuntimeError("Cache mismatch")
    check = {k: v for k, v in loaded.items() if k != "_signature"}
    if check != test_data:
        raise RuntimeError("Cache mismatch")

    clear_cache(key)

    return True


if __name__ == "__main__":
    print("CACHE ENGINE:", "PASS" if validate_cache_engine() else "FAIL")