from core.repository.universal_repository_extraction_engine import (
    extract_repository,
)


def test_extract_repository():
    result = extract_repository(".")

    assert "repository_ir" in result
    assert result["repository_ir"]["ir"] == "repository_runtime"
    assert result["bounded"] is True


def test_extract_repository_has_topology():
    result = extract_repository(".")

    assert "runtime_topology" in result
    assert "languages" in result["repository_ir"]
