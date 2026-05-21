from core.connectors import extract_container_runtime


def test_container_topology():
    snapshot = {
        "containers": [{"id": "c1", "name": "api"}],
        "images": ["webweavex:1.1.1"],
        "networks": ["bridge"],
    }

    first = extract_container_runtime("docker", snapshot)
    second = extract_container_runtime("docker", snapshot)

    assert first == second
    assert first["containers"][0]["id"] == "c1"
