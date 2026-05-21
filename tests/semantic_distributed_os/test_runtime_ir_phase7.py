from core.ir.runtime_ir import (
    compile_runtime_ir,
)


def test_runtime_ir_phase7():

    r = compile_runtime_ir(
        source="x = 1",
        path="main.py",
        graph={
            "nodes": [
                {"id": "api"},
            ]
        },
    )

    assert (
        "semantic_actor_message"
        in r
    )

    assert (
        "semantic_crdt"
        in r
    )
