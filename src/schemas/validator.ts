/**
 * Converted from Python: core/schemas/validator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _loadSchema(filename: any): any {
  var base: any = py.div(py.path(py.metaFile(import.meta.url)).parent, "contracts");
  return py.jsonLoads(py.div(base, filename).read_text("utf-8"));
}
export function _checkType(expected: any, value: any): any {
  if (py.eq(expected, "object")) {
    return ((value !== null && typeof value === "object" && !Array.isArray(value) && !(value instanceof Set) && !(value instanceof Map)));
  }
  if (py.eq(expected, "array")) {
    return (Array.isArray(value));
  }
  if (py.eq(expected, "string")) {
    return (typeof value === "string");
  }
  if (py.eq(expected, "integer")) {
    return py.and2(((typeof value === "number" && Number.isInteger(value))), () => (!(typeof value === "boolean")));
  }
  if (py.eq(expected, "number")) {
    return py.and2(((typeof value === "number" && Number.isInteger(value)) || typeof value === "number"), () => (!(typeof value === "boolean")));
  }
  if (py.eq(expected, "boolean")) {
    return (typeof value === "boolean");
  }
  if (py.eq(expected, "null")) {
    return (value === null || value === undefined);
  }
  return true;
}
export function _validate(schema: any, data: any): any {
  var schema_type: any = py.get(schema, "type");
  if (((typeof schema_type === "string") && !py.truthy(_checkType(schema_type, data)))) {
    return false;
  }
  if (!((data !== null && typeof data === "object" && !Array.isArray(data) && !(data instanceof Set) && !(data instanceof Map)) || Array.isArray(data))) {
    return true;
  }
  if (((data !== null && typeof data === "object" && !Array.isArray(data) && !(data instanceof Set) && !(data instanceof Map)))) {
    var required: any = py.get(schema, "required", []);
    var key: any;
    for (key of py.iter(required)) {
      if (!py.contains(data, key)) {
        return false;
      }
    }
    var properties: any = py.get(schema, "properties", {});
    var value: any;
    for ([key, value] of py.items(data)) {
      if (py.contains(properties, key)) {
        if (!py.truthy(_validate(py.at(properties, key), value))) {
          return false;
        }
      } else if ((py.get(schema, "additionalProperties") === false)) {
        return false;
      }
    }
  }
  if ((Array.isArray(data))) {
    var item_schema: any = py.get(schema, "items");
    if (((item_schema !== null && typeof item_schema === "object" && !Array.isArray(item_schema) && !(item_schema instanceof Set) && !(item_schema instanceof Map)))) {
      var item: any;
      for (item of py.iter(data)) {
        if (!py.truthy(_validate(item_schema, item))) {
          return false;
        }
      }
    }
  }
  return true;
}
export function validateContract(data: any, contract: any): any {
  var schema: any = _loadSchema(contract);
  return _validate(schema, data);
}
