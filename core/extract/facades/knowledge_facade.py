from core.knowledge import (
    build_dependency_lineage,
    build_execution_flow,
    build_framework_relationships,
    build_repository_knowledge,
    build_semantic_graph,
    build_service_relationships,
    cluster_semantic_graph,
    reason_over_semantic_graph,
)
from core.knowledge.reconstruction.entity_resolution_engine import resolve_entities
from core.knowledge.reconstruction.concept_graph_engine import build_concept_graph
from core.knowledge.semantic_relationship_v2_engine import build_semantic_relationships as build_knowledge_relationships_v2
from core.knowledge.repository_knowledge_v2_engine import build_repository_knowledge_v2
from core.knowledge.document_knowledge_v2_engine import build_document_knowledge_v2
from core.knowledge.internet_knowledge_v2_engine import build_internet_knowledge_v2
from core.knowledge.architecture_knowledge_v2_engine import build_architecture_knowledge_v2
from core.knowledge.reconstruction import (
    build_architecture_knowledge as build_architecture_knowledge_v18,
    build_concept_graph as build_concept_graph_v18,
    build_dependency_knowledge as build_dependency_knowledge_v18,
    build_documentation_knowledge as build_documentation_knowledge_v18,
    build_repository_knowledge as build_repository_knowledge_v18,
    build_semantic_identity,
    resolve_entities as resolve_entities_v18,
)
