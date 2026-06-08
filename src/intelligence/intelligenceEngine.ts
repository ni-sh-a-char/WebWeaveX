/**
 * Converted from Python: core/intelligence/intelligence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { analyzeGraph } from "./graphAnalyzer.js";
import { computeCentrality } from "./centralityEngine.js";
import { detectClusters } from "./clusterEngine.js";
import { detectFlows } from "./flowEngine.js";
import { computeComplexity } from "./complexityEngine.js";
import { detectPatterns } from "./patternEngine.js";

export function _validateIntelligence(intel: any): any {
  var required: any = ["analysis", "central_nodes", "clusters", "flows", "complexity", "patterns"];
  var key: any;
  for (key of py.iter(required)) {
    if (!py.contains(intel, key)) {
      throw py.err("RuntimeError", `Invalid intelligence output: missing ${py.toStr(key)}`);
    }
  }
}
export function runIntelligence(graph: any): any {
  var nodes: any = py.get(graph, "nodes", []);
  var edges: any = py.get(graph, "edges", []);
  var analysis: any = analyzeGraph(nodes, edges);
  var central: any = computeCentrality(nodes, edges);
  var clusters: any = detectClusters(nodes, edges);
  var flows: any = detectFlows(edges);
  var complexity: any = computeComplexity(nodes, edges);
  var patterns: any = detectPatterns(analysis);
  var result: any = {"analysis": analysis, "central_nodes": py.slice(central, null, 5), "clusters": clusters, "flows": flows, "complexity": complexity, "patterns": patterns};
  _validateIntelligence(result);
  return result;
}
export { analyzeGraph, computeCentrality, computeComplexity, detectClusters, detectFlows, detectPatterns };
