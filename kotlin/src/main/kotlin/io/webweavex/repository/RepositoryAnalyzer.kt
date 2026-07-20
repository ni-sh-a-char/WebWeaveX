package io.webweavex.repository

data class RepositoryAnalysis(
    val files: List<String> = emptyList(),
    val languages: Map<String, Int> = emptyMap(),
    val dependencies: List<String> = emptyList(),
    val apiRoutes: List<String> = emptyList(),
    val fingerprint: String = ""
)

object RepositoryAnalyzer {
    fun analyze(text: String, sourceUrl: String = ""): RepositoryAnalysis {
        val files = Regex("[A-Za-z0-9_./-]+\\.(?:py|js|ts|dart|java|kt|go|rs)").
            findAll(text).map { it.value }.toSortedSet().toList()
        val extCounts = files.groupingBy { it.substringAfterLast(".") }.eachCount()
        val deps = Regex("(?:import|from)\\s+([A-Za-z0-9_.]+)").findAll(text).
            map { it.groupValues[1] }.toSortedSet().toList()
        val routes = Regex("(?:GET|POST|PUT|PATCH|DELETE)\\s+(/[A-Za-z0-9_/{}:]+)").
            findAll(text).map { it.groupValues[1] }.toSortedSet().toList()
        
        return RepositoryAnalysis(
            files = files,
            languages = extCounts,
            dependencies = deps,
            apiRoutes = routes,
            fingerprint = io.webweavex.fingerprint.Fingerprint.compute(mapOf("files" to files, "deps" to deps))
        )
    }
}
