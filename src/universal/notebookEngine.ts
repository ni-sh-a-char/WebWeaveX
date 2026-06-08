/**
 * Converted from Python: core/universal/notebook_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseNotebook(text: any): any {
  var src: any = py.or2(text, () => (""));
  try {
    var obj: any = py.jsonLoads(src);
  } catch (_e: any) {
    obj = {};
  }
  var cells: any = (((obj !== null && typeof obj === "object" && !Array.isArray(obj) && !(obj instanceof Set) && !(obj instanceof Map))) ? py.get(obj, "cells", []) : []);
  var cell_types: any = py.sorted(py.iter(cells).filter((c: any) => ((c !== null && typeof c === "object" && !Array.isArray(c) && !(c instanceof Set) && !(c instanceof Map)))).map((c: any) => py.get(c, "cell_type", "")));
  return {"cell_count": py.len(cells), "cell_types": cell_types};
}
