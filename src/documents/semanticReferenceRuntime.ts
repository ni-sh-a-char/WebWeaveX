/**
 * Converted from Python: core/documents/semantic_reference_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveSemanticReferences(refs: any): any {
  var resolved: any[] = [];
  var ref: any;
  for (ref of py.iter(py.sorted(refs, {key: ((r: any) => py.toStr(py.get(r, "target", ""))) as (item: any) => any}))) {
    py.listAppend(resolved, {"source": py.get(ref, "source"), "target": py.get(ref, "target"), "resolved": py.truthy(py.get(ref, "target"))});
  }
  return {"references": resolved, "count": py.len(resolved), "deterministic": true};
}
