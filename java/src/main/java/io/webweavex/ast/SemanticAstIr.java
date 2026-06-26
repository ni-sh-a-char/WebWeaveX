package io.webweavex.ast;

import io.webweavex.determinism.Normalization;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.ast.semantic_ast_ir_engine.compile_semantic_ast_ir} + the three pure AST
 * sub-engines ({@code symbol_resolution_engine}, {@code control_flow_engine},
 * {@code execution_path_engine}). Builds on {@link PythonAstEngine}. Reusable foundation for the AST
 * cluster ({@code query_semantics}/{@code reason_semantically}/{@code compile_repository}).
 */
public final class SemanticAstIr {

    private SemanticAstIr() {
    }

    private static final int MAX_EXECUTION_PATHS = 100;

    @SuppressWarnings("unchecked")
    private static List<Object> asList(Object o) {
        return o instanceof List ? (List<Object>) o : new ArrayList<>();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : new LinkedHashMap<>();
    }

    /** {@code core.ast.symbol_resolution_engine.resolve_symbols}. */
    public static Map<String, Object> resolveSymbols(Map<String, Object> astIr) {
        List<Object> symbols = new ArrayList<>();
        for (Object fObj : asList(astIr.get("functions"))) {
            Map<String, Object> fn = asMap(fObj);
            Map<String, Object> s = new LinkedHashMap<>();
            s.put("symbol", fn.get("name"));
            s.put("kind", "function");
            s.put("args", fn.getOrDefault("args", new ArrayList<>()));
            symbols.add(s);
        }
        for (Object cObj : asList(astIr.get("classes"))) {
            Map<String, Object> cls = asMap(cObj);
            Map<String, Object> s = new LinkedHashMap<>();
            s.put("symbol", cls.get("name"));
            s.put("kind", "class");
            s.put("bases", cls.getOrDefault("bases", new ArrayList<>()));
            symbols.add(s);
        }
        symbols.sort((a, b) -> Normalization.codePointCompare(
                String.valueOf(asMap(a).get("symbol")), String.valueOf(asMap(b).get("symbol"))));
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("symbols", symbols);
        out.put("symbol_count", (long) symbols.size());
        out.put("grounded", true);
        return out;
    }

    /** {@code core.ast.control_flow_engine.build_control_flow_graph}. */
    public static Map<String, Object> buildControlFlowGraph(Map<String, Object> astIr) {
        List<Object> funcs = asList(astIr.get("functions"));
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        for (Object fObj : funcs) {
            Map<String, Object> n = new LinkedHashMap<>();
            n.put("id", asMap(fObj).get("name"));
            n.put("type", "function");
            nodes.add(n);
        }
        for (int i = 0; i < funcs.size() - 1; i++) {
            Map<String, Object> e = new LinkedHashMap<>();
            e.put("from", asMap(funcs.get(i)).get("name"));
            e.put("to", asMap(funcs.get(i + 1)).get("name"));
            e.put("relation", "possible_flow");
            edges.add(e);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("bounded", true);
        out.put("deterministic", true);
        return out;
    }

    /** {@code core.ast.execution_path_engine.reconstruct_execution_paths}. */
    public static Map<String, Object> reconstructExecutionPaths(Map<String, Object> cfg) {
        List<Object> nodes = asList(cfg.get("nodes"));
        List<Object> paths = new ArrayList<>();
        int limit = Math.min(nodes.size(), MAX_EXECUTION_PATHS);
        for (int i = 0; i < limit; i++) {
            List<Object> p = new ArrayList<>();
            p.add(asMap(nodes.get(i)).get("id"));
            paths.add(p);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("paths", paths);
        out.put("path_count", (long) paths.size());
        out.put("bounded", true);
        return out;
    }

    /** {@code core.ast.semantic_ast_ir_engine.compile_semantic_ast_ir}. */
    public static Map<String, Object> compileSemanticAstIr(String code) {
        Map<String, Object> astIr = PythonAstEngine.parsePythonAst(code);
        Map<String, Object> symbols = resolveSymbols(astIr);
        Map<String, Object> cfg = buildControlFlowGraph(astIr);
        Map<String, Object> executionPaths = reconstructExecutionPaths(cfg);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("ast", astIr);
        out.put("symbols", symbols);
        out.put("control_flow_graph", cfg);
        out.put("execution_paths", executionPaths);
        out.put("semantic_grounded", true);
        out.put("deterministic", true);
        return out;
    }
}
