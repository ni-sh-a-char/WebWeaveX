from __future__ import annotations

from typing import Any, Dict

from core.documents.discourse_dependency_engine import reconstruct_discourse_dependencies
from core.documents.explanation_dependency_engine import reconstruct_explanation_dependencies
from core.documents.semantic_causality_engine import reconstruct_semantic_causality
from core.documents.semantic_dependency_engine import reconstruct_semantic_dependencies
from core.documents.semantic_dependency_reasoning_engine import reason_semantic_dependencies
from core.documents.semantic_flow_engine import reconstruct_semantic_flow
from core.documents.semantic_intent_engine import classify_semantic_intent
from core.documents.semantic_prerequisite_reasoning_engine import reason_prerequisites
from core.documents.semantic_section_reconstruction_engine import reconstruct_semantic_sections
from core.documents.semantic_support_chain_engine import reconstruct_support_chains
from core.documents.tutorial_dependency_engine import reconstruct_tutorial_dependencies


def reconstruct_document_cognition(text: str) -> Dict[str, Any]:
    sections = reconstruct_semantic_sections(text)
    deps = reconstruct_semantic_dependencies(text)
    reasoning = reason_semantic_dependencies(text)
    causality = reconstruct_semantic_causality(text)
    tutorial = reconstruct_tutorial_dependencies(text)
    prereqs = reason_prerequisites(text)
    discourse = reconstruct_discourse_dependencies(text)
    explanations = reconstruct_explanation_dependencies(text)
    support = reconstruct_support_chains(text)
    flow = reconstruct_semantic_flow(text)
    intent = classify_semantic_intent(text)
    causal_structure = causality.get("reconciled", {})
    return {
        "lexical_structure": sections.get("observed", {}).get("lexical", {}),
        "syntactic_structure": sections.get("observed", {}).get("syntactic", {}),
        "semantic_structure": sections.get("inferred", {}).get("semantic", {}),
        "discourse_structure": sections.get("inferred", {}).get("discourse", {}),
        "conceptual_structure": sections.get("inferred", {}).get("conceptual", {}),
        "causal_structure": causal_structure,
        "semantic_dependencies": deps.get("reconciled", {}),
        "tutorial_dependencies": tutorial.get("reconciled", {}),
        "concept_dependencies": prereqs.get("reconciled", {}),
        "causal_dependencies": causal_structure,
        "discourse_dependencies": discourse.get("reconciled", {}),
        "semantic_support_chains": support.get("semantic_support_chains", []),
        "dependency_reasoning": reasoning.get("reconciled", {}),
        "semantic_flow": flow.get("reconciled", {}),
        "tutorial_flow": tutorial.get("reconciled", {}),
        "explanation_dependencies": explanations.get("explanation_dependencies", []),
        "semantic_intent": intent.get("reconciled", {}),
        "evidence": sections.get("evidence", []),
        "lineage": sections.get("lineage", {}),
        "why": sections.get("why", {}),
        "parser_basis": sections.get("parser_basis", {}),
        "graph_basis": sections.get("graph_basis", {}),
        "semantic_basis": sections.get("semantic_basis", {}),
        "confidence_basis": sections.get("confidence_basis", {}),
        "contradictions": sections.get("contradicted", {}),
        "ambiguities": sections.get("ambiguities", []),
        "traceability": sections.get("traceability", {}),
        "uncertainty": sections.get("uncertainty", {}),
    }
