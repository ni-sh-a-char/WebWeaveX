package io.webweavex.interaction;

/**
 * Duck-typed page contract consumed by {@link InteractionReplay#replayInteractions}, mirroring the
 * {@code hasattr(page, "click"/"fill"/…)} guards in {@code core.interaction.browser_interaction_engine}.
 * The action handlers are <em>side-effect only</em>: the observable replay log is built purely from
 * {@code record_interaction}, independent of the page. A {@code null} page (or absent hooks) simply
 * skips the side effect — exactly as CPython's {@code if page is not None and hasattr(page, …)}.
 */
public interface ReplayPage {

    default boolean hasClick() {
        return false;
    }

    default void click(String selector) {
    }

    default boolean hasFill() {
        return false;
    }

    default void fill(String selector, String value) {
    }

    default boolean hasSelectOption() {
        return false;
    }

    default void selectOption(String selector, String value) {
    }

    default boolean hasHover() {
        return false;
    }

    default void hover(String selector) {
    }

    default boolean hasWaitForSelector() {
        return false;
    }

    default void waitForSelector(String selector) {
    }
}
