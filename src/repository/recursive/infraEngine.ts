/**
 * Converted from Python: core/repository/recursive/infra_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractInfra(text: any): any {
  var src: any = String(py.or2(text, () => (""))).toLowerCase();
  var out: any = py.iter(["terraform", "kubernetes", "helm", "docker"]).filter((k: any) => py.contains(src, k)).map((k: any) => k);
  return {"infra_stack": py.sorted(py.toSet(out))};
}
