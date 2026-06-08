/**
 * Converted from Python: core/output_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export function buildHumanReadable(exec_type: any, result: any): any {
  if (py.eq(exec_type, "code")) {
    var files: any = py.get(result, "files", []);
    var project_type: any = py.get(result, "project_type", "unknown");
    return `Generated ${py.toStr(py.len(files))} code files for a ${py.toStr(project_type)} project.`;
  }
  if (py.eq(exec_type, "data")) {
    var summary: any = py.get(result, "summary", "");
    var points: any = py.get(result, "key_points", []);
    var combined: any = py.add(py.add(summary, " "), py.join(" ", py.slice(points, null, 2)));
    return py.slice(py.strip(combined), null, 300);
  }
  if (py.eq(exec_type, "text")) {
    return py.slice(py.strip(py.toStr(result)), null, 300);
  }
  return "No meaningful result found.";
}
export function buildStructured(exec_type: any, result: any): any {
  if (!((result !== null && typeof result === "object" && !Array.isArray(result) && !(result instanceof Set) && !(result instanceof Map)))) {
    if (py.eq(exec_type, "text")) {
      return {"text": py.toStr(result)};
    }
    return {};
  }
  if (py.eq(exec_type, "code")) {
    return {"files": py.get(result, "files", []), "project_type": py.get(result, "project_type", "unknown"), "entry_points": py.get(result, "entry_points", []), "dependencies": py.get(result, "dependencies", [])};
  }
  if (py.eq(exec_type, "data")) {
    return result;
  }
  if (py.eq(exec_type, "text")) {
    return {"text": result};
  }
  return {};
}
export function buildUiSchema(exec_type: any, result: any): any {
  var components: any[] = [];
  if (py.eq(exec_type, "code")) {
    var f: any;
    for (f of py.iter(py.get(result, "files", []))) {
      py.listAppend(components, {"type": "code_block", "title": py.get(f, "path", ""), "content": py.get(f, "content", "")});
    }
  } else if (py.eq(exec_type, "data")) {
    py.listAppend(components, {"type": "summary", "content": py.get(result, "summary", "")});
    var p: any;
    for (p of py.iter(py.get(result, "key_points", []))) {
      py.listAppend(components, {"type": "bullet", "content": p});
    }
  } else if (py.eq(exec_type, "text")) {
    py.listAppend(components, {"type": "text", "content": py.toStr(result)});
  }
  return {"type": "ui_render", "components": components};
}
export function adjustConfidence(base_conf: any, top_result: any): any {
  if (!((top_result !== null && typeof top_result === "object" && !Array.isArray(top_result) && !(top_result instanceof Set) && !(top_result instanceof Map)))) {
    return py.toFloat(base_conf);
  }
  var recovered: any = py.get(top_result, "recovered", {});
  var count: any = py.get(recovered, "recovered_count", 0);
  var boost: any = py.min([py.mul(count, py.F(0.05)), py.F(0.2)]);
  return py.min([py.add(base_conf, boost), py.F(1.0)]);
}
export function fallbackOutput(): any {
  return {"human_readable": "No result", "structured_data": {}, "ui_schema": {"type": "empty", "components": []}, "confidence": py.F(0.0), "source": "unknown", "reconstructed_project": [], "version": "v1_phase_14"};
}
export function buildOutput(execution_result: any, top_result: any): any {
  if (!((execution_result !== null && typeof execution_result === "object" && !Array.isArray(execution_result) && !(execution_result instanceof Set) && !(execution_result instanceof Map)))) {
    return fallbackOutput();
  }
  var exec_type: any = py.get(execution_result, "execution_type", "fallback");
  var result: any = py.get(execution_result, "result", {});
  var base_conf: any = py.get(execution_result, "confidence", py.F(0.0));
  var confidence: any = adjustConfidence(base_conf, top_result);
  var source: any = py.get(top_result, "source", "unknown");
  var original_input: any = py.get(top_result, "original_input", "");
  var input_signature: any = py.get(top_result, "input_signature", "");
  if (!py.truthy(input_signature)) {
    input_signature = py.get(execution_result, "input_signature", "");
  }
  if ((!py.truthy(original_input) && py.contains(top_result, "queries"))) {
    var qbundle: any = py.get(top_result, "queries", {});
    original_input = py.get(qbundle, "original_input", "");
    if (!py.truthy(input_signature)) {
      input_signature = py.get(qbundle, "input_signature", "");
    }
  }
  var human: any = buildHumanReadable(exec_type, result);
  if ((!py.truthy(human) || (py.len(human) < 10))) {
    human = `Result for ${py.toStr(source)}: found matching content`;
  }
  var structured: any = buildStructured(exec_type, result);
  if ((!py.truthy(structured) || py.eq(structured, {}))) {
    structured = {"query_source": source, "has_content": (py.len(py.get(top_result, "html", "")) > 0)};
  }
  if (py.truthy(original_input)) {
    py.setItem(structured, "input_echo", py.slice(original_input, null, 50));
  }
  if (py.truthy(input_signature)) {
    py.setItem(structured, "input_signature", input_signature);
  }
  var ui: any = buildUiSchema(exec_type, result);
  if (!py.truthy(py.get(ui, "components"))) {
    ui = {"type": "ui_render", "components": [{"type": "text", "content": human}]};
  }
  return {"human_readable": py.or2(human, () => ("")), "structured_data": py.or2(structured, () => ({})), "ui_schema": py.or2(ui, () => ({"type": "empty", "components": []})), "confidence": py.toFloat(confidence), "source": py.or2(source, () => ("unknown")), "reconstructed_project": py.get(structured, "files", []), "version": "v1_phase_14"};
}
export function validateOutputEngine(): any {
  var test: any = {"execution_type": "data", "result": {"summary": "test", "key_points": ["a", "b"]}, "confidence": py.F(0.8)};
  var out: any = buildOutput(test, {"source": "test"});
  if (!py.contains(out, "human_readable")) throw py.err("AssertionError", "AssertionError");
  if (!py.contains(out, "structured_data")) throw py.err("AssertionError", "AssertionError");
  if (!py.contains(out, "ui_schema")) throw py.err("AssertionError", "AssertionError");
  if (!py.contains(out, "confidence")) throw py.err("AssertionError", "AssertionError");
  if (!py.contains(out, "source")) throw py.err("AssertionError", "AssertionError");
  if (!py.contains(out, "reconstructed_project")) throw py.err("AssertionError", "AssertionError");
  if (!py.contains(out, "version")) throw py.err("AssertionError", "AssertionError");
  var key: any;
  for (key of py.iter(out)) {
    if ((py.at(out, key) === null || py.at(out, key) === undefined)) {
      throw py.err("AssertionError", `None value in key: ${py.toStr(key)}`);
    }
  }
  return true;
}
