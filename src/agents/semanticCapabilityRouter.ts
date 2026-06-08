/**
 * Converted from Python: core/agents/semantic_capability_router.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function routeSemanticCapability(capability: any, agents: any): any {
  var ordered: any = py.sorted(agents, {key: ((x: any) => py.toStr(py.get(x, "id"))) as (item: any) => any});
  var agent: any;
  for (agent of py.iter(ordered)) {
    if (py.contains(py.get(agent, "capabilities", []), capability)) {
      return {"selected": py.get(agent, "id"), "capability": capability};
    }
  }
  return {"selected": null, "capability": capability};
}
