/**
 * Converted from Python: core/evidence/recursive_provenance_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveRecursiveProvenance(sources: any, lineage: any): any {
  return {"sources": [...py.iter(sources)], "lineage_depth": py.get(lineage, "depth", 0), "complete": py.truthy(sources)};
}
