/**
 * Converted from Python: core/identity/identity_rotation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildBrowserIdentity } from "./browserIdentityOrchestrator.js";
import { PROFILE_IDS } from "./browserProfileEngine.js";

export function rotateBrowserIdentity(identity: any): any {
  var current_index: any = py.toInt(py.get(identity, "rotation_index", 0));
  var next_index: any = py.mod(py.add(current_index, 1), py.len(PROFILE_IDS));
  var next_profile: any = py.at(PROFILE_IDS, next_index);
  var rotated: any = buildBrowserIdentity(next_profile);
  py.setItem(rotated, "rotation_index", next_index);
  py.setItem(rotated, "previous_profile_id", py.get(identity, "profile_id", "default"));
  return rotated;
}
export { PROFILE_IDS, buildBrowserIdentity };
