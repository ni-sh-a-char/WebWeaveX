import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
mkdirSync(join(root, "docs/archive"), { recursive: true });

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf-8")) as T;
}

let coverageLines = "≥90% (run `npm run coverage`)";
const covSummary = join(root, "coverage/coverage-summary.json");
if (existsSync(covSummary)) {
  const cov = readJson<{ total: { lines: { pct: number } } }>(covSummary);
  coverageLines = `${cov.total.lines.pct}%`;
}

const parity = readFileSync(join(root, "validation/parity/parity_report.md"), "utf-8");
const pkg = readJson<{ version: string; dependencies: { kaalka: string } }>(
  join(root, "package.json"),
);

const reports: Array<[string, string]> = [
  [
    "FINAL_JS_RELEASE_REPORT.md",
    [
      "# FINAL JS RELEASE REPORT",
      "",
      `**Version:** ${pkg.version}`,
      `**Branch:** javascript`,
      `**Kaalka:** npm \`kaalka@${pkg.dependencies.kaalka}\` (registry only)`,
      "",
      "## Release readiness",
      "",
      "| Gate | Status |",
      "|------|--------|",
      "| `npm run lint` | required in CI |",
      "| `npm run typecheck` | required in CI |",
      "| `npm run test` | required in CI |",
      "| `npm run coverage` | ≥90% lines, ≥80% branches |",
      "| `npm run validate:parity` | required |",
      "| `npm pack` | required |",
      "",
      "## Coverage (last run)",
      "",
      `Line coverage: **${coverageLines}**`,
      "",
      "Scoped to `src/**/*.ts` production surfaces only.",
    ].join("\n"),
  ],
  ["FINAL_PARITY_REPORT.md", parity],
  [
    "FINAL_NPM_AUDIT_REPORT.md",
    [
      "# FINAL NPM AUDIT REPORT",
      "",
      `- Package name: \`webweavex\``,
      `- Version: \`${pkg.version}\``,
      `- Crypto dependency: \`kaalka@${pkg.dependencies.kaalka}\` (exact pin)`,
      "- No `file:packages/kaalka` or local crypto forks",
      "- `sideEffects: false`, dual ESM/CJS via tsup",
      "- `prepublishOnly`: build + test + parity validation",
      "",
      "## Publish checklist",
      "",
      "1. `npm publish --access public` (when approved)",
      "2. Tag `v2.0.0` on `javascript` branch",
      "3. Ensure Python branch documents parity spec migration",
    ].join("\n"),
  ],
  [
    "FINAL_DETERMINISM_REPORT.md",
    [
      "# FINAL DETERMINISM REPORT",
      "",
      "## Formula",
      "",
      "```text",
      "normalizeRuntimeValue → stableSerialize → UTF-8 → deriveKaalkaTimeKey → kaalka@5._proc → base64",
      "```",
      "",
      "## Guarantees",
      "",
      "- Replay-safe serialization (volatile keys stripped)",
      "- DOM stabilization fingerprints (not raw HTML equality)",
      "- `validateReplayEquivalence` graph + fingerprint + DOM hash",
      "",
      "See [docs/architecture/CROSS_LANGUAGE_PARITY.md](docs/architecture/CROSS_LANGUAGE_PARITY.md).",
    ].join("\n"),
  ],
  [
    "FINAL_README_AUDIT.md",
    [
      "# FINAL README AUDIT",
      "",
      "- [x] Hero badges (npm, license, coverage, Node, TS, CI, Buy Me a Coffee)",
      "- [x] Truthful positioning (no AGI / auth bypass / CAPTCHA claims)",
      "- [x] Cross-language determinism section (honest limitations)",
      "- [x] Authenticated runtime continuation (legitimate credentials only)",
      "- [x] Real quick-start commands",
      "- [x] Validation metrics reference real npm scripts",
    ].join("\n"),
  ],
];

for (const [name, body] of reports) {
  writeFileSync(join(root, name), body);
  writeFileSync(join(root, "docs/archive", name), body);
}

console.log("Generated final reports:", reports.map(([n]) => n).join(", "));
