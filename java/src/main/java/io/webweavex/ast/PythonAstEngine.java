package io.webweavex.ast;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.PyRepr;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Port of {@code core.ast.python_ast_engine.parse_python_ast} via the certified JavaScript reference
 * ({@code src/ast/pythonAstEngine.ts}) — a lightweight line/indent scanner reproducing the summary
 * CPython's {@code ast.walk} produces (imports / functions / classes / assignments with line spans).
 * Python uses real {@code import ast}; this scanner matches its observable summary for standard
 * (4-space-indented) source, exactly as the JS port does (which is certified Py≡JS). Cross-language
 * reuse: the algorithm is JS's, not reinvented.
 *
 * <p>Foundational reusable subsystem for the AST cluster ({@code query_semantics}/
 * {@code reason_semantically}/{@code compile_repository}); the repository code-analysis layer
 * (epistemic-free, ~1100 L) builds on top of it.
 */
public final class PythonAstEngine {

    private PythonAstEngine() {
    }

    private static final String IDENT = "[A-Za-z_][A-Za-z0-9_]*";
    private static final Pattern RE_IMPORT = Pattern.compile("^import\\s+(.+)$", Pattern.DOTALL);
    private static final Pattern RE_FROM =
            Pattern.compile("^from\\s+([.\\w]+)\\s+import\\s+(.+)$", Pattern.DOTALL);
    private static final Pattern RE_DEF =
            Pattern.compile("^(?:async\\s+)?def\\s+(" + IDENT + ")\\s*\\(([\\s\\S]*?)\\)\\s*(?:->[^:]+)?:");
    private static final Pattern RE_CLASS =
            Pattern.compile("^class\\s+(" + IDENT + ")\\s*(?:\\(([^)]*)\\))?\\s*:");
    private static final Pattern RE_ASSIGN =
            Pattern.compile("^((?:" + IDENT + "\\s*,\\s*)*" + IDENT + ")\\s*=(?!=)([\\s\\S]*)$");
    private static final Pattern RE_IDENT_FULL = Pattern.compile("^" + IDENT + "$");
    private static final Pattern RE_CTRL =
            Pattern.compile("^(if|while|for|return|yield|assert|del|import|from|pass|raise)\\b");
    private static final Pattern RE_LEADING_WS = Pattern.compile("^[ \\t]*");
    private static final Pattern RE_VALIDATE = Pattern.compile("^[<>%?\\\\/,;:=&|!)\\]}]");

    /** SyntaxError parity — same observable path as CPython {@code ast.parse} raising. */
    public static final class PySyntaxError extends RuntimeException {
        public PySyntaxError(int line) {
            super("invalid syntax (<unknown>, line " + line + ")");
        }
    }

    private static final class Logical {
        String text;
        int lineno;
        int endLineno;
        int indent;
    }

    private static final class Stmt {
        String kind;
        int depth;
        int lineno;
        int endLineno;
        Map<String, Object> data;
    }

    private static int leadingIndent(String line) {
        Matcher m = RE_LEADING_WS.matcher(line);
        String ws = m.find() ? m.group() : "";
        return ws.replace("\t", "        ").length();
    }

    private static List<Logical> logicalLines(String code) {
        String[] raw = code.split("\r?\n", -1);
        List<Logical> out = new ArrayList<>();
        StringBuilder buf = new StringBuilder();
        int start = 0;
        int depth = 0;
        int indent = 0;
        String inStr = null;
        for (int i = 0; i < raw.length; i++) {
            String line = raw[i];
            if (buf.length() == 0) {
                String t = line.trim();
                if (t.isEmpty() || t.startsWith("#")) {
                    continue;
                }
                start = i + 1;
                indent = leadingIndent(line);
            }
            buf.append(buf.length() > 0 ? "\n" : "").append(line);
            int j = 0;
            while (j < line.length()) {
                char ch = line.charAt(j);
                String three = line.substring(j, Math.min(j + 3, line.length()));
                if (inStr != null) {
                    if (three.equals(inStr)) {
                        inStr = null;
                        j += 3;
                        continue;
                    }
                    j++;
                    continue;
                }
                if (three.equals("\"\"\"") || three.equals("'''")) {
                    inStr = three;
                    j += 3;
                    continue;
                }
                if (ch == '#') {
                    break;
                }
                if (ch == '(' || ch == '[' || ch == '{') {
                    depth++;
                } else if (ch == ')' || ch == ']' || ch == '}') {
                    depth--;
                }
                j++;
            }
            boolean endsContinuation = stripTrailing(line).endsWith("\\");
            if (depth > 0 || inStr != null || endsContinuation) {
                continue;
            }
            Logical lg = new Logical();
            lg.text = buf.toString();
            lg.lineno = start;
            lg.endLineno = i + 1;
            lg.indent = indent;
            out.add(lg);
            buf.setLength(0);
            depth = 0;
        }
        if (buf.length() > 0) {
            Logical lg = new Logical();
            lg.text = buf.toString();
            lg.lineno = start;
            lg.endLineno = raw.length;
            lg.indent = indent;
            out.add(lg);
        }
        return out;
    }

    private static String stripTrailing(String s) {
        int end = s.length();
        while (end > 0 && Character.isWhitespace(s.charAt(end - 1))) {
            end--;
        }
        return s.substring(0, end);
    }

    private static int blockEnd(List<Logical> lines, int idx) {
        int base = lines.get(idx).indent;
        int end = lines.get(idx).endLineno;
        for (int j = idx + 1; j < lines.size(); j++) {
            if (lines.get(j).indent <= base) {
                break;
            }
            end = lines.get(j).endLineno;
        }
        return end;
    }

    private static List<String> splitClean(String s, String sep) {
        List<String> out = new ArrayList<>();
        for (String part : s.split(Pattern.quote(sep), -1)) {
            out.add(part);
        }
        return out;
    }

    /** {@code parse_python_ast(code)}. */
    public static Map<String, Object> parsePythonAst(String code) {
        List<Logical> lines = logicalLines(code == null ? "" : code);
        List<Stmt> stmts = new ArrayList<>();

        for (int idx = 0; idx < lines.size(); idx++) {
            Logical lg = lines.get(idx);
            String stripped = lg.text.trim()
                    .replaceAll("\\\\\\s*\\n\\s*", " ")
                    .replaceAll("\\s*\\n\\s*", " ");
            int depth = lg.indent / 4;
            String firstLine = stripped.split("\n", -1)[0];
            if (!firstLine.isEmpty() && RE_VALIDATE.matcher(firstLine).find()) {
                throw new PySyntaxError(lg.lineno);
            }

            Matcher m = RE_IMPORT.matcher(stripped);
            if (m.matches() && !stripped.startsWith("import(")) {
                List<Object> modules = new ArrayList<>();
                for (String s : splitClean(m.group(1), ",")) {
                    String mod = s.trim().split("\\s+as\\s+", -1)[0].trim();
                    if (!mod.isEmpty()) {
                        modules.add(mod);
                    }
                }
                Stmt st = new Stmt();
                st.kind = "Import";
                st.depth = depth;
                st.lineno = lg.lineno;
                st.endLineno = lg.endLineno;
                st.data = new LinkedHashMap<>();
                st.data.put("modules", modules);
                stmts.add(st);
                continue;
            }
            m = RE_FROM.matcher(stripped);
            if (m.matches()) {
                List<Object> names = new ArrayList<>();
                for (String s : splitClean(m.group(2).replace("(", "").replace(")", ""), ",")) {
                    String nm = s.trim().split("\\s+as\\s+", -1)[0].trim();
                    if (!nm.isEmpty()) {
                        names.add(nm);
                    }
                }
                Stmt st = new Stmt();
                st.kind = "ImportFrom";
                st.depth = depth;
                st.lineno = lg.lineno;
                st.endLineno = lg.endLineno;
                st.data = new LinkedHashMap<>();
                st.data.put("module", m.group(1));
                st.data.put("names", names);
                stmts.add(st);
                continue;
            }
            m = RE_DEF.matcher(stripped);
            if (m.find() && m.start() == 0) {
                List<Object> args = new ArrayList<>();
                for (String s : splitClean(m.group(2), ",")) {
                    String a = s.trim().split("[:=]", -1)[0].trim();
                    // CPython node.args.args = positional-or-keyword only: exclude *args/**kwargs and
                    // the bare posonly "/" marker.
                    if (a.startsWith("*") || a.isEmpty() || a.equals("/")) {
                        continue;
                    }
                    args.add(a);
                }
                Stmt st = new Stmt();
                st.kind = "FunctionDef";
                st.depth = depth;
                st.lineno = lg.lineno;
                st.endLineno = blockEnd(lines, idx);
                st.data = new LinkedHashMap<>();
                st.data.put("name", m.group(1));
                st.data.put("args", args);
                stmts.add(st);
                continue;
            }
            m = RE_CLASS.matcher(stripped);
            if (m.find() && m.start() == 0) {
                List<Object> bases = new ArrayList<>();
                String basesRaw = m.group(2) == null ? "" : m.group(2);
                for (String s : splitClean(basesRaw, ",")) {
                    String b = s.trim();
                    if (!b.isEmpty() && !b.contains("=")) {
                        bases.add(RE_IDENT_FULL.matcher(b).matches() ? b : null);
                    }
                }
                Stmt st = new Stmt();
                st.kind = "ClassDef";
                st.depth = depth;
                st.lineno = lg.lineno;
                st.endLineno = blockEnd(lines, idx);
                st.data = new LinkedHashMap<>();
                st.data.put("name", m.group(1));
                st.data.put("bases", bases);
                stmts.add(st);
                continue;
            }
            m = RE_ASSIGN.matcher(stripped);
            if (m.matches() && !stripped.contains("==") && !RE_CTRL.matcher(stripped).find()) {
                // CPython: only single Name targets are counted. `b, c = ...` is one Tuple target
                // (no Names → []); the Assign node is emitted regardless of target count.
                List<Object> targets = new ArrayList<>();
                String lhs = m.group(1);
                if (!lhs.contains(",")) {
                    String t = lhs.trim();
                    if (RE_IDENT_FULL.matcher(t).matches()) {
                        targets.add(t);
                    }
                }
                Stmt st = new Stmt();
                st.kind = "Assign";
                st.depth = depth;
                st.lineno = lg.lineno;
                st.endLineno = lg.endLineno;
                st.data = new LinkedHashMap<>();
                st.data.put("targets", targets);
                stmts.add(st);
            }
        }

        // ast.walk is breadth-first: order by nesting depth, then line (stable).
        List<Stmt> ordered = new ArrayList<>(stmts);
        ordered.sort((a, b) -> a.depth != b.depth ? Integer.compare(a.depth, b.depth)
                : Integer.compare(a.lineno, b.lineno));

        List<Object> imports = new ArrayList<>();
        List<Object> functions = new ArrayList<>();
        List<Object> classes = new ArrayList<>();
        List<Object> assignments = new ArrayList<>();
        for (Stmt s : ordered) {
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("type", s.kind);
            node.put("lineno", (long) s.lineno);
            node.put("end_lineno", (long) s.endLineno);
            Map<String, Object> entry = new LinkedHashMap<>();
            switch (s.kind) {
                case "Import":
                    entry.put("modules", s.data.get("modules"));
                    entry.put("node", node);
                    imports.add(entry);
                    break;
                case "ImportFrom":
                    entry.put("module", s.data.get("module"));
                    entry.put("names", s.data.get("names"));
                    entry.put("node", node);
                    imports.add(entry);
                    break;
                case "FunctionDef":
                    entry.put("name", s.data.get("name"));
                    entry.put("args", s.data.get("args"));
                    entry.put("node", node);
                    functions.add(entry);
                    break;
                case "ClassDef":
                    entry.put("name", s.data.get("name"));
                    entry.put("bases", s.data.get("bases"));
                    entry.put("node", node);
                    classes.add(entry);
                    break;
                default:
                    entry.put("targets", s.data.get("targets"));
                    entry.put("node", node);
                    assignments.add(entry);
                    break;
            }
        }

        imports.sort((a, b) -> Normalization.codePointCompare(PyRepr.str(a), PyRepr.str(b)));
        functions.sort((a, b) -> Normalization.codePointCompare(name(a), name(b)));
        classes.sort((a, b) -> Normalization.codePointCompare(name(a), name(b)));

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("language", "python");
        out.put("imports", imports);
        out.put("functions", functions);
        out.put("classes", classes);
        out.put("assignments", assignments);
        out.put("ast_grounded", true);
        out.put("bounded", true);
        return out;
    }

    @SuppressWarnings("unchecked")
    private static String name(Object o) {
        return String.valueOf(((Map<String, Object>) o).get("name"));
    }
}
