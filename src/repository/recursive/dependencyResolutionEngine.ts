/**
 * Converted from Python: core/repository/recursive/dependency_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildDependencyGraph } from "../dependencyGraphEngine.js";

export function resolveDependencies(text: any): any {
  return buildDependencyGraph(text);
}
export { buildDependencyGraph };
