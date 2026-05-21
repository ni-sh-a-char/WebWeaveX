import tempfile
from pathlib import Path

from core.persistence import write_semantic_storage


def test_write_semantic_storage(tmp_path: Path):
    path = str(tmp_path / "semantic.json")
    r = write_semantic_storage(path, {"nodes": [{"id": "a"}]})
    assert r["written"] is True
    assert Path(path).exists()
