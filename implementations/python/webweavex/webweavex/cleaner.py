"""Text cleaner for WebWeaveX."""

import re
from typing import Optional, Dict, Any

from .utils import get_spec


class Cleaner:
    """Text cleaner that normalizes and strips text."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the cleaner."""
        self.spec = config or get_spec()
        self.clean_config = self.spec.get("clean", {})
        self.normalize_whitespace = self.clean_config.get("normalize_whitespace", True)
        self.strip = self.clean_config.get("strip", True)
        self.remove_empty_lines = self.clean_config.get("remove_empty_lines", True)

    def clean(self, text: str) -> str:
        """Clean text according to configuration."""
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
        """Normalize whitespace."""
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n[ \t]+', '\n', text)
        text = re.sub(r'[ \v]+', ' ', text)
        return text

    def _remove_empty_lines(self, text: str) -> str:
        """Remove empty lines."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
