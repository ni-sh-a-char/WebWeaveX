/**
 * Converted from Python: core/documents/semantic_reference_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildCoreferenceGraph } from "./coreferenceGraphEngine.js";

export function resolveSemanticReferences(text: any): any {
  return buildCoreferenceGraph(text);
}
export { buildCoreferenceGraph };
