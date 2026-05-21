from core.federation.repository_federation_engine import (
    federate_repositories,
)


def test_federation():

    r = federate_repositories([
        {
            "nodes": [
                {"id": "a"}
            ]
        }
    ])

    assert r["federated"] is True
