package com.webweavex

import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import java.io.File

object Validate {
    private val gson = GsonBuilder().setPrettyPrinting().create()
    private val webWeaveX = WebWeaveX()

    private const val TEST_CASES_PATH = "../../core/test_cases/test_cases.json"
    private const val OUTPUT_DIR = "../../test_output/kotlin"

    fun exportKotlinOutputs() {
        val testCasesFile = File(TEST_CASES_PATH)
        if (!testCasesFile.exists()) {
            println("Test cases not found: $TEST_CASES_PATH")
            System.exit(1)
        }

        val outputDir = File(OUTPUT_DIR)
        outputDir.mkdirs()

        val json = testCasesFile.readText()
        val testCases: List<Map<String, String>> = gson.fromJson(
            json,
            object : TypeToken<List<Map<String, String>>>() {}.type
        )

        println("Exporting Kotlin outputs...")
        println("=".repeat(50))

        val testCaseNames = mutableListOf<String>()

        for (tc in testCases) {
            val name = tc["name"] ?: continue
            val inputText = tc["input"] ?: ""

            println("Processing: $name")

            val result = webWeaveX.extract(inputText)
            val outputPath = File(OUTPUT_DIR, "$name.json")
            outputPath.writeText(gson.toJson(result))

            println("  Saved: ${outputPath.absolutePath}")
            testCaseNames.add(name)
        }

        println("=".repeat(50))
        println("Exported ${testCases.size} test cases to $OUTPUT_DIR")

        val manifestPath = File(OUTPUT_DIR, "manifest.json")
        val manifest = mapOf(
            "language" to "kotlin",
            "test_cases" to testCaseNames
        )
        manifestPath.writeText(gson.toJson(manifest))
        println("Manifest: ${manifestPath.absolutePath}")
    }
}

fun main() {
    Validate.exportKotlinOutputs()
}
