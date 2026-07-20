package io.webweavex.repository

import java.io.File

data class RepositoryFile(
    val path: String,
    val language: String,
    val size: Long,
    val extension: String
)

object RepositoryScanner {
    fun scan(root: File): List<RepositoryFile> {
        if (!root.exists()) return emptyList()
        return root.walkTopDown()
            .filter { it.isFile && !it.path.contains(".git") && !it.path.contains("node_modules") && !it.path.contains("build") }
            .map { RepositoryFile(it.path, LanguageDetector.detect(it), it.length(), it.extension) }
            .toList()
            .sortedBy { it.path }
    }
}
