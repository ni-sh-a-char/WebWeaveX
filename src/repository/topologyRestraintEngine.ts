/**
 * Converted from Python: core/repository/topology_restraint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { suppressSpeculativeTopologyEdge } from "./speculativeTopologyEngine.js";

export function restrainTopologyEdge(edge: any): any {
  var humbled: any = suppressSpeculativeTopologyEdge(edge);
  var suppressed: any = py.get(py.get(humbled, "unsupported", {}), "edge", false);
  return {...(humbled), "observed": py.get(edge, "observed", {}), "inferred": py.get(edge, "inferred", {}), "restraint": {"conservative": true, "propagation_allowed": !py.truthy(suppressed)}};
}
export { suppressSpeculativeTopologyEdge };
