from core.ir.runtime_ir import (
    compile_runtime_ir,
)


def test_runtime_ir_phase6():

    r = compile_runtime_ir(
        source="x = 1",
        path="main.py",
        graph={
            "tasks": [
                {"id": "t1"}
            ],
            "nodes": [
                {"id": "api"}
            ],
        },
    )

    assert (
        "semantic_hypergraph"
        in r
    )

    assert (
        "runtime_consistency"
        in r
    )
