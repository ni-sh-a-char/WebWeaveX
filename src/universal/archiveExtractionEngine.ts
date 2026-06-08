/**
 * Converted from Python: core/universal/archive_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function listArchiveEntries(names: any): any {
  return py.sorted(py.toSet(py.or2(names, () => ([]))));
}
