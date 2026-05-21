from core.repository.docker_semantic_engine import (
    parse_dockerfile_semantics,
)


def test_docker_parse():

    text = """
FROM python:3.11
RUN pip install flask
"""

    r = parse_dockerfile_semantics(text)

    assert r["count"] == 2
