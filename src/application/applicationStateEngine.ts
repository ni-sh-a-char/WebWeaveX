/**
 * Converted from Python: core/application/application_state_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildApplicationState(route: any, forms: any = null, modals: any = null, widgets: any = null, tabs: any = null, authenticated: any = false, runtime_state: any = null): any {
  return {"route": py.slice(py.toStr(route), null, 2000), "forms": py.slice([...py.iter(py.or2(forms, () => ([])))], null, 500), "modals": py.slice([...py.iter(py.or2(modals, () => ([])))], null, 200), "widgets": py.slice([...py.iter(py.or2(widgets, () => ([])))], null, 1000), "tabs": py.slice([...py.iter(py.or2(tabs, () => ([])))], null, 100), "authenticated": py.truthy(authenticated), "runtime_state": py.pyDict(py.or2(runtime_state, () => ({}))), "bounded": true};
}
