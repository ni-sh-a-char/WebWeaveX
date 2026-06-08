/**
 * Converted from Python: core/connectors/kubernetes_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractKubernetesRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"namespaces": py.sorted(py.get(snap, "namespaces", ["default"]), {key: (py.toStr) as (item: any) => any}), "pods": py.sorted(py.get(snap, "pods", []), {key: ((item: any) => py.toStr(py.get(item, "name", item))) as (item: any) => any}), "deployments": py.sorted(py.get(snap, "deployments", []), {key: ((item: any) => py.toStr(py.get(item, "name", item))) as (item: any) => any}), "services": [...py.iter(py.get(snap, "services", []))], "ingress": [...py.iter(py.get(snap, "ingress", []))], "topology": py.pyDict(py.get(snap, "topology", {})), "events": py.slice([...py.iter(py.get(snap, "events", []))], null, 5000), "degraded": py.get(snap, "degraded", false), "bounded": true};
}
