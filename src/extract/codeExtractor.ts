/**
 * Converted from Python: core/extract/code_extractor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractCodeFeatures(text: any): any {
  var src: any = py.or2(text, () => (""));
  var imports: any = py.sorted(py.toSet(py.reFindall("^\\s*(?:import|from)\\s+([A-Za-z0-9_\\.]+)", src, "m")));
  var exports: any = py.sorted(py.toSet(py.reFindall("^\\s*export\\s+(?:default\\s+)?(?:const|class|function)?\\s*([A-Za-z0-9_]+)?", src, "m")));
  return {"imports": imports, "exports": py.iter(exports).filter((e: any) => py.truthy(e)).map((e: any) => e)};
}
