/**
 * Converted from Python: core/schemas/normalized_schema.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let NORMALIZED_KEYS: any = ["code", "content", "dependencies", "fingerprint", "metadata", "raw_text", "relationships", "source_url"];
export function emptyNormalized(source_url: any = ""): any {
  return {"content": {}, "code": {}, "dependencies": {}, "metadata": {}, "relationships": {}, "raw_text": "", "source_url": py.or2(source_url, () => ("")), "fingerprint": ""};
}
