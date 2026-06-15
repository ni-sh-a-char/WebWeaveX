package io.webweavex.knowledge;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyFloat;
import io.webweavex.determinism.PyRound;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.evidence.contradiction_lattice_engine.build_contradiction_lattice}. */
public final class ContradictionLattice {

    private ContradictionLattice() {
    }

    public static Map<String, Object> build(List<Object> pairs) {
        List<List<String>> normalized = new ArrayList<>();
        for (Object po : pairs == null ? List.of() : pairs) {
            List<Object> p = Py.asList(po);
            if (p != null && p.size() >= 2) {
                normalized.add(List.of(Py.str(p.get(0)), Py.str(p.get(1))));
            }
        }
        int count = normalized.size();
        double pressure = PyRound.round(Math.min(1.0, count * 0.25), 3);

        List<List<String>> sorted = new ArrayList<>(normalized);
        sorted.sort(Comparator
                .comparing((List<String> p) -> p.get(0), Normalization::codePointCompare)
                .thenComparing(p -> p.get(1), Normalization::codePointCompare));
        List<Object> pairsOut = new ArrayList<>();
        for (List<String> p : sorted) {
            pairsOut.add(new ArrayList<Object>(p));
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("pairs", pairsOut);
        out.put("count", (long) count);
        out.put("pressure", pressure);
        out.put("rigor", "lattice_enumeration");
        out.put("deterministic_inputs",
                List.of("pair_count=" + count, "pressure=" + PyFloat.pyFloatRepr(pressure)));
        return out;
    }
}
