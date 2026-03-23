package com.webweavex

object Config {
    const val CHUNK_SIZE = 500
    const val CHUNK_OVERLAP = 50
    const val TOP_ENTITIES_COUNT = 10
    
    val EMAIL_REGEX = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}".toRegex()
    val URL_REGEX = "https?://[^\\s<>\"']+".toRegex()
    val NUMBER_REGEX = "\\b\\d+(?:\\.\\d+)?\\b".toRegex()
    val PHONE_REGEX = "\\+?[0-9]{1,4}?[-.\\s]?\\(?[0-9]{1,4}\\)?[-.\\s]?[0-9]{1,4}[-.\\s]?[0-9]{1,9}".toRegex()
    val CAPITALIZED_REGEX = "\\b[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*\\b".toRegex()
}
