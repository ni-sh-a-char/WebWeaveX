/**
 * Converted from Python: core/documents/reconstruction/architecture_doc_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractArchitectureSections(text: any): any {
  var vals: any = py.iter(py.reFinditer("^#{1,6}\\s+(.+)$", py.or2(text, () => ("")), "m")).filter((m: any) => py.any(py.iter(["architecture", "design", "system"]).map((k: any) => py.contains(String(m.group(1)).toLowerCase(), k)))).map((m: any) => py.strip(m.group(1)));
  return {"sections": py.sorted(py.toSet(vals))};
}
