/**
 * Converted from Python: core/reasoning/topology_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reasonTopology } from "../graph/topologyReasoningEngine.js";
import { detectCycles } from "../graph/semanticCycleAnalysisEngine.js";

export function reasonTopologySemantic(graph: any): any {
  var topo: any = reasonTopology(graph);
  var cycles: any = detectCycles(graph);
  return {...(topo), "cycles": cycles, "contradiction_pressure": py.get(cycles, "contradiction_pressure", 0), "explainable": true};
}
export { detectCycles, reasonTopology };
