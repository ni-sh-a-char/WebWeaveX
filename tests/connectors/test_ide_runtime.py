from core.connectors import extract_ide_runtime


def test_ide_runtime_vscode():
    snapshot = {
        "open_files": ["main.py", "README.md"],
        "terminals": [{"id": "t1"}],
        "tabs": ["main.py"],
    }

    ide = extract_ide_runtime("vscode", snapshot)

    assert ide["ide"] == "vscode"
    assert "main.py" in ide["open_files"]
