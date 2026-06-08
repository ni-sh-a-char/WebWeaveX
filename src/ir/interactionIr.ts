/**
 * Converted from Python: core/ir/interaction_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileInteractionIr(interactions: any, navigation_graph: any, modal_states: any, tab_states: any, route_transitions: any, replay_log: any, scroll_runtime: any = null, pagination_runtime: any = null): any {
  return {"ir": "interaction_runtime", "interactions": [...py.iter(interactions)], "navigation_graph": navigation_graph, "modal_states": modal_states, "tab_states": tab_states, "route_transitions": route_transitions, "replay_log": replay_log, "scroll_runtime": py.or2(scroll_runtime, () => ({"bounded": true})), "pagination_runtime": py.or2(pagination_runtime, () => ({"bounded": true})), "bounded": true};
}
