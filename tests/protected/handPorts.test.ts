import { beforeAll, afterAll, describe, expect, it } from "vitest";
import { spawn, type ChildProcess } from "node:child_process";
import { parsePythonAst } from "../../src/ast/pythonAstEngine.js";
import { parsePythonAst as repoParsePythonAst } from "../../src/repository/ast/pythonAstEngine.js";
import { extractSemanticAst } from "../../src/repository/semantic/semanticAstEngine.js";
import { buildSsaForm } from "../../src/ssa/ssaBuilderEngine.js";
import {
  dumpsDeterministic,
  dumpsCanonical,
  dumpsCanonicalV4,
  dumpsCanonicalV5,
  dumps_deterministic,
} from "../../src/serialize/deterministicSerializer.js";
import { ParserRegistry, parseSource, registerParser, getParser, listParsers } from "../../src/parsers/parserRegistry.js";
import { syncPlaywright, FakeBrowser, FakeContext, FakePage } from "../../src/browser/syncPlaywright.js";
import * as py from "../../src/runtime/pyCompat.js";

const PY_SAMPLE = [
  "import os, sys as system",
  "from pathlib import Path",
  "",
  "MAX = 10",
  "a, b = 1, 2",
  "",
  "def outer(x, y=2, *args):",
  "    inner = x + y",
  "    return inner",
  "",
  "async def later(q):",
  "    z = q",
  "",
  "class Widget(Base):",
  "    field = 'v'",
  "    def method(self, n):",
  "        count = n",
  "        return count",
  "",
  "result = outer(",
  "    1,",
  "    2,",
  ")",
].join("\n");

describe("python source analyzer (ast/pythonAstEngine)", () => {
  it("summarizes imports, functions, classes, assignments", () => {
    const out = parsePythonAst(PY_SAMPLE) as Record<string, Record<string, unknown>[]>;
    expect(out.language).toBe("python");
    const importEntries = out.imports;
    expect(importEntries.length).toBeGreaterThanOrEqual(2);
    const fnNames = out.functions.map((f) => f.name);
    expect(fnNames).toContain("outer");
    expect(fnNames).toContain("later");
    expect(fnNames).toContain("method");
    expect(out.classes.map((c) => c.name)).toContain("Widget");
    const targets = out.assignments.flatMap((a) => a.targets as string[]);
    expect(targets).toContain("MAX");
    expect(targets).toContain("result");
    expect(targets).toContain("inner");
  });

  it("tracks line spans for blocks", () => {
    const out = parsePythonAst("def f():\n    a = 1\n    b = 2\nc = 3\n") as {
      functions: { node: { lineno: number; end_lineno: number } }[];
    };
    expect(out.functions[0]!.node.lineno).toBe(1);
    expect(out.functions[0]!.node.end_lineno).toBe(3);
  });

  it("raises SyntaxError on clearly invalid python", () => {
    expect(() => parsePythonAst("<div>x</div>")).toThrowError(/invalid syntax/);
    expect(() => parsePythonAst(")broken")).toThrowError(/invalid syntax/);
  });

  it("handles empty source, comments and triple strings", () => {
    expect((parsePythonAst("") as { functions: unknown[] }).functions).toEqual([]);
    const out = parsePythonAst('# comment\n"""doc\nstring"""\nx = 1\n') as {
      assignments: { targets: string[] }[];
    };
    expect(out.assignments.flatMap((a) => a.targets)).toContain("x");
  });
});

describe("repository python ast summary", () => {
  it("reports nodes, imports and calls", () => {
    const out = repoParsePythonAst("import os\nfrom a.b import c\ndef f():\n    g(h(1))\n") as {
      nodes: { name: string; kind: string }[];
      imports: { module: string; kind: string }[];
      calls: { target: string }[];
    };
    expect(out.nodes.map((n) => n.name)).toContain("f");
    expect(out.imports.map((i) => i.module)).toContain("os");
    expect(out.imports.map((i) => i.module)).toContain("a.b");
    expect(out.calls.map((c) => c.target)).toContain("g");
    expect(out.calls.map((c) => c.target)).toContain("h");
  });

  it("returns parse_error payload on invalid source", () => {
    const out = repoParsePythonAst("<nope>", "myfile.py") as { parse_error: string; nodes: unknown[] };
    expect(out.parse_error).toContain("myfile.py");
    expect(out.nodes).toEqual([]);
  });
});

describe("semantic ast extraction", () => {
  it("detects python plus regex-derived symbols", () => {
    const out = extractSemanticAst("import os\ndef f(a):\n    pass\n");
    expect(out.languages).toContain("python");
    expect(out.functions).toContain("f");
    expect(out.imports).toContain("os");
  });

  it("detects other languages and structures", () => {
    const src = [
      "interface Shape { kind: string }",
      "export const make = () => 1;",
      "function render(props) { return props; }",
      "const widget = require('widget');",
      "class Box extends Base {}",
      "@Injectable",
      "List<string, int> values;",
      "trait Drawable {}",
    ].join("\n");
    const out = extractSemanticAst(src);
    expect(out.languages).toContain("javascript");
    expect(out.languages).toContain("typescript");
    expect(out.interfaces).toContain("Shape");
    expect(out.classes).toContain("Box");
    expect(out.traits).toContain("Drawable");
    expect(out.imports).toContain("widget");
    expect(out.exports).toContain("make");
    expect(out.annotations).toContain("Injectable");
    expect(out.decorators).toContain("@Injectable");
    expect(out.generics.length).toBeGreaterThan(0);
  });

  it("returns empty structure for plain html", () => {
    const out = extractSemanticAst("<div id='probe'>x</div>");
    expect(out.languages).toEqual([]);
    expect(out.symbols).toEqual([]);
  });
});

describe("ssa builder", () => {
  it("versions assignments", () => {
    const out = buildSsaForm("a = 1\nb = 2\na = 3\n") as {
      ssa_assignments: { variable: string; ssa_name: string }[];
      variable_versions: Record<string, number>;
    };
    expect(out.variable_versions.a).toBe(2);
    expect(out.variable_versions.b).toBe(1);
    expect(out.ssa_assignments.map((s) => s.ssa_name)).toContain("a_2");
  });

  it("propagates syntax errors from the analyzer", () => {
    expect(() => buildSsaForm("<bad>")).toThrowError(/invalid syntax/);
  });
});

describe("deterministic serializer", () => {
  it("matches python json formatting and sorts deeply", () => {
    const out = dumpsDeterministic({ b: 1, a: [3, 1, 2], s: "x" });
    expect(out).toBe('{"a":[1,2,3],"b":1,"s":"x"}');
  });

  it("renders boxed floats with float formatting", () => {
    // Integral floats canonicalize to int (cross-language contract).
    expect(dumpsDeterministic({ v: py.F(2) })).toBe('{"v":2}');
    expect(dumpsDeterministic({ v: py.F(0.16800000000000001) })).toBe('{"v":0.168}');
  });

  it("normalizes NFC, clamps non-finite, handles null/bool", () => {
    expect(dumpsDeterministic(["é"])).toBe(dumpsDeterministic(["é"]));
    expect(dumpsDeterministic(Infinity)).toBe("0");
    expect(dumpsDeterministic(py.F(Infinity))).toBe("0");
    expect(dumpsDeterministic({ t: true, n: null })).toBe('{"n":null,"t":true}');
    expect(dumpsDeterministic(0.1 + 0.2)).toBe("0.3");
  });

  it("exposes all aliases", () => {
    for (const fn of [dumpsCanonical, dumpsCanonicalV4, dumpsCanonicalV5, dumps_deterministic]) {
      expect(fn({ k: 1 })).toBe('{"k":1}');
    }
  });
});

describe("parser registry port", () => {
  it("detects languages by hint and extension", () => {
    expect(ParserRegistry.detect_language("", "PYTHON")).toBe("python");
    expect(ParserRegistry.detect_language("a/b.ts")).toBe("typescript");
    expect(ParserRegistry.detect_language("a/b.rs")).toBe("rust");
    expect(ParserRegistry.detect_language("a/b.unknown")).toBe("text");
  });

  it("parses python source end to end", () => {
    const out = parseSource("import os\ndef f():\n    return 1\n", "m.py");
    expect(out.language).toBe("python");
    expect(out.source_id).toBe("m.py");
    expect(out.semantic_graph).toBeDefined();
    expect((out.evidence as Record<string, unknown>).ast).toBeDefined();
    expect(out.parser_grounding).toBeDefined();
  });

  it("parses non-python source with language fallback", () => {
    const out = ParserRegistry.parse("function f() { return 1; }", "m.js");
    expect(out.language).toBe("javascript");
  });

  it("keeps the legacy registry surface", () => {
    registerParser("zz-test", { lang: "test" });
    expect(getParser("zz-test")?.lang).toBe("test");
    expect(getParser("missing-name")).toBeUndefined();
    expect(listParsers().length).toBeGreaterThan(0);
  });
});

describe("sync playwright facade", () => {
  let server: ChildProcess | null = null;

  beforeAll(async () => {
    server = spawn("python", ["-B", "tools/convergence/probe_http_server.py"], {
      stdio: "ignore",
    });
    await new Promise((r) => setTimeout(r, 1200));
  });

  afterAll(() => {
    server?.kill();
  });

  it("provides the python sync_api object graph", () => {
    const pw = syncPlaywright().start();
    const browser = pw.chromium.launch(true);
    expect(browser).toBeInstanceOf(FakeBrowser);
    const ctx = browser.new_context("UA", { width: 800, height: 600 }, "en-US", "UTC");
    expect(ctx).toBeInstanceOf(FakeContext);
    const page = ctx.new_page();
    expect(page).toBeInstanceOf(FakePage);
    expect(ctx.pages()).toHaveLength(1);
    ctx.add_cookies([{ name: "c", value: "1", url: "http://127.0.0.1:8787" }]);
    expect(ctx.cookies()).toHaveLength(1);
    page.set_extra_http_headers({ "x-probe": "1" });
    page.bring_to_front();
    pw.stop();
    browser.close();
    ctx.close();
    page.close();
  });

  it("captures a real page and replays reads", () => {
    const ctx = new FakeBrowser().new_context();
    const page = ctx.new_page();
    const requests: unknown[] = [];
    page.on("request", (r) => requests.push(r));
    page.goto("http://127.0.0.1:8787/probe");
    expect(page.title()).toBe("WebWeaveX Probe");
    expect(page.content()).toContain("Probe Fixture");
    expect(page.url).toContain("127.0.0.1");
    expect(requests.length).toBeGreaterThan(0);
    expect(page.evaluate("Object.keys(localStorage)")).toEqual({});
    expect(page.evaluate("document.body.scrollHeight")).toHaveProperty("scrollHeight");
    expect(page.evaluate("window.scrollTo(0, 10)")).toBeNull();
    expect(page.evaluate("1 + 1")).toBeNull();

    const h1 = page.query_selector("h1");
    expect(h1?.inner_text()).toBe("Probe Fixture");
    expect(h1?.text_content()).toBe("Probe Fixture");
    const links = page.query_selector_all("a");
    expect(links.length).toBe(2);
    expect(links[0]!.get_attribute("href")).toBe("/alpha");
    expect(page.query_selector("#missing-id")).toBeNull();
    expect(page.query_selector(".missing-class")).toBeNull();

    expect(() => page.click("#nope")).toThrowError(/Timeout 30000ms/);
    expect(() => page.fill("#nope", "v")).toThrowError(/Timeout/);
    expect(() => page.hover("#nope")).toThrowError(/Timeout/);
    expect(() => page.select_option("#nope", "v")).toThrowError(/Timeout/);
    expect(page.wait_for_selector("h1")).toBeTruthy();
    page.click("a");
    expect(ctx.cookies()).toBeDefined();
  }, 120_000);

  it("raises Page.goto errors for unreachable targets", () => {
    const page = new FakeBrowser().new_context().new_page();
    expect(() => page.goto("http://127.0.0.1:1/none")).toThrowError(/Page.goto/);
  }, 120_000);
});
