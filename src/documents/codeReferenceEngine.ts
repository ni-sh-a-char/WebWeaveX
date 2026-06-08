/**
 * Converted from Python: core/documents/code_reference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractCodeContext(text: any): any {
  var blocks: any = py.reFindall("```([a-zA-Z0-9_-]*)\\n(.*?)```", py.or2(text, () => ("")), "s");
  return {"count": py.len(blocks), "languages": py.sorted(py.toSet(py.iter(blocks).filter(([lang, _]: any) => py.truthy(lang)).map(([lang, _]: any) => String(lang).toLowerCase()))), "snippets": py.sorted(py.toSet(py.iter(blocks).filter(([_, body]: any) => py.truthy(py.strip(body))).map(([_, body]: any) => py.slice(py.strip(body), null, 200))))};
}
