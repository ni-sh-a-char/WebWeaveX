/**
 * Converted from Python: core/knowledge/architecture_similarity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function architectureSimilarity(a: any, b: any): any {
  var sa: any = py.toSet(py.get(py.or2(a, () => ({})), "styles", []));
  var sb: any = py.toSet(py.get(py.or2(b, () => ({})), "styles", []));
  var union: any = py.len(py.bitor(sa, sb));
  if (py.eq(union, 0)) {
    return {"score": py.F(1.0), "shared": []};
  }
  var inter: any = py.sorted(py.bitand(sa, sb));
  return {"score": py.div(py.len(inter), union), "shared": inter};
}
