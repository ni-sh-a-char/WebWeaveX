package io.webweavex.ir;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.ir._base} — shared empty IR fragments. */
public final class IrBase {

    private IrBase() {
    }

    public static Map<String, Object> emptyConfidence() {
        Map<String, Object> c = new LinkedHashMap<>();
        c.put("score", 0.0);
        c.put("basis", new ArrayList<>());
        c.put("deterministic", true);
        return c;
    }

    public static Map<String, Object> emptyLineage(String stage) {
        Map<String, Object> s = new LinkedHashMap<>();
        s.put("stage", stage);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("stages", new ArrayList<>(List.of(s)));
        out.put("depth", 1L);
        return out;
    }
}
