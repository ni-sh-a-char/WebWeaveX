"""
WebWeaveX API Layer V7

Pure pipeline entry point.
"""

import copy
from typing import Dict, Any

from core.full_pipeline import run_pipeline
from webweavex.api.schemas import validate_request
from webweavex.api.config import STRICT_CRE_DEFAULT, DEFAULT_FALLBACK
from core.version import ENGINE_VERSION

API_VERSION = ENGINE_VERSION


def _fallback_response() -> Dict[str, Any]:
    return copy.deepcopy(DEFAULT_FALLBACK)


def run(data: Dict[str, Any]) -> Dict[str, Any]:
    """Main API entry point."""
    
    req = validate_request(data)
    
    user_input = req["input"]
    mode = req["mode"]
    
    strict_mode = True if mode == "strict" else STRICT_CRE_DEFAULT
    
    try:
        result = run_pipeline(user_input, "compiler")
    except Exception as e:
        if strict_mode:
            raise RuntimeError("Pipeline execution failed") from e
        
        return {
            "structured_data": {"error": str(e)},
            "confidence": 0.0,
            "source": "error",
            "version": API_VERSION
        }
    
    # Add version
    result["version"] = API_VERSION
    
    return result