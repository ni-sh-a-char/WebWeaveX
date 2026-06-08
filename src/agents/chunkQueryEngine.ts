/**
 * Converted from Python: core/agents/chunk_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function queryChunks(streaming_meta: any): any {
  return py.get(streaming_meta, "chunk_order", []);
}
