from core.bytecode import (
    compile_semantic_bytecode,
)


def test_bytecode():

    ir = {
        "edges": [
            {
                "from": "a",
                "to": "b",
            }
        ]
    }

    r = compile_semantic_bytecode(
        ir,
    )

    assert r["count"] == 1
