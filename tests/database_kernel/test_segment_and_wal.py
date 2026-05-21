from pathlib import Path

from core.database import replay_wal, write_semantic_segment


def test_write_segment(tmp_path: Path):
    r = write_semantic_segment(str(tmp_path / "seg.json"), [{"id": "a"}])
    assert r["records"] == 1


def test_wal_replay():
    r = replay_wal([{"op": "insert"}, {"op": "commit"}])
    assert r["count"] == 2
