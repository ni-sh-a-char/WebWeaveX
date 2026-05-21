"""Production-safe deterministic logger config."""

from __future__ import annotations

import logging
import os
import time
import hashlib


def get_logger(name: str = "webweavex") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    level = os.getenv("WEBWEAVEX_LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, level, logging.INFO))
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def new_trace_id(seed: str = "") -> str:
    """
    Deterministic trace id helper.
    Keep this out of canonical extraction payloads if runtime timing differs.
    """
    value = seed or "webweavex-trace"
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()[:32]


def timed_block() -> float:
    return time.perf_counter()


def elapsed_ms(start: float) -> float:
    return round((time.perf_counter() - start) * 1000.0, 3)
