from __future__ import annotations

from typing import Any, Dict

from core.documents.argument_dependency_engine import build_argument_dependencies
from core.documents.concept_progression_engine import model_concept_progression
from core.documents.coreference_graph_engine import build_coreference_graph
from core.documents.document_dependency_graph_engine import build_document_dependency_graph
from core.documents.rhetorical_parser_engine import parse_rhetorical_structure
from core.documents.tutorial_prerequisite_engine import infer_tutorial_prerequisites


def build_document_semantic_ir(text: str) -> Dict[str, Any]:
    return {
        "rhetorical": parse_rhetorical_structure(text),
        "argument": build_argument_dependencies(text),
        "progression": model_concept_progression(text),
        "prerequisites": infer_tutorial_prerequisites(text),
        "coreference": build_coreference_graph(text),
        "dependency_graph": build_document_dependency_graph(text),
        "evidence": [
            "discourse:rhetorical",
            "discourse:argument",
            "discourse:progression",
            "discourse:prerequisites",
        ],
    }
