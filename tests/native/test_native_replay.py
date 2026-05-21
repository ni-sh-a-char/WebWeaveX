from core.native import extract_native


def test_native_replay_graph():
    result = extract_native(
        runtime="desktop",
        application="slack",
        application_cognition=False,
        persistent_runtime=False,
        merge_runtime_graph=True,
    )

    first = result["replay"]
    second = result["replay"]

    assert first == second
    assert result["unified_graph"]["ir"] == "unified_runtime_graph"
