package com.webweavex

data class Chunk(
    val text: String,
    val index: Int,
    val start: Int,
    val end: Int
) {
    fun toMap(): Map<String, Any> = mapOf("text" to text, "index" to index, "start" to start, "end" to end)
}

class Chunker {
    private val size = Config.CHUNK_SIZE
    private val overlap = Config.CHUNK_OVERLAP

    fun chunk(text: String): List<Chunk> {
        if (text.isEmpty()) return emptyList()

        val chunks = mutableListOf<Chunk>()
        var start = 0
        var index = 0

        while (start < text.length) {
            var end = start + size

            if (end < text.length) {
                end = findWordBoundary(text, end)
            }

            val chunkText = text.substring(start, minOf(end, text.length))
            if (chunkText.isNotBlank()) {
                chunks.add(Chunk(chunkText, index, start, end))
                index++
            }

            start = end - overlap
            if (start < 0) start = 0
        }

        return chunks
    }

    private fun findWordBoundary(text: String, position: Int): Int {
        if (position >= text.length) return position

        for (i in position downTo maxOf(0, position - 50)) {
            val c = text[i]
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
                return i
            }
        }

        return position
    }
}
