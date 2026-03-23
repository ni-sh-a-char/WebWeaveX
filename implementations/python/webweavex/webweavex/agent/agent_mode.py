"""Agent mode for AI integration."""

from typing import Dict, Any, List


def extract_agent(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate agent-friendly output from WXP result.
    
    Returns:
        Agent response with task, summary, actions, and confidence.
    """
    try:
        text = result.get("content", {}).get("text", "")
        entities = result.get("entities", [])
        relations = result.get("relations", [])
        
        summary = _generate_summary(entities, text)
        actions = _determine_actions(entities)
        confidence = _calculate_confidence(len(entities), len(relations), len(text))
        
        return {
            "task": "web_analysis",
            "input": text[:500] if len(text) > 500 else text,
            "output": result,
            "summary": summary,
            "actions": actions,
            "confidence": round(confidence, 2)
        }
    except Exception as e:
        return {
            "task": "web_analysis",
            "input": "",
            "output": {},
            "summary": f"Error processing input: {str(e)}",
            "actions": [],
            "confidence": 0.0
        }


def _generate_summary(entities: List[Dict], text: str) -> str:
    """Generate deterministic summary based on entities found."""
    if not entities:
        return "No entities extracted from input text."
    
    entity_types = set(e.get("type", "") for e in entities)
    type_counts = {}
    for e in entities:
        t = e.get("type", "")
        type_counts[t] = type_counts.get(t, 0) + 1
    
    parts = []
    for etype in sorted(entity_types):
        count = type_counts.get(etype, 0)
        parts.append(f"{count} {etype}(s)")
    
    return f"Extracted {len(entities)} entities ({', '.join(parts)}) from text."


def _determine_actions(entities: List[Dict]) -> List[str]:
    """Determine actions based on entity types present."""
    entity_types = set(e.get("type", "") for e in entities)
    actions = []
    
    if "url" in entity_types:
        actions.append("crawl")
    if "email" in entity_types:
        actions.append("contact")
    if "phone" in entity_types:
        actions.append("call")
    if len(entities) > 5:
        actions.append("extract_more")
    
    if not actions:
        actions.append("analyze")
    
    return actions


def _calculate_confidence(entity_count: int, relation_count: int, text_length: int) -> float:
    """Calculate confidence score deterministically."""
    if text_length == 0:
        return 0.0
    
    score = (entity_count + relation_count * 0.5) / max(text_length, 1)
    return min(score * 10, 1.0)
