/**
 * Converted from Python: core/autonomy/semantic_semanticity_validator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let REQUIRED_KEYS: any = ["goal"];
export function validateSemanticity(payload: any): any {
  var missing: any = py.iter(REQUIRED_KEYS).filter((key: any) => !py.truthy(py.get(payload, key))).map((key: any) => key);
  return {"semantic": !py.truthy(missing), "missing_keys": missing};
}
