"""
WebWeaveX API Configuration V7
"""

from core.version import ENGINE_VERSION

STRICT_CRE_DEFAULT = False

MAX_INPUT_LENGTH = 1000

SUPPORTED_MODES = ["compiler"]

API_VERSION = ENGINE_VERSION

DEFAULT_FALLBACK = {
    "structured_data": {},
    "confidence": 0.0,
    "source": "fallback",
    "version": ENGINE_VERSION
}