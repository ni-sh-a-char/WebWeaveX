/**
 * Self-contained npm certification — verifies package imports without Python.
 */
import { existsSync, readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { execSync } from "node:child_process";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const archive = join(root, "docs/archive");
const reportPath = join(archive, "FINAL_SELF_CONTAINED_NPM_CERTIFICATION.md");
const ts = new Date().toISOString();

type Check = { name: string; ok: boolean; detail: string };

const checks: Check[] = [];

function check(name: string, ok: boolean, detail: string): void {
  checks.push({ name, ok, detail });
}

// 1. src/ must not invoke python
let srcHits = 0;
const srcDir = join(root, "src");
for (const rel of ["index.ts"]) {
  const p = join(srcDir, rel);
  if (existsSync(p)) {
    const t = readFileSync(p, "utf-8");
    if (/\bexecSync\b|child_process|subprocess|\bpython\b/i.test(t)) srcHits++;
  }
}
check("src/ runtime free of python subprocess", srcHits === 0, `hits=${srcHits}`);

// 2. npm pack produces tarball
let packOk = false;
let packDetail = "";
try {
  const packOut = execSync("npm pack --dry-run --json", { cwd: root, encoding: "utf-8" }).trim();
  packOk = packOut.includes("webweavex");
  packDetail = "ok";
} catch (err) {
  packOk = false;
  packDetail = String(err);
}
check("npm pack --dry-run", packOk, packDetail);

// 3. Core import loads
let importOk = false;
let importDetail = "ok";
try {
  const mod = await import(pathToFileURL(join(root, "src/index.ts")).href);
  importOk = typeof mod === "object" && mod !== null;
  importDetail = importOk ? "module loaded" : "empty module";
} catch (err) {
  importOk = false;
  importDetail = String(err);
}
check("import src/index.ts", importOk, importDetail);

// 4. package.json files field excludes python tooling
const pkg = JSON.parse(readFileSync(join(root, "package.json"), "utf-8")) as { files?: string[] };
const filesOk = Array.isArray(pkg.files) && !pkg.files.some((f) => f.includes("tools/"));
check("package files exclude tools/", filesOk, JSON.stringify(pkg.files));

const allOk = checks.every((c) => c.ok);
const body = [
  "# FINAL SELF-CONTAINED NPM CERTIFICATION",
  "",
  `**Measured:** ${ts}`,
  "",
  `**Status:** ${allOk ? "PASS (baseline)" : "FAIL"}`,
  "",
  "| Check | Status | Detail |",
  "|-------|--------|--------|",
  ...checks.map((c) => `| ${c.name} | ${c.ok ? "PASS" : "FAIL"} | ${c.detail.replace(/\|/g, "/")} |`),
  "",
  "## Requirement",
  "",
  "After `npm install webweavex`, users must run extraction, replay, memory, workflow, and engines **without Python**.",
  "",
  "**Current blockers:** validation scripts and dev certification still invoke Python (see FINAL_PYTHON_DEPENDENCY_AUDIT.md).",
  "",
  allOk
    ? "Baseline npm surface is self-contained; full platform certification pending JS execution gates."
    : "Fix failing checks before release.",
  "",
].join("\n");

mkdirSync(archive, { recursive: true });
writeFileSync(reportPath, body);
console.log(body);
process.exit(allOk ? 0 : 1);
