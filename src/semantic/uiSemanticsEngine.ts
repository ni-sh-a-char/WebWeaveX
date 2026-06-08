/**
 * Converted from Python: core/semantic/ui_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let UI_INTENT_RULES: any = {"destructive": py.regex("\\b(delete|remove|destroy|revoke)\\b", "i"), "authentication": py.regex("\\b(login|sign\\s*in|password|oauth)\\b", "i"), "billing": py.regex("\\b(billing|invoice|payment|subscription)\\b", "i"), "monitoring": py.regex("\\b(monitor|alert|metric|status)\\b", "i"), "settings": py.regex("\\b(settings|preferences|configuration)\\b", "i"), "admin_panel": py.regex("\\b(admin|manage users|permissions)\\b", "i")};
export function extractUiSemantics(html: any = "", actions: any = null): any {
  var soup: any = py.soup(py.or2(html, () => ("")), "html.parser");
  var text: any = py.slice(soup.get_text(" ", true), null, 50000);
  actions = py.or2(actions, () => ([]));
  var intents: any = Object.fromEntries(py.iter(UI_INTENT_RULES).map((key: any) => ([key, false] as [any, any])));
  var intent: any;
  var pattern: any;
  for ([intent, pattern] of py.items(UI_INTENT_RULES)) {
    if (py.truthy(pattern.search(text))) {
      py.setItem(intents, intent, true);
    }
  }
  var buttons: any[] = [];
  var button: any;
  for (button of py.iter(py.slice(soup.find_all(["button", "a", "input"]), null, 2000))) {
    var label: any = py.slice(py.toStr(py.or2(button.get_text(true), () => (py.get(button, "value", "")))), null, 200);
    if (!py.truthy(label)) {
      continue;
    }
    var role: any = "primary_workflow";
    if (py.truthy(py.at(UI_INTENT_RULES, "destructive").search(label))) {
      role = "destructive";
    }
    py.listAppend(buttons, {"label": label, "role": role});
  }
  return {"destructive_actions": py.iter(buttons).filter((b: any) => py.eq(py.at(b, "role"), "destructive")).map((b: any) => b), "primary_workflows": py.slice(py.iter(buttons).filter((b: any) => py.eq(py.at(b, "role"), "primary_workflow")).map((b: any) => b), null, 500), "navigation_intent": py.truthy(soup.find_all("nav")), "dashboards": py.truthy(py.reSearch("dashboard|kpi|metrics", text, "i")), "forms": py.len(soup.find_all("form")), "admin_panels": py.at(intents, "admin_panel"), "settings": py.at(intents, "settings"), "authentication": py.at(intents, "authentication"), "billing": py.at(intents, "billing"), "monitoring": py.at(intents, "monitoring"), "actions": py.slice(actions, null, 1000), "bounded": true};
}
