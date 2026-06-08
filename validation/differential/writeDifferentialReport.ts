import { writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const archive = join(root, "docs/archive");

export type DifferentialSummary = {
  measured_at: string;
  families_passed: number;
  families_failed: number;
  probes_passed: number;
  probes_failed: number;
  families: Array<{ family: string; pass: boolean; failed_ids: string[] }>;
};

export function writeDifferentialReport(summary: DifferentialSummary): void {
  mkdirSync(archive, { recursive: true });
  const lines = [
    "# FINAL DIFFERENTIAL EQUIVALENCE REPORT",
    "",
    `**Measured:** ${summary.measured_at}`,
    "",
    "| Metric | Count |",
    "|--------|-------|",
    `| Families passed | ${summary.families_passed} |`,
    `| Families failed | ${summary.families_failed} |`,
    `| Probes passed | ${summary.probes_passed} |`,
    `| Probes failed | ${summary.probes_failed} |`,
    "",
    "## Family results",
    "",
    ...summary.families.map(
      (f) =>
        `- **${f.family}**: ${f.pass ? "PASS" : "FAIL"}${
          f.failed_ids.length ? ` — ${f.failed_ids.join(", ")}` : ""
        }`,
    ),
    "",
    "## Verdict",
    "",
    summary.families_failed === 0
      ? "**Differential equivalence: PASS**"
      : "**Differential equivalence: NOT ACHIEVED** — see failed families above.",
    "",
  ];
  writeFileSync(join(archive, "FINAL_DIFFERENTIAL_EQUIVALENCE_REPORT.md"), lines.join("\n"), "utf-8");
}
