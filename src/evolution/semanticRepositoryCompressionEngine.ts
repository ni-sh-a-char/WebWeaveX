/**
 * Converted from Python: core/evolution/semantic_repository_compression_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_COMPRESSED_KEYS: any = 256;
export function compressSemanticRepository(repository: any): any {
  var keys: any = py.slice(py.sorted(py.keys(repository)), null, MAX_COMPRESSED_KEYS);
  return {"compressed": Object.fromEntries(py.iter(keys).map((key: any) => ([key, py.at(repository, key)] as [any, any]))), "compression_ratio": py.round(py.div(py.len(keys), py.max([py.len(repository), 1])), 3)};
}
