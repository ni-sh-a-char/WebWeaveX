"""
WebWeaveX Output Engine (Phase 14)

Purpose:
    Convert execution results into:
    - Human-readable answers
    - Structured machine output
    - UI-ready schema
"""

import hashlib
from typing import Dict, Any


def build_human_readable(exec_type: str, result: dict) -> str:
    """Build human-readable output."""
    if exec_type == "code":
        files = result.get("files", [])
        project_type = result.get("project_type", "unknown")
        return f"Generated {len(files)} code files for a {project_type} project."

    if exec_type == "data":
        summary = result.get("summary", "")
        points = result.get("key_points", [])
        combined = summary + " " + " ".join(points[:2])
        return combined.strip()[:300]

    if exec_type == "text":
        return str(result).strip()[:300]

    return "No meaningful result found."


def build_structured(exec_type: str, result: dict) -> dict:
    """Build structured output."""
    if not isinstance(result, dict):
        if exec_type == "text":
            return {"text": str(result)}
        return {}

    if exec_type == "code":
        return {
            "files": result.get("files", []),
            "project_type": result.get("project_type", "unknown"),
            "entry_points": result.get("entry_points", []),
            "dependencies": result.get("dependencies", [])
        }

    if exec_type == "data":
        return result

    if exec_type == "text":
        return {"text": result}

    return {}


def build_ui_schema(exec_type: str, result: dict) -> dict:
    """Build UI-ready schema."""
    components = []

    if exec_type == "code":
        for f in result.get("files", []):
            components.append({
                "type": "code_block",
                "title": f.get("path", ""),
                "content": f.get("content", "")
            })

    elif exec_type == "data":
        components.append({
            "type": "summary",
            "content": result.get("summary", "")
        })

        for p in result.get("key_points", []):
            components.append({
                "type": "bullet",
                "content": p
            })

    elif exec_type == "text":
        components.append({
            "type": "text",
            "content": str(result)
        })

    return {
        "type": "ui_render",
        "components": components
    }


def adjust_confidence(base_conf: float, top_result: dict) -> float:
    """Adjust confidence based on recovered elements."""
    if not isinstance(top_result, dict):
        return float(base_conf)

    recovered = top_result.get("recovered", {})
    count = recovered.get("recovered_count", 0)

    boost = min(count * 0.05, 0.2)

    return min(base_conf + boost, 1.0)


def fallback_output() -> dict:
    """Fallback when no valid output."""
    return {
        "human_readable": "No result",
        "structured_data": {},
        "ui_schema": {"type": "empty", "components": []},
        "confidence": 0.0,
        "source": "unknown",
        "reconstructed_project": [],
        "version": "v1_phase_14"
    }


def build_output(execution_result: dict, top_result: dict) -> dict:
    """Main output builder."""
    if not isinstance(execution_result, dict):
        return fallback_output()

    exec_type = execution_result.get("execution_type", "fallback")
    result = execution_result.get("result", {})

    base_conf = execution_result.get("confidence", 0.0)
    confidence = adjust_confidence(base_conf, top_result)

    source = top_result.get("source", "unknown")
    original_input = top_result.get("original_input", "")
    input_signature = top_result.get("input_signature", "")

    if not input_signature:
        input_signature = execution_result.get("input_signature", "")

    if not original_input and "queries" in top_result:
        qbundle = top_result.get("queries", {})
        original_input = qbundle.get("original_input", "")
        if not input_signature:
            input_signature = qbundle.get("input_signature", "")

    human = build_human_readable(exec_type, result)

    if not human or len(human) < 10:
        human = f"Result for {source}: found matching content"

    structured = build_structured(exec_type, result)

    if not structured or structured == {}:
        structured = {
            "query_source": source,
            "has_content": len(top_result.get("html", "")) > 0
        }

    if original_input:
        structured["input_echo"] = original_input[:50]

    if input_signature:
        structured["input_signature"] = input_signature

    ui = build_ui_schema(exec_type, result)

    if not ui.get("components"):
        ui = {"type": "ui_render", "components": [{"type": "text", "content": human}]}

    return {
        "human_readable": human or "",
        "structured_data": structured or {},
        "ui_schema": ui or {"type": "empty", "components": []},
        "confidence": float(confidence),
        "source": source or "unknown",
        "reconstructed_project": structured.get("files", []),
        "version": "v1_phase_14"
    }


def validate_output_engine() -> bool:
    """Validate output engine."""
    test = {
        "execution_type": "data",
        "result": {"summary": "test", "key_points": ["a", "b"]},
        "confidence": 0.8
    }

    out = build_output(test, {"source": "test"})

    assert "human_readable" in out
    assert "structured_data" in out
    assert "ui_schema" in out
    assert "confidence" in out
    assert "source" in out
    assert "reconstructed_project" in out
    assert "version" in out

    for key in out:
        if out[key] is None:
            raise AssertionError(f"None value in key: {key}")

    return True


if __name__ == "__main__":
    print("OUTPUT ENGINE:", "PASS" if validate_output_engine() else "FAIL")