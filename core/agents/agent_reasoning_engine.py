from __future__ import annotations

def summarize_for_agent(result: dict):
    g=result.get('relationships',{}).get('execution_graph',{})
    return {"node_count": len(g.get('nodes',[])), "edge_count": len(g.get('edges',[])), "confidence": result.get('metadata',{}).get('confidence',0.0)}
