/**
 * Converted from Python: core/documents/architecture_document_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractArchitectureDocs(text: any): any {
  var src: any = py.or2(text, () => (""));
  var sections: any = py.iter(py.reFinditer("^#{1,6}\\s+(.+)$", src, "m")).filter((m: any) => py.contains(String(m.group(1)).toLowerCase(), "arch")).map((m: any) => py.strip(m.group(1)));
  return {"architecture_sections": py.sorted(py.toSet(sections))};
}
