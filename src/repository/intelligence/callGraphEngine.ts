/**
 * Converted from Python: core/repository/intelligence/call_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { parseSource } from "../../parsers/index.js";

export function _codeSample(text: any, path: any): any {
  var match: any = py.reSearch("```(?:python|py)?\\n(.*?)```", py.or2(text, () => ("")), "si");
  if (py.truthy(match)) {
    return [match.group(1), "snippet.py"];
  }
  return [py.or2(text, () => ("")), py.or2(path, () => ("input.py"))];
}
export function buildCallGraph(text: any, path: any = ""): any {
  const _d1 = py.iter(_codeSample(text, path)) as any[];
  var sample: any = _d1[0];
  var sample_path: any = _d1[1];
  var parsed: any = parseSource(sample, sample_path);
  var calls: any = py.get(py.get(parsed, "calls", {}), "calls", []);
  return {"calls": calls, "evidence": "parser_call_graph", "language": py.get(parsed, "language", "text")};
}
export { parseSource };
