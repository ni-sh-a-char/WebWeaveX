/**
 * Converted from Python: core/documents/explanation_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructDiscourseDependencies } from "./discourseDependencyEngine.js";

export function buildExplanationGraph(text: any): any {
  var deps: any = reconstructDiscourseDependencies(text);
  var flow: any = py.or2(py.get(py.get(deps, "reconciled", {}), "discourse_flow", []), () => ([]));
  return {"explains": py.iter(flow).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => ({"from": py.get(e, "from"), "to": py.get(e, "to")})), "edge_count": py.len(flow), "deterministic_inputs": [`edges=${py.toStr(py.len(flow))}`]};
}
export { reconstructDiscourseDependencies };
