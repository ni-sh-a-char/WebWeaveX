/**
 * Converted from Python: core/documents/semantic/semantic_diagram_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticDiagrams(text: any): any {
  var source: any = py.or2(text, () => (""));
  var mermaid: any = py.reFindall("```mermaid\\n(.*?)```", source, "s");
  var plantuml: any = py.reFindall("```plantuml\\n(.*?)```", source, "s");
  var images: any = py.sorted(py.toSet(py.reFindall("!\\[[^\\]]*\\]\\(([^)]+)\\)", source, "")));
  return {"mermaid": py.sorted(py.toSet(py.iter(mermaid).filter((m: any) => py.truthy(py.strip(m))).map((m: any) => py.strip(m)))), "plantuml": py.sorted(py.toSet(py.iter(plantuml).filter((p: any) => py.truthy(py.strip(p))).map((p: any) => py.strip(p)))), "image_refs": images};
}
