/**
 * Converted from Python: core/engineering/semantic_incident_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_INCIDENT_EVENTS: any = 10000;
export function reconstructSemanticIncident(events: any): any {
  var ordered: any = py.slice(py.sorted(events, {key: ((x: any) => [py.get(x, "timestamp", 0), py.toStr(py.get(x, "id"))]) as (item: any) => any}), null, MAX_INCIDENT_EVENTS);
  return {"incident_path": ordered, "bounded": true};
}
