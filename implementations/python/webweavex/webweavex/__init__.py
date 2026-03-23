"""WebWeaveX - Universal installable library for web intelligence."""

__version__ = "1.0.0"

from .client import WebWeaveX
from .schema import (
    WXPResult,
    Entity,
    Chunk,
    Relation,
    Graph,
    GraphNode,
    GraphEdge,
    Insights,
    Meta,
    Content,
)
from .config import DEFAULT_CONFIG, get_config, set_config
from .agent.tool_schema import get_tool_schema, get_all_tools, get_capabilities
from .validation.schema_checker import (
    validate_wxp_result,
    validate_agent_result,
    validate_memory_block,
    validate_rag_chunks,
    check_key_order,
)

__all__ = [
    "WebWeaveX",
    "WXPResult",
    "Entity",
    "Chunk",
    "Relation",
    "Graph",
    "GraphNode",
    "GraphEdge",
    "Insights",
    "Meta",
    "Content",
    "DEFAULT_CONFIG",
    "get_config",
    "set_config",
    "get_tool_schema",
    "get_all_tools",
    "get_capabilities",
    "validate_wxp_result",
    "validate_agent_result",
    "validate_memory_block",
    "validate_rag_chunks",
    "check_key_order",
    "__version__",
]
