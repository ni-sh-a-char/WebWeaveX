/**
 * Converted from Python: core/documents/reconstruction/dependency_reference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractDependencyReferences(text: any): any {
  var src: any = py.or2(text, () => (""));
  var refs: any = py.sorted(py.toSet(py.reFindall("(?:pip install|npm install|cargo add|pub add)\\s+([A-Za-z0-9_.@/-]+)", src, "")));
  return {"dependencies": refs};
}
