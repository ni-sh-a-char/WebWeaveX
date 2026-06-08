/**
 * Converted from Python: core/navigation/navigation_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { trackNavigationRoutes } from "./routeTrackingEngine.js";
import { detectSinglePageApplication } from "./spaDetectionEngine.js";

export function runNavigationRuntime(page: any): any {
  var spa: any = detectSinglePageApplication(page);
  var routes: any = trackNavigationRoutes(page);
  return {"spa": spa, "routes": routes, "bounded": true};
}
export { detectSinglePageApplication, trackNavigationRoutes };
