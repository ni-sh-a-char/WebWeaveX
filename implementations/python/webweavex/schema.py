"""WebWeaveX Schema - Unified WXP v1 Schema."""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union


def _sort_dict(data: Any) -> Any:
    """Recursively sort dictionary for deterministic output."""
    if isinstance(data, dict):
        return {k: _sort_dict(v) for k, v in sorted(data.items())}
    elif isinstance(data, list):
        return [_sort_dict(item) for item in data]
    return data


def _to_json_safe(obj: Any) -> str:
    """Convert object to JSON with deterministic sorting."""
    def default_serializer(o):
        if hasattr(o, 'to_dict'):
            return o.to_dict()
        if hasattr(o, '__dict__'):
            return o.__dict__
        return str(o)
    return json.dumps(obj, sort_keys=True, default=default_serializer, ensure_ascii=False)


@dataclass
class Meta:
    url: str = ""
    title: str = ""

    def to_dict(self) -> Dict[str, str]:
        result = {}
        if self.url:
            result["url"] = self.url
        if self.title:
            result["title"] = self.title
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


@dataclass
class Content:
    text: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {"text": self.text}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


@dataclass
class Entity:
    type: str
    value: str

    def to_dict(self) -> Dict[str, str]:
        return {"type": self.type, "value": self.value}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    def __hash__(self):
        return hash((self.type, self.value))

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.type == other.type and self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return (self.type, self.value) < (other.type, other.value)


@dataclass
class Chunk:
    text: str
    index: int
    start: int
    end: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "index": self.index,
            "start": self.start,
            "end": self.end,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


@dataclass
class Relation:
    source: str
    target: str
    type: str = "cooccurrence"

    def to_dict(self) -> Dict[str, str]:
        return {
            "source": self.source,
            "target": self.target,
            "type": self.type,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    def __hash__(self):
        return hash((self.source, self.target, self.type))

    def __eq__(self, other):
        if not isinstance(other, Relation):
            return False
        return (self.source == other.source and 
                self.target == other.target and 
                self.type == other.type)

    def __lt__(self, other):
        if not isinstance(other, Relation):
            return NotImplemented
        return (self.source, self.target, self.type) < (other.source, other.target, other.type)


@dataclass 
class GraphNode:
    id: str
    type: str
    value: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {"id": self.id, "type": self.type, "value": self.value}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, GraphNode):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, GraphNode):
            return NotImplemented
        return self.id < other.id


@dataclass
class GraphEdge:
    source: str
    target: str
    weight: int = 1
    directed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
        }
        if self.directed:
            result["directed"] = True
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    def __hash__(self):
        return hash((self.source, self.target))

    def __eq__(self, other):
        if not isinstance(other, GraphEdge):
            return False
        return self.source == other.source and self.target == other.target

    def __lt__(self, other):
        if not isinstance(other, GraphEdge):
            return NotImplemented
        return (self.source, self.target) < (other.source, other.target)


@dataclass
class Graph:
    nodes: List[GraphNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in sorted(self.nodes)],
            "edges": [e.to_dict() for e in sorted(self.edges)],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


@dataclass
class Insights:
    top_entities: List[Dict[str, Any]] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    entity_counts: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "top_entities": _sort_dict(self.top_entities),
            "stats": _sort_dict(self.stats),
            "entity_counts": _sort_dict(self.entity_counts),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


class WXPResult:
    """Unified WXP v1 Result - All crawls return this structure."""

    def __init__(
        self,
        url: str = "",
        title: str = "",
        text: str = "",
        chunks: Optional[List[Chunk]] = None,
        entities: Optional[List[Entity]] = None,
        relations: Optional[List[Relation]] = None,
        graph: Optional[Graph] = None,
        insights: Optional[Insights] = None,
    ):
        self.meta = Meta(url=url, title=title)
        self.content = Content(text=text)
        self.chunks = chunks if chunks is not None else []
        self.entities = entities if entities is not None else []
        self.relations = relations if relations is not None else []
        self.graph = graph if graph is not None else Graph()
        self.insights = insights if insights is not None else Insights()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary following WXP v1 schema."""
        result = {
            "meta": self.meta.to_dict(),
            "content": self.content.to_dict(),
        }
        if self.chunks:
            result["chunks"] = [c.to_dict() for c in self.chunks]
        if self.entities:
            result["entities"] = [e.to_dict() for e in sorted(self.entities)]
        if self.relations:
            result["relations"] = [r.to_dict() for r in sorted(self.relations)]
        if self.graph.nodes or self.graph.edges:
            result["graph"] = self.graph.to_dict()
        if self.insights.top_entities or self.insights.stats:
            result["insights"] = self.insights.to_dict()
        return _sort_dict(result)

    def to_json(self, indent: bool = False) -> str:
        """Convert to JSON string with deterministic output."""
        kwargs = {"sort_keys": True}
        if indent:
            kwargs["indent"] = 2
        return json.dumps(self.to_dict(), **kwargs)

    def get_entity_count(self, entity_type: str) -> int:
        """Get count of entities by type."""
        return sum(1 for e in self.entities if e.type == entity_type)

    def get_top_entities(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top N entities by frequency."""
        counts = {}
        for e in self.entities:
            key = (e.type, e.value)
            counts[key] = counts.get(key, 0) + 1
        
        sorted_entities = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return [
            {"type": t, "value": v, "count": c}
            for (t, v), c in sorted_entities[:n]
        ]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WXPResult":
        """Create WXPResult from dictionary."""
        meta = data.get("meta", {})
        content = data.get("content", {})
        
        result = cls(
            url=meta.get("url", ""),
            title=meta.get("title", ""),
            text=content.get("text", ""),
        )
        
        chunks_data = data.get("chunks", [])
        result.chunks = [Chunk(**c) for c in chunks_data]
        
        entities_data = data.get("entities", [])
        result.entities = [Entity(**e) for e in entities_data]
        
        relations_data = data.get("relations", [])
        result.relations = [Relation(**r) for r in relations_data]
        
        graph_data = data.get("graph", {})
        if graph_data:
            nodes = [GraphNode(**n) for n in graph_data.get("nodes", [])]
            edges = [GraphEdge(**e) for e in graph_data.get("edges", [])]
            result.graph = Graph(nodes=nodes, edges=edges)
        
        insights_data = data.get("insights", {})
        if insights_data:
            result.insights = Insights(
                top_entities=insights_data.get("top_entities", []),
                stats=insights_data.get("stats", {}),
                entity_counts=insights_data.get("entity_counts", {}),
            )
        
        return result
