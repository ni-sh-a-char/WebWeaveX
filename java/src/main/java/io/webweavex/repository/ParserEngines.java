package io.webweavex.repository;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.PyJsonParse;
import io.webweavex.determinism.PyText;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Port of the canonical Python parser sub-engines that feed {@code compile_repository_ir}'s observable
 * output — the text-path (regex) engines from {@code core.parsers.*}: symbol resolution, call graph,
 * dependency resolution, runtime/framework resolution, import resolution, syntax recovery, parser
 * budget. Reuse of the existing Python/JS implementation (Rule 3); epistemic-free (normalize/cognition
 * fields are discarded downstream — see {@code FRONTIER_ANALYSIS.md}). Reusable foundation for the
 * repository IR / AST cluster.
 */
public final class ParserEngines {

    private ParserEngines() {
    }

    private static TreeSet<String> cpSet() {
        return new TreeSet<>(Normalization::codePointCompare);
    }

    private static List<Object> sortedList(Set<String> s) {
        return new ArrayList<>(s);
    }

    private static List<String> findAll(Pattern p, String src) {
        List<String> out = new ArrayList<>();
        Matcher m = p.matcher(src);
        while (m.find()) {
            out.add(m.group(1));
        }
        return out;
    }

    // ---------------------------------------------------------------- enforce_budget
    private static final int MAX_BYTES = 5_000_000;

    /** {@code core.parsers.parser_budget_engine.enforce_budget}. */
    public static String enforceBudget(String source) {
        String s = source == null ? "" : source;
        byte[] raw = s.getBytes(StandardCharsets.UTF_8);
        if (raw.length <= MAX_BYTES) {
            return s;
        }
        return new String(raw, 0, MAX_BYTES, StandardCharsets.UTF_8);
    }

    // ---------------------------------------------------------------- recover_syntax
    /** {@code core.parsers.syntax_recovery_engine.recover_syntax}. */
    public static String recoverSyntax(String source, String language) {
        String text = source == null ? "" : source;
        if (language.toLowerCase().equals("python")) {
            List<String> lines = PyText.splitlines(text);
            List<String> repaired = new ArrayList<>();
            int balance = 0;
            for (String ln : lines) {
                repaired.add(rstrip(ln));
                balance += count(ln, '(') - count(ln, ')');
            }
            while (balance > 0) {
                repaired.add(")");
                balance--;
            }
            return String.join("\n", repaired);
        }
        return text;
    }

    private static int count(String s, char c) {
        int n = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == c) {
                n++;
            }
        }
        return n;
    }

    private static String rstrip(String s) {
        int end = s.length();
        while (end > 0 && Character.isWhitespace(s.charAt(end - 1))) {
            end--;
        }
        return s.substring(0, end);
    }

    // ---------------------------------------------------------------- resolve_symbols (text/regex path)
    private static final String ID = "[A-Za-z_][A-Za-z0-9_]*";
    private static final Pattern RE_INTERFACE = Pattern.compile("\\binterface\\s+(" + ID + ")");
    private static final Pattern RE_TRAIT = Pattern.compile("\\btrait\\s+(" + ID + ")");
    private static final Pattern RE_CLASS = Pattern.compile("\\bclass\\s+(" + ID + ")");
    private static final Pattern RE_FUNC = Pattern.compile("\\b(?:def|function|fun|fn)\\s+(" + ID + ")");
    private static final Pattern RE_METHOD = Pattern.compile("\\b(?:public|private|protected)?\\s*\\w+\\s+(\\w+)\\s*\\(");

    /** {@code core.parsers.symbol_resolution_engine.resolve_symbols} — text/regex path. */
    public static Map<String, Object> resolveSymbols(String source, String language) {
        String src = source == null ? "" : source;
        TreeSet<String> classes = cpSet();
        TreeSet<String> functions = cpSet();
        TreeSet<String> methods = cpSet();
        TreeSet<String> interfaces = cpSet();
        TreeSet<String> traits = cpSet();
        // text path: the python-ast branch is skipped (lang != "python"); regex block always runs.
        interfaces.addAll(findAll(RE_INTERFACE, src));
        traits.addAll(findAll(RE_TRAIT, src));
        classes.addAll(findAll(RE_CLASS, src));
        functions.addAll(findAll(RE_FUNC, src));
        methods.addAll(findAll(RE_METHOD, src));

        TreeSet<String> symbols = cpSet();
        symbols.addAll(classes);
        symbols.addAll(functions);
        symbols.addAll(methods);
        symbols.addAll(interfaces);
        symbols.addAll(traits);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("classes", sortedList(classes));
        out.put("functions", sortedList(functions));
        out.put("methods", sortedList(methods));
        out.put("interfaces", sortedList(interfaces));
        out.put("traits", sortedList(traits));
        out.put("imports", new ArrayList<>());
        out.put("exports", new ArrayList<>());
        out.put("decorators", new ArrayList<>());
        out.put("symbols", sortedList(symbols));
        return out;
    }

    // ---------------------------------------------------------------- build_call_graph (text path)
    private static final Pattern RE_CALL = Pattern.compile("([A-Za-z_][A-Za-z0-9_]*)\\s*\\(");
    private static final Set<String> CALL_SKIP = Set.of("if", "for", "while", "switch", "return", "new", "typeof");

    /** {@code core.parsers.call_graph_engine.build_call_graph} — text path. */
    public static Map<String, Object> buildCallGraph(String source, String language) {
        String src = source == null ? "" : source;
        TreeSet<String> uniq = new TreeSet<>((a, b) -> Normalization.codePointCompare(a, b));
        // text path: regex calls from "<module>"
        Matcher m = RE_CALL.matcher(src);
        while (m.find()) {
            String name = m.group(1);
            if (!CALL_SKIP.contains(name)) {
                uniq.add(name);
            }
        }
        List<Object> calls = new ArrayList<>();
        for (String to : uniq) {
            Map<String, Object> e = new LinkedHashMap<>();
            e.put("from", "<module>");
            e.put("to", to);
            calls.add(e);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("calls", calls);
        return out;
    }

    // ---------------------------------------------------------------- resolve_dependencies
    private static final Pattern RE_CARGO = Pattern.compile("^([A-Za-z0-9_-]+)\\s*=\\s*\"", Pattern.MULTILINE);
    private static final Pattern RE_GO = Pattern.compile("^\\s*([a-zA-Z0-9./_-]+)\\s+v", Pattern.MULTILINE);
    private static final Pattern RE_PIN = Pattern.compile("^\\s*([A-Za-z0-9_.-]+)==[A-Za-z0-9_.-]+\\s*$", Pattern.MULTILINE);
    private static final Pattern RE_OP = Pattern.compile("^\\s*([A-Za-z0-9_.-]+)\\s*[><=~!]", Pattern.MULTILINE);
    private static final Pattern RE_BARE = Pattern.compile("^\\s*([A-Za-z0-9_.-]+)\\s*$", Pattern.MULTILINE);
    private static final Pattern RE_IMPL = Pattern.compile("implementation\\s+[\"']([A-Za-z0-9_.:-]+)[\"']");
    private static final Pattern RE_ARTIFACT = Pattern.compile("<artifactId>([^<]+)</artifactId>");

    /** {@code core.parsers.dependency_resolution_engine.resolve_dependencies}. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> resolveDependencies(String source, String path) {
        String src = source == null ? "" : source;
        TreeSet<String> deps = cpSet();
        TreeSet<String> managers = cpSet();

        if (path.contains("package.json") || src.contains("\"dependencies\"")) {
            managers.add("npm");
            int start = src.indexOf('{');
            if (start >= 0) {
                int end = src.lastIndexOf('}');
                if (end >= start) {
                    try {
                        Object parsed = PyJsonParse.loads(src.substring(start, end + 1));
                        if (parsed instanceof Map) {
                            Map<String, Object> blob = (Map<String, Object>) parsed;
                            for (String section : new String[] {"dependencies", "devDependencies", "peerDependencies"}) {
                                Object block = blob.get(section);
                                if (block instanceof Map) {
                                    deps.addAll(((Map<String, Object>) block).keySet());
                                }
                            }
                        }
                    } catch (RuntimeException ignored) {
                        // json decode error -> pass
                    }
                }
            }
        }
        if (path.endsWith("Cargo.toml") || src.contains("[dependencies]")) {
            managers.add("cargo");
            deps.addAll(findAll(RE_CARGO, src));
        }
        if (path.endsWith("go.mod") || src.substring(0, Math.min(200, src.length())).contains("module ")) {
            managers.add("go");
            deps.addAll(findAll(RE_GO, src));
        }
        deps.addAll(findAll(RE_PIN, src));
        deps.addAll(findAll(RE_OP, src));
        deps.addAll(findAll(RE_BARE, src));
        deps.addAll(findAll(RE_IMPL, src));
        deps.addAll(findAll(RE_ARTIFACT, src));

        if (path.contains("requirements.txt") || src.contains("pip")) {
            managers.add("pip");
        }
        if (path.contains("build.gradle")) {
            managers.add("gradle");
        }
        if (path.contains("pom.xml")) {
            managers.add("maven");
        }
        if (path.contains("pubspec.yaml")) {
            managers.add("pub");
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("dependencies", sortedList(deps));
        out.put("package_managers", sortedList(managers));
        return out;
    }

    // ---------------------------------------------------------------- resolve_imports
    /** {@code core.parsers.import_resolution_engine.resolve_imports}. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> resolveImports(Map<String, Object> symbols, String sourceId) {
        TreeSet<String> imports = cpSet();
        TreeSet<String> exports = cpSet();
        if (symbols != null) {
            Object imp = symbols.get("imports");
            if (imp instanceof List) {
                for (Object o : (List<Object>) imp) {
                    imports.add(String.valueOf(o));
                }
            }
            Object exp = symbols.get("exports");
            if (exp instanceof List) {
                for (Object o : (List<Object>) exp) {
                    exports.add(String.valueOf(o));
                }
            }
        }
        TreeSet<String> nodes = cpSet();
        nodes.add(sourceId);
        nodes.addAll(imports);
        nodes.addAll(exports);
        List<Object> edges = new ArrayList<>();
        for (String imp : imports) {
            Map<String, Object> e = new LinkedHashMap<>();
            e.put("from", sourceId);
            e.put("to", imp);
            edges.add(e);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("nodes", sortedList(nodes));
        out.put("edges", edges);
        out.put("exports", sortedList(exports));
        return out;
    }

    // ---------------------------------------------------------------- resolve_runtime
    private static final Map<String, Set<String>> FRAMEWORK_HINTS = new LinkedHashMap<>();
    private static final Set<String> FRAMEWORK_DEPS = Set.of(
            "django", "flask", "fastapi", "react", "next", "express", "spring-boot", "spring",
            "flutter", "gin", "actix", "tokio");

    static {
        FRAMEWORK_HINTS.put("python", Set.of("django", "flask", "fastapi", "uvicorn", "celery"));
        FRAMEWORK_HINTS.put("node", Set.of("react", "next", "express", "nestjs", "@angular/core"));
        FRAMEWORK_HINTS.put("jvm", Set.of("spring-boot", "spring", "kotlin"));
        FRAMEWORK_HINTS.put("rust", Set.of("tokio", "actix-web"));
        FRAMEWORK_HINTS.put("go", Set.of("gin", "echo"));
        FRAMEWORK_HINTS.put("dart", Set.of("flutter"));
    }

    /** {@code core.parsers.runtime_resolution_engine.resolve_runtime}. */
    public static Map<String, Object> resolveRuntime(List<Object> dependencies, List<Object> imports) {
        Set<String> deps = new java.util.HashSet<>();
        for (Object d : dependencies == null ? List.of() : dependencies) {
            deps.add(String.valueOf(d).toLowerCase());
        }
        List<String> imps = new ArrayList<>();
        for (Object i : imports == null ? List.of() : imports) {
            imps.add(String.valueOf(i).toLowerCase());
        }
        TreeSet<String> runtimes = cpSet();
        TreeSet<String> frameworks = cpSet();
        TreeSet<String> apiInd = cpSet();
        for (Map.Entry<String, Set<String>> e : FRAMEWORK_HINTS.entrySet()) {
            boolean depHit = deps.stream().anyMatch(e.getValue()::contains);
            boolean impHit = imps.stream().anyMatch(i -> e.getValue().stream().anyMatch(i::contains));
            if (depHit || impHit) {
                runtimes.add(e.getKey());
                TreeSet<String> inter = cpSet();
                for (String h : e.getValue()) {
                    if (deps.contains(h)) {
                        inter.add(h);
                    }
                }
                frameworks.addAll(inter);
            }
        }
        if (imps.stream().anyMatch(i -> i.startsWith("python") || i.endsWith(".py"))) {
            runtimes.add("python");
        }
        if (deps.contains("fastapi") || deps.contains("flask") || deps.contains("django")) {
            apiInd.add("http_api");
        }
        if (deps.contains("graphql")) {
            apiInd.add("graphql");
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("runtimes", sortedList(runtimes));
        out.put("frameworks", sortedList(frameworks));
        out.put("api_indicators", sortedList(apiInd));
        return out;
    }

    // ---------------------------------------------------------------- resolve_frameworks
    /** {@code core.parsers.framework_resolution_engine.resolve_frameworks}. */
    public static Map<String, Object> resolveFrameworks(List<Object> dependencies, List<Object> imports,
            List<Object> decorators) {
        Set<String> deps = new java.util.HashSet<>();
        for (Object d : dependencies == null ? List.of() : dependencies) {
            deps.add(String.valueOf(d).toLowerCase());
        }
        StringBuilder impJoin = new StringBuilder();
        List<String> impList = new ArrayList<>();
        for (Object i : imports == null ? List.of() : imports) {
            if (impJoin.length() > 0) {
                impJoin.append(' ');
            }
            impJoin.append(String.valueOf(i));
            impList.add(String.valueOf(i).toLowerCase());
        }
        String imps = impJoin.toString().toLowerCase();
        Set<String> decs = new java.util.HashSet<>();
        for (Object d : decorators == null ? List.of() : decorators) {
            decs.add(String.valueOf(d).toLowerCase());
        }
        String[] impSplit = imps.isEmpty() ? new String[0] : imps.split(" ");
        TreeSet<String> detected = cpSet();
        TreeSet<String> indicators = cpSet();
        for (String fw : FRAMEWORK_DEPS) {
            boolean hit = deps.contains(fw) || imps.contains(fw) || decs.contains(fw);
            if (!hit) {
                for (String i : impSplit) {
                    if (i.contains(fw)) {
                        hit = true;
                        break;
                    }
                }
            }
            if (hit) {
                detected.add(fw);
            }
            if (deps.contains(fw)) {
                indicators.add(fw);
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("frameworks", sortedList(detected));
        out.put("indicators", sortedList(indicators));
        return out;
    }

    // ---------------------------------------------------------------- resolve_api_surface
    private static final Pattern RE_ROUTE_DEC =
            Pattern.compile("@(?:app|router)\\.(get|post|put|delete|patch)\\(['\"]([^'\"]+)");
    private static final Pattern RE_ROUTE_VERB =
            Pattern.compile("\\b(?:GET|POST|PUT|DELETE|PATCH)\\s+(/[^\\s'\"]+)");
    private static final Set<String> ROUTE_DECORATORS =
            Set.of("get", "post", "put", "delete", "patch", "route");

    /** {@code core.parsers.api_resolution_engine.resolve_api_surface} — text/regex path. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> resolveApiSurface(String source, String language) {
        String src = source == null ? "" : source;
        Map<String, Object> symbols = resolveSymbols(src, language);
        // raw routes preserves Python's mixed list (decorator strings, 2-tuples, path strings)
        // before the `sorted(set(str(r) ...))` collapse; `rest = bool(routes)` reads this raw list.
        List<String> raw = new ArrayList<>();
        Object decs = symbols.get("decorators");
        if (decs instanceof List) {
            for (Object d : (List<Object>) decs) {
                String dec = String.valueOf(d);
                if (ROUTE_DECORATORS.contains(dec)) {
                    raw.add(dec);
                }
            }
        }
        Matcher m1 = RE_ROUTE_DEC.matcher(src);
        while (m1.find()) {
            // Python re.findall with 2 groups yields tuples; str(tuple) -> "('g1', 'g2')".
            // ponytail: matches CPython tuple repr for route literals (no embedded quote/backslash escaping).
            raw.add("('" + m1.group(1) + "', '" + m1.group(2) + "')");
        }
        Matcher m2 = RE_ROUTE_VERB.matcher(src);
        while (m2.find()) {
            raw.add(m2.group(1));
        }
        TreeSet<String> routes = cpSet();
        for (String r : raw) {
            if (!r.isEmpty()) {
                routes.add(r);
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("routes", sortedList(routes));
        out.put("graphql", src.toLowerCase().contains("graphql"));
        out.put("rest", !raw.isEmpty());
        out.put("evidence", "parser_symbols_and_patterns");
        return out;
    }

    // ---------------------------------------------------------------- build_semantic_graph
    private static final int MAX_GRAPH_NODES = 5000;
    private static final int MAX_GRAPH_EDGES = 20000;
    private static final char EK = ' '; // edge-key separator: lower than any identifier char,
    // so codePoint compare on "from to" matches Python tuple (from, to) ordering exactly.

    /** {@code core.parsers.semantic_graph_engine.build_semantic_graph}. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> buildSemanticGraph(Map<String, Object> parsed) {
        Map<String, Object> symbols = asMap(parsed.get("symbols"));
        Map<String, Object> imports = asMap(parsed.get("imports"));
        Map<String, Object> calls = asMap(parsed.get("calls"));
        String sourceId = firstTruthy(parsed.get("source_id"), parsed.get("language"), "module");

        TreeSet<String> nodeIds = cpSet();
        nodeIds.add(sourceId);
        for (String key : new String[] {"classes", "functions", "interfaces", "symbols"}) {
            Object names = symbols.get(key);
            if (names instanceof List) {
                for (Object n : (List<Object>) names) {
                    nodeIds.add(String.valueOf(n));
                }
            }
        }
        for (Object e : asList(imports.get("edges"))) {
            if (e instanceof Map) {
                nodeIds.add(String.valueOf(((Map<String, Object>) e).getOrDefault("to", "")));
            }
        }
        // edge_meta: TreeMap keyed by "from to" → sorted iteration == Python sorted(tuple keys).
        TreeMap<String, String> edgeMeta = new TreeMap<>(Normalization::codePointCompare);
        for (Object e : asList(imports.get("edges"))) {
            if (e instanceof Map) {
                Map<String, Object> ed = (Map<String, Object>) e;
                String f = str(ed.get("from"));
                String t = str(ed.get("to"));
                if (!f.isEmpty() && !t.isEmpty()) {
                    edgeMeta.put(f + EK + t, "observed");
                }
            }
        }
        for (Object e : asList(calls.get("calls"))) {
            if (e instanceof Map) {
                Map<String, Object> ed = (Map<String, Object>) e;
                String f = str(ed.get("from"));
                String t = str(ed.get("to"));
                if (!f.isEmpty() && !t.isEmpty()) {
                    nodeIds.add(f);
                    nodeIds.add(t);
                    edgeMeta.putIfAbsent(f + EK + t, "observed"); // net basis is always "observed"
                }
            }
        }

        List<Object> nodes = new ArrayList<>();
        Set<String> allowed = new java.util.HashSet<>();
        for (String nid : nodeIds) {
            if (nid.isEmpty() || nodes.size() >= MAX_GRAPH_NODES) {
                continue;
            }
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("id", nid);
            node.put("kind", "symbol");
            node.put("metadata", new LinkedHashMap<>());
            nodes.add(node);
            allowed.add(nid);
        }
        List<Object> edgeList = new ArrayList<>();
        for (Map.Entry<String, String> en : edgeMeta.entrySet()) {
            if (edgeList.size() >= MAX_GRAPH_EDGES) {
                break;
            }
            int sep = en.getKey().indexOf(EK);
            String f = en.getKey().substring(0, sep);
            String t = en.getKey().substring(sep + 1);
            if (allowed.contains(f) && allowed.contains(t)) {
                Map<String, Object> meta = new LinkedHashMap<>();
                meta.put("edge_basis", en.getValue());
                List<Object> ev = new ArrayList<>();
                ev.add("parser:graph");
                meta.put("evidence", ev);
                Map<String, Object> edge = new LinkedHashMap<>();
                edge.put("from", f);
                edge.put("to", t);
                edge.put("metadata", meta);
                edgeList.add(edge);
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("nodes", nodes);
        out.put("edges", edgeList);
        out.put("max_edges", MAX_GRAPH_EDGES);
        return out;
    }

    // ---------------------------------------------------------------- require_parser_evidence
    private static final Set<String> GROUNDING_SUPPORTED = Set.of(
            "python", "javascript", "typescript", "rust", "go", "java", "kotlin", "dart");

    /** {@code core.parsers.formal_parser_grounding_engine.require_parser_evidence}. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> requireParserEvidence(Map<String, Object> parsed) {
        String lang = firstTruthy(parsed.get("language"), null, "text").toLowerCase();
        Map<String, Object> sym = asMap(parsed.get("symbols"));
        Object flagsObj = parsed.get("evidence");
        if (flagsObj == null) {
            flagsObj = parsed.get("parser_evidence");
        }
        boolean flagsTruthy = flagsObj instanceof Map && !((Map<String, Object>) flagsObj).isEmpty();
        int symbolCount = 0;
        for (String k : new String[] {"classes", "functions", "imports", "exports", "interfaces"}) {
            symbolCount += asList(sym.get(k)).size();
        }
        boolean applicable = GROUNDING_SUPPORTED.contains(lang);
        boolean grounded = applicable ? (symbolCount > 0 || flagsTruthy) : true;
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("language", lang);
        out.put("applicable", applicable);
        out.put("grounded", grounded);
        out.put("symbol_count", symbolCount);
        out.put("parser_required", applicable);
        List<Object> det = new ArrayList<>();
        det.add("lang=" + lang);
        det.add("symbols=" + symbolCount);
        out.put("deterministic_inputs", det);
        return out;
    }

    // ---------------------------------------------------------------- shared helpers
    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static List<Object> asList(Object o) {
        return o instanceof List ? (List<Object>) o : new ArrayList<>();
    }

    private static String str(Object o) {
        return o == null ? "" : String.valueOf(o);
    }

    /** Python {@code str(a or b or default)} over the first truthy (non-null, non-empty) value. */
    private static String firstTruthy(Object a, Object b, String def) {
        String sa = a == null ? "" : String.valueOf(a);
        if (!sa.isEmpty()) {
            return sa;
        }
        String sb = b == null ? "" : String.valueOf(b);
        if (!sb.isEmpty()) {
            return sb;
        }
        return def;
    }
}
