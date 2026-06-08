/**
 * Converted from Python: core/documents/intelligence/knowledge_block_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractKnowledgeBlocks(text: any): any {
  var lines: any = py.iter(py.splitlines(py.or2(text, () => ("")))).filter((ln: any) => py.truthy(py.strip(ln))).map((ln: any) => py.strip(ln));
  var blocks: any[] = [];
  var buf: any[] = [];
  var ln: any;
  for (ln of py.iter(lines)) {
    py.listAppend(buf, ln);
    if ((py.len(buf) >= 8)) {
      py.listAppend(blocks, py.join(" ", buf));
      buf = [];
    }
  }
  if (py.truthy(buf)) {
    py.listAppend(blocks, py.join(" ", buf));
  }
  return {"knowledge_blocks": blocks};
}
