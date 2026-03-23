"""WebWeaveX Entities - Regex-based entity extraction with defaults."""

import re
from typing import List, Set, Dict, Any, Optional

from .config import DEFAULT_CONFIG
from .schema import Entity


class EntityEngine:
    """Regex-based entity extraction with built-in patterns."""

    DEFAULT_PATTERNS = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "url": r"https?://[^\s<>\"']+",
        "number": r"\b\d+(?:\.\d+)?\b",
        "phone": r"\+?[0-9]{1,4}?[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}",
        "capitalized": r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b",
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        patterns_config = cfg.get("entity_patterns", DEFAULT_CONFIG["entity_patterns"])
        self._compiled_patterns: Dict[str, re.Pattern] = {}
        self._load_patterns(patterns_config)

    def _load_patterns(self, patterns_config: Dict[str, Any]) -> None:
        """Load patterns from config."""
        for name, pattern_config in patterns_config.items():
            if isinstance(pattern_config, dict):
                regex = pattern_config.get("regex", "")
            else:
                regex = str(pattern_config)
            
            if regex:
                try:
                    self._compiled_patterns[name] = re.compile(regex)
                except re.error:
                    pass

        for name, pattern in self.DEFAULT_PATTERNS.items():
            if name not in self._compiled_patterns:
                try:
                    self._compiled_patterns[name] = re.compile(pattern)
                except re.error:
                    pass

    def extract(self, text: str) -> List[Entity]:
        """Extract entities deterministically."""
        if not text:
            return []

        seen: Set[str] = set()
        entities: List[Entity] = []

        for name, pattern in sorted(self._compiled_patterns.items()):
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ""
                value = str(match).strip()
                if value and len(value) > 0:
                    key = f"{name}:{value}"
                    if key not in seen:
                        seen.add(key)
                        entities.append(Entity(type=name, value=value))

        return sorted(entities)

    def extract_by_type(self, text: str, entity_type: str) -> List[Entity]:
        """Extract entities of a specific type."""
        if not text or entity_type not in self._compiled_patterns:
            return []

        pattern = self._compiled_patterns[entity_type]
        matches = pattern.findall(text)
        seen: Set[str] = set()
        entities: List[Entity] = []

        for match in matches:
            if isinstance(match, tuple):
                match = match[0] if match else ""
            value = str(match).strip()
            if value and value not in seen:
                seen.add(value)
                entities.append(Entity(type=entity_type, value=value))

        return sorted(entities)

    def get_pattern_names(self) -> List[str]:
        """Get list of pattern names."""
        return sorted(self._compiled_patterns.keys())
