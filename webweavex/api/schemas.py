"""
WebWeaveX API Schemas V7

Minimal validation for pure pipeline.
"""

from typing import Dict, Any


def validate_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate request input."""
    if not isinstance(data, dict):
        raise ValueError("Invalid request format")
    
    user_input = data.get("input")
    
    if not isinstance(user_input, str):
        raise ValueError("input must be string")
    
    user_input = user_input.strip()
    
    if not user_input:
        raise ValueError("input cannot be empty")
    
    mode = data.get("mode", "compiler")
    
    if mode not in ["compiler"]:
        mode = "compiler"
    
    return {
        "input": user_input,
        "mode": mode
    }


def validate_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate response output."""
    required_keys = {
        "structured_data",
        "confidence",
        "source",
        "version"
    }
    
    if not isinstance(data, dict):
        raise RuntimeError("Invalid pipeline output")
    
    if not all(k in data for k in required_keys):
        raise RuntimeError("Invalid output schema")
    
    for key in required_keys:
        if data.get(key) is None:
            raise RuntimeError(f"None value in {key}")
    
    if not isinstance(data["confidence"], (int, float)):
        raise RuntimeError("Invalid confidence type")
    
    return data


def _empty_fallback() -> Dict[str, Any]:
    """Empty fallback response."""
    return {
        "structured_data": {},
        "confidence": 0.0,
        "source": "fallback",
        "version": "v7"
    }