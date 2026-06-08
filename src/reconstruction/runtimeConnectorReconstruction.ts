/**
 * Converted from Python: core/reconstruction/runtime_connector_reconstruction.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _CONNECTOR_KINDS: any = ["database", "api", "kubernetes", "docker", "telemetry", "ide", "cicd"];
export function reconstructConnectorRuntime(connectors: any = null, live_ir: any = null): any {
  connectors = py.or2(connectors, () => ([]));
  live_ir = py.or2(live_ir, () => ({}));
  var rebuilt: any[] = [];
  var index: any;
  var connector: any;
  for ([index, connector] of py.enumerate(py.slice(connectors, null, 1000))) {
    var kind: any = py.toStr(py.get(connector, "kind", py.get(connector, "type", "api")));
    if (!py.contains(_CONNECTOR_KINDS, kind)) {
      kind = "api";
    }
    py.listAppend(rebuilt, {"id": py.toStr(py.get(connector, "id", `connector:${py.toStr(index)}`)), "kind": kind, "state": py.pyDict(py.get(connector, "state", {})), "reconstructed": true});
  }
  var streams: any = py.get(live_ir, "streams", py.get(live_ir, "connectors", []));
  if (((streams !== null && typeof streams === "object" && !Array.isArray(streams) && !(streams instanceof Set) && !(streams instanceof Map)))) {
    streams = py.get(streams, "streams", []);
  }
  return {"connectors": py.sorted(rebuilt, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "streams": ((Array.isArray(streams)) ? py.slice([...py.iter(streams)], null, 1000) : []), "bounded": true};
}
