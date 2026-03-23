"""WebWeaveX Pipeline - Core processing pipeline."""

from typing import Dict, Any, List, Optional

from .config import DEFAULT_CONFIG, get_config
from .fetcher import Fetcher
from .parser import Parser
from .cleaner import Cleaner
from .chunker import Chunker
from .entities import EntityEngine
from .relations import RelationEngine
from .graph import GraphEngine
from .insights import InsightsEngine
from .schema import WXPResult, Entity, Graph, Chunk


class Pipeline:
    """WebWeaveX processing pipeline: fetch -> parse -> clean -> chunk -> entities -> relations -> graph -> insights"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = get_config(config)
        self.fetcher = Fetcher(self.config)
        self.parser = Parser(self.config)
        self.cleaner = Cleaner(self.config)
        self.chunker = Chunker(self.config)
        self.entity_engine = EntityEngine(self.config)
        self.relation_engine = RelationEngine(self.config)
        self.graph_engine = GraphEngine(self.config)
        self.insights_engine = InsightsEngine(self.config)

    def _process(self, text: str, url: str = "") -> WXPResult:
        """Internal: Run full extraction pipeline on text."""
        cleaned_text = self.cleaner.clean(text)
        chunks = self.chunker.chunk(cleaned_text)
        entities = self.entity_engine.extract(cleaned_text)
        relations = self.relation_engine.extract(entities, chunks)
        graph = self.graph_engine.build(entities)
        insights = self.insights_engine.compute(entities, chunks, cleaned_text)

        return WXPResult(
            url=url,
            title="",
            text=cleaned_text,
            chunks=chunks,
            entities=entities,
            relations=relations,
            graph=graph,
            insights=insights
        )

    def crawl(self, url: str) -> WXPResult:
        """Execute full pipeline on URL."""
        html = self.fetcher.fetch(url)
        title = self.parser.extract_title(html)
        text = self.parser.parse(html, url)
        cleaned_text = self.cleaner.clean(text)
        chunks = self.chunker.chunk(cleaned_text)
        entities = self.entity_engine.extract(cleaned_text)
        relations = self.relation_engine.extract(entities, chunks)
        graph = self.graph_engine.build(entities)
        insights = self.insights_engine.compute(entities, chunks, cleaned_text)

        return WXPResult(
            url=url,
            title=title,
            text=cleaned_text,
            chunks=chunks,
            entities=entities,
            relations=relations,
            graph=graph,
            insights=insights
        )

    def extract_from_html(self, html: str, url: str = "") -> WXPResult:
        """Extract from HTML without fetching."""
        title = self.parser.extract_title(html)
        text = self.parser.parse(html, url)
        cleaned_text = self.cleaner.clean(text)
        chunks = self.chunker.chunk(cleaned_text)
        entities = self.entity_engine.extract(cleaned_text)
        relations = self.relation_engine.extract(entities, chunks)
        graph = self.graph_engine.build(entities)
        insights = self.insights_engine.compute(entities, chunks, cleaned_text)

        return WXPResult(
            url=url,
            title=title,
            text=cleaned_text,
            chunks=chunks,
            entities=entities,
            relations=relations,
            graph=graph,
            insights=insights
        )

    def extract_from_text(self, text: str) -> WXPResult:
        """Extract from raw text."""
        return self._process(text)

    def clean(self, text: str) -> str:
        """Clean text."""
        return self.cleaner.clean(text)

    def chunk(self, text: str) -> List[Chunk]:
        """Chunk text."""
        cleaned = self.cleaner.clean(text)
        return self.chunker.chunk(cleaned)

    def entities(self, text: str) -> List[Entity]:
        """Extract entities from text."""
        cleaned = self.cleaner.clean(text)
        return self.entity_engine.extract(cleaned)

    def graph(self, text: str) -> Graph:
        """Build entity graph from text."""
        cleaned = self.cleaner.clean(text)
        entities = self.entity_engine.extract(cleaned)
        return self.graph_engine.build(entities)

    def rag(self, url: str, query: str) -> Dict[str, Any]:
        """RAG: retrieve relevant chunks and answer query."""
        result = self.crawl(url)
        relevant_chunks = [
            {"text": c.text, "index": c.index}
            for c in result.chunks
            if any(word.lower() in c.text.lower() for word in query.split())
        ]
        return {
            "url": url,
            "query": query,
            "chunks": relevant_chunks,
            "total_chunks": len(result.chunks),
        }

    def compare(self, url1: str, url2: str) -> Dict[str, Any]:
        """Compare two URLs and return differences."""
        return self.diff(url1, url2)

    def weave(self, urls: List[str]) -> Dict[str, Any]:
        """Combine content from multiple URLs."""
        results = []
        all_entities = []
        for url in urls:
            try:
                result = self.crawl(url)
                results.append({
                    "url": url,
                    "title": result.meta.title,
                    "entity_count": len(result.entities),
                    "entities": [{"type": e.type, "value": e.value} for e in result.entities],
                })
                all_entities.extend(result.entities)
            except Exception:
                results.append({"url": url, "error": "Failed to fetch"})
        return {
            "urls": urls,
            "results": results,
            "total_entities": len(all_entities),
        }

    def diff(self, url1: str, url2: str) -> Dict[str, Any]:
        """Compare two URLs and return differences."""
        result1 = self.crawl(url1)
        result2 = self.crawl(url2)

        entities1 = {(e.type, e.value) for e in result1.entities}
        entities2 = {(e.type, e.value) for e in result2.entities}

        common = entities1 & entities2
        only_in_1 = entities1 - entities2
        only_in_2 = entities2 - entities1

        return {
            "url1": url1,
            "url2": url2,
            "common_count": len(common),
            "only_in_url1_count": len(only_in_1),
            "only_in_url2_count": len(only_in_2),
            "url1_entities": list(only_in_1),
            "url2_entities": list(only_in_2),
        }
