/**
 * Converted from Python: core/graph_export_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { dumpsDeterministic } from "./serialize/deterministicSerializer.js";

export function exportGraph(graph: any): any {
  return dumpsDeterministic(graph);
}
export { dumpsDeterministic };
