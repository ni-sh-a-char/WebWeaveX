from core.database.semantic_graph_database import (
    SemanticGraphDatabase,
)


def test_graph_database():

    db = SemanticGraphDatabase()

    db.insert_node({
        "id": "a",
    })

    assert (
        db.query_node("a")["id"]
        == "a"
    )
