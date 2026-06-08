/**
 * Converted from Python: core/ir/topology_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reasonTopology } from "../graph/topologyReasoningEngine.js";
import { detectCycles } from "../graph/semanticCycleAnalysisEngine.js";
import { emptyLineage } from "./_base.js";

export let TopologyIR: any = py.at(Object, [py.toStr, Object]);
export function compileTopologyIr(graph: any): any {
  var topo: any = reasonTopology(graph);
  var cycles: any = detectCycles(graph);
  return {"topology": topo, "cycles": cycles, "edges": py.get(graph, "edges", []), "lineage": emptyLineage("topology_ir"), "confidence": {"score": (py.truthy(py.get(topo, "proved")) ? py.F(0.9) : py.F(0.4)), "deterministic": true}};
}
export { detectCycles, emptyLineage, reasonTopology };
