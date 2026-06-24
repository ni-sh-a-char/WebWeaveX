package io.webweavex.streaming;

import java.util.List;

/**
 * Duck-typed page contract consumed by the deterministic stream-capture engines
 * ({@code capture_websocket_frames}, {@code track_websocket_connections},
 * {@code capture_dom_mutations}), mirroring the {@code hasattr(page, "_test_*")} probing
 * CPython performs in {@code core.streaming.*}.
 *
 * <p>These engines never touch a live browser: they read only {@code _test_*} attributes of
 * the page (or return empty when the attribute is absent / the page is {@code null}). A real
 * Playwright page simply lacks the {@code _test_*} hooks, so each {@code hasX()} predicate
 * models the corresponding {@code hasattr} guard and absent hooks are honoured exactly.
 */
public interface StreamPage {

    /** {@code hasattr(page, "_test_websocket_frames")}. */
    default boolean hasTestWebsocketFrames() {
        return false;
    }

    /** {@code page._test_websocket_frames}. */
    default List<Object> testWebsocketFrames() {
        return null;
    }

    /** {@code hasattr(page, "_test_websocket_connections")}. */
    default boolean hasTestWebsocketConnections() {
        return false;
    }

    /** {@code page._test_websocket_connections}. */
    default List<Object> testWebsocketConnections() {
        return null;
    }

    /** {@code hasattr(page, "_test_dom_mutations")}. */
    default boolean hasTestDomMutations() {
        return false;
    }

    /** {@code page._test_dom_mutations}. */
    default List<Object> testDomMutations() {
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
}
