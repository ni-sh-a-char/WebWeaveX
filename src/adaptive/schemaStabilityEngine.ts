/**
 * Converted from Python: core/adaptive/schema_stability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function stabilizeExtractionSchema(payload: any): any {
  var stabilized: Record<string, any> = {};
  var key: any;
  for (key of py.iter(py.sorted(py.keys(payload)))) {
    var value: any = py.at(payload, key);
    if (((value !== null && typeof value === "object" && !Array.isArray(value) && !(value instanceof Set) && !(value instanceof Map)))) {
      py.setItem(stabilized, key, stabilizeExtractionSchema(value));
    } else if ((Array.isArray(value))) {
      py.setItem(stabilized, key, py.iter(value).map((item: any) => (((item !== null && typeof item === "object" && !Array.isArray(item) && !(item instanceof Set) && !(item instanceof Map))) ? stabilizeExtractionSchema(item) : item)));
    } else {
      py.setItem(stabilized, key, value);
    }
  }
  return {"schema": stabilized, "fields": py.sorted(_collectFields(stabilized)), "bounded": true};
}
export function _collectFields(payload: any, prefix: any = ""): any {
  var fields: any[] = [];
  if (((payload !== null && typeof payload === "object" && !Array.isArray(payload) && !(payload instanceof Set) && !(payload instanceof Map)))) {
    var key: any;
    for (key of py.iter(py.sorted(py.keys(payload)))) {
      var path: any = (py.truthy(prefix) ? `${py.toStr(prefix)}.${py.toStr(key)}` : py.toStr(key));
      py.listAppend(fields, path);
      py.extend(fields, _collectFields(py.at(payload, key), path));
    }
  }
  return fields;
}
