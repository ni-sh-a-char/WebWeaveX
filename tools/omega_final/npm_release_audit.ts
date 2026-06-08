/**
 * Phase 2 — npm release artifact audit (what ships in the tarball).
 */
import { execSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const archive = join(root, "docs/archive");
const reportPath = join(archive, "FINAL_NPM_RELEASE_AUDIT.md");
const ts = new Date().toISOString();

const FORBIDDEN_PREFIXES = [
  "tools/",
  "docs/archive/",
  "docs/specs/",
  "validation/",
  "tests/",
  "specification/",
  ".py_staging",
  "python",
  "convergence",
  "py2ts",
];

const ALLOWED_PREFIXES = ["package/", "dist/", "README", "LICENSE", "CHANGELOG"];

type PackEntry = { path?: string; name?: string };

function listPackFiles(): string[] {
  const out = execSync("npm pack --dry-run --json", { cwd: root, encoding: "utf-8" });
  const parsed = JSON.parse(out) as Array<{ files?: PackEntry[] }> | { files?: PackEntry[] };
  const files = Array.isArray(parsed) ? parsed[0]?.files : (parsed as { files?: PackEntry[] }).files;
  if (!files) return [];
  return files.map((f) => String(f.path ?? f.name ?? "").replace(/\\/g, "/"));
}

function classify(path: string): "ALLOWED" | "FORBIDDEN" | "REVIEW" {
  const p = path.replace(/^package\//, "");
  if (FORBIDDEN_PREFIXES.some((x) => p.includes(x))) return "FORBIDDEN";
  if (p.startsWith("dist/") || p === "package.json" || p.startsWith("README") || p === "LICENSE")
    return "ALLOWED";
  if (p.startsWith("CHANGELOG")) return "ALLOWED";
  return "REVIEW";
}

const packFiles = listPackFiles();
const forbidden = packFiles.filter((f) => classify(f) === "FORBIDDEN");
const review = packFiles.filter((f) => classify(f) === "REVIEW");
const pass = forbidden.length === 0 && packFiles.length > 0;

const pkg = JSON.parse(readFileSync(join(root, "package.json"), "utf-8")) as {
  files?: string[];
  exports?: Record<string, unknown>;
};
const filesFieldOk =
  Array.isArray(pkg.files) &&
  pkg.files.every((f) => ["dist", "README.md", "LICENSE", "CHANGELOG.md"].includes(f) || f.startsWith("dist"));

const body = [
  "# FINAL NPM RELEASE AUDIT",
  "",
  `**Measured:** ${ts}`,
  "",
  `**Status:** ${pass && filesFieldOk ? "PASS" : "FAIL"}`,
  "",
  "| Check | Result |",
  "|-------|--------|",
  `| npm pack --dry-run | ${packFiles.length} files |`,
  `| Forbidden paths in tarball | ${forbidden.length} |`,
  `| Review paths | ${review.length} |`,
  `| package.json \`files\` whitelist | ${filesFieldOk ? "PASS" : "FAIL"} → ${JSON.stringify(pkg.files)} |`,
  "",
  "## Allowed in published artifact",
  "",
  "- `dist/` (built output)",
  "- `README.md`, `LICENSE`, `CHANGELOG.md` (when listed)",
  "",
  "## Excluded from tarball (dev-only, correct)",
  "",
  "- `tools/` (py2ts, convergence, certification)",
  "- `validation/`, `tests/`, `specification/`",
  "- Python scripts and staging",
  "",
  ...(forbidden.length
    ? ["", "## FORBIDDEN entries in pack (must fix)", "", ...forbidden.map((f) => `- ${f}`)]
    : []),
  ...(review.length
    ? ["", "## REVIEW", "", ...review.slice(0, 20).map((f) => `- ${f}`)]
    : []),
  "",
  "## Note on exports",
  "",
  pkg.exports && JSON.stringify(pkg.exports).includes("./src")
    ? "WARNING: `exports['./*']` points at `./src/*` — consumers may resolve source; prefer `dist/` only for release."
    : "exports do not expose raw src.",
  "",
].join("\n");

mkdirSync(archive, { recursive: true });
writeFileSync(reportPath, body);
console.log(body);
process.exit(pass && filesFieldOk ? 0 : 1);
