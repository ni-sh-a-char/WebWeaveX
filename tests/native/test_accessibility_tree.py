from core.native.accessibility_tree_engine import extract_accessibility_tree
from core.native.native_memory_engine import save_native_runtime, load_native_runtime


def test_accessibility_extraction():
    snapshot = {
        "nodes": [
            {"id": "b1", "role": "button", "name": "Submit"},
            {"id": "f1", "role": "textbox", "name": "Email"},
            {"id": "d1", "role": "dialog", "name": "Confirm"},
        ],
    }

    tree = extract_accessibility_tree(snapshot, backend="uia")

    assert len(tree["buttons"]) == 1
    assert len(tree["text_inputs"]) == 1
    assert len(tree["dialogs"]) == 1
