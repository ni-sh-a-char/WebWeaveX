/**
 * Converted from Python: core/intent_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export let INTENT_TYPES: any = {"calculator": "ui_app", "weather": "information", "news": "information", "stock": "information", "code": "code_request", "api": "api_request"};
export function _detectType(text: any): any {
  var text_lower: any = String(text).toLowerCase();
  var keyword: any;
  var intent_type: any;
  for ([keyword, intent_type] of py.items(INTENT_TYPES)) {
    if (py.contains(text_lower, keyword)) {
      return intent_type;
    }
  }
  return "generic";
}
export function _extractKeywords(text: any): any {
  var words: any = py.split(String(text).toLowerCase());
  return py.iter(words).filter((w: any) => (py.len(w) > 2)).map((w: any) => w);
}
export function _estimateComplexity(text: any): any {
  var length: any = py.len(py.split(text));
  if ((length <= 2)) {
    return "low";
  } else if ((length <= 5)) {
    return "medium";
  } else {
    return "high";
  }
}
export function resolveIntent(user_input: any): any {
  if (!(typeof user_input === "string")) {
    throw py.err("TypeError", "user_input must be a string");
  }
  if (py.eq(py.strip(user_input), "")) {
    throw py.err("ValueError", "user_input cannot be empty");
  }
  var intent: any = {"type": _detectType(user_input), "goal": user_input, "keywords": _extractKeywords(user_input), "complexity": _estimateComplexity(user_input), "version": "v1_phase_2"};
  return intent;
}
export function validateIntentEngine(): any {
  var test_input: any = "calculator app";
  var result: any = resolveIntent(test_input);
  var required_keys: any = ["type", "goal", "keywords", "complexity", "version"];
  if (!((result !== null && typeof result === "object" && !Array.isArray(result) && !(result instanceof Set) && !(result instanceof Map)))) {
    throw py.err("RuntimeError", "Intent output is not dict");
  }
  var key: any;
  for (key of py.iter(required_keys)) {
    if (!py.contains(result, key)) {
      throw py.err("RuntimeError", `Missing key: ${py.toStr(key)}`);
    }
  }
  if (!py.eq(py.at(result, "goal"), test_input)) {
    throw py.err("RuntimeError", "Goal mismatch");
  }
  if (!(Array.isArray(py.at(result, "keywords")))) {
    throw py.err("RuntimeError", "Keywords must be list");
  }
  return true;
}
