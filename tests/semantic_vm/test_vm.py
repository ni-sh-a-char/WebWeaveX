from core.bytecode import (
    compile_semantic_bytecode,
)

from core.vm import (
    SemanticVirtualMachine,
)


def test_vm_executes():

    ir = {
        "edges": [
            {
                "from": "x",
                "to": "y",
            }
        ]
    }

    bc = compile_semantic_bytecode(
        ir,
    )

    vm = SemanticVirtualMachine()

    r = vm.execute(
        bc["instructions"]
    )

    assert r["executed"] == 1
