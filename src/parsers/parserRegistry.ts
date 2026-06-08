/**
 * Parser registry — faithful port of core/parsers/parser_registry.py.
 * Hand-written production module (protected).
 */
import * as py from "../runtime/pyCompat.js";
import { parseAst } from "./astEngine.js";
import { buildCallGraph } from "./callGraphEngine.js";
import { resolveDependencies } from "./dependencyResolutionEngine.js";
import { resolveImports } from "./importResolutionEngine.js";
import { ParserBudget, enforceBudget } from "./parserBudgetEngine.js";
import { recoverSyntax } from "./parserRecoveryEngine.js";
import { resolveRuntime } from "./runtimeResolutionEngine.js";
import { resolveApiSurface } from "./apiResolutionEngine.js";
import { resolveFrameworks } from "./frameworkResolutionEngine.js";
import { buildSemanticGraph } from "./semanticGraphEngine.js";
import { resolveSymbols } from "./symbolResolutionEngine.js";
import { normalizeParserOutput } from "./parserOutputEngine.js";
import { requireParserEvidence } from "./formalParserGroundingEngine.js";

const _EXTENSION_LANGUAGE: Record<string, string> = {
  ".py": "python",
  ".js": "javascript",
  ".jsx": "javascript",
  ".ts": "typescript",
  ".tsx": "typescript",
  ".java": "java",
  ".kt": "kotlin",
  ".go": "go",
  ".rs": "rust",
  ".dart": "dart",
};

export class ParserRegistry {
  static detect_language(path = "", hint = ""): string {
    if (py.truthy(hint)) return String(hint).toLowerCase();
    const ext = py.path(path).suffix.toLowerCase();
    return _EXTENSION_LANGUAGE[ext] ?? "text";
  }

  static parse(
    source: string,
    path = "",
    language_hint = "",
    budget: ParserBudget | null = null,
  ): Record<string, unknown> {
    const language = ParserRegistry.detect_language(path, language_hint);
    const bounded = enforceBudget(source, budget);
    const recovered = recoverSyntax(bounded, language);
    const astTree = parseAst(recovered, language) as Record<string, unknown>;
    const symbols = resolveSymbols(recovered, language, astTree) as Record<string, unknown>;
    const calls = buildCallGraph(recovered, language) as Record<string, unknown>;
    const imports = resolveImports(symbols, py.truthy(path) ? path : language) as Record<string, unknown>;
    const deps = resolveDependencies(recovered, path) as Record<string, unknown>;
    const runtime = resolveRuntime(
      py.get(deps, "dependencies", []) as unknown[],
      py.get(symbols, "imports", []) as unknown[],
    ) as Record<string, unknown>;
    const frameworks = resolveFrameworks(
      py.get(deps, "dependencies", []) as unknown[],
      py.get(symbols, "imports", []) as unknown[],
      py.get(symbols, "decorators") as unknown,
    ) as Record<string, unknown>;
    const apiSurface = resolveApiSurface(recovered, language, path) as Record<string, unknown>;
    const parsed: Record<string, unknown> = {
      language,
      source_id: py.truthy(path) ? path : language,
      ast: astTree,
      symbols,
      calls,
      imports,
      dependencies: deps,
      runtime,
      frameworks,
      api_surface: apiSurface,
    };
    parsed["semantic_graph"] = buildSemanticGraph(parsed);
    const evidence: Record<string, unknown> = {
      ast: py.truthy(py.get(astTree, "nodes")),
      symbols: py.truthy(py.get(symbols, "symbols")),
      calls: py.truthy(py.get(calls, "calls")),
      dependencies: py.truthy(py.get(deps, "dependencies")),
      tree_sitter: language !== "python" && !py.truthy(py.get(astTree, "parse_error")),
    };
    parsed["evidence"] = evidence;
    if (py.truthy(py.get(astTree, "parse_error"))) {
      evidence["parse_error"] = true;
    }
    const normalized = normalizeParserOutput(parsed) as Record<string, unknown>;
    Object.assign(parsed, normalized);
    parsed["parser_grounding"] = requireParserEvidence(parsed);
    return parsed;
  }
}

export function parseSource(
  source: string,
  path = "",
  language_hint = "",
  budget: ParserBudget | null = null,
): Record<string, unknown> {
  return ParserRegistry.parse(source, path, language_hint, budget);
}

/* legacy registry surface (kept for compatibility) */
const REGISTRY = new Map<string, Record<string, unknown>>();

export function registerParser(name: string, meta: Record<string, unknown>): void {
  REGISTRY.set(name, { ...meta, name, bounded: true });
}

export function listParsers(): Array<Record<string, unknown>> {
  return [...REGISTRY.values()].sort((a, b) => (String(a.name) < String(b.name) ? -1 : 1));
}

export function getParser(name: string): Record<string, unknown> | undefined {
  return REGISTRY.get(name);
}
