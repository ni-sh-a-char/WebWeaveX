"""WebWeaveX Client - Main API."""

from typing import Dict, Any, List, Optional

from .config import DEFAULT_CONFIG, get_config
from .pipeline import Pipeline
from .schema import WXPResult


class WebWeaveX:
    """Main WebWeaveX client API."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = get_config(config)
        self._pipeline = None

    @property
    def pipeline(self) -> Pipeline:
        if self._pipeline is None:
            self._pipeline = Pipeline(self.config)
        return self._pipeline

    def crawl(self, url: str) -> WXPResult:
        """Crawl a URL and return WXPResult."""
        return self.pipeline.crawl(url)

    def extract(self, html: str, url: str = "") -> WXPResult:
        """Extract from HTML."""
        return self.pipeline.extract_from_html(html, url)

    def extract_text(self, text: str) -> WXPResult:
        """Extract from raw text."""
        return self.pipeline.extract_text(text)

    def clean(self, text: str) -> str:
        """Clean text."""
        from .cleaner import Cleaner
        cleaner = Cleaner(self.config)
        return cleaner.clean(text)

    def chunk(self, text: str) -> List:
        """Chunk text."""
        from .chunker import Chunker
        from .schema import Chunk
        chunker = Chunker(self.config)
        return chunker.chunk(text)

    def entities(self, text: str) -> List:
        """Extract entities from text."""
        from .entities import EntityEngine
        engine = EntityEngine(self.config)
        return engine.extract(text)

    def relations(self, text: str) -> List:
        """Extract relations from text."""
        from .relations import RelationEngine
        from .entities import EntityEngine
        from .chunker import Chunker
        engine = RelationEngine(self.config)
        entity_engine = EntityEngine(self.config)
        chunker = Chunker(self.config)
        entities = entity_engine.extract(text)
        chunks = chunker.chunk(text)
        return engine.extract(entities, chunks)

    def graph(self, text: str) -> Dict:
        """Build graph from text."""
        from .graph import GraphEngine
        from .entities import EntityEngine
        engine = GraphEngine(self.config)
        entity_engine = EntityEngine(self.config)
        entities = entity_engine.extract(text)
        return engine.build(entities).to_dict()

    def compare(self, urls: List[str]) -> Dict[str, Any]:
        """Compare multiple URLs."""
        return self.pipeline.compare(urls)

    def diff(self, url1: str, url2: str) -> Dict[str, Any]:
        """Compare two URLs."""
        return self.pipeline.diff(url1, url2)

    def ask(self, url: str, prompt: str, provider: Optional[str] = None) -> str:
        """Ask a question about URL content using AI."""
        from .ai import AIEngine
        result = self.crawl(url)
        context = result.content.text[:4000] if result.content else ""
        full_prompt = f"Context from {url}:\n{context}\n\nQuestion: {prompt}"
        
        ai = AIEngine(self.config)
        return ai.call_model(full_prompt, provider=provider)

    def rag(self, url: str, query: str) -> Dict[str, Any]:
        """Retrieve relevant chunks for a query."""
        result = self.crawl(url)
        query_lower = query.lower()
        relevant_chunks = []

        for chunk in result.chunks:
            if any(word in chunk.text.lower() for word in query_lower.split()):
                relevant_chunks.append(chunk)

        return {
            "url": url,
            "query": query,
            "chunks": [c.to_dict() for c in relevant_chunks[:5]],
            "entities": [e.to_dict() for e in result.entities],
        }

    def monitor(self, url: str, interval: int = 60) -> Dict[str, Any]:
        """Monitor URL for changes (returns current state, no background loop)."""
        current = self.crawl(url)
        return {
            "url": url,
            "text_length": len(current.content.text) if current.content else 0,
            "entity_count": len(current.entities),
            "chunk_count": len(current.chunks),
            "status": "fetched",
        }
