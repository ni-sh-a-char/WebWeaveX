from core.actors import (
    SemanticActorSystem,
)


def test_actor_system():

    system = (
        SemanticActorSystem()
    )

    system.create_actor("a")

    system.send(
        "a",
        {"x": 1},
    )

    r = system.receive("a")

    assert r["x"] == 1
