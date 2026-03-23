"""WebWeaveX Pipeline Tests - Comprehensive testing."""

import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from webweavex import WebWeaveX
from webweavex.schema import WXPResult, Entity, Chunk, Relation, Graph
from webweavex.entities import EntityEngine
from webweavex.chunker import Chunker
from webweavex.cleaner import Cleaner
from webweavex.relations import RelationEngine
from webweavex.graph import GraphEngine
from webweavex.insights import InsightsEngine


class TestWXPResult:
    """Test WXPResult schema."""

    def test_wxpresult_creation(self):
        result = WXPResult(
            url="https://example.com",
            title="Example",
            text="Hello World"
        )
        assert result.meta.url == "https://example.com"
        assert result.meta.title == "Example"
        assert result.content.text == "Hello World"

    def test_wxpresult_to_dict(self):
        result = WXPResult(
            url="https://example.com",
            text="Contact test@example.com"
        )
        result.entities = [Entity(type="email", value="test@example.com")]
        
        data = result.to_dict()
        assert "meta" in data
        assert "content" in data
        assert "entities" in data
        assert data["meta"]["url"] == "https://example.com"

    def test_wxpresult_to_json(self):
        result = WXPResult(url="https://example.com", text="Test")
        json_str = result.to_json()
        parsed = json.loads(json_str)
        assert parsed["meta"]["url"] == "https://example.com"

    def test_wxpresult_deterministic_json(self):
        result1 = WXPResult(
            url="https://example.com",
            text="Contact test@example.com"
        )
        result1.entities = [Entity(type="email", value="test@example.com")]
        
        result2 = WXPResult(
            url="https://example.com",
            text="Contact test@example.com"
        )
        result2.entities = [Entity(type="email", value="test@example.com")]
        
        assert result1.to_json() == result2.to_json()


class TestEntityExtraction:
    """Test entity extraction."""

    def test_extract_emails(self):
        engine = EntityEngine()
        text = "Contact us at support@example.com or sales@example.org"
        entities = engine.extract(text)
        
        emails = [e for e in entities if e.type == "email"]
        assert len(emails) == 2
        assert any(e.value == "support@example.com" for e in emails)
        assert any(e.value == "sales@example.org" for e in emails)

    def test_extract_urls(self):
        engine = EntityEngine()
        text = "Visit https://example.com and http://test.org"
        entities = engine.extract(text)
        
        urls = [e for e in entities if e.type == "url"]
        assert len(urls) == 2

    def test_extract_numbers(self):
        engine = EntityEngine()
        text = "The price is 100 dollars and 50 cents"
        entities = engine.extract(text)
        
        numbers = [e for e in entities if e.type == "number"]
        assert len(numbers) >= 1

    def test_deduplication(self):
        engine = EntityEngine()
        text = "Email test@test.com and again test@test.com"
        entities = engine.extract(text)
        
        emails = [e for e in entities if e.type == "email"]
        values = [e.value for e in emails]
        assert values.count("test@test.com") == 1

    def test_deterministic_order(self):
        engine = EntityEngine()
        text = "b@test.com a@test.com c@test.com"
        entities = engine.extract(text)
        
        emails = [e for e in entities if e.type == "email"]
        values = [e.value for e in emails]
        assert values == sorted(values)


class TestCleaner:
    """Test text cleaning."""

    def test_normalize_whitespace(self):
        cleaner = Cleaner()
        text = "Hello    World\n\n  Test  "
        result = cleaner.clean(text)
        
        assert "  " not in result
        assert "\n\n" not in result

    def test_strip_text(self):
        cleaner = Cleaner()
        text = "   Hello World   "
        result = cleaner.clean(text)
        
        assert result.startswith("Hello")
        assert result.endswith("World")

    def test_remove_empty_lines(self):
        cleaner = Cleaner()
        text = "Line 1\n\n\nLine 2"
        result = cleaner.clean(text)
        
        lines = [l for l in result.split('\n') if l.strip()]
        assert len(lines) == 2


class TestChunker:
    """Test text chunking."""

    def test_basic_chunking(self):
        chunker = Chunker()
        text = "A" * 1000
        chunks = chunker.chunk(text)
        
        assert len(chunks) > 1
        assert all(c.index >= 0 for c in chunks)

    def test_overlap(self):
        chunker = Chunker({"chunking": {"size": 100, "overlap": 20}})
        text = "A" * 200
        chunks = chunker.chunk(text)
        
        if len(chunks) >= 2:
            overlap_text = chunks[1].text[:20]
            assert overlap_text == "A" * 20

    def test_chunk_metadata(self):
        chunker = Chunker()
        text = "Hello World Test"
        chunks = chunker.chunk(text)
        
        assert chunks[0].index == 0
        assert chunks[0].start == 0


class TestRelations:
    """Test relation extraction."""

    def test_extract_relations(self):
        engine = RelationEngine()
        entities = [
            Entity(type="email", value="test@test.com"),
            Entity(type="url", value="https://example.com"),
        ]
        chunks = [Chunk(text="Email test@test.com visit https://example.com", index=0, start=0, end=50)]
        
        relations = engine.extract(entities, chunks)
        
        assert len(relations) >= 1
        assert all(isinstance(r, Relation) for r in relations)


class TestGraphEngine:
    """Test graph building."""

    def test_build_empty_graph(self):
        engine = GraphEngine()
        result = engine.build([])
        
        assert result.nodes == []
        assert result.edges == []

    def test_build_graph(self):
        engine = GraphEngine()
        entities = [
            Entity(type="email", value="test@test.com"),
            Entity(type="url", value="https://example.com"),
        ]
        result = engine.build(entities)
        
        assert len(result.nodes) == 2
        assert len(result.edges) == 1

    def test_deterministic_order(self):
        engine = GraphEngine()
        entities = [
            Entity(type="url", value="https://z.com"),
            Entity(type="email", value="a@test.com"),
        ]
        result = engine.build(entities)
        
        node_types = [n.type for n in result.nodes]
        assert node_types == sorted(node_types)


class TestInsights:
    """Test insights computation."""

    def test_compute_insights(self):
        engine = InsightsEngine()
        entities = [
            Entity(type="email", value="test@test.com"),
            Entity(type="email", value="a@test.com"),
            Entity(type="url", value="https://example.com"),
        ]
        chunks = [Chunk(text="test", index=0, start=0, end=4)]
        
        insights = engine.compute(entities, chunks, "test text")
        
        assert insights.stats["total_entities"] == 3
        assert insights.stats["total_chunks"] == 1


class TestClientAPI:
    """Test client API."""

    def test_client_initialization(self):
        wx = WebWeaveX()
        assert wx.pipeline is not None

    def test_clean_method(self):
        wx = WebWeaveX()
        result = wx.clean("  Hello    World  ")
        assert result == "Hello World"

    def test_chunk_method(self):
        wx = WebWeaveX()
        chunks = wx.chunk("A" * 1000)
        assert len(chunks) > 0

    def test_entities_method(self):
        wx = WebWeaveX()
        entities = wx.entities("Contact test@test.com")
        assert len(entities) > 0

    def test_graph_method(self):
        wx = WebWeaveX()
        result = wx.graph("Email test@test.com")
        assert "nodes" in result
        assert "edges" in result


class TestDeterminism:
    """Test deterministic output."""

    def test_entities_deterministic(self):
        engine = EntityEngine()
        text = "test@test.com a@test.com b@test.com c@test.com"
        
        run1 = engine.extract(text)
        run2 = engine.extract(text)
        
        assert [e.to_dict() for e in run1] == [e.to_dict() for e in run2]

    def test_graph_deterministic(self):
        engine = GraphEngine()
        entities = [
            Entity(type="email", value="c@test.com"),
            Entity(type="email", value="a@test.com"),
            Entity(type="email", value="b@test.com"),
        ]
        
        run1 = engine.build(entities)
        run2 = engine.build(entities)
        
        assert run1.to_json() == run2.to_json()

    def test_chunk_deterministic(self):
        chunker = Chunker()
        text = "A" * 1000
        
        run1 = chunker.chunk(text)
        run2 = chunker.chunk(text)
        
        assert [c.to_dict() for c in run1] == [c.to_dict() for c in run2]

    def test_result_deterministic(self):
        result1 = WXPResult(
            url="https://example.com",
            text="Contact test@example.com"
        )
        result1.entities = [Entity(type="email", value="test@example.com")]
        result1.relations = [Relation(source="email:test@example.com", target="url:example.com")]
        
        result2 = WXPResult(
            url="https://example.com",
            text="Contact test@example.com"
        )
        result2.entities = [Entity(type="email", value="test@example.com")]
        result2.relations = [Relation(source="email:test@example.com", target="url:example.com")]
        
        assert result1.to_json() == result2.to_json()


class TestAgentTools:
    """Test agent system."""

    def test_agent_task_crawl(self):
        wx = WebWeaveX()
        result = wx.pipeline.extract_text("Contact test@example.com")
        
        assert result is not None
        assert result.content is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
