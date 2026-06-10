"""Execute Python (canonical) semantic-IR closure functions; emit output + hash.
Usage: PYTHONPATH=<py2.0.1> python run_python.py fixtures.json > python_results.json
"""
import importlib
import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H

# fn name -> module path (canonical source location)
REGISTRY = {
    # A.1 — core.documents leaves
    "extract_rhetorical_structure": "core.documents.rhetorical_structure_engine",
    "assign_semantic_roles": "core.documents.semantic_role_engine",
    "extract_headings": "core.documents.heading_engine",
    "reconstruct_argument_dependencies": "core.documents.argument_dependency_engine",
    "resolve_coreferences": "core.documents.coreference_resolution_engine",
    # A.2 — core.semantic pressure leaves
    "compute_ambiguity_pressure": "core.semantic.ambiguity_pressure_engine",
    "compute_contradiction_pressure": "core.semantic.contradiction_pressure_engine",
    "compute_evidence_boundary_pressure": "core.semantic.evidence_boundary_pressure_engine",
    "compute_evidence_decay_pressure": "core.semantic.evidence_decay_pressure_engine",
    "compute_recursive_boundary_pressure": "core.semantic.recursive_boundary_pressure_engine",
    "compute_recursive_convergence_pressure": "core.semantic.recursive_convergence_pressure_engine",
    "compute_recursive_dependency_pressure": "core.semantic.recursive_dependency_pressure_engine",
    "compute_semantic_boundary_pressure": "core.semantic.semantic_boundary_pressure_engine",
    "compute_truth_boundary_pressure": "core.semantic.truth_boundary_pressure_engine",
    "compute_uncertainty_pressure": "core.semantic.uncertainty_pressure_engine",
    # A.2 — core.ir._base leaves
    "empty_confidence": "core.ir._base",
    "empty_lineage": "core.ir._base",
    "merge_evidence": "core.ir._base",
    # A.2 — core.graph leaves
    "model_graph_entropy": "core.graph.graph_entropy_engine",
    "detect_cycles": "core.graph.semantic_cycle_analysis_engine",
    "prove_topology": "core.graph.topology_proof_engine",
    # A.2 — core.repository leaves
    "reason_api_surface": "core.repository.api_surface_reasoning_engine",
    "reconstruct_execution_flow": "core.repository.execution_flow_engine",
    "detect_infra_signals": "core.repository.infra_semantic_engine",
    "resolve_runtime_dependencies": "core.repository.runtime_dependency_engine",
    "infer_service_interactions": "core.repository.service_interaction_engine",
    # A.2 — core.ast leaves
    "build_control_flow_graph": "core.ast.control_flow_engine",
    "reconstruct_execution_paths": "core.ast.execution_path_engine",
    "resolve_symbols": "core.ast.symbol_resolution_engine",
}


def main():
    fixtures = json.load(open(sys.argv[1], encoding="utf-8"))
    out = []
    for fx in fixtures:
        fn = fx["fn"]
        try:
            mod = importlib.import_module(REGISTRY[fn])
            result = getattr(mod, fn)(*fx["args"])
            out.append({"id": fx["id"], "fn": fn, "output": result, "hash": H(result)})
        except Exception as e:  # noqa: BLE001
            out.append({"id": fx["id"], "fn": fn,
                        "error": f"{type(e).__name__}: {e}"})
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
