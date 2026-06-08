/**
 * Converted from Python: core/serialize/bounded_serializer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { dumpsDeterministic } from "./deterministicSerializer.js";

export let MAX_SERIALIZE_BYTES: any = 50000000;
export function dumpsBounded(value: any, max_bytes: any = MAX_SERIALIZE_BYTES): any {
  var out: any = dumpsDeterministic(value);
  var raw: any = py.encode(out, "utf-8");
  if ((py.len(raw) <= max_bytes)) {
    return out;
  }
  return py.decode(py.slice(raw, null, max_bytes), "utf-8");
}
export { dumpsDeterministic };
