/**
 * Converted from Python: core/universal/adaptive_parser_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseAdaptive(text: any, fmt: any): any {
  var src: any = py.or2(text, () => (""));
  if (py.eq(fmt, "json")) {
    try {
      var obj: any = py.jsonLoads(src);
      if (((obj !== null && typeof obj === "object" && !Array.isArray(obj) && !(obj instanceof Set) && !(obj instanceof Map)))) {
        return {"kind": "json-object", "keys": py.sorted(py.keys(obj))};
      }
      if ((Array.isArray(obj))) {
        return {"kind": "json-array", "length": py.len(obj)};
      }
    } catch (_e: any) {
      return {"kind": "json-invalid"};
    }
  }
  return {"kind": `${py.toStr(fmt)}-text`, "length": py.len(src)};
}
