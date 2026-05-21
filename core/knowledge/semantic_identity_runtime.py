from __future__ import annotations

from core.knowledge.semantic_identity_resolver import resolve_semantic_identities


def resolve_identities_runtime(entities, namespace=""):
    return resolve_semantic_identities(entities, namespace)
