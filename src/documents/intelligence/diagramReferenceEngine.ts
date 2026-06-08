/**
 * Converted from Python: core/documents/intelligence/diagram_reference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractDiagramRefs(text: any): any {
  var src: any = py.or2(text, () => (""));
  var refs: any = py.sorted(py.toSet(py.reFindall("(?:mermaid|plantuml|diagram)[: ]", src, "i")));
  return {"diagram_references": refs};
}
