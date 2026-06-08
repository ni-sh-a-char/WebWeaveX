/**
 * Converted from Python: core/internet/information_diffusion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { modelSemanticPropagation } from "./semanticPropagationEngine.js";

export function analyzeInformationDiffusion(seed: any, graph_edges: any): any {
  return modelSemanticPropagation(seed, graph_edges);
}
export { modelSemanticPropagation };
