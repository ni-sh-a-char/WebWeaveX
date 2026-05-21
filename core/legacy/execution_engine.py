"""
WebWeaveX Execution Engine (Phase 9)

Purpose:
    Convert ranked results into real usable output
    Deterministic, fail-safe execution

STRICT RULES:
    No eval/exec without sandbox
    No filesystem writes
    No network calls
    No randomness
"""

from typing import Dict, Any

from core.code_reconstruction import reconstruct_project


# ---------------------------
# EXECUTION TYPE DETECTION
# ---------------------------

def detect_execution_type(top_result: dict) -> str:
    base = top_result.get("base", {})
    metadata = base.get("metadata", {})

    code_blocks = metadata.get("code_blocks", 0)
    text_len = metadata.get("text_length", 0)

    if code_blocks > 0:
        return "code"

    if text_len > 1000:
        return "data"

    if text_len > 100:
        return "text"

    return "fallback"


# ---------------------------

# ---------------------------
# UI GENERATION
# ---------------------------

def build_ui(top_result: dict) -> dict:
    base = top_result.get("base", {})

    text = base.get("text", "")
    code = base.get("code", [])

    components = []

    if text:
        components.append({
            "type": "text",
            "content": text[:500]
        })

    for block in code:
        components.append({
            "type": "code",
            "content": block.get("content", "")
        })

    return {
        "type": "dynamic_ui",
        "components": components
    }


# ---------------------------
# DATA STRUCTURING
# ---------------------------

def structure_data(text: str) -> dict:
    if not text:
        return {}

    sentences = text.split(".")[:5]

    return {
        "summary": text[:200],
        "key_points": [s.strip() for s in sentences if s.strip()]
    }


# ---------------------------
# TEXT MODE
# ---------------------------

def process_text(text: str) -> str:
    return text.strip() if isinstance(text, str) else ""


def fallback(top_result: dict) -> dict:
    base = top_result.get("base", {})
    text = base.get("text", "")

    return {
        "execution_type": "fallback",
        "result": text[:300] if text else "",
        "confidence": 0.3,
        "fallback_used": True,
        "input_signature": top_result.get("input_signature", "") or global_input_signature,
        "version": "v1_phase_11"
    }


# ---------------------------
# MAIN EXECUTION
# ---------------------------

def execute_result(top_result: dict, global_input_signature: str = "") -> dict:
    if not isinstance(top_result, dict):
        return fallback({})

    exec_type = detect_execution_type(top_result)

    base = top_result.get("base", {})
    text = base.get("text", "")
    code_blocks = base.get("code", [])

    # CODE EXECUTION - use real CRE
    if exec_type == "code":
        url = top_result.get("url", "")

        html = top_result.get("html", "") or base.get("text", "")

        reconstructed = reconstruct_project(html, url, deterministic=True)

        if not reconstructed:
            reconstructed = {
                "files": [],
                "project_type": "unknown",
                "confidence": 0.0,
                "entry_points": [],
                "dependencies": []
            }

        return {
            "execution_type": "code",
            "result": reconstructed,
            "confidence": 0.9,
            "fallback_used": False,
            "input_signature": top_result.get("input_signature", "") or global_input_signature,
            "version": "v1_phase_11"
        }

    # DATA MODE
    if exec_type == "data":
        return {
            "execution_type": "data",
            "result": structure_data(text),
            "confidence": 0.8,
            "fallback_used": False,
            "input_signature": top_result.get("input_signature", "") or global_input_signature,
            "version": "v1_phase_11"
        }

    # TEXT MODE
    if exec_type == "text":
        return {
            "execution_type": "text",
            "result": text,
            "confidence": 0.7,
            "fallback_used": False,
            "input_signature": top_result.get("input_signature", "") or global_input_signature,
            "version": "v1_phase_11"
        }

    return fallback(top_result)


# ---------------------------
# VALIDATION
# ---------------------------

def validate_execution_engine() -> bool:
    test_input = {
        "base": {
            "text": "test output",
            "code": [],
            "metadata": {"text_length": 100, "code_blocks": 0}
        }
    }

    result = execute_result(test_input)

    if not isinstance(result, dict):
        raise RuntimeError("Invalid output")

    required = ["execution_type", "result", "confidence", "fallback_used", "version"]
    for key in required:
        if key not in result:
            raise RuntimeError(f"Missing key: {key}")

    return True


if __name__ == "__main__":
    ok = validate_execution_engine()
    print("EXECUTION ENGINE VALIDATION:", "PASS" if ok else "FAIL")