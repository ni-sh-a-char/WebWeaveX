/**
 * Converted from Python: core/reasoning/semantic_traversal_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import { semanticTraverse } from "../query/semanticTraversalEngine.js";

export function traverseWithConstraints(graph: any, start: any, max_depth: any = 10): any {
  return semanticTraverse(graph, start, max_depth);
}
export { semanticTraverse };
