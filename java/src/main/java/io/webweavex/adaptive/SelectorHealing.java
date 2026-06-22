package io.webweavex.adaptive;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyRepr;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Port of {@code core.adaptive.selector_healing_engine.heal_selector} for the portable
 * (empty-HTML) contract. The canon also accepts an {@code html} string and, when non-empty, builds
 * a BeautifulSoup-backed semantic anchor; that branch is Tier-C (needs the lxml/bs4 Soup engine).
 * With {@code html=""} (the default), {@code build_semantic_anchor} parses an empty document and
 * yields no matches, so the {@code semantic_anchor} strategy never contributes and the output is a
 * pure, bs4-independent function of {@code selector} + {@code dom_nodes} (proven: the empty-HTML
 * path is deterministic and portable). This method certifies exactly that contract, byte-exact.
 * Zero new substrate.
 */
public final class SelectorHealing {

    private SelectorHealing() {
    }

    private static final int MAX_CANDIDATES = 100;
    private static final Pattern ID_TOKEN = Pattern.compile("#([a-zA-Z0-9_-]+)");
    private static final Pattern CLASS_TOKEN = Pattern.compile("\\.([a-zA-Z0-9_-]+)");

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : new LinkedHashMap<>();
    }

    private static String str(Object o) {
        return PyRepr.str(o);
    }

    private static String selectorToken(String selector) {
        Matcher idm = ID_TOKEN.matcher(selector);
        if (idm.find()) {
            return idm.group(1).replace("-", " ").replace("_", " ").toLowerCase(Locale.ROOT);
        }
        Matcher cm = CLASS_TOKEN.matcher(selector);
        if (cm.find()) {
            return cm.group(1).replace("-", " ").replace("_", " ").toLowerCase(Locale.ROOT);
        }
        return selector.strip().toLowerCase(Locale.ROOT);
    }

    private static String slice(String s, int n) {
        return s.length() > n ? s.substring(0, n) : s;
    }

    /** {@code heal_selector(selector, dom_nodes, html="")} — empty-HTML portable contract. */
    public static Map<String, Object> healSelector(String selector, List<Object> domNodes) {
        List<Object> nodes = domNodes;
        List<Object> strategies = new ArrayList<>();
        // semantic_anchor: skipped — empty HTML yields no anchors (bs4-independent).

        // text_anchor
        List<Object> capped = nodes.size() > MAX_CANDIDATES ? nodes.subList(0, MAX_CANDIDATES) : nodes;
        String token = selectorToken(selector);
        for (Object no : capped) {
            Map<String, Object> node = asMap(no);
            String text = str(Py.get(node, "text", "")).toLowerCase(Locale.ROOT);
            String tag = str(Py.get(node, "tag", "div"));
            if (!token.isEmpty() && text.contains(token)) {
                Map<String, Object> s = new LinkedHashMap<>();
                s.put("strategy", "text_anchor");
                s.put("selector", tag + ":has-text('" + slice(str(Py.get(node, "text", "")), 100) + "')");
                strategies.add(s);
                break;
            }
        }

        // attribute_anchor (loop runs regardless; breaks once any strategy exists)
        for (Object no : capped) {
            Map<String, Object> node = asMap(no);
            Object attrsObj = node.get("attrs");
            if (attrsObj instanceof Map) {
                Map<String, Object> attrs = asMap(attrsObj);
                TreeSet<String> sortedKeys = new TreeSet<>(Normalization::codePointCompare);
                sortedKeys.addAll(attrs.keySet());
                for (String key : sortedKeys) {
                    if (key.equals("aria-label") || key.equals("data-testid") || key.equals("name")
                            || key.equals("id")) {
                        String value = str(attrs.get(key));
                        Map<String, Object> s = new LinkedHashMap<>();
                        s.put("strategy", "attribute_anchor");
                        s.put("selector", "[" + key + "='" + slice(value, 200) + "']");
                        strategies.add(s);
                        break;
                    }
                }
            }
            if (!strategies.isEmpty()) {
                break;
            }
        }

        if (strategies.isEmpty()) {
            String parentTag = nodes.isEmpty() ? "div" : str(Py.get(asMap(nodes.get(0)), "tag", "div"));
            Map<String, Object> s = new LinkedHashMap<>();
            s.put("strategy", "structural_fallback");
            s.put("selector", parentTag);
            strategies.add(s);
        }

        Map<String, Object> healed = asMap(strategies.get(0));
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("original", selector);
        out.put("healed_selector", healed.get("selector"));
        out.put("strategy", healed.get("strategy"));
        out.put("candidates", strategies.size() > 10 ? new ArrayList<>(strategies.subList(0, 10)) : strategies);
        out.put("bounded", true);
        return out;
    }
}
