"""Entity extraction engine for WebWeaveX."""

import re
from typing import List, Set, Dict, Any, Optional

from .schema import Entity
from .utils import get_spec


class EntityEngine:
    """Regex-based entity extraction engine."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the entity engine."""
        self.spec = config or get_spec()
        self.patterns = self.spec.get("entity_patterns", {})
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns."""
        compiled = {}
        for name, config in self.patterns.items():
            regex = config.get("regex", "")
            try:
                compiled[name] = re.compile(regex)
            except re.error:
                pass
        return compiled

    def extract(self, text: str) -> List[Entity]:
        """Extract entities from text."""
        if not text:
            return []

        entities: Set[Entity] = set()

        for name, pattern in self._compiled_patterns.items():
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ""
                entity = Entity(type=name, value=str(match).strip())
                if entity.value:
                    entities.add(entity)

        result = list(entities)
        result.sort(key=lambda e: (e.type, e.value))

        return result

    def extract_by_type(self, text: str, entity_type: str) -> List[Entity]:
        """Extract entities of a specific type."""
        if not text or entity_type not in self._compiled_patterns:
            return []

        pattern = self._compiled_patterns[entity_type]
        matches = pattern.findall(text)
        
        entities = []
        seen = set()
        
        for match in matches:
            if isinstance(match, tuple):
                match = match[0] if match else ""
            value = str(match).strip()
            if value and value not in seen:
                entities.append(Entity(type=entity_type, value=value))
                seen.add(value)

        entities.sort(key=lambda e: e.value)
        return entities
