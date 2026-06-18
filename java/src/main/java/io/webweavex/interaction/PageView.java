package io.webweavex.interaction;

/**
 * Duck-typed page contract consumed by {@link Pagination#extractPaginatedContent}, mirroring
 * the attribute/method probing CPython's {@code core.interaction.pagination_engine} performs
 * via {@code getattr}/{@code hasattr} on a page object.
 *
 * <p>A real (e.g. Playwright) page exposes {@code url} and {@code click(selector)}; the
 * deterministic test/replay protocol additionally exposes {@code _test_url},
 * {@code _test_next_url}, and {@code _test_paginate(current)}. Each {@code hasX()} predicate
 * models the corresponding {@code hasattr(page, …)} guard, so absent hooks are honoured
 * exactly (no default substitution where Python would skip the branch).
 */
public interface PageView {

    /** {@code hasattr(page, "_test_url")}. */
    default boolean hasTestUrl() {
        return false;
    }

    /** Value of {@code page._test_url}. */
    default Object testUrl() {
        return null;
    }

    /** Assignment {@code page._test_url = current_url} (only when {@link #hasTestUrl()}). */
    default void setTestUrl(String url) {
    }

    /** {@code hasattr(page, "url")}. */
    default boolean hasUrl() {
        return false;
    }

    /** Value of {@code page.url}. */
    default Object url() {
        return null;
    }

    /** {@code hasattr(page, "click")}. */
    default boolean hasClick() {
        return false;
    }

    /** {@code page.click(selector)} — may raise (caught → loop break). */
    default void click(String selector) {
    }

    /** {@code hasattr(page, "_test_next_url")}. */
    default boolean hasTestNextUrl() {
        return false;
    }

    /** Value of {@code page._test_next_url}. */
    default Object testNextUrl() {
        return "";
    }

    /** {@code hasattr(page, "_test_paginate")}. */
    default boolean hasTestPaginate() {
        return false;
    }

    /** {@code page._test_paginate(current_url)} — next URL (no {@code str()} coercion in Python). */
    default String testPaginate(String currentUrl) {
        return "";
    }
}
