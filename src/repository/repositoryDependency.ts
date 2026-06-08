import { readFileSync } from "node:fs";

export function extractRepositoryDependencies(
  files: Array<{ path: string }>,
): Record<string, unknown> {
  const dependencies: Record<string, string> = {};
  const edges: Array<Record<string, unknown>> = [];
  for (const file of files) {
    try {
      const raw = JSON.parse(readFileSync(file.path, "utf-8")) as {
        dependencies?: Record<string, string>;
      };
      Object.assign(dependencies, raw.dependencies ?? {});
    } catch {
      /* skip invalid */
    }
  }
  for (const name of Object.keys(dependencies).sort()) {
    edges.push({ from: "package", to: name, type: "depends_on" });
  }
  return { dependencies, edges, bounded: true };
}
