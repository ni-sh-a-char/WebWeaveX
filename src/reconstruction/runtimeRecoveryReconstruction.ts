/**
 * Converted from Python: core/reconstruction/runtime_recovery_reconstruction.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recoverReconstructedRuntime(checkpoint: any = null, failed_segments: any = null): any {
  checkpoint = py.or2(checkpoint, () => ({}));
  var failed: any = [...py.iter(py.or2(failed_segments, () => ([])))];
  return {"checkpoint_restored": py.truthy(checkpoint), "failed_segments_recovered": py.len(failed), "segments": py.sorted(failed, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "replay_safe": true, "bounded": true};
}
