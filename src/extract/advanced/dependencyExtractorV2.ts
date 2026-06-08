/**
 * Converted from Python: core/extract/advanced/dependency_extractor_v2.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildDependencyGraph } from "../../repository/dependencyGraphEngine.js";

export function extractDependenciesV2(text: any): any {
  return buildDependencyGraph(text);
}
export { buildDependencyGraph };
