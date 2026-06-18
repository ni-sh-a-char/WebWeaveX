package io.webweavex.documents;

import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyText;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Port of {@code core.documents.universal_document_extraction_engine.extract_document_runtime}
 * and its full first-party closure (structure / hierarchy / citation / reference / table
 * engines, the document knowledge-graph, presentation and spreadsheet engines, and the
 * {@code core.ir.document_runtime_ir} compiler).
 *
 * <p>Verified free of BeautifulSoup, lxml, browser, OCR, PDF, DOCX, network and LLM
 * dependencies (see {@code java/JAVA_SESSION_4B_DEPENDENCY_PROOF.md}). A pure
 * {@code str}/{@code re}/{@code list}/{@code dict} transform — deterministic, no hashing
 * inside the engine; parity is proven on the serialized output.
 */
public final class DocumentRuntime {

    private DocumentRuntime() {
    }

    private static final int MAX_SECTIONS = 5000;
    private static final int MAX_REFERENCES = 5000;
    private static final int MAX_TABLES = 1000;
    private static final int MAX_ROWS = 10000;
    private static final int MAX_NODES = 10000;
    private static final int MAX_SLIDES = 1000;
    private static final int MAX_SHEETS = 500;

    // re.compile(r"\[(\d+)\]") — Python \d is Unicode by default.
    private static final Pattern CITATION_PATTERN =
            Pattern.compile("\\[(\\d+)\\]", Pattern.UNICODE_CHARACTER_CLASS);

    private static final Set<String> REFERENCE_SECTIONS = Set.of("references", "bibliography");

    /** {@code extract_document_runtime(text, slides=None, workbook=None)}. */
    public static Map<String, Object> extractDocumentRuntime(
            String text, List<Object> slides, Map<String, Object> workbook) {
        Map<String, Object> structure = buildDocumentStructure(text);
        Map<String, Object> hierarchy = buildDocumentHierarchy(structure);
        Map<String, Object> citations = extractCitations(text);
        Map<String, Object> references = extractReferences(structure);
        Map<String, Object> tables = extractDocumentTables(text);
        Map<String, Object> knowledgeGraph = buildDocumentKnowledgeGraph(structure);
        Map<String, Object> slidePayload =
                extractPresentationStructure(slides == null ? new ArrayList<>() : slides);
        Map<String, Object> worksheetPayload =
                extractSpreadsheetStructure(workbook == null ? new LinkedHashMap<>() : workbook);
        Map<String, Object> documentIr = compileDocumentRuntimeIr(
                structure, hierarchy, citations, references, tables, knowledgeGraph,
                slidePayload, worksheetPayload);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("structure", structure);
        out.put("hierarchy", hierarchy);
        out.put("citations", citations);
        out.put("references", references);
        out.put("tables", tables);
        out.put("slides", slidePayload);
        out.put("worksheets", worksheetPayload);
        out.put("knowledge_graph", knowledgeGraph);
        out.put("document_ir", documentIr);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.documents.document_structure_engine.build_document_structure}. */
    static Map<String, Object> buildDocumentStructure(String text) {
        List<Object> sections = new ArrayList<>();
        Map<String, Object> current = newSection("root");

        List<String> lines = PyText.splitlines(text);
        int limit = Math.min(lines.size(), MAX_SECTIONS);
        for (int i = 0; i < limit; i++) {
            String stripped = PyText.strip(lines.get(i));
            if (stripped.startsWith("#")) {
                if (!content(current).isEmpty()) {
                    sections.add(current);
                }
                current = newSection(PyText.strip(PyText.lstrip(stripped, "#")));
            } else {
                content(current).add(stripped);
            }
        }
        if (!content(current).isEmpty()) {
            sections.add(current);
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("sections", sections);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> newSection(String title) {
        Map<String, Object> s = new LinkedHashMap<>();
        s.put("title", title);
        s.put("content", new ArrayList<>());
        return s;
    }

    @SuppressWarnings("unchecked")
    private static List<Object> content(Map<String, Object> section) {
        return (List<Object>) section.get("content");
    }

    @SuppressWarnings("unchecked")
    private static List<Object> sectionsOf(Map<String, Object> structure) {
        Object v = structure.get("sections");
        return v instanceof List ? (List<Object>) v : new ArrayList<>();
    }

    /** {@code core.documents.document_hierarchy_engine.build_document_hierarchy}. */
    static Map<String, Object> buildDocumentHierarchy(Map<String, Object> structure) {
        List<Object> hierarchy = new ArrayList<>();
        List<Object> sections = sectionsOf(structure);
        for (int idx = 0; idx < sections.size(); idx++) {
            Map<String, Object> section = (Map<String, Object>) sections.get(idx);
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("id", "section_" + idx);
            node.put("title", section.get("title"));
            node.put("children", new ArrayList<>());
            hierarchy.add(node);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("hierarchy", hierarchy);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.documents.citation_extraction_engine.extract_citations}. */
    static Map<String, Object> extractCitations(String text) {
        List<Object> citations = new ArrayList<>();
        Matcher m = CITATION_PATTERN.matcher(text);
        while (m.find()) {
            if (citations.size() >= MAX_REFERENCES) {
                break;
            }
            Map<String, Object> c = new LinkedHashMap<>();
            c.put("citation", m.group(1));
            citations.add(c);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("citations", citations);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.documents.reference_extraction_engine.extract_references}. */
    @SuppressWarnings("unchecked")
    static Map<String, Object> extractReferences(Map<String, Object> structure) {
        List<Object> references = new ArrayList<>();
        for (Object so : sectionsOf(structure)) {
            Map<String, Object> section = (Map<String, Object>) so;
            Object titleObj = Py.get(section, "title", "");
            String title = PyText.strip(titleObj == null ? "" : titleObj.toString())
                    .toLowerCase(Locale.ROOT);
            if (REFERENCE_SECTIONS.contains(title)) {
                Object cont = Py.get(section, "content", new ArrayList<>());
                if (cont instanceof List) {
                    references.addAll((List<Object>) cont);
                }
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("references", references);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.documents.document_table_engine.extract_document_tables}. */
    static Map<String, Object> extractDocumentTables(String text) {
        List<Object> tables = new ArrayList<>();
        List<Object> rows = new ArrayList<>();
        for (String line : PyText.splitlines(text)) {
            if (line.indexOf('|') >= 0) {
                List<Object> cells = new ArrayList<>();
                for (String part : line.split(Pattern.quote("|"), -1)) {
                    cells.add(PyText.strip(part));
                }
                rows.add(cells);
            }
        }
        if (!rows.isEmpty()) {
            Map<String, Object> table = new LinkedHashMap<>();
            table.put("rows", slice(rows, MAX_ROWS));
            tables.add(table);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("tables", slice(tables, MAX_TABLES));
        out.put("bounded", true);
        return out;
    }

    /** {@code core.knowledge.document_knowledge_graph_engine.build_document_knowledge_graph}. */
    @SuppressWarnings("unchecked")
    static Map<String, Object> buildDocumentKnowledgeGraph(Map<String, Object> structure) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        List<Object> sections = sectionsOf(structure);
        for (int idx = 0; idx < sections.size(); idx++) {
            Map<String, Object> section = (Map<String, Object>) sections.get(idx);
            String nodeId = "section_" + idx;
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("id", nodeId);
            node.put("title", section.get("title"));
            nodes.add(node);
            if (idx > 0) {
                Map<String, Object> edge = new LinkedHashMap<>();
                edge.put("from", "section_" + (idx - 1));
                edge.put("to", nodeId);
                edge.put("relation", "next_section");
                edges.add(edge);
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("nodes", slice(nodes, MAX_NODES));
        out.put("edges", slice(edges, MAX_NODES));
        out.put("bounded", true);
        return out;
    }

    /** {@code core.presentation.presentation_extraction_engine.extract_presentation_structure}. */
    @SuppressWarnings("unchecked")
    static Map<String, Object> extractPresentationStructure(List<Object> slides) {
        List<Object> parsed = new ArrayList<>();
        int limit = Math.min(slides.size(), MAX_SLIDES);
        for (int idx = 0; idx < limit; idx++) {
            Map<String, Object> slide = (Map<String, Object>) slides.get(idx);
            Map<String, Object> p = new LinkedHashMap<>();
            p.put("slide", (long) idx);
            p.put("title", Py.get(slide, "title", null));
            p.put("content", Py.get(slide, "content", null));
            parsed.add(p);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("slides", parsed);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.spreadsheets.spreadsheet_extraction_engine.extract_spreadsheet_structure}. */
    @SuppressWarnings("unchecked")
    static Map<String, Object> extractSpreadsheetStructure(Map<String, Object> workbook) {
        List<Object> sheets = new ArrayList<>();
        int count = 0;
        for (Map.Entry<String, Object> e : workbook.entrySet()) {
            if (count >= MAX_SHEETS) {
                break;
            }
            Map<String, Object> sheet = new LinkedHashMap<>();
            sheet.put("sheet", e.getKey());
            Object rows = e.getValue();
            sheet.put("rows", rows instanceof List ? slice((List<Object>) rows, MAX_ROWS) : rows);
            sheets.add(sheet);
            count++;
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("worksheets", sheets);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.ir.document_runtime_ir.compile_document_runtime_ir}. */
    static Map<String, Object> compileDocumentRuntimeIr(
            Map<String, Object> structure, Map<String, Object> hierarchy,
            Map<String, Object> citations, Map<String, Object> references,
            Map<String, Object> tables, Map<String, Object> knowledgeGraph,
            Map<String, Object> slides, Map<String, Object> worksheets) {
        Map<String, Object> s = (slides == null || slides.isEmpty()) ? emptyList("slides") : slides;
        Map<String, Object> w =
                (worksheets == null || worksheets.isEmpty()) ? emptyList("worksheets") : worksheets;

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("ir", "document_runtime");
        out.put("document_structure", structure);
        out.put("sections", structure.getOrDefault("sections", new ArrayList<>()));
        out.put("hierarchy", hierarchy);
        out.put("tables", tables);
        out.put("slides", s);
        out.put("worksheets", w);
        out.put("citations", citations);
        out.put("references", references);
        out.put("knowledge_graph", knowledgeGraph);
        out.put("structure", structure);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> emptyList(String key) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put(key, new ArrayList<>());
        m.put("bounded", true);
        return m;
    }

    private static List<Object> slice(List<Object> xs, int n) {
        return new ArrayList<>(xs.subList(0, Math.min(n, xs.size())));
    }
}
