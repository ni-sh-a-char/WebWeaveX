package io.webweavex;

/**
 * Top-level package facade exposing the module-level version constants of the canonical
 * Python package ({@code webweavex.__version__} / {@code webweavex.version}).
 *
 * <p>Python 3.0.0 declares {@code __version__ = "3.0.0"} and {@code version = __version__}
 * (a PEP 440 public alias). Both are byte-exact module constants with no runtime dependency,
 * so they are trivially portable and certified against {@code golden_vectors_s28.json}.
 */
public final class WebWeaveX {

    private WebWeaveX() {
    }

    /** {@code webweavex.__version__} / {@code webweavex.version}. */
    public static final String VERSION = "3.0.0";
}

