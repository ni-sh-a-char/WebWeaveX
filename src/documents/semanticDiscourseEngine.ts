/**
 * Converted from Python: core/documents/semantic_discourse_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseDiscourseStructure } from "./discourseParserEngine.js";
import { structureCognition } from "../evidence/index.js";

export function analyzeSemanticDiscourse(text: any): any {
  var structure: any = parseDiscourseStructure(text);
  var observed: any = {"lexical": py.at(structure, "lexical"), "syntactic": py.at(structure, "syntactic")};
  var inferred: any = {"discourse": py.at(structure, "discourse"), "conceptual": py.at(structure, "conceptual")};
  return structureCognition(observed, inferred, {"structure": structure});
}
export { parseDiscourseStructure, structureCognition };
