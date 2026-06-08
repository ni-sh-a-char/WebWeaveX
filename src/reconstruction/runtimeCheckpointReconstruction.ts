/**
 * Converted from Python: core/reconstruction/runtime_checkpoint_reconstruction.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { restoreReconstructionSnapshot } from "./runtimeSnapshotEngine.js";

export function reconstructFromCheckpoint(checkpoint: any): any {
  var restored: any = restoreReconstructionSnapshot(checkpoint);
  return {"reconstructed_from_checkpoint": true, "state": py.get(restored, "state", {}), "topology": py.get(restored, "topology", {}), "replay_chains": py.get(restored, "replay_chains", []), "bounded": true};
}
export { restoreReconstructionSnapshot };
