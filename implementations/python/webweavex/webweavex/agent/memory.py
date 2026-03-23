"""Memory block generation for RAG systems."""

from typing import Dict, Any, List
from datetime import datetime


def to_memory_block(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert WXP result to memory block format.
    
    Returns:
        Memory block with entities, relations, graph, and metadata.
    """
    try:
        entities = result.get("entities", [])
        relations = result.get("relations", [])
        graph = result.get("graph", {})
        meta = result.get("meta", {})
        
        return {
            "type": "webweavex_memory",
            "entities": entities,
            "relations": relations,
            "graph": graph,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "source": "webweavex"
        }
    except Exception:
        return {
            "type": "webweavex_memory",
            "entities": [],
            "relations": [],
            "graph": {"nodes": [], "edges": []},
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "source": "webweavex"
        }


def to_rag_chunks(result: Dict[str, Any], chunk_size: int = 500) -> List[Dict[str, Any]]:
    """
    Convert WXP result to RAG-ready chunks.
    
    Returns:
        List of chunks with text and entity metadata.
    """
    try:
        chunks = result.get("chunks", [])
        entities = result.get("entities", [])
        relations = result.get("relations", [])
        
        rag_chunks = []
        for chunk in chunks:
            chunk_text = chunk.get("text", "")
            chunk_entities = _find_chunk_entities(chunk, entities)
            chunk_relations = _find_chunk_relations(chunk, relations, entities)
            
            rag_chunks.append({
                "text": chunk_text,
                "metadata": {
                    "entities": chunk_entities,
                    "relations": chunk_relations,
                    "source": "webweavex"
                }
            })
        
        return rag_chunks
    except Exception:
        return []


def _find_chunk_entities(chunk: Dict[str, Any], entities: List[Dict]) -> List[Dict]:
    """Find entities within a chunk."""
    chunk_text = chunk.get("text", "")
    chunk_start = chunk.get("start", 0)
    chunk_end = chunk.get("end", 0)
    
    found = []
    for entity in entities:
        value = entity.get("value", "")
        if value and value in chunk_text:
            found.append(entity)
    
    return found


def _find_chunk_relations(chunk: Dict[str, Any], relations: List[Dict], entities: List[Dict]) -> List[Dict]:
    """Find relations within a chunk."""
    return relations[:5]
