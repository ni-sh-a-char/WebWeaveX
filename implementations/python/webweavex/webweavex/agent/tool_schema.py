"""Tool schema definitions for AI agents."""

from typing import Dict, Any, List


def get_tool_schema() -> Dict[str, Any]:
    """
    Get WebWeaveX tool schema for AI agent integration.
    
    Returns:
        OpenAI-compatible tool schema.
    """
    return {
        "name": "webweavex_extract",
        "description": "Extract structured intelligence from text including entities, relationships, and graph data",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "The text or HTML content to analyze"
                }
            },
            "required": ["input"]
        }
    }


def get_all_tools() -> List[Dict[str, Any]]:
    """Get all available tools."""
    return [
        get_tool_schema(),
        {
            "name": "webweavex_entities",
            "description": "Extract only entities from text",
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "The text to analyze for entities"
                    }
                },
                "required": ["input"]
            }
        },
        {
            "name": "webweavex_graph",
            "description": "Extract entity graph from text",
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "The text to analyze"
                    }
                },
                "required": ["input"]
            }
        }
    ]


def get_capabilities() -> List[str]:
    """Get list of supported capabilities."""
    return [
        "extract",
        "entities",
        "graph",
        "rag",
        "agent_mode",
        "memory_export",
        "streaming"
    ]
