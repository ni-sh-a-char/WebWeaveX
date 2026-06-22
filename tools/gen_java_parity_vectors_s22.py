#!/usr/bin/env python3
"""Session-22 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s22.py <out.json>

Covers query_documents + the 21 pure document semantic-IR engines. The tutorial path's
structure_cognition only contributes passthrough fields (no epistemic math reaches the output,
verified), so this is byte-exact without the epistemic engine. Python is the oracle.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.query.document_query_engine import query_documents
from core.documents.document_semantic_ir_engine import build_document_semantic_ir
from core.documents.rhetorical_structure_engine import extract_rhetorical_structure
from core.documents.semantic_role_engine import assign_semantic_roles
from core.documents.rhetorical_parser_engine import parse_rhetorical_structure
from core.documents.argument_dependency_engine import build_argument_dependencies
from core.documents.argument_graph_engine import build_argument_graph
from core.documents.semantic_discourse_parser import parse_semantic_discourse
from core.documents.concept_transition_engine import model_concept_transitions
from core.documents.semantic_transition_engine import model_semantic_transitions
from core.documents.concept_progression_engine import model_concept_progression
from core.documents.heading_engine import extract_headings
from core.documents.section_engine import extract_sections
from core.documents.instructional_flow_engine import extract_instructional_flow
from core.documents.instructional_semantics_engine import analyze_instructional_semantics
from core.documents.tutorial_prerequisite_engine import infer_tutorial_prerequisites
from core.documents.coreference_resolution_engine import resolve_coreferences
from core.documents.coreference_graph_engine import build_coreference_graph
from core.documents.document_dependency_graph_engine import build_document_dependency_graph

DOCS = [
    ("empty", ""),
    ("simple", "# Setup\nFirst install the package.\n## Step 1: Configure\n"
               "Because it needs config, set the key.\nTherefore run init.\n- item one\n"
               "## Step 2: Run\nThen execute it. Note: backup first."),
    ("headings_html", "<h1>Intro</h1>\n## Markdown Head\n<h2>Sub</h2>\nSome text it refers to this."),
    ("numbered", "1. first step\n2. second step\n3. third step\nFor example, do X."),
    ("roles", "Because reasons.\nTherefore conclusion.\nNote: be careful.\nFor instance, an example."),
    ("unicode", "# Café Setup\nInstall café-tool.\n## Étape 1\nThis is café. They love it."),
    ("code_fence", "# Title\n```\ncode here\n```\n- bullet\nThus done."),
]


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 22: document semantic IR + query_documents)"}

    out["query_documents"] = [ev(n, {"text": t}, query_documents(t)) for n, t in DOCS]

    def section(name, fn):
        out[name] = [ev(n, {"text": t}, fn(t)) for n, t in DOCS]

    section("build_document_semantic_ir", build_document_semantic_ir)
    section("extract_rhetorical_structure", extract_rhetorical_structure)
    section("assign_semantic_roles", assign_semantic_roles)
    section("parse_rhetorical_structure", parse_rhetorical_structure)
    section("build_argument_dependencies", build_argument_dependencies)
    section("build_argument_graph", build_argument_graph)
    section("parse_semantic_discourse", parse_semantic_discourse)
    section("model_concept_transitions", model_concept_transitions)
    section("model_semantic_transitions", model_semantic_transitions)
    section("model_concept_progression", model_concept_progression)
    section("extract_headings", extract_headings)
    section("extract_sections", extract_sections)
    section("extract_instructional_flow", extract_instructional_flow)
    section("analyze_instructional_semantics", analyze_instructional_semantics)
    section("infer_tutorial_prerequisites", infer_tutorial_prerequisites)
    section("resolve_coreferences", resolve_coreferences)
    section("build_coreference_graph", build_coreference_graph)
    section("build_document_dependency_graph", build_document_dependency_graph)

    from core.documents.argument_dependency_engine import reconstruct_argument_dependencies
    rad_cases = [
        ("seq", [{"id": "c0", "order": 0}, {"id": "c1", "order": 1}, {"id": "c2", "order": 2}]),
        ("explicit", [{"id": "a", "order": 0}, {"id": "b", "order": 1, "depends_on": "a"}]),
        ("empty", []),
        ("over_cap", [{"id": "c%d" % i, "order": i} for i in range(305)]),
    ]
    out["reconstruct_argument_dependencies"] = [
        ev(n, {"claims": cl}, reconstruct_argument_dependencies(cl)) for n, cl in rad_cases
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s22.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
