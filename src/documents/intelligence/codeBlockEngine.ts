/**
 * Converted from Python: core/documents/intelligence/code_block_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractCodeBlocks(text: any): any {
  var blocks: any = py.iter(py.reFindall("```[\\w-]*\\n(.*?)```", py.or2(text, () => ("")), "s")).filter((b: any) => py.truthy(py.strip(b))).map((b: any) => py.strip(b));
  return {"code_blocks": py.sorted(blocks)};
}
