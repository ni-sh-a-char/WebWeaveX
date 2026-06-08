/**
 * SSA form builder — faithful port of core/ssa/ssa_builder_engine.py.
 * Hand-written production module (protected); reuses the Python source
 * analyzer for assignment discovery.
 */
import { parsePythonAst } from "../ast/pythonAstEngine.js";

export function buildSsaForm(code: string): Record<string, unknown> {
  const parsed = parsePythonAst(code) as {
    assignments: { targets: string[]; node: { lineno: number | null } }[];
  };
  const counters: Record<string, number> = {};
  const assignments: Record<string, unknown>[] = [];
  for (const a of parsed.assignments) {
    for (const name of a.targets) {
      counters[name] = (counters[name] ?? 0) + 1;
      assignments.push({
        variable: name,
        ssa_name: `${name}_${counters[name]}`,
        lineno: a.node.lineno,
      });
    }
  }
  return {
    ssa_assignments: assignments,
    variable_versions: counters,
    bounded: true,
    deterministic: true,
  };
}
