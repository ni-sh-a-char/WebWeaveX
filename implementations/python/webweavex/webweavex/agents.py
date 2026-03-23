"""Agent system for WebWeaveX."""

from typing import Dict, Any, Optional, List
import json

from .tools import ToolRegistry, ToolBuilder, ToolResult
from .ai import AIEngine
from .utils import get_spec


class Agent:
    """Lightweight agent for task execution."""

    def __init__(self, client: Any, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent."""
        self.spec = config or get_spec()
        self.client = client
        self.tool_registry = ToolRegistry()
        self.ai_engine = AIEngine()
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all available tools."""
        builder = ToolBuilder(self.client)
        for tool in builder.build_all():
            self.tool_registry.register(tool)

    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute a task using the appropriate tool."""
        tool_name = self._select_tool(task)
        
        if not tool_name:
            return {
                "success": False,
                "error": "Could not determine appropriate tool for task",
                "task": task
            }

        params = self._extract_params(task, tool_name)
        
        result = self.tool_registry.execute(tool_name, **params)
        
        return {
            "task": task,
            "tool": tool_name,
            "params": params,
            "result": result.to_dict() if isinstance(result, ToolResult) else result
        }

    def _select_tool(self, task: str) -> Optional[str]:
        """Select the appropriate tool for a task."""
        task_lower = task.lower()
        
        tool_keywords = {
            "crawl": ["crawl", "fetch", "scrape", "get content", "download"],
            "rag": ["rag", "retrieve", "query", "search", "find"],
            "graph": ["graph", "entities", "relationships"],
            "compare": ["compare", "comparison", "differences"],
            "weave": ["weave", "combine", "merge", "synthesize"],
            "diff": ["diff", "difference", "changes"],
        }

        for tool_name, keywords in tool_keywords.items():
            for keyword in keywords:
                if keyword in task_lower:
                    return tool_name

        return None

    def _extract_params(self, task: str, tool_name: str) -> Dict[str, Any]:
        """Extract parameters from the task description."""
        params = {}
        
        import re
        url_pattern = r'https?://[^\s<>"\'\)]+'
        urls = re.findall(url_pattern, task)
        
        if tool_name in ["crawl", "rag"]:
            if urls:
                params["url"] = urls[0]
            if tool_name == "rag" and "query" in task.lower():
                query_match = re.search(r'query[:\s]+["\']?([^"\']+)["\']?', task, re.IGNORECASE)
                if query_match:
                    params["query"] = query_match.group(1)
                else:
                    params["query"] = task
        
        elif tool_name in ["compare", "weave"]:
            params["urls"] = urls if urls else []
        
        elif tool_name == "diff":
            if len(urls) >= 2:
                params["url1"] = urls[0]
                params["url2"] = urls[1]
            elif urls:
                params["url1"] = urls[0]
                params["url2"] = ""
        
        elif tool_name == "graph":
            if not urls:
                text_match = re.search(r'text[:\s]+["\']?([^"\']+)["\']?', task, re.IGNORECASE)
                if text_match:
                    params["text"] = text_match.group(1)
                else:
                    params["text"] = task

        return params

    def list_tools(self) -> List[str]:
        """List available tools."""
        return self.tool_registry.list_tools()

    def add_tool(self, name: str, description: str, params: List[str], func: Any) -> None:
        """Add a custom tool."""
        from .tools import ToolDefinition
        self.tool_registry.register(ToolDefinition(
            name=name,
            description=description,
            params=params,
            func=func
        ))
