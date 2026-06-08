/**
 * Converted from Python: core/parsers/parser_streaming_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { ParserBudget, enforceBudget } from "./parserBudgetEngine.js";
import { ParserRegistry } from "./parserRegistry.js";

export function* streamParse(source: any, path: any = "", language_hint: any = "", chunk_lines: any = 500, budget: any = null): any {
  var bounded: any = enforceBudget(source, budget);
  var lines: any = py.splitlines(bounded);
  if (!py.truthy(lines)) {
    yield ParserRegistry.parse("", path, language_hint, budget);
    return;
  }
  var chunks: any[] = [];
  var i: any;
  for (i of py.range(0, py.len(lines), py.max([1, chunk_lines]))) {
    py.listAppend(chunks, py.join("\n", py.slice(lines, i, py.add(i, chunk_lines))));
  }
  var idx: any;
  var chunk: any;
  for ([idx, chunk] of py.enumerate(chunks)) {
    var parsed: any = ParserRegistry.parse(chunk, path, language_hint, budget);
    py.setItem(parsed, "chunk_index", idx);
    py.setItem(parsed, "chunk_count", py.len(chunks));
    yield parsed;
  }
}
export { ParserBudget, ParserRegistry, enforceBudget };
