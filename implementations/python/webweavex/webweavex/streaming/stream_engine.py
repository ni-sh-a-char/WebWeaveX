"""Streaming engine for progressive extraction."""

from typing import Iterator, Dict, Any, Generator, Optional


def extract_stream(text: str, pipeline) -> Generator[str, None, None]:
    """
    Stream extraction stages.
    
    Yields:
        Stage names: cleaning, chunking, entities, relations, graph, insights
    """
    try:
        yield "cleaning"
        
        yield "chunking"
        cleaned = pipeline.cleaner.clean(text)
        chunks = pipeline.chunker.chunk(cleaned)
        
        yield "entities"
        entities = pipeline.entity_engine.extract(cleaned)
        
        yield "relations"
        relations = pipeline.relation_engine.extract(entities, chunks)
        
        yield "graph"
        graph = pipeline.graph_engine.build(entities)
        
        yield "insights"
        insights = pipeline.insights_engine.compute(entities, chunks, cleaned)
        
    except Exception as e:
        yield "error"
        yield f"Error: {str(e)}"
