/**
 * Converted from Python: core/identity/language_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _LANGUAGES: any = {"default": ["en-US", "en"], "profile_a": ["en-GB", "en"], "profile_b": ["en-US", "en"]};
export function buildLanguageRuntime(profile_id: any = "default"): any {
  var profile: any = (py.contains(_LANGUAGES, profile_id) ? profile_id : "default");
  return {"languages": [...py.iter(py.at(_LANGUAGES, profile))], "bounded": true};
}
