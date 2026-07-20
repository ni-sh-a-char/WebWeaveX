package io.webweavex.repository

import java.io.File

object LanguageDetector {
    private val extMap = mapOf(
        "kt" to "Kotlin", "kts" to "Kotlin", "java" to "Java",
        "py" to "Python", "js" to "JavaScript", "ts" to "TypeScript",
        "tsx" to "TypeScript", "dart" to "Dart", "go" to "Go",
        "rs" to "Rust", "c" to "C", "cpp" to "C++", "h" to "C/C++",
        "cs" to "C#", "swift" to "Swift", "php" to "PHP", "rb" to "Ruby",
        "html" to "HTML", "css" to "CSS", "json" to "JSON", "xml" to "XML",
        "yaml" to "YAML", "yml" to "YAML", "md" to "Markdown", "toml" to "TOML",
        "gradle" to "Gradle", "groovy" to "Groovy", "scala" to "Scala"
    )

    private val manifestMap = mapOf(
        "build.gradle" to "Gradle", "build.gradle.kts" to "Kotlin",
        "pom.xml" to "Maven", "Cargo.toml" to "Rust", "go.mod" to "Go",
        "package.json" to "Node.js", "requirements.txt" to "Python",
        "pyproject.toml" to "Python", "setup.py" to "Python",
        "pubspec.yaml" to "Dart", "composer.json" to "PHP",
        "Gemfile" to "Ruby", "Podfile" to "Swift",
        "AndroidManifest.xml" to "Android",
        "Dockerfile" to "Docker", "docker-compose.yml" to "Docker",
        ".github/workflows" to "GitHub Actions"
    )

    fun detect(file: File): String {
        val name = file.name
        val ext = file.extension.lowercase()
        return extMap[ext] ?: manifestMap.entries.find { name.contains(it.key) }?.value ?: "Unknown"
    }

    fun detectProject(root: File): String {
        val manifests = root.listFiles()?.map { it.name } ?: emptyList()
        return when {
            manifests.any { it == "build.gradle.kts" || it == "build.gradle" } -> "Gradle"
            manifests.any { it == "pom.xml" } -> "Maven"
            manifests.any { it == "Cargo.toml" } -> "Rust"
            manifests.any { it == "go.mod" } -> "Go"
            manifests.any { it == "package.json" } -> "Node.js"
            manifests.any { it == "pyproject.toml" || it == "requirements.txt" } -> "Python"
            manifests.any { it == "pubspec.yaml" } -> "Dart"
            else -> "Unknown"
        }
    }
}
