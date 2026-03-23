package com.webweavex

data class Entity(
    val type: String,
    val value: String
) {
    fun toMap(): Map<String, String> = mapOf("type" to type, "value" to value)
}

class Entities {
    fun extract(text: String): List<Entity> {
        if (text.isEmpty()) return emptyList()

        val entities = mutableListOf<Entity>()
        val seen = mutableSetOf<String>()

        extractPattern(text, Config.EMAIL_REGEX, "email", entities, seen)
        extractPattern(text, Config.URL_REGEX, "url", entities, seen)
        extractPattern(text, Config.NUMBER_REGEX, "number", entities, seen)
        extractPattern(text, Config.PHONE_REGEX, "phone", entities, seen)
        extractPattern(text, Config.CAPITALIZED_REGEX, "capitalized", entities, seen)

        return entities
    }

    private fun extractPattern(
        text: String,
        pattern: Regex,
        type: String,
        entities: MutableList<Entity>,
        seen: MutableSet<String>
    ) {
        pattern.findAll(text).forEach { match ->
            val value = match.value
            val key = "$type:$value"
            if (!seen.contains(key)) {
                seen.add(key)
                entities.add(Entity(type, value))
            }
        }
    }
}
