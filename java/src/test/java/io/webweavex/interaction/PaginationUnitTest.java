package io.webweavex.interaction;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Unit coverage for {@link Pagination} and the {@link PageView} default-method contract —
 * the {@code url}-fallback branch and default {@code click()}/{@code setTestUrl()} paths the
 * fixture-driven parity vectors never reach. Concrete expected values, not self-consistency.
 */
class PaginationUnitTest {

    @Test
    void pageViewDefaultContract() {
        PageView p = new PageView() {
        };
        assertFalse(p.hasTestUrl());
        assertNull(p.testUrl());
        assertFalse(p.hasUrl());
        assertNull(p.url());
        assertFalse(p.hasClick());
        assertFalse(p.hasTestNextUrl());
        assertEquals("", p.testNextUrl());
        assertFalse(p.hasTestPaginate());
        assertEquals("", p.testPaginate("x"));
        p.setTestUrl("y"); // default no-op
        p.click("z");      // default no-op
    }

    @Test
    void nullPageYieldsSingleEmptyUrlPage() {
        Map<String, Object> out = Pagination.extractPaginatedContent(null, "a.next");
        List<?> pages = (List<?>) out.get("pages");
        assertEquals(1, pages.size());
        assertEquals("", ((Map<?, ?>) pages.get(0)).get("url"));
        assertEquals(0L, ((Map<?, ?>) pages.get(0)).get("order"));
        assertEquals(1L, out.get("visited_count"));
        assertEquals(true, out.get("loop_prevented"));
        assertEquals(true, out.get("bounded"));
    }

    @Test
    void urlFallbackWhenNoTestUrl() {
        PageView p = new PageView() {
            @Override
            public boolean hasUrl() {
                return true;
            }

            @Override
            public Object url() {
                return "home";
            }
        };
        Map<String, Object> out = Pagination.extractPaginatedContent(p, "a.next");
        List<?> pages = (List<?>) out.get("pages");
        assertEquals(1, pages.size());
        assertEquals("home", ((Map<?, ?>) pages.get(0)).get("url"));
    }

    @Test
    void defaultClickInvokedDuringPagination() {
        PageView p = new PageView() {
            private String u = "p0";

            @Override
            public boolean hasTestUrl() {
                return true;
            }

            @Override
            public Object testUrl() {
                return u;
            }

            @Override
            public void setTestUrl(String url) {
                this.u = url;
            }

            @Override
            public boolean hasClick() {
                return true; // exercises the default no-op click()
            }

            @Override
            public boolean hasTestPaginate() {
                return true;
            }

            @Override
            public String testPaginate(String currentUrl) {
                return currentUrl.equals("p0") ? "p1" : "";
            }
        };
        Map<String, Object> out = Pagination.extractPaginatedContent(p, "a.next");
        List<?> pages = (List<?>) out.get("pages");
        assertEquals(2, pages.size());
        assertEquals("p0", ((Map<?, ?>) pages.get(0)).get("url"));
        assertEquals("p1", ((Map<?, ?>) pages.get(1)).get("url"));
        assertEquals(2L, out.get("visited_count"));
    }
}
