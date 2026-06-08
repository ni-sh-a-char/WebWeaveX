/**
 * Converted from Python: core/universal/infra_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseInfra(text: any): any {
  var src: any = String(py.or2(text, () => (""))).toLowerCase();
  var infra: any[] = [];
  var k: any;
  for (k of py.iter(["terraform", "kubernetes", "helm", "dockerfile", "compose"])) {
    if (py.contains(src, k)) {
      py.listAppend(infra, k);
    }
  }
  return {"infra_components": py.sorted(py.toSet(infra))};
}
