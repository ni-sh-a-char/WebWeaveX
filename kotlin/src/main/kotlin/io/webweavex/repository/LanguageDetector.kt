package io.webweavex.repository

import java.io.File

object LanguageDetector {
    private val extMap = mapOf(
        "kt" to "Kotlin", "java" to "Java", "py" to "Python", "js" to "JavaScript",
        "ts" to "TypeScript", "dart" to "Dart", "go" to "Go", "rs" to "Rust",
        "c" to "C", "cpp" to "C++", "cs" to "C#", "swift" to "Swift",
        "php" to "PHP", "rb" to "Ruby", "html" to "HTML", "css" to "CSS",
        "json" to "JSON", "xml" to "XML", "yaml" to "YAML", "yml" to "YAML",
        "md" to "Markdown", "toml" to "TOML", "gradle" to "Gradle",
        "xml" to "Maven", "dockerfile" to "Docker"
    )

    fun detect(file: File): String {
        val ext = file.extension.lowercase()
        return extMap[ext] ?: "Unknown"
    }
}
