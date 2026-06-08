/**
 * Bulk Python (core/) → TypeScript (src/) converter for WebWeaveX javascript branch.
 * Reads files via `git show origin/python:<path>`.
 */
import { execSync, spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync, readFileSync, existsSync, rmSync, copyFileSync } from "node:fs";
import { dirname, join, relative, posix } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const manifestPath = join(root, "tools/py2ts/manifest.txt");
const srcRoot = join(root, "src");
const legacyRoot = join(root, "src-legacy-handwritten");
const reportPath = join(root, "docs/architecture/PYTHON_TO_JS_CONVERSION_REPORT.md");

function snakeToCamel(s) {
  return s.replace(/_([a-z0-9])/g, (_, c) => c.toUpperCase());
}

function pyBasenameToTs(pyPath) {
  const base = pyPath.split("/").pop().replace(/\.py$/, "");
  if (base === "__init__") return "index.ts";
  return `${snakeToCamel(base)}.ts`;
}

function pyCorePathToTs(pyPath) {
  const rel = pyPath.replace(/^core\//, "");
  const parts = rel.split("/");
  const file = parts.pop();
  const dir = parts.join("/");
  const tsFile = pyBasenameToTs(file);
  return dir ? join(dir, tsFile).replace(/\\/g, "/") : tsFile;
}

function gitShow(pyPath) {
  const r = spawnSync("git", ["show", `origin/python:${pyPath}`], {
    cwd: root,
    encoding: "utf-8",
    maxBuffer: 20 * 1024 * 1024,
  });
  if (r.status !== 0) return null;
  return r.stdout;
}

function convertImportLine(line, currentTsDir) {
  const mFrom = line.match(/^from\s+core\.([\w.]+)\s+import\s+(.+)$/);
  if (mFrom) {
    const modPath = mFrom[1].replace(/\./g, "/");
    const targetDir = dirname(join("src", modPath));
    let rel = posix.relative(currentTsDir, targetDir);
    if (!rel.startsWith(".")) rel = `./${rel}`;
    const imports = mFrom[2].replace(/\(([^)]+)\)/g, "$1");
    return `import { ${imports.trim()} } from "${rel}/index.js";`;
  }
  const mImport = line.match(/^import\s+core\.([\w.]+)(?:\s+as\s+(\w+))?/);
  if (mImport) {
    const modPath = mImport[1].replace(/\./g, "/");
    const targetDir = dirname(join("src", modPath));
    let rel = posix.relative(currentTsDir, targetDir);
    if (!rel.startsWith(".")) rel = `./${rel}`;
    const alias = mImport[2] ? ` as ${mImport[2]}` : "";
    return `import * as ${mImport[2] || snakeToCamel(modPath.split("/").pop())}${alias} from "${rel}/index.js";`;
  }
  return null;
}

function convertPythonToTs(py, pyPath, tsRelPath) {
  const tsDir = posix.dirname(tsRelPath).replace(/\\/g, "/");
  const lines = py.split(/\r?\n/);
  const out = [];
  const isInit = pyPath.endsWith("__init__.py");

  out.push("/**");
  out.push(` * Converted from Python: ${pyPath}`);
  out.push(" * @generated — WebWeaveX python→javascript library port");
  out.push(" */");
  out.push("// @ts-nocheck");
  out.push("");

  let inClass = false;
  let classIndent = 0;
  const exports = [];

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    const trimmed = line.trim();

    if (trimmed.startsWith('"""') || trimmed.startsWith("'''")) {
      if ((trimmed.match(/"""|'''/g) || []).length < 2) {
        i++;
        while (i < lines.length && !lines[i].includes('"""') && !lines[i].includes("'''")) i++;
      }
      continue;
    }
    if (trimmed.startsWith("#") && !trimmed.startsWith("# type:")) continue;
    if (trimmed === "from __future__ import annotations") continue;
    if (trimmed.startsWith("__all__")) continue;

    const imp = convertImportLine(trimmed, tsDir === "." ? "src" : join("src", tsDir).replace(/\\/g, "/"));
    if (imp) {
      out.push(imp);
      continue;
    }
    if (trimmed.startsWith("import ") && !trimmed.startsWith("import {")) {
      const conv = convertImportLine(trimmed, tsDir === "." ? "src" : join("src", tsDir).replace(/\\/g, "/"));
      if (conv) {
        out.push(conv);
        continue;
      }
    }

    line = line
      .replace(/\bTrue\b/g, "true")
      .replace(/\bFalse\b/g, "false")
      .replace(/\bNone\b/g, "null")
      .replace(/\bself\b/g, "this")
      .replace(/Dict\[/g, "Record<")
      .replace(/List\[/g, "Array<")
      .replace(/Tuple\[/g, "[")
      .replace(/Optional\[/g, "")
      .replace(/\| None/g, " | undefined")
      .replace(/: Any\b/g, ": unknown")
      .replace(/dict\[/g, "Record<")
      .replace(/list\[/g, "Array<")
      .replace(/ -> None:/g, ":")
      .replace(/ -> None$/g, "")
      .replace(/pathlib\.Path/g, "string");

    if (/^class\s+(\w+)/.test(trimmed)) {
      const cn = trimmed.match(/^class\s+(\w+)/)[1];
      exports.push(cn);
      out.push(line.replace(/^class\s+(\w+).*:/, "export class $1 {"));
      inClass = true;
      classIndent = line.search(/\S/);
      continue;
    }

    if (/^async def\s+(\w+)/.test(trimmed)) {
      const fn = trimmed.match(/^async def\s+(\w+)/)[1];
      if (!inClass) exports.push(snakeToCamel(fn));
      line = line.replace(/^(\s*)async def\s+(\w+)/, `$1export async function ${snakeToCamel(fn)}`);
    } else if (/^def\s+(\w+)/.test(trimmed)) {
      const fn = trimmed.match(/^def\s+(\w+)/)[1];
      if (!inClass) exports.push(snakeToCamel(fn));
      line = line.replace(/^(\s*)def\s+(\w+)/, `$1export function ${snakeToCamel(fn)}`);
    }

    line = line
      .replace(/\*\*/g, "**")
      .replace(/f"([^"]*)"/g, '"$1"')
      .replace(/f'([^']*)'/g, "'$1'");

    if (inClass && trimmed && line.search(/\S/) <= classIndent && !trimmed.startsWith("@") && !/^def /.test(trimmed) && !/^async def/.test(trimmed)) {
      if (!out[out.length - 1]?.trim().endsWith("}")) out.push("}");
      inClass = false;
    }

    out.push(line);
  }

  if (inClass) out.push("}");

  if (isInit) {
    const initOut = [
      "/**",
      ` * Barrel converted from ${pyPath}`,
      " */",
      "// @ts-nocheck",
      "",
    ];
    for (const line of lines) {
      const m = line.match(/^from core\.[\w.]+\.(\w+)\s+import\s+(.+)$/);
      if (m) {
        const mod = m[1];
        const names = m[2].replace(/[()]/g, "").split(",").map((s) => s.trim().split(" as ")[0]);
        for (const n of names) {
          if (n && n !== "*") initOut.push(`export { ${snakeToCamel(n)} } from "./${snakeToCamel(mod)}.js";`);
        }
      }
    }
    return initOut.join("\n") + "\n";
  }

  return out.join("\n") + "\n";
}

function loadManifest() {
  const raw = execSync("git ls-tree -r --name-only origin/python -- core/", {
    cwd: root,
    encoding: "utf-8",
  });
  writeFileSync(manifestPath, raw, "utf-8");
  return raw
    .split(/\r?\n/)
    .map((l) => l.replace(/\0/g, "").trim())
    .filter((l) => l.endsWith(".py"));
}

function main() {
  const manifest = loadManifest();
  console.log(`Converting ${manifest.length} Python modules...`);

  if (existsSync(legacyRoot)) rmSync(legacyRoot, { recursive: true, force: true });
  if (existsSync(srcRoot)) {
    mkdirSync(legacyRoot, { recursive: true });
    console.log("Backing up existing src/ to src-legacy-handwritten/");
    execSync(
      `powershell -NoProfile -Command "Copy-Item -Path '${srcRoot.replace(/'/g, "''")}' -Destination '${legacyRoot.replace(/'/g, "''")}' -Recurse -Force"`,
      { stdio: "inherit" },
    );
    rmSync(srcRoot, { recursive: true, force: true });
  }
  mkdirSync(srcRoot, { recursive: true });

  let ok = 0;
  let fail = 0;
  const failures = [];

  for (const pyPath of manifest) {
    const py = gitShow(pyPath);
    if (py == null) {
      fail++;
      failures.push(pyPath);
      continue;
    }
    const tsRel = pyCorePathToTs(pyPath);
    const tsFull = join(srcRoot, tsRel);
    mkdirSync(dirname(tsFull), { recursive: true });
    try {
      const ts = convertPythonToTs(py, pyPath, tsRel);
      writeFileSync(tsFull, ts, "utf-8");
      ok++;
    } catch (e) {
      fail++;
      failures.push(`${pyPath}: ${e.message}`);
    }
    if ((ok + fail) % 200 === 0) console.log(`  progress: ${ok + fail}/${manifest.length}`);
  }

  const indexTs = `/**
 * WebWeaveX — full Python core library port (npm package entry).
 * @generated
 */
// @ts-nocheck
export * from "./kernel/runtimePipeline.js";
export * from "./crypto/kaalkaRuntimeEngine.js";
export * from "./contracts/runtimeContracts.js";
export * from "./graph/runtimeGraphEngine.js";
export * from "./memory/runtimeMemoryEngine.js";
export * from "./replay/replayEquivalenceEngine.js";
export * from "./reconstruction/runtimeReconstructionEngine.js";
export * from "./orchestration/orchestrationEngine.js";
export * from "./semantic/semanticOrchestrator.js";
export const VERSION = "2.0.0";
`;
  writeFileSync(join(srcRoot, "index.ts"), indexTs, "utf-8");

  const report = [
    "# Python → JavaScript Library Conversion Report",
    "",
    `**Date:** ${new Date().toISOString()}`,
    "",
    "| Metric | Count |",
    "|--------|-------|",
    `| Python modules (core/) | ${manifest.length} |`,
    `| Converted | ${ok} |`,
    `| Failed | ${fail} |`,
    "",
    "## Layout",
    "",
    "- Python: `core/<package>/<module>.py`",
    "- JavaScript: `src/<package>/<moduleCamelCase>.ts`",
    "- `__init__.py` → `index.ts` barrel exports",
    "",
    "## Notes",
    "",
    "- Generated files include `// @ts-nocheck` for batch compile; refine critical paths for strict typing.",
    "- Prior hand-written `src/` backed up to `src-legacy-handwritten/`.",
    "- npm entry: `src/index.ts`",
    "",
    fail ? `### Failures (${fail})\n\n${failures.slice(0, 50).map((f) => `- ${f}`).join("\n")}` : "",
  ].join("\n");

  mkdirSync(dirname(reportPath), { recursive: true });
  writeFileSync(reportPath, report, "utf-8");

  console.log(`Done: ${ok} converted, ${fail} failed`);
  console.log(`Report: ${reportPath}`);
}

main();
