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
from .schema import WXPResult


class Pipeline:
    """WebWeaveX processing pipeline: fetch → parse → clean → chunk → entities → relations → graph → insights"""

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

    def extract_text(self, text: str) -> WXPResult:
        """Extract from raw text."""
        cleaned_text = self.cleaner.clean(text)
        chunks = self.chunker.chunk(cleaned_text)
        entities = self.entity_engine.extract(cleaned_text)
        relations = self.relation_engine.extract(entities, chunks)
        graph = self.graph_engine.build(entities)
        insights = self.insights_engine.compute(entities, chunks, cleaned_text)

        return WXPResult(
            text=cleaned_text,
            chunks=chunks,
            entities=entities,
            relations=relations,
            graph=graph,
            insights=insights
        )

    def compare(self, urls: List[str]) -> Dict[str, Any]:
        """Compare multiple URLs."""
        results = []
        for url in urls:
            result = self.crawl(url)
            results.append({
                "url": url,
                "entities": result.entities,
                "entity_count": len(result.entities),
            })

        all_entities = []
        for r in results:
            all_entities.extend(r["entities"])

        common_types = {}
        if len(results) >= 2:
            first_entities = set((e.type, e.value) for e in results[0]["entities"])
            for r in results[1:]:
                first_entities &= set((e.type, e.value) for e in r["entities"])
            common_types = {"count": len(first_entities)}

        return {
            "urls": sorted(urls),
            "results": results,
            "common_entity_count": common_types.get("count", 0),
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
        }
