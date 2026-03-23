"""Main client API for WebWeaveX."""

from typing import Dict, Any, List, Optional, Generator

from .pipeline import Pipeline
from .schema import WXPResult, Entity, Graph, Chunk, Insights
from .agent.agent_mode import extract_agent
from .agent.memory import to_memory_block, to_rag_chunks
from .agent.tool_schema import get_tool_schema, get_all_tools, get_capabilities


class WebWeaveX:
    """Main client for WebWeaveX library."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize WebWeaveX client."""
        self.config = config or {}
        self.pipeline = Pipeline(self.config)

    def crawl(self, url: str) -> WXPResult:
        """Crawl a URL and return full WXP result."""
        return self.pipeline.crawl(url)

    def extract(self, text_or_html: str) -> WXPResult:
        """Extract from text or HTML. Auto-detects input type."""
        try:
            if text_or_html.strip().startswith("<") and "</html>" in text_or_html.lower():
                return self.pipeline.extract_from_html(text_or_html)
            return self.pipeline.extract_from_text(text_or_html)
        except Exception:
            return WXPResult(
                url="",
                title="",
                text="",
                chunks=[],
                entities=[],
                relations=[],
                graph=Graph(nodes=[], edges=[]),
                insights=Insights(
                    entity_counts={},
                    stats={},
                    top_entities=[]
                )
            )

    def clean(self, text: str) -> str:
        """Clean text."""
        return self.pipeline.clean(text)

    def chunk(self, text: str) -> List[Chunk]:
        """Chunk text into pieces."""
        return self.pipeline.chunk(text)

    def entities(self, text: str) -> List[Entity]:
        """Extract entities from text."""
        return self.pipeline.entities(text)

    def graph(self, text: str) -> Graph:
        """Build entity graph from text."""
        return self.pipeline.graph(text)

    def rag(self, url: str, query: str) -> Dict[str, Any]:
        """Retrieve relevant chunks and answer query."""
        return self.pipeline.rag(url, query)

    def compare(self, url1: str, url2: str) -> Dict[str, Any]:
        """Compare two URLs and return differences."""
        return self.pipeline.diff(url1, url2)

    def weave(self, urls: List[str]) -> Dict[str, Any]:
        """Combine content from multiple URLs."""
        return self.pipeline.weave(urls)

    def diff(self, url1: str, url2: str) -> Dict[str, Any]:
        """Show differences between two URLs."""
        return self.pipeline.diff(url1, url2)

    def extract_agent(self, text: str) -> Dict[str, Any]:
        """Extract with AI-agent friendly output."""
        try:
            result = self.extract(text)
            return extract_agent(result.to_dict())
        except Exception as e:
            return {
                "task": "web_analysis",
                "input": text[:500] if len(text) > 500 else text,
                "output": {},
                "summary": f"Error: {str(e)}",
                "actions": [],
                "confidence": 0.0
            }

    def to_memory_block(self, result: Any) -> Dict[str, Any]:
        """Convert result to memory block format."""
        try:
            result_dict = result.to_dict() if hasattr(result, 'to_dict') else result
            return to_memory_block(result_dict)
        except Exception:
            return {
                "type": "webweavex_memory",
                "entities": [],
                "relations": [],
                "graph": {"nodes": [], "edges": []},
                "timestamp": "",
                "source": "webweavex"
            }

    def to_rag_chunks(self, result: Any) -> List[Dict[str, Any]]:
        """Convert result to RAG-ready chunks."""
        try:
            result_dict = result.to_dict() if hasattr(result, 'to_dict') else result
            return to_rag_chunks(result_dict)
        except Exception:
            return []

    def extract_stream(self, text: str) -> Generator[str, None, None]:
        """Stream extraction stages."""
        from .streaming.stream_engine import extract_stream
        yield from extract_stream(text, self.pipeline)

    def pretty_print(self, result: Any) -> str:
        """Format result as human-readable text."""
        try:
            result_dict = result.to_dict() if hasattr(result, 'to_dict') else result
            insights = result_dict.get("insights", {})
            stats = insights.get("stats", {})
            
            lines = [
                "=" * 50,
                "WebWeaveX Analysis",
                "=" * 50,
                "",
                "ENTITY SUMMARY:",
                "-" * 30,
            ]
            
            entity_counts = insights.get("entity_counts", {})
            for key, count in sorted(entity_counts.items()):
                lines.append(f"  {key}: {count}")
            
            lines.extend([
                "",
                "STATISTICS:",
                "-" * 30,
                f"  Total Entities: {stats.get('total_entities', 0)}",
                f"  Unique Entities: {stats.get('unique_entities', 0)}",
                f"  Entity Types: {stats.get('entity_types', 0)}",
                f"  Total Relations: {stats.get('total_relations', 0)}",
                f"  Total Chunks: {stats.get('total_chunks', 0)}",
                f"  Text Length: {stats.get('text_length', 0)}",
                f"  Word Count: {stats.get('word_count', 0)}",
                "",
                "=" * 50,
            ])
            
            return "\n".join(lines)
        except Exception as e:
            return f"Error formatting output: {str(e)}"

    @staticmethod
    def get_tool_schema() -> Dict[str, Any]:
        """Get tool schema for AI agents."""
        return get_tool_schema()

    @staticmethod
    def get_all_tools() -> List[Dict[str, Any]]:
        """Get all available tools."""
        return get_all_tools()

    @staticmethod
    def get_capabilities() -> List[str]:
        """Get list of supported capabilities."""
        return get_capabilities()
