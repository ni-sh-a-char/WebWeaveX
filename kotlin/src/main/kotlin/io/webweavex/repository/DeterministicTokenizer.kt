package io.webweavex.repository

object DeterministicTokenizer {
    fun tokenize(text: String): List<String> {
        if (text.isEmpty()) return emptyList()
        val tokens = mutableListOf<String>()
        val current = StringBuilder()
        
        for (c in text) {
            when {
                c.isLetterOrDigit() || c == '_' -> current.append(c.lowercaseChar())
                current.isNotEmpty() -> {
                    tokens.add(current.toString())
                    current.clear()
                }
            }
        }
        if (current.isNotEmpty()) tokens.add(current.toString())
        return tokens.distinct()
    }
    
    fun tokenizeCamelCase(text: String): List<String> {
        if (text.isEmpty()) return emptyList()
        val tokens = mutableListOf<String>()
        val current = StringBuilder()
        var prevWasUpper = false
        
        for (c in text) {
            when {
                c.isUpperCase() -> {
                    if (current.isNotEmpty()) {
                        tokens.add(current.toString().lowercase())
                        current.clear()
                    }
                    current.append(c.lowercaseChar())
                    prevWasUpper = true
                }
                c.isLetterOrDigit() -> {
                    if (prevWasUpper && current.isNotEmpty() && !c.isUpperCase()) {
                        tokens.add(current.toString().lowercase())
                        current.clear()
                    }
                    current.append(c)
                    prevWasUpper = false
                }
                else -> {
                    if (current.isNotEmpty()) {
                        tokens.add(current.toString().lowercase())
                        current.clear()
                    }
                    prevWasUpper = false
                }
            }
        }
        if (current.isNotEmpty()) tokens.add(current.toString().lowercase())
        return tokens.distinct()
    }
}
