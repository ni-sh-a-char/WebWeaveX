/**
 * Converted from Python: core/internet/cross_source_contradiction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { detectEvidenceConflicts } from "./evidenceConflictEngine.js";

export function mapCrossSourceContradictions(claims: any): any {
  return detectEvidenceConflicts(claims);
}
export { detectEvidenceConflicts };
