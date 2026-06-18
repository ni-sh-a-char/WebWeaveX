package io.webweavex.documents;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Unit coverage for {@link DocumentRuntime} sub-engine branches not exercised by the
 * cross-language parity vectors (empty-section drop, reference collection, non-list
 * worksheet rows, the IR empty-slides/worksheets default). Concrete expected values —
 * not self-consistency.
 */
class DocumentRuntimeUnitTest {

    @Test
    void spreadsheetListAndNonListRows() {
        Map<String, Object> wb = new LinkedHashMap<>();
        wb.put("S1", new ArrayList<>(List.of(List.of("a", "b"))));
        wb.put("S2", "raw"); // non-list rows -> kept unchanged (else branch)
        Map<String, Object> out = DocumentRuntime.extractSpreadsheetStructure(wb);
        List<?> sheets = (List<?>) out.get("worksheets");
        assertEquals(2, sheets.size());
        assertEquals("S1", ((Map<?, ?>) sheets.get(0)).get("sheet"));
        assertEquals(List.of(List.of("a", "b")), ((Map<?, ?>) sheets.get(0)).get("rows"));
        assertEquals("raw", ((Map<?, ?>) sheets.get(1)).get("rows"));
        assertEquals(true, out.get("bounded"));
    }

    @Test
    void irEmptySlidesAndWorksheetsUseDefault() {
        Map<String, Object> struct = DocumentRuntime.buildDocumentStructure("# A\nbody\n");
        Map<String, Object> ir = DocumentRuntime.compileDocumentRuntimeIr(
                struct, new LinkedHashMap<>(), new LinkedHashMap<>(), new LinkedHashMap<>(),
                new LinkedHashMap<>(), new LinkedHashMap<>(),
                new LinkedHashMap<>(), new LinkedHashMap<>());
        assertEquals("document_runtime", ir.get("ir"));
        Map<?, ?> slides = (Map<?, ?>) ir.get("slides");
        assertEquals(new ArrayList<>(), slides.get("slides"));
        assertEquals(true, slides.get("bounded"));
        Map<?, ?> worksheets = (Map<?, ?>) ir.get("worksheets");
        assertEquals(new ArrayList<>(), worksheets.get("worksheets"));
        assertEquals(true, worksheets.get("bounded"));
    }

    @Test
    void structureDropsEmptySectionsOnHeadingAfterHeading() {
        Map<String, Object> s = DocumentRuntime.buildDocumentStructure("# A\n# B\ncontent\n");
        List<?> sections = (List<?>) s.get("sections");
        assertEquals(1, sections.size()); // empty section "A" is dropped
        assertEquals("B", ((Map<?, ?>) sections.get(0)).get("title"));
        assertEquals(List.of("content"), ((Map<?, ?>) sections.get(0)).get("content"));
    }

    @Test
    void referencesSectionCollected() {
        Map<String, Object> struct =
                DocumentRuntime.buildDocumentStructure("# Doc\nintro\n## References\nr1\nr2\n");
        Map<String, Object> refs = DocumentRuntime.extractReferences(struct);
        assertEquals(List.of("r1", "r2"), refs.get("references"));
        assertEquals(true, refs.get("bounded"));
    }

    @Test
    void citationsAndTablesAndHierarchy() {
        Map<String, Object> c = DocumentRuntime.extractCitations("a [1] b [22] c");
        List<?> cits = (List<?>) c.get("citations");
        assertEquals(2, cits.size());
        assertEquals("1", ((Map<?, ?>) cits.get(0)).get("citation"));
        assertEquals("22", ((Map<?, ?>) cits.get(1)).get("citation"));

        Map<String, Object> t = DocumentRuntime.extractDocumentTables("a | b\nc | d\n");
        List<?> tables = (List<?>) t.get("tables");
        assertEquals(1, tables.size());
        List<?> rows = (List<?>) ((Map<?, ?>) tables.get(0)).get("rows");
        assertEquals(List.of("a", "b"), rows.get(0));
        assertEquals(List.of("c", "d"), rows.get(1));

        Map<String, Object> struct = DocumentRuntime.buildDocumentStructure("# A\nx\n## B\ny\n");
        Map<String, Object> h = DocumentRuntime.buildDocumentHierarchy(struct);
        List<?> hierarchy = (List<?>) h.get("hierarchy");
        assertEquals("section_0", ((Map<?, ?>) hierarchy.get(0)).get("id"));
        assertEquals("A", ((Map<?, ?>) hierarchy.get(0)).get("title"));
    }

    @Test
    void endToEndShape() {
        Map<String, Object> out = DocumentRuntime.extractDocumentRuntime("# T\nx\n", null, null);
        assertEquals(true, out.get("bounded"));
        assertEquals("document_runtime", ((Map<?, ?>) out.get("document_ir")).get("ir"));
        Map<?, ?> slides = (Map<?, ?>) out.get("slides");
        assertEquals(new ArrayList<>(), slides.get("slides"));
        Map<?, ?> kg = (Map<?, ?>) out.get("knowledge_graph");
        assertEquals(true, kg.get("bounded"));
    }
}
