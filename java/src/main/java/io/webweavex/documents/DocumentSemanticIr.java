package io.webweavex.documents;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyRepr;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Port of the {@code core.documents} semantic-IR engines + {@code core.ir.document_ir} compiler +
 * {@code query_documents} (def in {@code core.query.document_query_engine}). The runtime closure is
 * 21 pure text/NLP engines (~417 lines). The tutorial path passes through
 * {@code core.evidence.structure_cognition}, but every epistemic-computed field is discarded by the
 * document path (verified: {@code query_documents} output contains none) — only the passthrough
 * {@code observed/inferred/reconciled} fields are read. So {@link #structureCognition} is a faithful
 * passthrough and the whole subsystem is byte-exact without the 4496-line epistemic engine. Pure;
 * zero new substrate.
 */
public final class DocumentSemanticIr {

    private DocumentSemanticIr() {
    }

    // -------------------------------------------------------------- helpers

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : map();
    }

    @SuppressWarnings("unchecked")
    private static List<Object> asList(Object o) {
        return o instanceof List ? (List<Object>) o : new ArrayList<>();
    }

    private static String str(Object o) {
        return PyRepr.str(o);
    }

    private static Map<String, Object> mapOf(Object... kv) {
        Map<String, Object> m = map();
        for (int i = 0; i < kv.length; i += 2) {
            m.put((String) kv[i], kv[i + 1]);
        }
        return m;
    }

    /** Faithful Python {@code str.splitlines()} (no trailing empty for a final line break). */
    private static List<String> splitlines(String text) {
        List<String> out = new ArrayList<>();
        if (text == null || text.isEmpty()) {
            return out;
        }
        int n = text.length();
        int i = 0;
        int start = 0;
        while (i < n) {
            char c = text.charAt(i);
            boolean brk = isLineBreak(c);
            if (brk) {
                out.add(text.substring(start, i));
                if (c == '\r' && i + 1 < n && text.charAt(i + 1) == '\n') {
                    i++;
                }
                i++;
                start = i;
            } else {
                i++;
            }
        }
        if (start < n) {
            out.add(text.substring(start, n));
        }
        return out;
    }

    private static boolean isLineBreak(char c) {
        int v = c;
        return v == 10 || v == 13 || v == 11 || v == 12 || v == 28
                || v == 29 || v == 30 || v == 133 || v == 8232 || v == 8233;
    }

    /** Python {@code str.strip()} (Unicode whitespace both ends). */
    private static String strip(String s) {
        return s.strip();
    }

    private static String sliceStr(String s, int n) {
        return s.length() > n ? s.substring(0, n) : s;
    }

    private static List<Object> sortedSetStr(List<String> items) {
        TreeSet<String> ts = new TreeSet<>(Normalization::codePointCompare);
        for (String s : items) {
            ts.add(s);
        }
        return new ArrayList<>(ts);
    }

    // -------------------------------------------------------------- rhetorical_structure_engine

    private static final Pattern HEADING = Pattern.compile("^(#{1,6})\\s+(.+)$");
    private static final Pattern LIST_ITEM = Pattern.compile("^[-*]\\s+");

    public static Map<String, Object> extractRhetoricalStructure(String text) {
        List<String> lines = splitlines(text == null ? "" : text);
        List<Object> units = new ArrayList<>();
        for (int i = 0; i < lines.size(); i++) {
            String ln = strip(lines.get(i));
            Matcher hm = HEADING.matcher(ln);
            if (hm.matches()) {
                units.add(mapOf("type", "heading", "level", (long) hm.group(1).length(),
                        "title", hm.group(2), "line", (long) i));
            } else if (LIST_ITEM.matcher(ln).lookingAt()) {
                units.add(mapOf("type", "list_item", "line", (long) i));
            } else if (ln.startsWith("```")) {
                units.add(mapOf("type", "code_fence", "line", (long) i));
            }
        }
        Map<String, Object> out = map();
        out.put("units", units);
        out.put("unit_count", (long) units.size());
        out.put("deterministic_inputs", new ArrayList<>(List.of("units=" + units.size())));
        return out;
    }

    // -------------------------------------------------------------- semantic_role_engine

    private static final Object[][] ROLE_PATTERNS = {
        {Pattern.compile("\\b(example|for instance)\\b", Pattern.CASE_INSENSITIVE), "example"},
        {Pattern.compile("\\b(therefore|thus|hence)\\b", Pattern.CASE_INSENSITIVE), "conclusion"},
        {Pattern.compile("\\b(because|since|due to)\\b", Pattern.CASE_INSENSITIVE), "reason"},
        {Pattern.compile("\\b(note|warning|caution)\\b", Pattern.CASE_INSENSITIVE), "notice"},
    };

    public static Map<String, Object> assignSemanticRoles(String text) {
        List<Object> roles = new ArrayList<>();
        List<String> lines = splitlines(text == null ? "" : text);
        for (int i = 0; i < lines.size(); i++) {
            String ln = lines.get(i);
            for (Object[] pr : ROLE_PATTERNS) {
                if (((Pattern) pr[0]).matcher(ln).find()) {
                    roles.add(mapOf("line", (long) i, "role", pr[1], "text", sliceStr(ln, 120)));
                    break;
                }
            }
        }
        Map<String, Object> out = map();
        out.put("roles", roles);
        out.put("count", (long) roles.size());
        return out;
    }

    // -------------------------------------------------------------- rhetorical_parser_engine

    public static Map<String, Object> parseRhetoricalStructure(String text) {
        Map<String, Object> structure = extractRhetoricalStructure(text);
        Map<String, Object> roles = assignSemanticRoles(text);
        List<Object> units = asList(structure.get("units"));
        Map<Object, Object> roleMap = new LinkedHashMap<>();
        for (Object ro : asList(roles.get("roles"))) {
            Map<String, Object> r = asMap(ro);
            if (r.containsKey("line")) {
                roleMap.put(r.get("line"), r.get("role"));
            }
        }
        List<Object> enriched = new ArrayList<>();
        for (Object uo : units) {
            Map<String, Object> u = new LinkedHashMap<>(asMap(uo));
            Object role = roleMap.containsKey(u.get("line")) ? roleMap.get(u.get("line"))
                    : ("heading".equals(u.get("type")) ? "nucleus" : "span");
            u.put("role", role);
            enriched.add(u);
        }
        List<String> roleSet = new ArrayList<>();
        for (Object eo : enriched) {
            String role = str(Py.get(asMap(eo), "role", ""));
            if (!role.isEmpty()) {
                roleSet.add(role);
            }
        }
        List<Object> detInputs = new ArrayList<>(asList(structure.get("deterministic_inputs")));
        detInputs.add("roles=" + asList(roles.get("roles")).size());
        Map<String, Object> out = map();
        out.put("units", enriched);
        out.put("unit_count", (long) enriched.size());
        out.put("roles", roles.get("roles"));
        out.put("rhetorical_roles", sortedSetStr(roleSet));
        out.put("deterministic_inputs", detInputs);
        return out;
    }

    // -------------------------------------------------------------- argument engines

    private static final int MAX_EDGES = 300;

    public static Map<String, Object> reconstructArgumentDependencies(List<Object> claims) {
        List<Object> ordered = new ArrayList<>(claims);
        ordered.sort((a, b) -> Long.compare(asLong(Py.get(asMap(a), "order", 0L)),
                asLong(Py.get(asMap(b), "order", 0L))));
        List<Object> edges = new ArrayList<>();
        for (int idx = 1; idx < ordered.size(); idx++) {
            Map<String, Object> prev = asMap(ordered.get(idx - 1));
            Map<String, Object> cur = asMap(ordered.get(idx));
            if (Py.truthy(cur.get("depends_on"))) {
                edges.add(mapOf("from", cur.get("depends_on"), "to", cur.get("id"),
                        "metadata", mapOf("kind", "argument_support", "basis", "explicit_dependency")));
            } else {
                edges.add(mapOf("from", prev.get("id"), "to", cur.get("id"),
                        "metadata", mapOf("kind", "argument_sequence", "basis", "document_order")));
            }
        }
        List<Object> capped = edges.size() > MAX_EDGES ? new ArrayList<>(edges.subList(0, MAX_EDGES)) : edges;
        Map<String, Object> out = map();
        out.put("edges", capped);
        out.put("count", (long) Math.min(edges.size(), MAX_EDGES));
        out.put("deterministic", true);
        return out;
    }

    public static Map<String, Object> buildArgumentDependencies(String text) {
        List<Object> claims = new ArrayList<>();
        int i = 0;
        for (String raw : splitlines(text == null ? "" : text)) {
            String ln = strip(raw);
            if (!ln.isEmpty()) {
                claims.add(mapOf("id", "c" + i, "order", (long) i, "content", ln));
                i++;
            }
        }
        Map<String, Object> r = reconstructArgumentDependencies(claims);
        List<Object> nodes = new ArrayList<>();
        for (Object co : claims) {
            Map<String, Object> c = asMap(co);
            nodes.add(mapOf("id", c.get("id"), "content", Py.get(c, "content", null)));
        }
        Map<String, Object> out = map();
        out.put("dependencies", r.get("edges"));
        out.put("nodes", nodes);
        out.put("evidence", new ArrayList<>(List.of("discourse:argument_order")));
        out.put("deterministic", true);
        return out;
    }

    public static Map<String, Object> buildArgumentGraph(String text) {
        Map<String, Object> rhet = extractRhetoricalStructure(text);
        List<Object> headings = new ArrayList<>();
        for (Object uo : asList(rhet.get("units"))) {
            if ("heading".equals(asMap(uo).get("type"))) {
                headings.add(uo);
            }
        }
        List<Object> nodes = new ArrayList<>();
        for (int i = 0; i < headings.size(); i++) {
            nodes.add(mapOf("id", "h" + i, "role", i == 0 ? "claim" : "support",
                    "title", str(Py.get(asMap(headings.get(i)), "title", ""))));
        }
        List<Object> edges = new ArrayList<>();
        for (int i = 0; i < nodes.size() - 1; i++) {
            edges.add(mapOf("from", asMap(nodes.get(i)).get("id"), "to", asMap(nodes.get(i + 1)).get("id")));
        }
        Map<String, Object> out = map();
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("deterministic_inputs", new ArrayList<>(List.of("nodes=" + nodes.size())));
        return out;
    }

    // -------------------------------------------------------------- discourse / transitions

    public static Map<String, Object> parseSemanticDiscourse(String text) {
        Map<String, Object> rhet = extractRhetoricalStructure(text);
        Map<String, Object> arg = buildArgumentGraph(text);
        List<Object> det = new ArrayList<>(asList(rhet.get("deterministic_inputs")));
        det.add("args=" + asList(arg.get("nodes")).size());
        Map<String, Object> out = map();
        out.put("rhetorical", rhet);
        out.put("argument", arg);
        out.put("transitions", arg.get("edges"));
        out.put("deterministic_inputs", det);
        return out;
    }

    public static Map<String, Object> modelConceptTransitions(String text) {
        Map<String, Object> d = parseSemanticDiscourse(text);
        List<Object> transitions = new ArrayList<>();
        for (Object eo : asList(d.get("transitions"))) {
            if (eo instanceof Map) {
                Map<String, Object> e = asMap(eo);
                if (Py.truthy(e.get("from")) && Py.truthy(e.get("to"))) {
                    transitions.add(mapOf("from", e.get("from"), "to", e.get("to"), "kind", "discourse"));
                }
            }
        }
        Map<String, Object> out = map();
        out.put("transitions", transitions);
        out.put("count", (long) transitions.size());
        return out;
    }

    public static Map<String, Object> modelSemanticTransitions(String text) {
        Map<String, Object> trans = modelConceptTransitions(text);
        Map<String, Object> rhet = parseRhetoricalStructure(text);
        List<Object> headings = new ArrayList<>();
        for (Object uo : asList(rhet.get("units"))) {
            if ("heading".equals(asMap(uo).get("type"))) {
                headings.add(uo);
            }
        }
        List<Object> transitions = new ArrayList<>(asList(trans.get("transitions")));
        for (int i = 0; i < headings.size() - 1; i++) {
            transitions.add(mapOf("from", str(Py.get(asMap(headings.get(i)), "title", "")),
                    "to", str(Py.get(asMap(headings.get(i + 1)), "title", "")), "kind", "section_transition"));
        }
        Map<String, Object> out = map();
        out.put("transitions", transitions);
        out.put("count", (long) transitions.size());
        out.put("evidence", new ArrayList<>(List.of("discourse:transitions")));
        return out;
    }

    public static Map<String, Object> modelConceptProgression(String text) {
        Map<String, Object> trans = modelSemanticTransitions(text);
        List<Object> progression = new ArrayList<>();
        List<Object> transitions = asList(trans.get("transitions"));
        for (int i = 0; i < transitions.size(); i++) {
            Map<String, Object> t = asMap(transitions.get(i));
            progression.add(mapOf("index", (long) i, "from", t.get("from"), "to", t.get("to"),
                    "introduces", t.get("to")));
        }
        Map<String, Object> out = map();
        out.put("progression", progression);
        out.put("concept_count", (long) progression.size());
        out.put("deterministic_inputs", new ArrayList<>(List.of("concepts=" + progression.size())));
        return out;
    }

    // -------------------------------------------------------------- headings / sections

    private static final Pattern HEADING_MD = Pattern.compile("^(#{1,6})\\s+(.+)$", Pattern.MULTILINE);
    private static final Pattern HEADING_HTML =
            Pattern.compile("<h([1-6])[^>]*>(.*?)</h\\1>", Pattern.CASE_INSENSITIVE | Pattern.DOTALL);

    public static Map<String, Object> extractHeadings(String text) {
        String src = text == null ? "" : text;
        List<Object> all = new ArrayList<>();
        Matcher md = HEADING_MD.matcher(src);
        while (md.find()) {
            all.add(mapOf("level", (long) md.group(1).length(), "title", strip(md.group(2))));
        }
        Matcher html = HEADING_HTML.matcher(src);
        while (html.find()) {
            all.add(mapOf("level", (long) Long.parseLong(html.group(1)), "title", strip(html.group(2))));
        }
        all.sort((a, b) -> {
            int c = Long.compare(asLong(asMap(a).get("level")), asLong(asMap(b).get("level")));
            return c != 0 ? c : Normalization.codePointCompare(str(asMap(a).get("title")), str(asMap(b).get("title")));
        });
        Map<String, Object> out = map();
        out.put("headings", all);
        return out;
    }

    public static Map<String, Object> extractSections(String text) {
        List<Object> heads = asList(extractHeadings(text).get("headings"));
        List<String> sections = new ArrayList<>();
        List<Object> hierarchy = new ArrayList<>();
        for (Object ho : heads) {
            Map<String, Object> h = asMap(ho);
            sections.add(str(Py.get(h, "title", "")));
            hierarchy.add(mapOf("title", str(Py.get(h, "title", "")), "level", Py.get(h, "level", 1L)));
        }
        Map<String, Object> out = map();
        out.put("sections", sortedSetStr(sections));
        out.put("hierarchy", hierarchy);
        return out;
    }

    // -------------------------------------------------------------- instructional

    private static final List<String> STEP_KEYWORDS =
            List.of("step", "tutorial", "install", "setup", "prerequisite");

    public static Map<String, Object> extractInstructionalFlow(String text) {
        Map<String, Object> rhet = extractRhetoricalStructure(text);
        List<Object> steps = new ArrayList<>();
        for (Object uo : asList(rhet.get("units"))) {
            Map<String, Object> u = asMap(uo);
            if ("heading".equals(u.get("type"))) {
                String title = str(Py.get(u, "title", "")).toLowerCase(java.util.Locale.ROOT);
                boolean kw = false;
                for (String k : STEP_KEYWORDS) {
                    if (title.contains(k)) {
                        kw = true;
                        break;
                    }
                }
                if (kw) {
                    steps.add(mapOf("title", u.get("title"), "line", u.get("line")));
                } else if (asLong(Py.get(u, "level", 9L)) <= 2) {
                    steps.add(mapOf("title", u.get("title"), "line", u.get("line"), "implicit", true));
                }
            }
        }
        List<Object> prereq = new ArrayList<>();
        for (int i = 0; i < steps.size() - 1; i++) {
            prereq.add(asMap(steps.get(i)).get("title"));
        }
        Map<String, Object> out = map();
        out.put("steps", steps);
        out.put("prerequisites", prereq);
        out.put("deterministic_inputs", new ArrayList<>(List.of("steps=" + steps.size())));
        return out;
    }

    public static Map<String, Object> analyzeInstructionalSemantics(String text) {
        Map<String, Object> flow = extractInstructionalFlow(text);
        Map<String, Object> roles = assignSemanticRoles(text);
        List<Object> ordering = new ArrayList<>();
        List<Object> steps = asList(flow.get("steps"));
        for (int i = 0; i < steps.size(); i++) {
            ordering.add(mapOf("step", (long) (i + 1), "title", str(Py.get(asMap(steps.get(i)), "title", ""))));
        }
        List<Object> notices = new ArrayList<>();
        for (Object ro : asList(roles.get("roles"))) {
            if ("notice".equals(asMap(ro).get("role"))) {
                notices.add(ro);
            }
        }
        Map<String, Object> out = map();
        out.put("ordering", ordering);
        out.put("prerequisites", flow.get("prerequisites"));
        out.put("notices", notices);
        out.put("evidence", new ArrayList<>(List.of("discourse:instructional_flow")));
        out.put("deterministic_inputs", new ArrayList<>(List.of("steps=" + ordering.size())));
        return out;
    }

    // -------------------------------------------------------------- tutorial (structure_cognition passthrough)

    /**
     * Passthrough port of {@code core.evidence.grounding_engine.structure_cognition}: the document
     * path only ever reads the {@code observed/inferred/reconciled} fields back out; every
     * epistemic-computed field is discarded (verified — {@code query_documents} output contains
     * none), so reproducing those fields is unnecessary for byte-exact parity on this path.
     */
    private static Map<String, Object> structureCognition(Map<String, Object> observed,
            Map<String, Object> inferred, Map<String, Object> reconciled) {
        Map<String, Object> out = map();
        out.put("observed", observed);
        out.put("inferred", inferred);
        out.put("reconciled", reconciled);
        return out;
    }

    private static final Pattern NUMBERED = Pattern.compile("^\\s*\\d+\\.\\s+(.+)$", Pattern.MULTILINE);

    public static Map<String, Object> extractTutorialFlow(String text) {
        List<Object> hierarchy = asList(extractSections(text == null ? "" : text).get("hierarchy"));
        List<String> steps = new ArrayList<>();
        for (Object ho : hierarchy) {
            String title = str(Py.get(asMap(ho), "title", ""));
            if (!title.isEmpty()) {
                steps.add(title);
            }
        }
        if (steps.isEmpty()) {
            List<String> found = new ArrayList<>();
            Matcher m = NUMBERED.matcher(text == null ? "" : text);
            while (m.find()) {
                found.add(m.group(1));
            }
            steps = new ArrayList<>();
            for (Object s : sortedSetStr(found)) {
                steps.add((String) s);
            }
        }
        Map<String, Object> observed = mapOf("steps", new ArrayList<Object>(steps));
        List<Object> requiresPrior = new ArrayList<>();
        for (int i = 1; i < steps.size(); i++) {
            if (!steps.get(i).isEmpty() && !steps.get(i - 1).isEmpty()) {
                requiresPrior.add(mapOf("step", steps.get(i), "requires", steps.get(i - 1)));
            }
        }
        Map<String, Object> inferred = mapOf("requires_prior", requiresPrior);
        List<Object> flowEdges = new ArrayList<>();
        for (int i = 0; i < Math.max(0, steps.size() - 1); i++) {
            flowEdges.add(mapOf("from", steps.get(i), "to", steps.get(i + 1)));
        }
        Map<String, Object> reconciled = mapOf("steps", new ArrayList<Object>(steps), "flow_edges", flowEdges);
        Map<String, Object> result = structureCognition(observed, inferred, reconciled);
        return result;
    }

    public static Map<String, Object> reconstructTutorialDependencies(String text) {
        Map<String, Object> flow = extractTutorialFlow(text);
        List<Object> requires = asList(asMap(Py.get(flow, "inferred", map())).get("requires_prior"));
        List<Object> steps = asList(asMap(Py.get(flow, "reconciled", map())).get("steps"));
        Map<String, Object> observed = mapOf("steps", steps);
        Map<String, Object> inferred = mapOf("tutorial_dependencies", requires, "prerequisite_edges", requires);
        Map<String, Object> reconciled = mapOf("tutorial_flow", Py.get(flow, "reconciled", map()),
                "dependencies", requires);
        return structureCognition(observed, inferred, reconciled);
    }

    public static Map<String, Object> inferTutorialPrerequisites(String text) {
        Map<String, Object> inst = analyzeInstructionalSemantics(text);
        Map<String, Object> legacy = reconstructTutorialDependencies(text);
        List<Object> chain = new ArrayList<>();
        List<Object> steps = asList(inst.get("ordering"));
        for (int i = 1; i < steps.size(); i++) {
            chain.add(mapOf("prerequisite", str(Py.get(asMap(steps.get(i - 1)), "title", "")),
                    "requires", str(Py.get(asMap(steps.get(i)), "title", "")),
                    "evidence", "discourse:instructional_order"));
        }
        Map<String, Object> out = map();
        out.put("chain", chain);
        out.put("prerequisites", inst.get("prerequisites"));
        out.put("legacy_flow", Py.get(legacy, "reconciled", map()));
        out.put("deterministic_inputs", new ArrayList<>(List.of("chain=" + chain.size())));
        return out;
    }

    // -------------------------------------------------------------- coreference

    private static final Pattern HEADING_FIND = Pattern.compile("^#{1,6}\\s+(.+)$", Pattern.MULTILINE);
    private static final Pattern PRONOUN =
            Pattern.compile("\\b(it|this|that|they|these|those)\\b", Pattern.CASE_INSENSITIVE);

    public static Map<String, Object> resolveCoreferences(String text) {
        String src = text == null ? "" : text;
        List<String> headings = new ArrayList<>();
        Matcher hm = HEADING_FIND.matcher(src);
        while (hm.find()) {
            headings.add(hm.group(1));
        }
        List<String> pronouns = new ArrayList<>();
        Matcher pm = PRONOUN.matcher(src);
        while (pm.find()) {
            pronouns.add(pm.group(1));
        }
        String antecedent = headings.isEmpty() ? "" : headings.get(headings.size() - 1);
        List<Object> chains = new ArrayList<>();
        for (int i = 0; i < Math.min(pronouns.size(), 50); i++) {
            chains.add(mapOf("pronoun", pronouns.get(i), "antecedent", antecedent));
        }
        Map<String, Object> out = map();
        out.put("chains", chains);
        out.put("count", (long) chains.size());
        return out;
    }

    public static Map<String, Object> buildCoreferenceGraph(String text) {
        Map<String, Object> coref = resolveCoreferences(text);
        Map<String, Object> rhet = parseRhetoricalStructure(text);
        List<Object> nodes = new ArrayList<>();
        for (Object uo : asList(rhet.get("units"))) {
            Map<String, Object> u = asMap(uo);
            if ("heading".equals(u.get("type"))) {
                String title = str(Py.get(u, "title", ""));
                if (!title.isEmpty()) {
                    nodes.add(mapOf("id", title, "kind", "entity"));
                }
            }
        }
        List<Object> edges = new ArrayList<>();
        for (Object co : asList(coref.get("chains"))) {
            Map<String, Object> c = asMap(co);
            if (Py.truthy(c.get("antecedent"))) {
                edges.add(mapOf("from", str(Py.get(c, "pronoun", "")), "to", str(Py.get(c, "antecedent", "")),
                        "evidence", new ArrayList<>(List.of("discourse:coref"))));
            }
        }
        List<Object> cappedEdges = edges.size() > 100 ? new ArrayList<>(edges.subList(0, 100)) : edges;
        Map<String, Object> out = map();
        out.put("nodes", nodes);
        out.put("edges", cappedEdges);
        out.put("chains", coref.get("chains"));
        return out;
    }

    public static Map<String, Object> buildDocumentDependencyGraph(String text) {
        Map<String, Object> flow = extractInstructionalFlow(text);
        Map<String, Object> trans = modelConceptTransitions(text);
        List<Object> nodes = new ArrayList<>();
        List<Object> steps = asList(flow.get("steps"));
        for (int i = 0; i < steps.size(); i++) {
            nodes.add(mapOf("id", str(Py.get(asMap(steps.get(i)), "title", "step" + i)), "kind", "step"));
        }
        Map<String, Object> out = map();
        out.put("nodes", nodes);
        out.put("edges", trans.get("transitions"));
        out.put("prerequisites", flow.get("prerequisites"));
        return out;
    }

    // -------------------------------------------------------------- top engine + IR + query

    public static Map<String, Object> buildDocumentSemanticIr(String text) {
        Map<String, Object> out = map();
        out.put("rhetorical", parseRhetoricalStructure(text));
        out.put("argument", buildArgumentDependencies(text));
        out.put("progression", modelConceptProgression(text));
        out.put("prerequisites", inferTutorialPrerequisites(text));
        out.put("coreference", buildCoreferenceGraph(text));
        out.put("dependency_graph", buildDocumentDependencyGraph(text));
        out.put("evidence", new ArrayList<>(List.of("discourse:rhetorical", "discourse:argument",
                "discourse:progression", "discourse:prerequisites")));
        return out;
    }

    private static Map<String, Object> emptyLineage(String stage) {
        Map<String, Object> m = map();
        m.put("stages", new ArrayList<>(List.of(mapOf("stage", stage))));
        m.put("depth", 1L);
        return m;
    }

    private static Map<String, Object> mergeEvidence(List<Object> part) {
        List<String> items = new ArrayList<>();
        for (Object e : (part == null ? new ArrayList<>() : part)) {
            if (Py.truthy(e)) {
                items.add(str(e));
            }
        }
        Map<String, Object> m = map();
        m.put("items", sortedSetStr(items));
        m.put("count", (long) sortedSetStr(items).size());
        return m;
    }

    public static Map<String, Object> compileDocumentIr(String text) {
        Map<String, Object> raw = buildDocumentSemanticIr(text);
        Map<String, Object> rhet = asMap(raw.get("rhetorical"));
        Map<String, Object> arg = asMap(raw.get("argument"));
        Map<String, Object> ir = map();
        ir.put("concepts", new ArrayList<>());
        ir.put("claims", arg.get("nodes"));
        ir.put("arguments", arg.get("dependencies"));
        ir.put("tutorial_steps", Py.get(asMap(raw.get("prerequisites")), "chain", new ArrayList<>()));
        ir.put("dependencies", new ArrayList<>());
        ir.put("references", new ArrayList<>());
        ir.put("contradictions", new ArrayList<>());
        ir.put("rhetorical_units", Py.get(rhet, "units", new ArrayList<>()));
        ir.put("semantic_roles", Py.get(rhet, "roles", new ArrayList<>()));
        ir.put("explanation_chains", Py.get(asMap(raw.get("dependency_graph")), "edges", new ArrayList<>()));
        ir.put("concept_progressions", Py.get(asMap(raw.get("progression")), "progression", new ArrayList<>()));
        ir.put("instructional_flows", Py.get(asMap(raw.get("prerequisites")), "prerequisites", new ArrayList<>()));
        ir.put("semantic_graph", raw.get("dependency_graph"));
        ir.put("semantic_evidence", mergeEvidence(asList(raw.get("evidence"))));
        ir.put("lineage", emptyLineage("document_semantic_ir"));
        Map<String, Object> confidence = map();
        confidence.put("score", Py.truthy(ir.get("rhetorical_units")) ? 0.7 : 0.3);
        confidence.put("basis", raw.get("evidence"));
        confidence.put("deterministic", true);
        ir.put("confidence", confidence);
        ir.put("_raw", raw);
        return ir;
    }

    /** {@code query_documents(text)}. */
    public static Map<String, Object> queryDocuments(String text) {
        Map<String, Object> ir = compileDocumentIr(text);
        Map<String, Object> out = map();
        out.put("ir", ir);
        out.put("claims", Py.get(ir, "claims", new ArrayList<>()));
        out.put("tutorial_steps", Py.get(ir, "tutorial_steps", new ArrayList<>()));
        out.put("explainable", true);
        return out;
    }

    private static long asLong(Object v) {
        if (v instanceof Number) {
            return ((Number) v).longValue();
        }
        if (v instanceof String) {
            try {
                return Long.parseLong(((String) v).trim());
            } catch (NumberFormatException e) {
                return 0;
            }
        }
        return 0;
    }
}
