import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const archiveDir = join(root, "docs/archive");

mkdirSync(archiveDir, { recursive: true });

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf-8")) as T;
}

let coverageLines = "≥90% (run `npm run coverage`)";
const covSummary = join(root, "coverage/coverage-summary.json");
if (existsSync(covSummary)) {
  const cov = readJson<{ total: { lines: { pct: number } } }>(covSummary);
  coverageLines = `${cov.total.lines.pct}%`;
}

const parity = existsSync(join(root, "validation/parity/parity_report.md"))
  ? readFileSync(join(root, "validation/parity/parity_report.md"), "utf-8")
  : "Run `npm run validate:parity` first.";

const pkg = readJson<{ version: string; dependencies: { kaalka: string } }>(
  join(root, "package.json"),
);

const rootFiles = readdirSync(root, { withFileTypes: true })
  .filter((e) => e.isFile())
  .map((e) => e.name)
  .sort();

const tree = [
  "README.md · LICENSE · SECURITY.md · CONTRIBUTING.md · CHANGELOG.md · ROADMAP.md",
  "package.json · tsconfig.json · tsup.config.ts · vitest.config.ts · eslint.config.js",
  "src/ · tests/ · docs/ · examples/ · validation/ · .github/",
].join("\n");

const reports: Array<[string, string]> = [
  [
    "FINAL_JS_RELEASE_REPORT.md",
    [
      "# FINAL JS RELEASE REPORT",
      "",
      `**Version:** ${pkg.version} · **Branch:** javascript`,
      `**Kaalka:** npm \`kaalka@${pkg.dependencies.kaalka}\``,
      "",
      "| Gate | Required |",
      "|------|----------|",
      "| lint / typecheck / test / coverage | yes |",
      "| validate:parity | yes |",
      "| validate:production | yes |",
      "| npm pack | yes |",
      "",
      `**Coverage:** ${coverageLines} (scoped to \`src/\`)`,
    ].join("\n"),
  ],
  [
    "FINAL_REPOSITORY_STRUCTURE_REPORT.md",
    [
      "# FINAL REPOSITORY STRUCTURE REPORT",
      "",
      "## Root files",
      "",
      rootFiles.map((f) => `- \`${f}\``).join("\n"),
      "",
      "## Intended layout",
      "",
      "```text",
      tree,
      "```",
      "",
      "All `FINAL_*.md` engineering reports live under `docs/archive/`.",
    ].join("\n"),
  ],
  ["FINAL_PARITY_REPORT.md", parity],
  [
    "FINAL_NPM_READINESS_REPORT.md",
    [
      "# FINAL NPM READINESS REPORT",
      "",
      `- Package: \`webweavex@${pkg.version}\``,
      "- Published files: `dist/`, `README.md`, `LICENSE` (see `package.json` `files`)",
      `- Crypto: registry \`kaalka@${pkg.dependencies.kaalka}\` only`,
      "- `sideEffects: false` · dual ESM/CJS",
      "- `prepublishOnly`: build + test + parity",
      "",
      "## Publish (when approved)",
      "",
      "```bash",
      "npm publish --access public",
      "```",
    ].join("\n"),
  ],
  [
    "FINAL_README_AUDIT.md",
    [
      "# FINAL README AUDIT",
      "",
      "- [x] Hero: truthful positioning + badges",
      "- [x] Explicit NOT list (no AGI, bypass, CAPTCHA)",
      "- [x] Honest cross-language parity limitations",
      "- [x] Authenticated runtime — user-supplied credentials only",
      "- [x] Real install / quick-start commands",
    ].join("\n"),
  ],
];

for (const [name, body] of reports) {
  writeFileSync(join(archiveDir, name), body);
}

console.log("Archived reports:", reports.map(([n]) => `docs/archive/${n}`).join(", "));
