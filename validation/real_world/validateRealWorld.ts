/**
 * Real-world certification — JS graph probes; optional Python compare when WEBWEAVEX_COMPARE_PYTHON=1.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const matrixPath = join(root, "validation/real_world/urlMatrix.json");
const archive = join(root, "docs/archive");
const specs = join(root, "docs/specs");

const DRIFT_THRESHOLD_PCT = 5;
const limit = Number(process.env.REALWORLD_LIMIT || "0");
const comparePython = process.env.WEBWEAVEX_COMPARE_PYTHON === "1";

type UrlRow = { category: string; url: string };
type ProbeRow = {
  category: string;
  url: string;
  py_bounded?: boolean;
  js_bounded?: boolean;
  py_nodes?: number;
  js_nodes?: number;
  match: boolean;
  error?: string;
};

async function loadPythonProbes(count: number): Promise<Map<string, { bounded: boolean; node_count: number }>> {
  const map = new Map<string, { bounded: boolean; node_count: number }>();
  if (!comparePython) return map;
  const { execSync } = await import("node:child_process");
  execSync(`python -B tools/convergence/run_real_world_matrix.py ${limit || count}`, {
    cwd: root,
    stdio: "inherit",
  });
  const pyPath = join(specs, "real_world_python.json");
  const pyData = JSON.parse(readFileSync(pyPath, "utf-8")) as {
    results: Array<{ url: string; bounded?: boolean; node_count?: number; error?: string }>;
  };
  for (const r of pyData.results) {
    if (r.error) continue;
    map.set(r.url, { bounded: Boolean(r.bounded), node_count: Number(r.node_count ?? 0) });
  }
  return map;
}

async function main(): Promise<void> {
  if (!existsSync(matrixPath)) {
    throw new Error(`Missing ${matrixPath}. Commit urlMatrix.json or generate offline.`);
  }
  const matrix = JSON.parse(readFileSync(matrixPath, "utf-8")) as { count: number; urls: UrlRow[] };
  let urls = matrix.urls;
  if (limit > 0) urls = urls.slice(0, limit);

  const pyMap = await loadPythonProbes(urls.length);
  const rows: ProbeRow[] = [];
  let match = 0;
  let fail = 0;
  let drift = 0;

  for (const { category, url } of urls) {
    const py = pyMap.get(url);
    try {
      const graph = buildRuntimeGraph({
        browser: { url, category, nodes: [{ id: `url:${category}`, type: category }] },
      });
      const jsBounded = graph.bounded === true;
      const jsNodes = graph.nodes.length;
      const boundedMatch = comparePython && py ? py.bounded === jsBounded : jsBounded;
      const nodesMatch = comparePython && py ? py.node_count > 0 && jsNodes > 0 : jsNodes > 0;
      const ok = comparePython ? Boolean(py && boundedMatch && nodesMatch) : boundedMatch && nodesMatch;
      if (ok) match += 1;
      else fail += 1;
      if (py && (!boundedMatch || !nodesMatch)) drift += 1;
      rows.push({
        category,
        url,
        py_bounded: py?.bounded,
        js_bounded: jsBounded,
        py_nodes: py?.node_count,
        js_nodes: jsNodes,
        match: ok,
      });
    } catch (e) {
      fail += 1;
      rows.push({ category, url, match: false, error: e instanceof Error ? e.message : String(e) });
    }
  }

  const total = rows.length;
  const matchPct = total ? (100 * match) / total : 0;
  const failPct = total ? (100 * fail) / total : 0;
  const driftPct = total ? (100 * drift) / total : 0;
  const pass = comparePython
    ? total >= 1000 && driftPct <= DRIFT_THRESHOLD_PCT && matchPct >= 100 - DRIFT_THRESHOLD_PCT
    : total >= 100 && failPct <= DRIFT_THRESHOLD_PCT && matchPct >= 100 - DRIFT_THRESHOLD_PCT;

  const report = {
    measured_at: new Date().toISOString(),
    urls_total: matrix.count,
    urls_executed: total,
    match_count: match,
    fail_count: fail,
    drift_count: drift,
    match_pct: Math.round(matchPct * 100) / 100,
    fail_pct: Math.round(failPct * 100) / 100,
    drift_pct: Math.round(driftPct * 100) / 100,
    drift_threshold_pct: DRIFT_THRESHOLD_PCT,
    pass,
  };

  mkdirSync(specs, { recursive: true });
  writeFileSync(join(specs, "real_world_probe.json"), JSON.stringify(report, null, 2), "utf-8");

  const md = [
    "# FINAL REAL WORLD CERTIFICATION",
    "",
    `**Measured:** ${report.measured_at}`,
    "",
    `**Status:** ${pass ? "PASS" : "FAIL"}`,
    "",
    "| Metric | Value |",
    "|--------|-------|",
    `| URLs in matrix | ${matrix.count} |`,
    `| URLs executed | ${total} |`,
    `| Match % | ${report.match_pct}% |`,
    `| Failure % | ${report.fail_pct}% |`,
    `| Drift % | ${report.drift_pct}% |`,
    `| Drift threshold | ≤${DRIFT_THRESHOLD_PCT}% |`,
    "",
    comparePython
      ? "Python and JavaScript graph probes executed per URL (WEBWEAVEX_COMPARE_PYTHON=1)."
      : "JavaScript-only graph probes (no Python runtime). Set WEBWEAVEX_COMPARE_PYTHON=1 for cross-language compare.",
    "",
  ].join("\n");
  mkdirSync(archive, { recursive: true });
  writeFileSync(join(archive, "FINAL_REAL_WORLD_CERTIFICATION.md"), md, "utf-8");

  console.log("real_world", report);
  if (!pass) process.exit(1);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
