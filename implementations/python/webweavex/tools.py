"""WebWeaveX Tools - Tool registry and execution (PURE SYNC)."""

from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass

from .config import DEFAULT_CONFIG


@dataclass
class ToolDefinition:
    name: str
    description: str
    params: List[str]
    func: Callable


@dataclass
class ToolResult:
    tool: str
    success: bool
    result: Any
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "tool": self.tool,
            "success": self.success,
            "result": self.result,
        }
        if self.error:
            result["error"] = self.error
        return result


class ToolRegistry:
    """Registry for tools."""

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[ToolDefinition]:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def execute(self, name: str, **kwargs) -> ToolResult:
        tool = self._tools.get(name)
        if not tool:
            return ToolResult(
                tool=name,
                success=False,
                result=None,
                error=f"Tool '{name}' not found"
            )

        try:
            result = tool.func(**kwargs)
            return ToolResult(tool=name, success=True, result=result)
        except Exception as e:
            return ToolResult(tool=name, success=False, result=None, error=str(e))


class ToolBuilder:
    """Builder for creating tools - PURE SYNC FUNCTIONS."""

    def __init__(self, client):
        self.client = client

    def create_crawl_tool(self) -> ToolDefinition:
        def crawl_func(url: str):
            result = self.client.crawl(url)
            return result.to_dict()

        return ToolDefinition(
            name="crawl",
            description="Fetch and process a URL",
            params=["url"],
            func=crawl_func
        )

    def create_rag_tool(self) -> ToolDefinition:
        def rag_func(url: str, query: str):
            return self.client.rag(url, query)

        return ToolDefinition(
            name="rag",
            description="Retrieve relevant chunks for a query",
            params=["url", "query"],
            func=rag_func
        )

    def create_graph_tool(self) -> ToolDefinition:
        def graph_func(text: str):
            return self.client.graph(text)

        return ToolDefinition(
            name="graph",
            description="Generate entity graph from text",
            params=["text"],
            func=graph_func
        )

    def create_compare_tool(self) -> ToolDefinition:
        def compare_func(urls: List[str]):
            return self.client.compare(urls)

        return ToolDefinition(
            name="compare",
            description="Compare content from multiple URLs",
            params=["urls"],
            func=compare_func
        )

    def create_diff_tool(self) -> ToolDefinition:
        def diff_func(url1: str, url2: str):
            return self.client.diff(url1, url2)

        return ToolDefinition(
            name="diff",
            description="Show differences between URLs",
            params=["url1", "url2"],
            func=diff_func
        )

    def create_entities_tool(self) -> ToolDefinition:
        def entities_func(text: str):
            entities = self.client.entities(text)
            return [e.to_dict() for e in entities]

        return ToolDefinition(
            name="entities",
            description="Extract entities from text",
            params=["text"],
            func=entities_func
        )

    def build_all(self) -> List[ToolDefinition]:
        return [
            self.create_crawl_tool(),
            self.create_rag_tool(),
            self.create_graph_tool(),
            self.create_compare_tool(),
            self.create_diff_tool(),
            self.create_entities_tool(),
        ]
