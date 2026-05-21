from core.adaptive import (
    load_adaptive_memory,
    remember_extraction_runtime,
    save_adaptive_memory,
)


def test_adaptive_memory_replay(tmp_path):
    memory = remember_extraction_runtime(
        {
            "selectors": {},
            "healed_selectors": {},
            "pagination_patterns": [],
            "modal_solutions": [],
            "interaction_chains": [],
        },
        {
            "selectors": {"primary": "body"},
            "healed_selectors": {"primary": "[aria-label='Next']"},
        },
    )

    path = tmp_path / "adaptive.enc"
    save_adaptive_memory(str(path), memory, "adaptive-key")

    loaded = load_adaptive_memory(str(path), "adaptive-key")

    assert loaded["available"] is True
    assert loaded["memory"] == memory
