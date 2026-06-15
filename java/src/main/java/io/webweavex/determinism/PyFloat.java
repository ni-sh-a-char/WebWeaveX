package io.webweavex.determinism;

import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Python {@code repr(float)} for doubles — the cross-language canonical float
 * form. Python renders the shortest round-trip digits, positional for decimal
 * exponents in {@code [-4, 15]}, otherwise scientific notation with a sign and
 * at-least-two-digit exponent.
 *
 * <p>{@link Double#toString} cannot be used: on Java 17 it is not guaranteed to
 * produce the shortest representation and its formatting thresholds differ from
 * Python. Instead the shortest round-tripping decimal is found by probing
 * increasing precision (version independent), then reformatted by Python's
 * rules — matching the Dart {@code pyFloatRepr} port exactly.
 */
public final class PyFloat {

    private PyFloat() {
    }

    private static final Pattern SCI =
            Pattern.compile("^(\\d)(?:\\.(\\d+))?[eE]([+-]\\d+)$");

    public static String pyFloatRepr(double x) {
        if (Double.isNaN(x)) {
            return "nan";
        }
        if (x == Double.POSITIVE_INFINITY) {
            return "inf";
        }
        if (x == Double.NEGATIVE_INFINITY) {
            return "-inf";
        }
        if (x == Math.rint(x) && Math.abs(x) < 1e16) {
            // Integral magnitude < 1e16 → "N.0" (Python keeps the sign of -0.0).
            String sign = (Double.doubleToRawLongBits(x) < 0) ? "-" : "";
            long magnitude = (long) Math.abs(x);
            return sign + magnitude + ".0";
        }

        String sign = x < 0 ? "-" : "";
        String[] parts = shortestScientific(Math.abs(x));
        String lead = parts[0];
        String rest = parts[1];
        int exp = Integer.parseInt(parts[2]);

        if (exp < -4 || exp >= 16) {
            String mant = rest.isEmpty() ? lead : lead + "." + rest;
            String esign = exp < 0 ? "-" : "+";
            int eabs = Math.abs(exp);
            String epad = (eabs < 10 ? "0" : "") + eabs;
            return sign + mant + "e" + esign + epad;
        }

        String digits = lead + rest;
        if (exp < 0) {
            return sign + "0." + "0".repeat(-exp - 1) + digits;
        }
        if (digits.length() <= exp + 1) {
            StringBuilder padded = new StringBuilder(digits);
            while (padded.length() < exp + 1) {
                padded.append('0');
            }
            return sign + padded + ".0";
        }
        return sign + digits.substring(0, exp + 1) + "." + digits.substring(exp + 1);
    }

    /**
     * Returns {@code {leadDigit, restDigits, exponent}} for the shortest decimal
     * that round-trips to {@code a} (a &gt; 0, finite, non-integral-or-huge).
     */
    private static String[] shortestScientific(double a) {
        String chosen = null;
        for (int prec = 0; prec <= 17; prec++) {
            String s = String.format(Locale.ROOT, "%." + prec + "e", a);
            if (Double.parseDouble(s) == a) {
                chosen = s;
                break;
            }
        }
        if (chosen == null) {
            chosen = String.format(Locale.ROOT, "%.17e", a);
        }
        Matcher m = SCI.matcher(chosen);
        if (!m.matches()) {
            throw new IllegalStateException("unexpected scientific form: " + chosen);
        }
        String lead = m.group(1);
        String rest = m.group(2) == null ? "" : m.group(2);
        // Trim trailing zeros from the fractional digits (Java pads to prec).
        int end = rest.length();
        while (end > 0 && rest.charAt(end - 1) == '0') {
            end--;
        }
        rest = rest.substring(0, end);
        return new String[] {lead, rest, m.group(3)};
    }
}
