from core.repository.kubernetes_semantic_engine import (
    parse_kubernetes_semantics,
)


def test_k8s_parse():

    text = """
apiVersion: v1
kind: Pod
metadata:
  name: app
"""

    r = parse_kubernetes_semantics(text)

    assert r["count"] == 1
