from core.native.native_window_engine import extract_native_windows
from core.native.native_ui_graph_engine import build_native_ui_graph
from core.native.accessibility_tree_engine import extract_accessibility_tree


def test_window_stability():
    snapshot = {
        "windows": [
            {
                "id": "w1",
                "title": "App",
                "z_order": 2,
                "focused": True,
            },
            {
                "id": "w2",
                "title": "Background",
                "z_order": 1,
            },
        ],
        "focused_window": "App",
    }

    first_windows = extract_native_windows(snapshot)
    second_windows = extract_native_windows(snapshot)

    accessibility = extract_accessibility_tree({"nodes": []})
    first_graph = build_native_ui_graph(first_windows, accessibility, [])
    second_graph = build_native_ui_graph(second_windows, accessibility, [])

    assert first_windows == second_windows
    assert first_graph == second_graph
