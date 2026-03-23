"""Tests for WebWeaveX Python implementation."""

import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from webweavex import WebWeaveX
from webweavex.schema import Entity, Chunk, CrawlResult, GraphResult
from webweavex.entities import EntityEngine
from webweavex.cleaner import Cleaner
from webweavex.chunker import Chunker
from webweavex.graph import GraphEngine


class TestEntityExtraction:
    """Test entity extraction."""

    def test_extract_emails(self):
        """Test email extraction."""
        engine = EntityEngine()
        text = "Contact us at support@example.com or sales@example.org"
        entities = engine.extract(text)
        
        emails = [e for e in entities if e.type == "email"]
        assert len(emails) == 2
        assert any(e.value == "support@example.com" for e in emails)
        assert any(e.value == "sales@example.org" for e in emails)

    def test_extract_urls(self):
        """Test URL extraction."""
        engine = EntityEngine()
        text = "Visit https://example.com and http://test.org"
        entities = engine.extract(text)
        
        urls = [e for e in entities if e.type == "url"]
        assert len(urls) == 2
        assert any("example.com" in e.value for e in urls)

    def test_extract_numbers(self):
        """Test number extraction."""
        engine = EntityEngine()
        text = "The price is 100 dollars and 50 cents"
        entities = engine.extract(text)
        
        numbers = [e for e in entities if e.type == "number"]
        assert len(numbers) >= 1
        assert any(e.value == "100" for e in numbers)

    def test_extract_capitalized(self):
        """Test capitalized phrase extraction."""
        engine = EntityEngine()
        text = "Hello World and New York City"
        entities = engine.extract(text)
        
        capitalized = [e for e in entities if e.type == "capitalized"]
        assert len(capitalized) >= 2
        assert any(e.value == "Hello World" for e in capitalized)

    def test_deduplication(self):
        """Test entity deduplication."""
        engine = EntityEngine()
        text = "Email test@test.com and again test@test.com"
        entities = engine.extract(text)
        
        emails = [e for e in entities if e.type == "email"]
        values = [e.value for e in emails]
        assert values.count("test@test.com") == 1

    def test_deterministic_order(self):
        """Test entities are returned in deterministic order."""
        engine = EntityEngine()
        text = "b@test.com a@test.com c@test.com"
        entities = engine.extract(text)
        
        emails = [e for e in entities if e.type == "email"]
        values = [e.value for e in emails]
        assert values == sorted(values)


class TestCleaner:
    """Test text cleaning."""

    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        cleaner = Cleaner()
        text = "Hello    World\n\n  Test  "
        result = cleaner.clean(text)
        
        assert "  " not in result
        assert "\n\n" not in result

    def test_strip_text(self):
        """Test text stripping."""
        cleaner = Cleaner()
        text = "   Hello World   "
        result = cleaner.clean(text)
        
        assert result.startswith("Hello")
        assert result.endswith("World")

    def test_remove_empty_lines(self):
        """Test empty line removal."""
        cleaner = Cleaner()
        text = "Line 1\n\n\nLine 2"
        result = cleaner.clean(text)
        
        lines = [l for l in result.split('\n') if l.strip()]
        assert len(lines) == 2


class TestChunker:
    """Test text chunking."""

    def test_basic_chunking(self):
        """Test basic chunking."""
        chunker = Chunker()
        text = "A" * 1000
        chunks = chunker.chunk(text)
        
        assert len(chunks) > 1
        assert all(c.index >= 0 for c in chunks)

    def test_overlap(self):
        """Test chunk overlap."""
        chunker = Chunker({"chunking": {"size": 100, "overlap": 20}})
        text = "A" * 200
        chunks = chunker.chunk(text)
        
        if len(chunks) >= 2:
            overlap_text = chunks[1].text[:20]
            assert overlap_text == "A" * 20

    def test_chunk_metadata(self):
        """Test chunk metadata."""
        chunker = Chunker()
        text = "Hello World Test"
        chunks = chunker.chunk(text)
        
        assert chunks[0].index == 0
        assert chunks[0].start == 0
        assert chunks[0].end == len(chunks[0].text)


class TestGraphEngine:
    """Test graph building."""

    def test_build_empty_graph(self):
        """Test building empty graph."""
        engine = GraphEngine()
        result = engine.build([])
        
        assert result.nodes == []
        assert result.edges == []

    def test_build_graph(self):
        """Test building graph from entities."""
        engine = GraphEngine()
        entities = [
            Entity(type="email", value="test@test.com"),
            Entity(type="url", value="https://example.com"),
        ]
        result = engine.build(entities)
        
        assert len(result.nodes) == 2
        assert len(result.edges) == 1

    def test_deterministic_order(self):
        """Test graph output is deterministic."""
        engine = GraphEngine()
        entities = [
            Entity(type="url", value="https://z.com"),
            Entity(type="email", value="a@test.com"),
            Entity(type="url", value="https://b.com"),
        ]
        result = engine.build(entities)
        
        node_types = [n.type for n in result.nodes]
        assert node_types == sorted(node_types)


class TestClientAPI:
    """Test client API."""

    def test_client_initialization(self):
        """Test client initialization."""
        wx = WebWeaveX()
        assert wx.pipeline is not None
        assert wx.ai is not None

    def test_clean_method(self):
        """Test clean method."""
        wx = WebWeaveX()
        result = wx.clean("  Hello    World  ")
        assert result == "Hello World"

    def test_chunk_method(self):
        """Test chunk method."""
        wx = WebWeaveX()
        chunks = wx.chunk("A" * 1000)
        assert len(chunks) > 0

    def test_entities_method(self):
        """Test entities method."""
        wx = WebWeaveX()
        entities = wx.entities("Contact test@test.com")
        assert len(entities) > 0

    def test_graph_method_text(self):
        """Test graph method with text."""
        wx = WebWeaveX()
        result = wx.graph("Email test@test.com")
        assert result is not None

    def test_agent_tools(self):
        """Test agent tools listing."""
        wx = WebWeaveX()
        tools = wx.list_agent_tools()
        assert "crawl" in tools
        assert "rag" in tools
        assert "graph" in tools


class TestDeterminism:
    """Test deterministic output."""

    def test_entities_deterministic(self):
        """Test entity extraction is deterministic."""
        engine = EntityEngine()
        text = "test@test.com a@test.com b@test.com c@test.com"
        
        run1 = engine.extract(text)
        run2 = engine.extract(text)
        
        assert [e.to_dict() for e in run1] == [e.to_dict() for e in run2]

    def test_graph_deterministic(self):
        """Test graph building is deterministic."""
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
        """Test chunking is deterministic."""
        chunker = Chunker()
        text = "A" * 1000
        
        run1 = chunker.chunk(text)
        run2 = chunker.chunk(text)
        
        assert [c.to_dict() for c in run1] == [c.to_dict() for c in run2]


class TestSchema:
    """Test schema classes."""

    def test_entity_to_dict(self):
        """Test Entity to_dict."""
        entity = Entity(type="email", value="test@test.com")
        result = entity.to_dict()
        
        assert result == {"type": "email", "value": "test@test.com"}

    def test_entity_equality(self):
        """Test Entity equality."""
        e1 = Entity(type="email", value="test@test.com")
        e2 = Entity(type="email", value="test@test.com")
        
        assert e1 == e2
        assert hash(e1) == hash(e2)

    def test_chunk_to_dict(self):
        """Test Chunk to_dict."""
        chunk = Chunk(text="Hello", index=0, start=0, end=5)
        result = chunk.to_dict()
        
        assert result["text"] == "Hello"
        assert result["index"] == 0

    def test_graph_result_to_dict(self):
        """Test GraphResult to_dict."""
        result = GraphResult(
            nodes=[Entity(type="email", value="test@test.com")],
            edges=[{"source": "email:test@test.com", "target": "url:x.com", "weight": 1}]
        )
        dict_result = result.to_dict()
        
        assert "nodes" in dict_result
        assert "edges" in dict_result

    def test_crawl_result_to_dict(self):
        """Test CrawlResult to_dict."""
        result = CrawlResult(
            url="https://example.com",
            text="Hello World"
        )
        dict_result = result.to_dict()
        
        assert dict_result["url"] == "https://example.com"
        assert dict_result["text"] == "Hello World"


class TestAgentSystem:
    """Test agent system."""

    def test_execute_crawl_task(self):
        """Test crawl task execution."""
        wx = WebWeaveX()
        result = wx.agent_task("crawl https://example.com")
        
        assert result["task"] == "crawl https://example.com"
        assert result["tool"] == "crawl"

    def test_execute_graph_task(self):
        """Test graph task execution."""
        wx = WebWeaveX()
        result = wx.agent_task("extract graph from test@test.com email")
        
        assert "tool" in result

    def test_tool_selection(self):
        """Test tool selection logic."""
        wx = WebWeaveX()
        
        crawl_result = wx.agent.execute_task("crawl https://example.com")
        assert crawl_result["tool"] == "crawl"
        
        graph_result = wx.agent.execute_task("show graph entities")
        assert graph_result["tool"] == "graph"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
