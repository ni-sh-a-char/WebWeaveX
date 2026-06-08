/**
 * Converted from Python: core/evolution/semantic_adaptation_policy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function enforceAdaptationPolicies(runtime: any, policies: any): any {
  var allowed: any[] = [];
  var denied: any[] = [];
  var policy: any;
  for (policy of py.iter(policies)) {
    var key: any = py.get(policy, "key");
    if ((py.truthy(key) && py.contains(runtime, key))) {
      py.listAppend(allowed, policy);
    } else {
      py.listAppend(denied, policy);
    }
  }
  return {"allowed": allowed, "denied": denied};
}
