package io.webweavex.interaction;

/**
 * Duck-typed page contract consumed by {@link InfiniteScroll#extractInfiniteScroll}, mirroring
 * the {@code hasattr}/{@code getattr} probing CPython's {@code core.interaction.infinite_scroll_engine}
 * performs. The deterministic contract reads {@code _test_dom_hash}/{@code _test_html} and drives
 * {@code _test_scroll()}; the real Playwright hooks ({@code evaluate}, {@code content}) are probed
 * but optional and never required for the parity-proven path.
 */
public interface ScrollPage {

    /** {@code hasattr(page, "_test_dom_hash")}. */
    default boolean hasTestDomHash() {
        return false;
    }

    /** {@code page._test_dom_hash}. */
    default Object testDomHash() {
        return null;
    }

    /** {@code hasattr(page, "_test_html")}. */
    default boolean hasTestHtml() {
        return false;
    }

    /** {@code page._test_html}. */
    default String testHtml() {
        return null;
    }

    /** {@code hasattr(page, "content") and callable(page.content)}. */
    default boolean hasContent() {
        return false;
    }

    /** {@code page.content()} — may raise (caught → empty html). */
    default String content() {
        return "";
    }

    /** {@code hasattr(page, "evaluate")}. */
    default boolean hasEvaluate() {
        return false;
    }

    /** {@code page.evaluate(script)} — may raise (caught → ignored). */
    default void evaluate(String script) {
    }

    /** {@code hasattr(page, "_test_scroll")}. */
    default boolean hasTestScroll() {
        return false;
    }

    /** {@code page._test_scroll()}. */
    default void testScroll() {
    }
}
