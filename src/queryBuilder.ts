/**
 * Converted from Python: core/query_builder.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export function _buildBaseQuery(intent: any): any {
  return py.strip(py.get(intent, "goal", ""));
}
export function _enhanceForSource(base_query: any, source: any): any {
  if (py.eq(source, "github")) {
    return `${py.toStr(base_query)} implementation github`;
  } else if (py.eq(source, "stackoverflow")) {
    return `${py.toStr(base_query)} error solution stackoverflow`;
  } else if (py.eq(source, "codepen")) {
    return `${py.toStr(base_query)} javascript demo codepen`;
  } else if (py.eq(source, "docs")) {
    return `${py.toStr(base_query)} official documentation`;
  } else if (py.eq(source, "news")) {
    return `${py.toStr(base_query)} latest news`;
  } else if (py.eq(source, "web")) {
    return base_query;
  }
  return base_query;
}
export function buildQueries(intent: any, source_plan: any): any {
  if (!((intent !== null && typeof intent === "object" && !Array.isArray(intent) && !(intent instanceof Set) && !(intent instanceof Map)))) {
    throw py.err("TypeError", "intent must be a dict");
  }
  if (!((source_plan !== null && typeof source_plan === "object" && !Array.isArray(source_plan) && !(source_plan instanceof Set) && !(source_plan instanceof Map)))) {
    throw py.err("TypeError", "source_plan must be a dict");
  }
  if (!py.contains(source_plan, "sources")) {
    throw py.err("ValueError", "source_plan missing 'sources'");
  }
  var base_query: any = _buildBaseQuery(intent);
  var original_input: any = py.get(intent, "goal", "");
  var input_signature: any = py.slice(py.hashNew("sha256", py.encode(original_input)).hexdigest(), null, 12);
  var queries: any[] = [];
  var seen: Set<any> = new Set();
  var item: any;
  for (item of py.iter(py.at(source_plan, "sources"))) {
    var source: any = py.get(item, "source");
    if (!py.truthy(source)) {
      continue;
    }
    var query: any = _enhanceForSource(base_query, source);
    if (!py.contains(seen, query)) {
      py.listAppend(queries, {"source": source, "query": query, "priority": py.get(item, "priority", 0), "input_signature": input_signature});
      py.setAdd(seen, query);
    }
  }
  var expansion_suffixes: any = ["tutorial", "example", "github", "how to build", "implementation", "architecture", "best practices"];
  var suffix: any;
  for (suffix of py.iter(expansion_suffixes)) {
    var exp_query: any = `${py.toStr(base_query)} ${py.toStr(suffix)}`;
    var exp_enhanced: any = _enhanceForSource(exp_query, "web");
    if (!py.contains(seen, exp_enhanced)) {
      py.listAppend(queries, {"source": "web", "query": exp_enhanced, "priority": 10, "input_signature": input_signature});
      py.setAdd(seen, exp_enhanced);
    }
  }
  var result: any = {"base_query": base_query, "original_input": original_input, "input_signature": input_signature, "queries": queries, "total_queries": py.len(queries), "version": "v1_phase_4"};
  return result;
}
export function validateQueryBuilder(): any {
  var test_intent: any = {"type": "ui_app", "goal": "calculator app", "keywords": ["calculator", "app"], "complexity": "medium", "version": "v1_phase_2"};
  var test_source_plan: any = {"intent_type": "ui_app", "sources": [{"source": "github", "priority": 1}, {"source": "codepen", "priority": 2}, {"source": "stackoverflow", "priority": 3}], "total_sources": 3, "version": "v1_phase_3"};
  var result: any = buildQueries(test_intent, test_source_plan);
  if (!((result !== null && typeof result === "object" && !Array.isArray(result) && !(result instanceof Set) && !(result instanceof Map)))) {
    throw py.err("RuntimeError", "Result is not dict");
  }
  if (!py.contains(result, "queries")) {
    throw py.err("RuntimeError", "Missing queries");
  }
  if (py.eq(py.len(py.at(result, "queries")), 0)) {
    throw py.err("RuntimeError", "No queries generated");
  }
  return true;
}
