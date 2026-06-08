/**
 * Converted from Python: core/universal/openapi_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseOpenapi(text: any): any {
  var src: any = py.or2(text, () => (""));
  try {
    var obj: any = py.jsonLoads(src);
  } catch (_e: any) {
    obj = {};
  }
  var paths: any = (((obj !== null && typeof obj === "object" && !Array.isArray(obj) && !(obj instanceof Set) && !(obj instanceof Map))) ? py.sorted(py.keys(py.or2(py.get(obj, "paths"), () => ({})))) : []);
  return {"paths": paths, "version": py.toStr(py.or2((((obj !== null && typeof obj === "object" && !Array.isArray(obj) && !(obj instanceof Set) && !(obj instanceof Map))) ? py.get(obj, "openapi") : ""), () => ("")))};
}
