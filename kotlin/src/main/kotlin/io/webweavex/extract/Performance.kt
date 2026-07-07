package io.webweavex.extract

/**
 * Performance enrichment stage (self-contained tier-0 functions). Ports:
 * `core.performance.streaming_engine.{parser_pool,lazy_extract}`,
 * `chunk_budget_engine.budgeted_chunks`, `memory_budget_engine.memory_budget`,
 * `security.hardening.timeout_guard_engine.timeout_guard`.
 *
 * Mirrors `io.webweavex.extract.Performance` (Java) line for line — the
 * proof-of-concept stage for K0. Python/Java `len`/slicing on text is by code
 * point, so chunking and preview truncation use `codePointCount`/
 * `offsetByCodePoints`, never UTF-16 `.length`/`.substring` indices directly.
 *
 * NOTE: stream_parse/incremental_parse depend on ParserRegistry.parse (Parser
 * stage, not yet ported).
 */
object Performance {

    @JvmStatic
    fun parserPool(): Map<String, Any> {
        val out = LinkedHashMap<String, Any>()
        out["size"] = 1
        out["deterministic"] = true
        return out
    }

    // Python raw[i:i+size] slices by code point; step by size code points.
    @JvmStatic
    @JvmOverloads
    fun budgetedChunks(text: String?, chunkSize: Int = 50_000): List<String> {
        val raw = text ?: ""
        val size = maxOf(1024, chunkSize)
        val out = ArrayList<String>()
        val cp = raw.codePointCount(0, raw.length)
        var i = 0
        while (i < cp) {
            val start = raw.offsetByCodePoints(0, i)
            val end = raw.offsetByCodePoints(0, minOf(i + size, cp))
            out.add(raw.substring(start, end))
            i += size
        }
        if (out.isEmpty()) out.add("")
        return out
    }

    @JvmStatic
    @JvmOverloads
    fun memoryBudget(bytesUsed: Long, limit: Long = 1_000_000_000L): Map<String, Any> {
        val used = maxOf(0L, bytesUsed)
        val lim = maxOf(1L, limit)
        val out = LinkedHashMap<String, Any>()
        out["ok"] = used <= lim
        out["bytes_used"] = used
        out["limit"] = lim
        return out
    }

    @JvmStatic
    @JvmOverloads
    fun timeoutGuard(elapsedMs: Double, limitMs: Double = 10_000.0): Map<String, Any> {
        val out = LinkedHashMap<String, Any>()
        out["ok"] = elapsedMs <= limitMs
        return out
    }

    @JvmStatic
    fun lazyExtract(text: String?): Map<String, Any> {
        val raw = text ?: ""
        val cp = raw.codePointCount(0, raw.length)
        val preview = raw.substring(0, raw.offsetByCodePoints(0, minOf(200, cp)))
        val out = LinkedHashMap<String, Any>()
        out["length"] = cp
        out["preview"] = preview
        return out
    }
}
