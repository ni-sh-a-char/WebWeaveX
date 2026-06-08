/**
 * Converted from Python: core/streaming/memory_guard.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function enforceMemoryLimit(text: any, max_bytes: any = 5000000): any {
  var raw: any = py.encode(py.or2(text, () => ("")), "utf-8");
  if ((py.len(raw) <= max_bytes)) {
    return py.or2(text, () => (""));
  }
  return py.decode(py.slice(raw, null, max_bytes), "utf-8");
}
