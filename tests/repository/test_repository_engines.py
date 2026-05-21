from core.repository.repository_api_extraction_engine import (
    extract_repository_apis,
)
from core.repository.repository_dependency_engine import (
    extract_dependencies,
)
from core.repository.repository_infra_detection_engine import (
    detect_repository_infra,
)
from core.repository.repository_language_detection_engine import (
    detect_repository_languages,
)
from core.repository.repository_service_detection_engine import (
    detect_repository_services,
)


def test_detect_languages():
    files = [
        {"path": "a.py", "extension": ".py"},
        {"path": "b.js", "extension": ".js"},
    ]
    result = detect_repository_languages(files)

    assert result["languages"]["python"] == 1
    assert result["primary_language"] == "python"


def test_extract_dependencies():
    source = "import os\nfrom core import x\n"
    result = extract_dependencies(source)

    assert "os" in result["imports"]
    assert "core" in result["imports"]


def test_extract_apis():
    source = '@app.route("/health")\nrouter.get("/items")\n'
    result = extract_repository_apis(source)

    assert "/health" in result["routes"]
    assert "/items" in result["routes"]


def test_detect_services_and_infra():
    files = [
        {"path": "/app/Dockerfile"},
        {"path": "/app/docker-compose.yml"},
    ]
    services = detect_repository_services(files)
    infra = detect_repository_infra(files)

    assert len(services["services"]) == 2
    assert len(infra["infra"]) == 2
