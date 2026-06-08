/**
 * Converted from Python: core/application/form_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_FORMS: any = 500;
export function buildFormRuntime(html: any): any {
  var soup: any = py.soup(py.or2(html, () => ("")), "html.parser");
  var forms: any[] = [];
  var form: any;
  for (form of py.iter(py.slice(soup.find_all("form"), null, MAX_FORMS))) {
    var inputs: any[] = [];
    var field: any;
    for (field of py.iter(form.find_all(["input", "select", "textarea"]))) {
      py.listAppend(inputs, {"name": py.slice(py.toStr(py.get(field, "name", "")), null, 200), "type": py.slice(py.toStr(py.get(field, "type", field.name)), null, 50), "required": field.has_attr("required")});
    }
    var csrf_fields: any = py.iter(form.find_all("input")).filter((inp: any) => py.contains(String(py.toStr(py.get(inp, "name", ""))).toLowerCase(), "csrf")).map((inp: any) => py.get(inp, "name", ""));
    py.listAppend(forms, {"action": py.slice(py.toStr(py.get(form, "action", "")), null, 500), "inputs": py.sorted(inputs, {key: ((item: any) => py.at(item, "name")) as (item: any) => any}), "csrf_fields": py.sorted(csrf_fields), "multi_step": (py.len(form.find_all("fieldset")) > 1), "bounded": true});
  }
  return {"forms": forms, "form_count": py.len(forms), "bounded": true};
}
