package io.webweavex.multimodal;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Port of the multimodal / OCR cluster under the canonical cross-language contract — the OCR runtime
 * is treated as ABSENT (exactly as the JavaScript port hardcodes {@code pytesseract = null} in
 * {@code src/ocr/ocrEngine.ts}, and as the canonical cross-language golden vectors are generated).
 * Under this contract {@code extract_ocr} returns {@code ocr_dependencies_missing}, the downstream
 * layout/tables/forms/charts/ui engines operate on empty regions, and the output is fully
 * deterministic and language-portable.
 *
 * <p>Ports {@code core.ocr.ocr_engine.extract_ocr} (no-OCR path), the pure
 * {@code core.layout/tables/vision} engines, {@code core.ir.multimodal_ir.compile_multimodal_ir},
 * {@code core.multimodal.…extract_multimodal}, and {@code core.ingestion.…ingest_input}/
 * {@code detect_input_type}. Frontier reduction (Session 32): the OCR family is portable for the
 * canonical OCR-absent contract — superseding the earlier conservative blocker.
 */
public final class MultimodalRuntime {

    private MultimodalRuntime() {
    }

    private static final Map<String, String> SUPPORTED_EXTENSIONS = new LinkedHashMap<>();

    static {
        SUPPORTED_EXTENSIONS.put(".pdf", "pdf");
        SUPPORTED_EXTENSIONS.put(".docx", "docx");
        SUPPORTED_EXTENSIONS.put(".pptx", "pptx");
        SUPPORTED_EXTENSIONS.put(".xlsx", "xlsx");
        SUPPORTED_EXTENSIONS.put(".csv", "csv");
        SUPPORTED_EXTENSIONS.put(".json", "json");
        SUPPORTED_EXTENSIONS.put(".xml", "xml");
        SUPPORTED_EXTENSIONS.put(".html", "html");
        SUPPORTED_EXTENSIONS.put(".md", "markdown");
        SUPPORTED_EXTENSIONS.put(".txt", "text");
        SUPPORTED_EXTENSIONS.put(".py", "repository");
        SUPPORTED_EXTENSIONS.put(".js", "repository");
        SUPPORTED_EXTENSIONS.put(".ts", "repository");
        SUPPORTED_EXTENSIONS.put(".zip", "archive");
        SUPPORTED_EXTENSIONS.put(".png", "image");
        SUPPORTED_EXTENSIONS.put(".jpg", "image");
        SUPPORTED_EXTENSIONS.put(".jpeg", "image");
    }

    private static final Set<String> INPUT_KEYWORDS = Set.of("email", "password", "username", "search");
    private static final Set<String> CHART_TERMS = Set.of("revenue", "sales", "growth", "profit");
    private static final Set<String> BUTTON_KEYWORDS = Set.of("submit", "login", "sign in", "continue");

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static List<Object> asList(Object o) {
        return o instanceof List ? (List<Object>) o : new ArrayList<>();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : map();
    }

    /** Python {@code pathlib.Path(path).suffix.lower()} — last component's final extension. */
    private static String suffix(String path) {
        String base = path;
        int slash = Math.max(base.lastIndexOf('/'), base.lastIndexOf('\\'));
        if (slash >= 0) {
            base = base.substring(slash + 1);
        }
        int dot = base.lastIndexOf('.');
        if (dot > 0 && dot < base.length() - 1) {
            return base.substring(dot).toLowerCase();
        }
        return "";
    }

    /** {@code core.ingestion.universal_ingestion_engine.detect_input_type}. */
    public static String detectInputType(String path) {
        if (path.startsWith("http://") || path.startsWith("https://")) {
            return "url";
        }
        return SUPPORTED_EXTENSIONS.getOrDefault(suffix(path), "unknown");
    }

    /** {@code core.ocr.ocr_engine.extract_ocr} — canonical OCR-absent path. */
    public static Map<String, Object> extractOcr(String path) {
        Map<String, Object> out = map();
        out.put("available", false);
        out.put("regions", new ArrayList<>());
        out.put("reason", "ocr_dependencies_missing");
        out.put("bounded", true);
        return out;
    }

    /** {@code core.layout.layout_detection_engine.detect_layout_blocks}. */
    public static Map<String, Object> detectLayoutBlocks(List<Object> ocrRegions) {
        List<Object> blocks = new ArrayList<>();
        int limit = Math.min(ocrRegions.size(), 10000);
        for (int idx = 0; idx < limit; idx++) {
            Map<String, Object> region = asMap(ocrRegions.get(idx));
            Map<String, Object> b = map();
            b.put("id", "block_" + idx);
            b.put("bbox", region.get("bbox"));
            b.put("text", region.getOrDefault("text", ""));
            b.put("type", "text_block");
            blocks.add(b);
        }
        Map<String, Object> out = map();
        out.put("blocks", blocks);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.tables.table_extraction_engine.extract_tables}. */
    public static Map<String, Object> extractTables(Map<String, Object> layoutBlocks) {
        List<Object> tables = new ArrayList<>();
        List<Object> currentRows = new ArrayList<>();
        for (Object bObj : asList(layoutBlocks.get("blocks"))) {
            String text = Py.str(asMap(bObj).getOrDefault("text", ""));
            if (text.contains("|")) {
                List<Object> row = new ArrayList<>();
                for (String x : text.split("\\|", -1)) {
                    row.add(x.strip());
                }
                currentRows.add(row);
            }
        }
        if (!currentRows.isEmpty()) {
            Map<String, Object> t = map();
            t.put("rows", currentRows.subList(0, Math.min(currentRows.size(), 1000)));
            tables.add(t);
        }
        Map<String, Object> out = map();
        out.put("tables", tables);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.vision.form_extraction_engine.extract_forms}. */
    public static Map<String, Object> extractForms(Map<String, Object> blocks) {
        List<Object> forms = new ArrayList<>();
        for (Object bObj : asList(blocks.get("blocks"))) {
            Map<String, Object> block = asMap(bObj);
            String text = Py.str(block.getOrDefault("text", "")).toLowerCase();
            if (INPUT_KEYWORDS.contains(text)) {
                Map<String, Object> f = map();
                f.put("field", text);
                f.put("bbox", block.get("bbox"));
                forms.add(f);
            }
        }
        Map<String, Object> out = map();
        out.put("forms", forms);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.vision.chart_detection_engine.detect_charts}. */
    public static Map<String, Object> detectCharts(Map<String, Object> blocks) {
        boolean detected = false;
        for (Object bObj : asList(blocks.get("blocks"))) {
            String text = Py.str(asMap(bObj).getOrDefault("text", "")).toLowerCase();
            for (String term : CHART_TERMS) {
                if (text.contains(term)) {
                    detected = true;
                    break;
                }
            }
            if (detected) {
                break;
            }
        }
        Map<String, Object> chart = map();
        chart.put("detected", detected);
        List<Object> charts = new ArrayList<>();
        charts.add(chart);
        Map<String, Object> out = map();
        out.put("charts", charts);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.vision.ui_component_detection_engine.detect_ui_components}. */
    public static Map<String, Object> detectUiComponents(Map<String, Object> blocks) {
        List<Object> components = new ArrayList<>();
        for (Object bObj : asList(blocks.get("blocks"))) {
            Map<String, Object> block = asMap(bObj);
            String text = Py.str(block.getOrDefault("text", "")).toLowerCase();
            if (BUTTON_KEYWORDS.contains(text)) {
                Map<String, Object> c = map();
                c.put("type", "button");
                c.put("text", text);
                c.put("bbox", block.get("bbox"));
                components.add(c);
            }
        }
        Map<String, Object> out = map();
        out.put("components", components);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.ir.multimodal_ir.compile_multimodal_ir}. */
    public static Map<String, Object> compileMultimodalIr(Map<String, Object> layout, Map<String, Object> tables,
            Map<String, Object> forms, Map<String, Object> charts, Map<String, Object> ui) {
        Map<String, Object> out = map();
        out.put("ir", "multimodal");
        out.put("semantic_blocks", layout.getOrDefault("blocks", new ArrayList<>()));
        out.put("layout_tree", layout);
        out.put("tables", tables);
        out.put("charts", charts);
        out.put("forms", forms);
        out.put("navigation", new ArrayList<>());
        out.put("ui_components", ui);
        out.put("layout", layout);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.multimodal.universal_multimodal_extraction_engine.extract_multimodal}. */
    public static Map<String, Object> extractMultimodal(String path) {
        Map<String, Object> ocr = extractOcr(path);
        Map<String, Object> layout = detectLayoutBlocks(asList(ocr.getOrDefault("regions", new ArrayList<>())));
        Map<String, Object> tables = extractTables(layout);
        Map<String, Object> forms = extractForms(layout);
        Map<String, Object> charts = detectCharts(layout);
        Map<String, Object> ui = detectUiComponents(layout);
        Map<String, Object> mir = compileMultimodalIr(layout, tables, forms, charts, ui);
        Map<String, Object> out = map();
        out.put("ocr", ocr);
        out.put("layout", layout);
        out.put("tables", tables);
        out.put("forms", forms);
        out.put("charts", charts);
        out.put("ui", ui);
        out.put("multimodal_ir", mir);
        out.put("bounded", true);
        return out;
    }

    /** {@code core.ingestion.universal_ingestion_engine.ingest_input}. */
    public static Map<String, Object> ingestInput(String path) {
        String inputType = detectInputType(path);
        Map<String, Object> out = map();
        if (inputType.equals("image")) {
            out.put("path", path);
            out.put("type", "image");
            out.put("input_type", inputType);
            out.put("supported", true);
            out.put("multimodal", extractMultimodal(path));
            out.put("bounded", true);
            return out;
        }
        out.put("path", path);
        out.put("input_type", inputType);
        out.put("supported", !inputType.equals("unknown"));
        out.put("bounded", true);
        return out;
    }
}
