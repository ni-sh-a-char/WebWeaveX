from __future__ import annotations

from typing import Any, Dict, List


def run_semantic_pipeline(steps: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    from core.ir.document_ir import compile_document_ir
    from core.ir.repository_ir import compile_repository_ir
    from core.runtime.semantic_execution_graph import SemanticExecutionGraph

    graph = SemanticExecutionGraph()
    results: Dict[str, Any] = {}
    for step in steps[:16]:
        graph.add_node(step, "pipeline_step")
        if step == "document" and context.get("text"):
            results["document"] = compile_document_ir(context["text"])
        elif step == "repository" and context.get("source"):
            results["repository"] = compile_repository_ir(context["source"], context.get("path", ""))
    return {"results": results, "graph": graph.to_dict(), "steps_run": steps[:16]}
