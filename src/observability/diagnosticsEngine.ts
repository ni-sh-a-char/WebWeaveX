/**
 * Converted from Python: core/observability/diagnostics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractionDiagnostics(result: any): any {
  return {"raw_text_bytes": py.len(py.encode(py.or2(py.get(result, "raw_text", ""), () => ("")), "utf-8")), "graph_edges": py.len(py.get(py.get(py.get(result, "relationships", {}), "execution_graph", {}), "edges", [])), "has_repository": py.truthy(py.get(py.get(result, "content", {}), "repository")), "has_documents": py.truthy(py.get(py.get(result, "content", {}), "documents"))};
}
