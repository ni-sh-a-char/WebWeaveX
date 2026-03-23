"""Text chunker for WebWeaveX."""

from typing import List, Optional, Dict, Any

from .schema import Chunk
from .utils import get_spec


class Chunker:
    """Text chunker with sliding window."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the chunker."""
        self.spec = config or get_spec()
        self.chunking_config = self.spec.get("chunking", {})
        self.chunk_size = self.chunking_config.get("size", 500)
        self.overlap = self.chunking_config.get("overlap", 50)
        self.method = self.chunking_config.get("method", "sliding_window")
        self.preserve_words = self.chunking_config.get("preserve_words", True)

    def chunk(self, text: str) -> List[Chunk]:
        """Chunk text using sliding window method."""
        if not text:
            return []

        chunks = []
        start = 0
        index = 0

        while start < len(text):
            end = start + self.chunk_size

            if self.preserve_words and end < len(text):
                end = self._find_word_boundary(text, end)

            chunk_text = text[start:end]
            if chunk_text.strip():
                chunks.append(Chunk(
                    text=chunk_text,
                    index=index,
                    start=start,
                    end=end
                ))
                index += 1

            start = end - self.overlap
            if start < 0:
                start = 0

        return chunks

    def _find_word_boundary(self, text: str, position: int) -> int:
        """Find the nearest word boundary before position."""
        if position >= len(text):
            return position

        for i in range(position, max(0, position - 50), -1):
            if text[i] in ' \t\n\r':
                return i

        return position
