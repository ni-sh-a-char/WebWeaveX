/**
 * Converted from Python: core/repository/intelligence_v3/ast_normalization_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { parseSource } from "../../parsers/index.js";

export function normalizeAst(text: any, path: any = ""): any {
  var parsed: any = parseSource(py.or2(text, () => ("")), path);
  var ast_data: any = py.get(parsed, "ast", {});
  var symbols: any = py.get(parsed, "symbols", {});
  return {"language": py.get(parsed, "language", "text"), "ast": ast_data, "symbols": symbols};
}
export { parseSource };
