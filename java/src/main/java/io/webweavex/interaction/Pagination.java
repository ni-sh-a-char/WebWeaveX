package io.webweavex.interaction;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Port of {@code core.interaction.pagination_engine.extract_paginated_content} — walk a
 * page's "next" links up to {@code MAX_PAGES}, recording {@code {url, order}} per page with
 * cycle prevention. Deterministic over a {@link PageView}; verified free of BeautifulSoup,
 * lxml, browser, OCR, PDF, DOCX, network and LLM dependencies (the module is self-contained;
 * see {@code java/JAVA_SESSION_4B_DEPENDENCY_PROOF.md}).
 */
public final class Pagination {

    private Pagination() {
    }

    private static final int MAX_PAGES = 100;

    /** {@code extract_paginated_content(page, next_selector)}. */
    public static Map<String, Object> extractPaginatedContent(PageView page, String nextSelector) {
        Set<String> visited = new LinkedHashSet<>();
        List<Object> pages = new ArrayList<>();

        String currentUrl = "";
        if (page != null) {
            Object tu;
            if (page.hasTestUrl()) {
                tu = page.testUrl();
            } else if (page.hasUrl()) {
                tu = page.url();
            } else {
                tu = "";
            }
            currentUrl = Py.str(tu);
        }

        while (pages.size() < MAX_PAGES) {
            if (visited.contains(currentUrl)) {
                break;
            }
            visited.add(currentUrl);

            Map<String, Object> p = new LinkedHashMap<>();
            p.put("url", currentUrl);
            p.put("order", (long) pages.size());
            pages.add(p);

            if (nextSelector == null || nextSelector.isEmpty()) {
                break;
            }

            if (page != null && page.hasClick()) {
                try {
                    page.click(nextSelector);
                } catch (RuntimeException e) {
                    break;
                }
            }

            String nextUrl = Py.str(
                    page != null && page.hasTestNextUrl() ? page.testNextUrl() : "");

            if (nextUrl.isEmpty() || nextUrl.equals(currentUrl)) {
                if (page != null && page.hasTestPaginate()) {
                    String pg = page.testPaginate(currentUrl);
                    nextUrl = pg == null ? "" : pg;
                }
            }

            if (nextUrl.isEmpty() || visited.contains(nextUrl)) {
                break;
            }

            currentUrl = nextUrl;
            if (page != null && page.hasTestUrl()) {
                page.setTestUrl(currentUrl);
            }
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("pages", pages);
        out.put("visited_count", (long) visited.size());
        out.put("loop_prevented", pages.size() < MAX_PAGES);
        out.put("bounded", true);
        return out;
    }
}
