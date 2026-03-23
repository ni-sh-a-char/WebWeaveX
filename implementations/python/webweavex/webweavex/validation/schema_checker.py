"""Schema validation utilities."""

from typing import Dict, Any, List, Tuple


def validate_wxp_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate WXP result against schema.
    
    Returns:
        (is_valid, error_messages)
    """
    errors = []
    
    required_keys = ["meta", "content", "chunks", "entities", "relations", "graph", "insights"]
    for key in required_keys:
        if key not in result:
            errors.append(f"Missing required key: {key}")
    
    if "meta" in result:
        if not isinstance(result["meta"], dict):
            errors.append("meta must be a dict")
        else:
            if "title" not in result["meta"]:
                errors.append("meta missing 'title'")
            if "url" not in result["meta"]:
                errors.append("meta missing 'url'")
    
    if "content" in result:
        if not isinstance(result["content"], dict):
            errors.append("content must be a dict")
        elif "text" not in result["content"]:
            errors.append("content missing 'text'")
    
    if "entities" in result:
        if not isinstance(result["entities"], list):
            errors.append("entities must be a list")
    
    if "relations" in result:
        if not isinstance(result["relations"], list):
            errors.append("relations must be a list")
    
    if "graph" in result:
        if not isinstance(result["graph"], dict):
            errors.append("graph must be a dict")
        else:
            if "nodes" not in result["graph"]:
                errors.append("graph missing 'nodes'")
            if "edges" not in result["graph"]:
                errors.append("graph missing 'edges'")
    
    if "insights" in result:
        if not isinstance(result["insights"], dict):
            errors.append("insights must be a dict")
        else:
            if "entity_counts" not in result["insights"]:
                errors.append("insights missing 'entity_counts'")
            if "stats" not in result["insights"]:
                errors.append("insights missing 'stats'")
            if "top_entities" not in result["insights"]:
                errors.append("insights missing 'top_entities'")
    
    return len(errors) == 0, errors


def validate_agent_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate agent mode result."""
    errors = []
    
    required_keys = ["task", "input", "output", "summary", "actions", "confidence"]
    for key in required_keys:
        if key not in result:
            errors.append(f"Missing required key: {key}")
    
    if "task" in result and result["task"] != "web_analysis":
        errors.append("task must be 'web_analysis'")
    
    if "confidence" in result:
        if not isinstance(result["confidence"], (int, float)):
            errors.append("confidence must be a number")
        elif result["confidence"] < 0 or result["confidence"] > 1:
            errors.append("confidence must be between 0 and 1")
    
    return len(errors) == 0, errors


def validate_memory_block(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate memory block format."""
    errors = []
    
    required_keys = ["type", "entities", "relations", "graph", "timestamp", "source"]
    for key in required_keys:
        if key not in result:
            errors.append(f"Missing required key: {key}")
    
    if "type" in result and result["type"] != "webweavex_memory":
        errors.append("type must be 'webweavex_memory'")
    
    if "source" in result and result["source"] != "webweavex":
        errors.append("source must be 'webweavex'")
    
    return len(errors) == 0, errors


def validate_rag_chunks(result: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Validate RAG chunks format."""
    errors = []
    
    if not isinstance(result, list):
        errors.append("RAG chunks must be a list")
        return False, errors
    
    for i, chunk in enumerate(result):
        if not isinstance(chunk, dict):
            errors.append(f"Chunk {i} must be a dict")
            continue
        
        if "text" not in chunk:
            errors.append(f"Chunk {i} missing 'text'")
        if "metadata" not in chunk:
            errors.append(f"Chunk {i} missing 'metadata'")
    
    return len(errors) == 0, errors


def check_key_order(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Check if key order is deterministic (alphabetical)."""
    errors = []
    
    result_keys = list(result.keys())
    expected_top_order = sorted(result_keys)
    
    if result_keys != expected_top_order:
        errors.append(f"Keys not in alphabetical order. Got: {result_keys}")
    
    if "graph" in result:
        graph_keys = list(result["graph"].keys())
        expected_graph_order = sorted(graph_keys)
        if graph_keys != expected_graph_order:
            errors.append(f"Graph keys not in alphabetical order. Got: {graph_keys}")
    
    if "insights" in result:
        insights_keys = list(result["insights"].keys())
        expected_insights_order = sorted(insights_keys)
        if insights_keys != expected_insights_order:
            errors.append(f"Insights keys not in alphabetical order. Got: {insights_keys}")
    
    return len(errors) == 0, errors
