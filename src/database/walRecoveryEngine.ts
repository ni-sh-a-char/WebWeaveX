/**
 * Converted from Python: core/database/wal_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function replayWal(entries: any): any {
  var recovered: any[] = [];
  var entry: any;
  for (entry of py.iter(entries)) {
    py.listAppend(recovered, entry);
  }
  return {"recovered": recovered, "count": py.len(recovered)};
}
