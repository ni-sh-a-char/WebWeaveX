/**
 * Converted from Python: core/native/electron/electron_storage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractElectronStorage(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  var indexed_db: any = py.sorted(py.get(snap, "indexed_db", []), {key: ((item: any) => py.toStr(py.get(item, "name", ""))) as (item: any) => any});
  var local_storage: any = py.pyDict(py.sorted(py.items(py.or2(py.get(snap, "local_storage"), () => ({})))));
  var session_storage: any = py.pyDict(py.sorted(py.items(py.or2(py.get(snap, "session_storage"), () => ({})))));
  return {"indexed_db": indexed_db, "local_storage": local_storage, "session_storage": session_storage, "bounded": true};
}
