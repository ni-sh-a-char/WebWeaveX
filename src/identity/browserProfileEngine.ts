/**
 * Converted from Python: core/identity/browser_profile_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHash } from "../crypto/kaalkaHashEngine.js";

export let PROFILE_IDS: any = ["default", "profile_a", "profile_b"];
export function buildBrowserProfile(profile_id: any = "default"): any {
  var bounded_id: any = (py.contains(PROFILE_IDS, profile_id) ? profile_id : "default");
  var seed: any = computeKaalkaHash(bounded_id);
  return {"profile_id": bounded_id, "profile_seed": seed, "rotation_index": 0, "bounded": true};
}
export { computeKaalkaHash };
