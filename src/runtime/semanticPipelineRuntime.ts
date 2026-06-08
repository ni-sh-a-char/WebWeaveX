/**
 * Converted from Python: core/runtime/semantic_pipeline_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";
import { compileDocumentIr } from "../ir/documentIr.js";
import { compileRepositoryIr } from "../ir/repositoryIr.js";
import { SemanticExecutionGraph } from "./semanticExecutionGraph.js";

export function runSemanticPipeline(steps: any, context: any): any {
  var graph: any = new SemanticExecutionGraph();
  var results: Record<string, any> = {};
  var step: any;
  for (step of py.iter(py.slice(steps, null, 16))) {
    graph.add_node(step, "pipeline_step");
    if ((py.eq(step, "document") && py.truthy(py.get(context, "text")))) {
      py.setItem(results, "document", compileDocumentIr(py.at(context, "text")));
    } else if ((py.eq(step, "repository") && py.truthy(py.get(context, "source")))) {
      py.setItem(results, "repository", compileRepositoryIr(py.at(context, "source"), py.get(context, "path", "")));
    }
  }
  return {"results": results, "graph": graph.to_dict(), "steps_run": py.slice(steps, null, 16)};
}
export { SemanticExecutionGraph, compileDocumentIr, compileRepositoryIr };
