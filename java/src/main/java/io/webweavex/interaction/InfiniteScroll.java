package io.webweavex.interaction;

import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.interaction.infinite_scroll_engine.extract_infinite_scroll} — scroll a page
 * until its DOM hash stabilises for two consecutive rounds (or {@code MAX_SCROLLS}). Deterministic
 * over a {@link ScrollPage}: the DOM hash comes from {@code _test_dom_hash}/{@code _test_html} via
 * the certified {@link Kaalka#computeKaalkaHash}. Browser-free — the live {@code page.evaluate}
 * scroll is probed but optional. See {@code java/JAVA_PLAYWRIGHT_VERDICT.md}.
 */
public final class InfiniteScroll {

    private InfiniteScroll() {
    }

    private static final int MAX_SCROLLS = 100;

    private static String slice(String s, int n) {
        return s.length() <= n ? s : s.substring(0, n);
    }

    /** {@code _dom_hash(page)}. */
    private static String domHash(ScrollPage page) {
        if (page.hasTestDomHash() && Py.truthy(page.testDomHash())) {
            return Py.str(page.testDomHash());
        }
        String html = "";
        if (page.hasTestHtml()) {
            html = Py.str(page.testHtml());
        } else if (page.hasContent()) {
            try {
                html = Py.str(page.content());
            } catch (RuntimeException e) {
                html = "";
            }
        }
        return Kaalka.computeKaalkaHash(slice(html, 1_000_000));
    }

    /** {@code extract_infinite_scroll(page)}. */
    public static Map<String, Object> extractInfiniteScroll(ScrollPage page) {
        int scrolls = 0;
        List<Object> chunks = new ArrayList<>();
        String previousHash = domHash(page);
        int stableRounds = 0;

        while (scrolls < MAX_SCROLLS) {
            if (page != null && page.hasEvaluate()) {
                try {
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)");
                } catch (RuntimeException e) {
                    // pass
                }
            }
            if (page.hasTestScroll()) {
                page.testScroll();
            }
            scrolls++;
            String currentHash = domHash(page);

            Map<String, Object> chunk = new LinkedHashMap<>();
            chunk.put("scroll", (long) scrolls);
            chunk.put("dom_hash", currentHash);
            chunks.add(chunk);

            if (currentHash.equals(previousHash)) {
                stableRounds++;
            } else {
                stableRounds = 0;
            }

            if (stableRounds >= 2) {
                break;
            }
            previousHash = currentHash;
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("scrolls", (long) scrolls);
        out.put("chunks", chunks);
        out.put("stopped_on_stable_dom", stableRounds >= 2);
        out.put("bounded", true);
        return out;
    }
}
