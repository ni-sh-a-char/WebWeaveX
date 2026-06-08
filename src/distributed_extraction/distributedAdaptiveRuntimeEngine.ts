/**
 * Converted from Python: core/distributed_extraction/distributed_adaptive_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function synchronizeAdaptiveRuntime(adaptive_states: any): any {
  var healed: Record<string, any> = {};
  var pagination: any[] = [];
  var modals: any[] = [];
  var schemas: any[] = [];
  var state: any;
  for (state of py.iter(adaptive_states)) {
    var memory: any = py.get(state, "memory", py.get(state, "adaptive_runtime", {}));
    py.update(healed, py.get(memory, "healed_selectors", {}));
    py.extend(pagination, py.get(memory, "pagination_patterns", []));
    py.extend(modals, py.get(memory, "modal_solutions", []));
    var schema: any = py.get(state, "schema", {});
    py.listAppend(schemas, [...py.iter(py.get(schema, "fields", []))]);
  }
  var stable_fields: any = py.sorted(py.toSet(py.iter(schemas).flatMap((fields: any) => py.iter(fields).map((field: any) => field))));
  return {"healed_selectors": py.pyDict(py.sorted(py.items(healed))), "pagination_patterns": py.sorted(py.toSet(pagination)), "modal_solutions": py.slice(modals, null, 1000), "stable_schema_fields": stable_fields, "bounded": true};
}
