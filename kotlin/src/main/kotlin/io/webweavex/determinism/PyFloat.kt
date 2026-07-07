package io.webweavex.determinism

import java.util.Locale
import java.util.regex.Pattern

/**
 * Python `repr(float)` for doubles — the cross-language canonical float form.
 * Mirrors `io.webweavex.determinism.PyFloat` (Java): shortest round-tripping
 * decimal found by probing increasing precision (version independent), then
 * reformatted by Python's rules.
 */
object PyFloat {

    private val SCI: Pattern = Pattern.compile("^(\\d)(?:\\.(\\d+))?[eE]([+-]\\d+)$")

    @JvmStatic
    fun pyFloatRepr(x: Double): String {
        if (x.isNaN()) return "nan"
        if (x == Double.POSITIVE_INFINITY) return "inf"
        if (x == Double.NEGATIVE_INFINITY) return "-inf"
        if (x == Math.rint(x) && Math.abs(x) < 1e16) {
            // Integral magnitude < 1e16 -> "N.0" (Python keeps the sign of -0.0).
            val sign = if (java.lang.Double.doubleToRawLongBits(x) < 0) "-" else ""
            val magnitude = Math.abs(x).toLong()
            return "$sign$magnitude.0"
        }

        val sign = if (x < 0) "-" else ""
        val (lead, rest, expStr) = shortestScientific(Math.abs(x))
        val exp = expStr.toInt()

        if (exp < -4 || exp >= 16) {
            val mant = if (rest.isEmpty()) lead else "$lead.$rest"
            val esign = if (exp < 0) "-" else "+"
            val eabs = Math.abs(exp)
            val epad = (if (eabs < 10) "0" else "") + eabs
            return "$sign${mant}e$esign$epad"
        }

        val digits = lead + rest
        if (exp < 0) {
            return sign + "0." + "0".repeat(-exp - 1) + digits
        }
        if (digits.length <= exp + 1) {
            val padded = StringBuilder(digits)
            while (padded.length < exp + 1) padded.append('0')
            return "$sign$padded.0"
        }
        return sign + digits.substring(0, exp + 1) + "." + digits.substring(exp + 1)
    }

    /**
     * Returns (leadDigit, restDigits, exponent) for the shortest decimal that
     * round-trips to `a` (a > 0, finite, non-integral-or-huge).
     */
    private fun shortestScientific(a: Double): Triple<String, String, String> {
        var chosen: String? = null
        for (prec in 0..17) {
            val s = String.format(Locale.ROOT, "%.${prec}e", a)
            if (s.toDouble() == a) {
                chosen = s
                break
            }
        }
        if (chosen == null) {
            chosen = String.format(Locale.ROOT, "%.17e", a)
        }
        val m = SCI.matcher(chosen)
        require(m.matches()) { "unexpected scientific form: $chosen" }
        val lead = m.group(1)
        var rest = m.group(2) ?: ""
        // Trim trailing zeros from the fractional digits (Java pads to prec).
        var end = rest.length
        while (end > 0 && rest[end - 1] == '0') end--
        rest = rest.substring(0, end)
        return Triple(lead, rest, m.group(3))
    }
}
