from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime


def test_reconstruction_determinism():
    sources = {
        "semantic_ir": {"ir": "semantic_runtime", "domain": "analytics"},
        "workflow_ir": {"ir": "workflow_runtime", "objective": "monitor"},
        "runtime_graph": {"nodes": [{"id": "n1"}], "edges": []},
    }

    first = reconstruct_runtime(
        semantic_ir=sources["semantic_ir"],
        workflow_ir=sources["workflow_ir"],
        runtime_graph=sources["runtime_graph"],
        tick=1,
    )
    second = reconstruct_runtime(
        semantic_ir=sources["semantic_ir"],
        workflow_ir=sources["workflow_ir"],
        runtime_graph=sources["runtime_graph"],
        tick=1,
    )

    assert first == second
    assert first["reconstructed"] is True
