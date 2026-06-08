/**
 * Converted from Python: core/repository/event_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelEventFlow } from "./eventFlowEngine.js";

export function modelEventCausality(source: any, path: any = ""): any {
  var flow: any = modelEventFlow(source, path);
  var events: any = ((Array.isArray(py.get(flow, "events"))) ? py.get(flow, "events", []) : []);
  var causal: any = py.range(py.max([0, py.sub(py.len(events), 1)])).map((i: any) => ({"cause": py.at(events, i), "effect": py.at(events, py.add(i, 1))}));
  return {"causal_chain": causal, "evidence": [py.get(flow, "evidence", "event_topology")], "deterministic": true};
}
export { modelEventFlow };
