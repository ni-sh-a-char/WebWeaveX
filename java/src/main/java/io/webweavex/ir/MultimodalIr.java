package io.webweavex.ir;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.ir.multimodal_ir.compile_multimodal_ir}. Output is
 * byte-identical to Python under {@code compute_deterministic_hash}.
 */
public final class MultimodalIr {

    private MultimodalIr() {
    }

    public static Map<String, Object> compile(
            Map<String, Object> layout,
            Map<String, Object> tables,
            Map<String, Object> forms,
            Map<String, Object> charts,
            Map<String, Object> ui) {

        Object blocks = Py.get(layout, "blocks", new ArrayList<>());

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("ir", "multimodal");
        out.put("semantic_blocks", blocks);
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
}
