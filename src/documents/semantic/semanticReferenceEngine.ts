/**
 * Converted from Python: core/documents/semantic/semantic_reference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticReferences(text: any): any {
  var source: any = py.or2(text, () => (""));
  var links: any = py.sorted(py.toSet(py.reFindall("https?://[^\\s)\\]>'\\\"]+", source, "")));
  var anchors: any = py.sorted(py.toSet(py.reFindall("\\[[^\\]]+\\]\\((#[^)]+)\\)", source, "")));
  var citations: any = py.sorted(py.toSet(py.reFindall("\\[(\\d+)\\]", source, "")));
  return {"external": links, "anchors": anchors, "citations": citations};
}
