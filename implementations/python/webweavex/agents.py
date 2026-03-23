"""WebWeaveX Agent - Rule-based planner agent."""

from typing import Dict, Any, Optional, List
import re

from .config import DEFAULT_CONFIG
from .tools import ToolRegistry, ToolBuilder, ToolResult


class Agent:
    """Lightweight rule-based agent."""

    def __init__(self, client, config: Optional[Dict[str, Any]] = None):
        self.config = config or DEFAULT_CONFIG
        self.client = client
        self.tool_registry = ToolRegistry()
        self._register_tools()

    def _register_tools(self) -> None:
        builder = ToolBuilder(self.client)
        for tool in builder.build_all():
            self.tool_registry.register(tool)

    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute task using rule-based tool selection."""
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
        """Rule-based tool selection."""
        task_lower = task.lower()

        tool_keywords = {
            "crawl": ["crawl", "fetch", "scrape", "get content", "download", "fetch url"],
            "rag": ["rag", "retrieve", "query", "search", "find relevant"],
            "graph": ["graph", "entities", "relationships", "entity graph"],
            "compare": ["compare", "comparison"],
            "diff": ["diff", "difference", "changes", "compare urls"],
            "entities": ["entities", "extract", "find entities"],
        }

        for tool_name, keywords in tool_keywords.items():
            for keyword in keywords:
                if keyword in task_lower:
                    return tool_name

        return None

    def _extract_params(self, task: str, tool_name: str) -> Dict[str, Any]:
        """Extract parameters using regex."""
        params: Dict[str, Any] = {}
        
        url_pattern = r'https?://[^\s<>"\')]+'
        urls = re.findall(url_pattern, task)

        if tool_name in ["crawl"]:
            if urls:
                params["url"] = urls[0]

        elif tool_name in ["rag"]:
            if urls:
                params["url"] = urls[0]
            query_match = re.search(r'query[:\s]+["\']?([^"\']+)["\']?', task, re.IGNORECASE)
            if query_match:
                params["query"] = query_match.group(1)
            else:
                params["query"] = task

        elif tool_name in ["compare"]:
            params["urls"] = urls if urls else []

        elif tool_name in ["diff"]:
            if len(urls) >= 2:
                params["url1"] = urls[0]
                params["url2"] = urls[1]
            elif urls:
                params["url1"] = urls[0]
                params["url2"] = ""

        elif tool_name in ["graph", "entities"]:
            text_match = re.search(r'text[:\s]+["\']?(.+?)["\']?$', task, re.IGNORECASE | re.MULTILINE)
            if text_match:
                params["text"] = text_match.group(1).strip()
            else:
                params["text"] = task

        return params

    def list_tools(self) -> List[str]:
        return self.tool_registry.list_tools()

    def add_tool(self, name: str, description: str, params: List[str], func: Any) -> None:
        from .tools import ToolDefinition
        self.tool_registry.register(ToolDefinition(
            name=name,
            description=description,
            params=params,
            func=func
        ))
