/**
 * Converted from Python: core/documents/semantic_coreference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildCoreferenceGraph } from "./coreferenceGraphEngine.js";

export function resolveSemanticCoreference(text: any): any {
  return buildCoreferenceGraph(text);
}
export { buildCoreferenceGraph };
