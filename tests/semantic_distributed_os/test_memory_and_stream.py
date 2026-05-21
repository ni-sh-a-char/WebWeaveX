from core.distributed_memory import SemanticMemoryFabric, replicate_semantic_region
from core.stream import SemanticStream


def test_memory_fabric():
    fabric = SemanticMemoryFabric()
    fabric.put("r1", "k", {"v": 1})
    assert fabric.get("r1", "k") == {"v": 1}


def test_replication():
    r = replicate_semantic_region({"x": 1}, replicas=2)
    assert len(r["replicas"]) == 2


def test_stream():
    s = SemanticStream()
    s.push({"e": 1})
    assert s.next()["e"] == 1
