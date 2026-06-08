/**
 * Converted from Python: core/documents/discourse_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_DISCOURSE: any = 200;
export class DiscourseMemory {
  declare _sections: any;
  constructor() {
    this._sections = [];
  }
  remember(section: any): any {
    if ((py.len(this._sections) < MAX_DISCOURSE)) {
      py.listAppend(this._sections, section);
    }
  }
  snapshot(): any {
    var ordered: any = py.sorted(this._sections, {key: ((s: any) => py.toInt(py.get(s, "order", 0))) as (item: any) => any});
    return {"sections": ordered, "count": py.len(ordered), "deterministic": true};
  }
}
