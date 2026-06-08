/**
 * Converted from Python: core/database/semantic_wal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticWAL {
  declare entries: any;
  constructor() {
    this.entries = [];
  }
  append(entry: any): any {
    py.listAppend(this.entries, entry);
  }
  replay(): any {
    return {"entries": [...py.iter(this.entries)], "count": py.len(this.entries)};
  }
}
