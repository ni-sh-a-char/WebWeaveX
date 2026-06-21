package io.webweavex.adaptive;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * Port of {@code core.adaptive.modal_recovery_engine.recover_modal_runtime}. Dependency-clean
 * (1 module, 0 forbidden). The Python function also performs live-{@code page} click side effects
 * via test hooks ({@code page._test_modals}, {@code page.click}); those affect no return value, so
 * the byte-exact contract is a pure function of the supplied {@code html} (the parity path is
 * {@code page=None}).
 */
public final class ModalRecovery {

    private ModalRecovery() {
    }

    private static final int MAX_RETRIES = 5;

    private static final String[] MODAL_CLOSE_SELECTORS = {
        "#cookie-accept",
        "[aria-label='Close']",
        "button.accept",
        ".modal-close",
    };

    /** Python {@code str.strip(chars)} — trims any leading/trailing char contained in {@code chars}. */
    private static String stripChars(String s, String chars) {
        int start = 0;
        int end = s.length();
        while (start < end && chars.indexOf(s.charAt(start)) >= 0) {
            start++;
        }
        while (end > start && chars.indexOf(s.charAt(end - 1)) >= 0) {
            end--;
        }
        return s.substring(start, end);
    }

    private static boolean selectorInHtml(String selector, String html) {
        String token = stripChars(selector, "#.[]");
        token = token.split("'", -1)[0];
        token = token.split("\"", -1)[0];
        return html.toLowerCase(Locale.ROOT).contains(token.toLowerCase(Locale.ROOT));
    }

    /** {@code recover_modal_runtime(page=None, html)} — pure function of {@code html}. */
    public static Map<String, Object> recoverModalRuntime(String html) {
        String h = html == null ? "" : html;
        List<Object> recovered = new ArrayList<>();
        long retries = 0;
        for (String selector : MODAL_CLOSE_SELECTORS) {
            if (retries >= MAX_RETRIES) {
                break;
            }
            if (selectorInHtml(selector, h)) {
                Map<String, Object> entry = new LinkedHashMap<>();
                entry.put("selector", selector);
                entry.put("recovered", true);
                recovered.add(entry);
                retries += 1;
                break;
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("recovered", recovered);
        out.put("retries", retries);
        out.put("bounded", true);
        return out;
    }
}
