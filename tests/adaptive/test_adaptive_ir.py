from core.ir.adaptive_runtime_ir import (
    adaptive_runtime_ir_to_graph,
    compile_adaptive_runtime_ir,
)


def test_adaptive_ir_graph():
    adaptive_ir = compile_adaptive_runtime_ir(
        adaptation={
            "fallback": {
                "chain": [
                    {"step": 0, "strategy": "primary", "selector": "body"},
                    {"step": 1, "strategy": "healed_selector", "selector": "button"},
                ]
            }
        },
        memory={"healed_selectors": {"primary": "button"}},
        schema={"fields": ["title"]},
        reconciliation={"consistent": True},
        snapshot={"dom": {}},
    )

    graph = adaptive_runtime_ir_to_graph(adaptive_ir)

    assert graph["nodes"]
    assert graph["edges"]
