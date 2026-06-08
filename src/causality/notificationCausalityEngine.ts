/**
 * Converted from Python: core/causality/notification_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function trackNotificationCausality(notifications: any, origin_events: any): any {
  var tracked: any[] = [];
  var origin_id: any = (py.truthy(origin_events) ? py.toStr(py.get(py.at(origin_events, (-1)), "id", "")) : "");
  var index: any;
  var notification: any;
  for ([index, notification] of py.enumerate(py.slice(notifications, null, 5000))) {
    if (((notification !== null && typeof notification === "object" && !Array.isArray(notification) && !(notification instanceof Set) && !(notification instanceof Map)))) {
      var notification_id: any = py.toStr(py.get(notification, "id", `notif:${py.toStr(index)}`));
      var user_interaction: any = py.truthy(py.get(notification, "interaction"));
    } else {
      notification_id = `notif:${py.toStr(index)}`;
      user_interaction = false;
    }
    py.listAppend(tracked, {"notification_id": notification_id, "origin_event": origin_id, "downstream_workflow": `workflow:notif:${py.toStr(index)}`, "user_interaction": user_interaction, "payload": py.toStr(notification)});
  }
  return {"notifications": tracked, "origin_event": origin_id, "count": py.len(tracked), "bounded": true};
}
