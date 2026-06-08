/**
 * Converted from Python: core/documents/semantic/semantic_example_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticExamples(text: any): any {
  var source: any = py.or2(text, () => (""));
  var fenced: any = py.reFindall("```([a-zA-Z0-9_-]*)\\n(.*?)```", source, "s");
  return {"count": py.len(fenced), "languages": py.sorted(py.toSet(py.iter(fenced).filter(([lang, _]: any) => py.truthy(lang)).map(([lang, _]: any) => String(lang).toLowerCase()))), "snippets": py.sorted(py.toSet(py.iter(fenced).filter(([_, snippet]: any) => py.truthy(py.strip(snippet))).map(([_, snippet]: any) => py.slice(py.strip(snippet), null, 200))))};
}
