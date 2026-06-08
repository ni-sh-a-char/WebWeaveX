/**
 * Converted from Python: core/agents/agent_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function summarizeForAgent(result: any): any {
  var g: any = py.get(py.get(result, "relationships", {}), "execution_graph", {});
  return {"node_count": py.len(py.get(g, "nodes", [])), "edge_count": py.len(py.get(g, "edges", [])), "confidence": py.get(py.get(result, "metadata", {}), "confidence", py.F(0.0))};
}
