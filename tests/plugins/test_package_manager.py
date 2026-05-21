from core.plugins.semantic_package_manager import (
    SemanticPackageManager,
)


def test_package_install():
    manager = SemanticPackageManager()

    manager.install("semantic-core")

    assert "semantic-core" in manager.list_packages()
