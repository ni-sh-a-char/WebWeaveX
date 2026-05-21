from core.repository.repository_ingestion_engine import (
    ingest_repository,
)


def test_repository_ingestion_exists():
    result = ingest_repository(".")

    assert "bounded" in result
    assert result.get("available") is True
    assert result["file_count"] >= 1


def test_repository_ingestion_missing_path(tmp_path):
    missing = tmp_path / "does_not_exist"
    result = ingest_repository(str(missing))

    assert result["available"] is False
