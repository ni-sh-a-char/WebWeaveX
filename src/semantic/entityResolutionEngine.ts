/**
 * Converted from Python: core/semantic/entity_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveSemanticEntities(entities: any): any {
  var canonical: Record<string, any> = {};
  var resolved: any[] = [];
  var entity: any;
  for (entity of py.iter(py.sorted(entities, {key: ((item: any) => py.get(item, "id", "")) as (item: any) => any}))) {
    var label: any = py.strip(String(py.toStr(py.get(entity, "label", py.get(entity, "type", "")))).toLowerCase());
    var canonical_id: any = py.get(canonical, label);
    if (!py.truthy(canonical_id)) {
      canonical_id = py.toStr(py.get(entity, "id", ""));
      py.setItem(canonical, label, canonical_id);
    }
    py.listAppend(resolved, {...(entity), "canonical_id": canonical_id, "resolved": true});
  }
  return {"entities": resolved, "canonical_map": canonical, "bounded": true};
}
