from core.runtime_graph import (
    resolve_canonical_entity,
)


def test_entity_resolution():
    entity = resolve_canonical_entity({
        "name": "OpenAI",
        "type": "company",
    })

    assert entity["canonical_id"]
