"""Tools system for WebWeaveX."""

from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass

from .utils import get_spec


@dataclass
class ToolDefinition:
    """Definition of a tool."""
    name: str
    description: str
    params: List[str]
    func: Callable


@dataclass
class ToolResult:
    """Result from a tool execution."""
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
        """Initialize the registry."""
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return list(self._tools.keys())

    def execute(self, name: str, **kwargs) -> ToolResult:
        """Execute a tool."""
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
    """Builder for creating tools."""

    def __init__(self, client: Any):
        """Initialize with client reference."""
        self.client = client

    def create_crawl_tool(self) -> ToolDefinition:
        """Create the crawl tool."""
        async def crawl_func(url: str):
            return self.client.crawl(url)

        return ToolDefinition(
            name="crawl",
            description="Fetch and process a URL",
            params=["url"],
            func=crawl_func
        )

    def create_rag_tool(self) -> ToolDefinition:
        """Create the RAG tool."""
        async def rag_func(url: str, query: str):
            return self.client.rag(url, query)

        return ToolDefinition(
            name="rag",
            description="Retrieve relevant chunks for a query",
            params=["url", "query"],
            func=rag_func
        )

    def create_graph_tool(self) -> ToolDefinition:
        """Create the graph tool."""
        async def graph_func(text: str):
            return self.client.graph(text)

        return ToolDefinition(
            name="graph",
            description="Generate entity graph from text",
            params=["text"],
            func=graph_func
        )

    def create_compare_tool(self) -> ToolDefinition:
        """Create the compare tool."""
        async def compare_func(urls: List[str]):
            return self.client.compare(urls)

        return ToolDefinition(
            name="compare",
            description="Compare content from multiple URLs",
            params=["urls"],
            func=compare_func
        )

    def create_weave_tool(self) -> ToolDefinition:
        """Create the weave tool."""
        async def weave_func(urls: List[str]):
            return self.client.weave(urls)

        return ToolDefinition(
            name="weave",
            description="Combine content from multiple URLs",
            params=["urls"],
            func=weave_func
        )

    def create_diff_tool(self) -> ToolDefinition:
        """Create the diff tool."""
        async def diff_func(url1: str, url2: str):
            return self.client.diff(url1, url2)

        return ToolDefinition(
            name="diff",
            description="Show differences between URLs",
            params=["url1", "url2"],
            func=diff_func
        )

    def build_all(self) -> List[ToolDefinition]:
        """Build all standard tools."""
        return [
            self.create_crawl_tool(),
            self.create_rag_tool(),
            self.create_graph_tool(),
            self.create_compare_tool(),
            self.create_weave_tool(),
            self.create_diff_tool(),
        ]
