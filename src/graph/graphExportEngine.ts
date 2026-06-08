/**
 * Converted from Python: core/graph/graph_export_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { dumpsDeterministic } from "../serialize/deterministicSerializer.js";
import { normalizeGraphNodes } from "./graphReconstructionEngine.js";

export function exportGraph(graph: any): any {
  var normalized: any = normalizeGraphNodes((((graph !== null && typeof graph === "object" && !Array.isArray(graph) && !(graph instanceof Set) && !(graph instanceof Map))) ? graph : {}));
  return dumpsDeterministic(normalized);
}
export { dumpsDeterministic, normalizeGraphNodes };
