package io.webweavex.repository

import java.io.File

data class RepositorySummary(
    val totalFiles: Int,
    val languages: Map<String, Int>,
    val dependencies: List<String>,
    val apiRoutes: List<String>,
    val readmeSections: List<String>,
    val fingerprint: String
)

object RepositoryAnalyzerEngine {
    fun analyze(root: File): RepositorySummary {
        val files = RepositoryScanner.scan(root)
        val langCounts = files.groupBy { it.language }.mapValues { it.value.size }
        val readme = extractReadme(root)
        val deps = extractDependencies(root)
        val routes = extractApiRoutes(readme)
        val fp = io.webweavex.fingerprint.Fingerprint.compute(mapOf(
            "files" to files.map { it.path },
            "languages" to langCounts,
            "deps" to deps
        ))
        return RepositorySummary(
            totalFiles = files.size,
            languages = langCounts,
            dependencies = deps,
            apiRoutes = routes,
            readmeSections = readme,
            fingerprint = fp
        )
    }

    private fun extractReadme(root: File): List<String> {
        val readme = File(root, "README.md")
        if (!readme.exists()) return emptyList()
        return readme.readLines().filter { it.startsWith("#") }.map { it.trim() }
    }

    private fun extractDependencies(root: File): List<String> {
        val deps = mutableListOf<String>()
        val buildGradle = File(root, "build.gradle.kts")
        if (buildGradle.exists()) {
            Regex("implementation\\(\"([^\"]+)\"\\)").findAll(buildGradle.readText())
                .map { it.groupValues[1] }.forEach { deps.add(it) }
        }
        return deps.distinct().sorted()
    }

    private fun extractApiRoutes(readme: List<String>): List<String> {
        return readme.flatMap { Regex("(?:GET|POST|PUT|PATCH|DELETE)\\s+(/[^\\s]+)").findAll(it).map { m -> m.groupValues[1] } }.distinct().sorted()
    }
}
