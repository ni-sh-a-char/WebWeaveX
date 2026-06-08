/**
 * Converted from Python: core/runtime/semantic_journal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export class SemanticJournal {
  declare entries: any;
  constructor() {
    this.entries = [];
  }
  record(event: any): any {
    py.listAppend(this.entries, event);
  }
  replay(): any {
    return {"entries": [...py.iter(this.entries)], "count": py.len(this.entries)};
  }
}
