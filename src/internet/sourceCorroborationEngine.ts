/**
 * Converted from Python: core/internet/source_corroboration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function corroborateSources(sources: any): any {
  var counts: Record<string, any> = {};
  var s: any;
  for (s of py.iter(py.or2(sources, () => ([])))) {
    var key: any = py.toStr(py.get(s, "url", py.get(s, "id", "")));
    if (py.truthy(key)) {
      py.setItem(counts, key, py.add(py.get(counts, key, 0), 1));
    }
  }
  var corroborated: any = py.items(counts).filter(([k, v]: any) => (v > 1)).map(([k, v]: any) => k);
  return {"corroboration_count": py.len(corroborated), "sources": py.len(py.or2(sources, () => ([]))), "deterministic_inputs": [`corroborated=${py.toStr(py.len(corroborated))}`]};
}
