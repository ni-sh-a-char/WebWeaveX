/**
 * Converted from Python: core/reconstruction/browser_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconstructBrowserRuntime(browser_ir: any = null, interaction_ir: any = null, identity: any = null, session: any = null, streaming: any = null, dom: any = null): any {
  browser_ir = py.or2(browser_ir, () => ({}));
  interaction_ir = py.or2(interaction_ir, () => ({}));
  identity = py.or2(identity, () => ({}));
  session = py.or2(session, () => ({}));
  streaming = py.or2(streaming, () => ({}));
  dom = py.or2(dom, () => ({}));
  var tabs: any = py.sorted(py.enumerate(py.or2(py.get(py.get(interaction_ir, "tab_states", {}), "tabs", []), () => (py.or2(py.get(py.get(browser_ir, "routes", {}), "history", []), () => ([{"path": py.get(browser_ir, "url", "/")}]))))).map(([index, route]: any) => ({"id": `tab:${py.toStr(index)}`, "path": py.toStr(py.get(route, "path", ""))})), {key: ((item: any) => py.at(item, "id")) as (item: any) => any});
  var navigation_history: any = py.sorted(py.enumerate(py.or2(py.get(py.get(interaction_ir, "route_transitions", {}), "routes", []), () => (py.or2(py.get(py.get(browser_ir, "navigation", {}), "history", []), () => ([]))))).map(([index, item]: any) => ({"path": py.toStr(py.get(item, "path", "")), "order": py.toInt(py.get(item, "order", index))})), {key: ((item: any) => py.at(item, "order")) as (item: any) => any});
  return {"tabs": tabs, "navigation_history": navigation_history, "dom_structure": py.pyDict(py.get(dom, "structure", py.get(dom, "nodes", {}))), "interaction_flows": py.slice([...py.iter(py.get(interaction_ir, "interactions", []))], null, 1000), "browser_identity": py.pyDict(identity), "authenticated_state": {"authenticated": py.truthy(py.get(session, "authenticated", false)), "cookies": py.sorted(py.get(session, "cookies", []), {key: ((c: any) => py.toStr(py.get(c, "name", ""))) as (item: any) => any})}, "storage": {"local": py.pyDict(py.get(session, "local_storage", {})), "session": py.pyDict(py.get(session, "session_storage", {}))}, "streaming_state": py.pyDict(streaming), "replay_safe": true, "bounded": true};
}
