from core.ir.distributed_extraction_ir import (
    compile_distributed_extraction_ir,
    distributed_extraction_ir_to_graph,
)


def test_distributed_ir_graph():
    ir = compile_distributed_extraction_ir(
        workers={"workers": [{"worker_id": "w0", "status": "idle"}]},
        queue={"queue": []},
        topology={"topology": {"nodes": [], "edges": []}},
        identities={"routes": []},
        streams={"events": []},
        adaptive={"healed_selectors": {}},
        checkpoint={"tick": 0},
        recovery={"recovered": True},
    )

    graph = distributed_extraction_ir_to_graph(ir)

    assert ir["ir"] == "distributed_extraction"
    assert graph["nodes"][0]["id"] == "w0"
