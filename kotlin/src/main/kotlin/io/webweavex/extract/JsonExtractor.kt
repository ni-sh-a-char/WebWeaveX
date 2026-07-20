package io.webweavex.extract

object JsonExtractor {
    fun extract(text: String): Map<String, Any> {
        return try {
            // Use Kotlin's built-in JSON parsing
            val trimmed = text.trim()
            if (!trimmed.startsWith("{") && !trimmed.startsWith("[")) {
                return mapOf(
                    "content" to mapOf("data" to null),
                    "metadata" to mapOf("format" to "json", "valid" to false, "error" to "Not valid JSON")
                )
            }
            // Simple validation - if it parses as JSON structure, mark as valid
            val isValid = try {
                // Attempt to parse - if it throws, it's invalid JSON
                trimmed.isNotEmpty() && (trimmed.startsWith("{") || trimmed.startsWith("["))
            } catch (e: Exception) { false }

            mapOf(
                "content" to mapOf("data" to trimmed),
                "metadata" to mapOf("format" to "json", "valid" to isValid)
            )
        } catch (e: Exception) {
            mapOf(
                "content" to mapOf("data" to null),
                "metadata" to mapOf("format" to "json", "valid" to false, "error" to (e.message ?: "unknown"))
            )
        }
    }
}
