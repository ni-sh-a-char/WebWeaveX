"""WebWeaveX Cleaner - Text cleaning and normalization."""

import re
from typing import Optional, Dict, Any

from .config import DEFAULT_CONFIG


class Cleaner:
    """Text cleaner with deterministic output."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        self.clean_config = cfg.get("clean", DEFAULT_CONFIG["clean"])
        self.normalize_whitespace = self.clean_config.get("normalize_whitespace", True)
        self.strip = self.clean_config.get("strip", True)
        self.remove_empty_lines = self.clean_config.get("remove_empty_lines", True)

    def clean(self, text: str) -> str:
        """Clean text deterministically."""
        if not text:
            return ""

        if self.normalize_whitespace:
            text = self._normalize_whitespace(text)

        if self.strip:
            text = text.strip()

        if self.remove_empty_lines:
            text = self._remove_empty_lines(text)

        return text

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize all whitespace to single spaces."""
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n[ \t]+', '\n', text)
        text = re.sub(r'[\v]+', ' ', text)
        text = re.sub(r'\r\n', '\n', text)
        return text

    def _remove_empty_lines(self, text: str) -> str:
        """Remove empty lines while preserving structure."""
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]
        return '\n'.join(lines)
