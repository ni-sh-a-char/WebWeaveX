package io.webweavex

import java.io.File

/**
 * Minimal JSON reader — just enough to parse `vectors.json` / `java_index.json`
 * for [KotlinVerify]: objects, arrays, strings (with `\uXXXX` escapes), numbers
 * (integral -> Long, decimal/exponent -> Double), true/false/null.
 *
 * ponytail: hand-rolled instead of pulling in Jackson/Gson/kotlinx.serialization
 * — the harness only ever reads these two small, well-formed, machine-generated
 * files, so a ~100-line reader is less risk than a new build dependency. If a
 * later phase needs to *write* JSON or parse adversarial input, reach for a
 * real library instead of growing this one.
 */
private class MiniJsonParser(private val s: String) {
    private var i = 0

    fun parse(): Any? {
        skipWs()
        val v = parseValue()
        skipWs()
        return v
    }

    private fun skipWs() {
        while (i < s.length && s[i].isWhitespace()) i++
    }

    private fun parseValue(): Any? {
        skipWs()
        return when (s[i]) {
            '{' -> parseObject()
            '[' -> parseArray()
            '"' -> parseString()
            't' -> { expect("true"); true }
            'f' -> { expect("false"); false }
            'n' -> { expect("null"); null }
            else -> parseNumber()
        }
    }

    private fun expect(lit: String) {
        require(s.regionMatches(i, lit, 0, lit.length)) { "expected $lit at offset $i" }
        i += lit.length
    }

    private fun parseObject(): LinkedHashMap<String, Any?> {
        val out = LinkedHashMap<String, Any?>()
        i++ // {
        skipWs()
        if (i < s.length && s[i] == '}') { i++; return out }
        while (true) {
            skipWs()
            val key = parseString()
            skipWs()
            require(s[i] == ':') { "expected ':' at offset $i" }
            i++
            out[key] = parseValue()
            skipWs()
            if (i < s.length && s[i] == ',') { i++; continue }
            break
        }
        skipWs()
        require(s[i] == '}') { "expected '}' at offset $i" }
        i++
        return out
    }

    private fun parseArray(): ArrayList<Any?> {
        val out = ArrayList<Any?>()
        i++ // [
        skipWs()
        if (i < s.length && s[i] == ']') { i++; return out }
        while (true) {
            out.add(parseValue())
            skipWs()
            if (i < s.length && s[i] == ',') { i++; continue }
            break
        }
        skipWs()
        require(s[i] == ']') { "expected ']' at offset $i" }
        i++
        return out
    }

    private fun parseString(): String {
        require(s[i] == '"') { "expected '\"' at offset $i" }
        i++
        val sb = StringBuilder()
        while (s[i] != '"') {
            val c = s[i]
            if (c == '\\') {
                i++
                when (val esc = s[i]) {
                    '"' -> sb.append('"')
                    '\\' -> sb.append('\\')
                    '/' -> sb.append('/')
                    'b' -> sb.append('\b')
                    'f' -> sb.append('')
                    'n' -> sb.append('\n')
                    'r' -> sb.append('\r')
                    't' -> sb.append('\t')
                    'u' -> {
                        val hex = s.substring(i + 1, i + 5)
                        sb.append(hex.toInt(16).toChar())
                        i += 4
                    }
                    else -> throw IllegalArgumentException("bad escape \\$esc at offset $i")
                }
                i++
            } else {
                sb.append(c)
                i++
            }
        }
        i++ // closing quote
        return sb.toString()
    }

    private fun parseNumber(): Any {
        val start = i
        if (s[i] == '-') i++
        while (i < s.length && s[i].isDigit()) i++
        var isDouble = false
        if (i < s.length && s[i] == '.') {
            isDouble = true
            i++
            while (i < s.length && s[i].isDigit()) i++
        }
        if (i < s.length && (s[i] == 'e' || s[i] == 'E')) {
            isDouble = true
            i++
            if (i < s.length && (s[i] == '+' || s[i] == '-')) i++
            while (i < s.length && s[i].isDigit()) i++
        }
        val token = s.substring(start, i)
        return if (isDouble) token.toDouble() else token.toLong()
    }
}

fun parseJson(text: String): Any? = MiniJsonParser(text).parse()

fun parseJsonFile(path: String): Any? = parseJson(File(path).readText(Charsets.UTF_8))
