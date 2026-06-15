package io.webweavex.determinism;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Python {@code round(x, n)} — round-half-to-even on the exact binary value.
 * {@code Math.round} is half-up and would diverge; {@link BigDecimal} over the
 * exact double reproduces CPython's banker's rounding.
 */
public final class PyRound {

    private PyRound() {
    }

    public static double round(double x, int n) {
        if (Double.isNaN(x) || Double.isInfinite(x)) {
            return x;
        }
        return new BigDecimal(x).setScale(n, RoundingMode.HALF_EVEN).doubleValue();
    }
}
