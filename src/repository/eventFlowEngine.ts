/**
 * Converted from Python: core/repository/event_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { inferEventTopology } from "./eventTopologyEngine.js";

export function modelEventFlow(source: any, path: any = ""): any {
  var topo: any = inferEventTopology(source, path);
  return {"events": py.get(topo, "events", []), "evidence": py.get(topo, "evidence", ""), "topology": topo};
}
export { inferEventTopology };
