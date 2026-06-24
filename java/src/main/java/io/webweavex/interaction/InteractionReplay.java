package io.webweavex.interaction;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.interaction.interaction_replay_engine.replay_interactions} plus
 * {@code core.interaction.browser_interaction_engine.record_interaction}. The replay log is a pure
 * function of the interaction log (deterministic {@code record_interaction} entries); the page
 * handlers (click/fill/select/hover/wait) are side-effect only and never reach the output, so the
 * API is browser-free. See {@code java/JAVA_PLAYWRIGHT_VERDICT.md}.
 */
public final class InteractionReplay {

    private InteractionReplay() {
    }

    private static final int MAX_REPLAY_ACTIONS = 1000;

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : new LinkedHashMap<>();
    }

    /** Python {@code d.get(key, default)} — default only when the key is absent. */
    private static Object gd(Map<String, Object> m, String key, Object dflt) {
        return m.containsKey(key) ? m.get(key) : dflt;
    }

    /** {@code record_interaction(action, selector, metadata, step)}. */
    public static Map<String, Object> recordInteraction(
            String action, String selector, Map<String, Object> metadata, long step) {
        Map<String, Object> r = new LinkedHashMap<>();
        r.put("id", "interaction_" + step);
        r.put("timestamp", step);
        r.put("action", Py.str(action).strip());
        r.put("selector", Py.str(selector).strip());
        r.put("metadata", metadata == null ? new LinkedHashMap<>() : new LinkedHashMap<>(metadata));
        r.put("bounded", true);
        return r;
    }

    private static String fillValue(Map<String, Object> action) {
        if (action.containsKey("value")) {
            return Py.str(action.get("value"));
        }
        Object md = gd(action, "metadata", new LinkedHashMap<>());
        Map<String, Object> m = asMap(md);
        return Py.str(gd(m, "value", ""));
    }

    private static void dispatch(ReplayPage page, String type, Map<String, Object> action) {
        if (page == null) {
            return;
        }
        String selector = Py.str(gd(action, "selector", ""));
        switch (type) {
            case "click":
                if (page.hasClick()) {
                    page.click(selector);
                }
                break;
            case "fill":
                if (page.hasFill()) {
                    page.fill(selector, fillValue(action));
                }
                break;
            case "select":
                if (page.hasSelectOption()) {
                    page.selectOption(selector, fillValue(action));
                }
                break;
            case "hover":
                if (page.hasHover()) {
                    page.hover(selector);
                }
                break;
            case "wait":
                if (page.hasWaitForSelector()) {
                    page.waitForSelector(selector);
                }
                break;
            default:
                break;
        }
    }

    /** {@code replay_interactions(page, interaction_log)}. */
    public static Map<String, Object> replayInteractions(ReplayPage page, List<Object> interactionLog) {
        List<Object> replayLog = new ArrayList<>();
        List<Object> log = interactionLog == null ? new ArrayList<>() : interactionLog;
        int limit = Math.min(log.size(), MAX_REPLAY_ACTIONS);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> action = asMap(log.get(index));
            String actionType = Py.str(gd(action, "action", gd(action, "type", ""))).strip();

            dispatch(page, actionType, action);

            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("step", (long) index);
            entry.put("action", recordInteraction(
                    actionType, Py.str(gd(action, "selector", "")),
                    asMap(gd(action, "metadata", new LinkedHashMap<>())), index));
            entry.put("replayed", true);
            replayLog.add(entry);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("replay", replayLog);
        out.put("bounded", true);
        return out;
    }
}
