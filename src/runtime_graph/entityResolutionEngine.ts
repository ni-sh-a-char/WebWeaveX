/**
 * Converted from Python: core/runtime_graph/entity_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveCanonicalEntity(entity: any): any {
  var name: any = String(py.strip(py.toStr(py.get(entity, "name", "")))).toLowerCase();
  var entity_type: any = String(py.strip(py.toStr(py.get(entity, "type", "")))).toLowerCase();
  var canonical: any = `${py.toStr(entity_type)}:${py.toStr(name)}`;
  var fingerprint: any = py.hashNew("sha256", py.encode(canonical, "utf-8")).hexdigest();
  return {"canonical_id": fingerprint, "canonical_key": canonical, "entity": entity, "bounded": true};
}
