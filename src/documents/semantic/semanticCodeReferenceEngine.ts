/**
 * Converted from Python: core/documents/semantic/semantic_code_reference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticCodeReferences(text: any): any {
  var source: any = py.or2(text, () => (""));
  var inline: any = py.sorted(py.toSet(py.reFindall("`([^`]+)`", source, "")));
  var symbols: any = py.sorted(py.toSet(py.iter(inline).filter((i: any) => (py.contains(i, "(") || py.contains(i, ".") || py.contains(i, "/"))).map((i: any) => i)));
  return {"inline": inline, "symbols": symbols};
}
