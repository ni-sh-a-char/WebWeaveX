package io.webweavex.workflow

import io.webweavex.fingerprint.Fingerprint

data class WorkflowStep(
    val name: String,
    val action: (Map<String, Any>) -> Map<String, Any>,
    val dependsOn: List<String> = emptyList()
)

data class WorkflowResult(
    val steps: Map<String, Map<String, Any>>,
    val output: Map<String, Any>,
    val fingerprint: String,
    val success: Boolean
)

object WorkflowEngine {
    fun execute(steps: List<WorkflowStep>, input: Map<String, Any>): WorkflowResult {
        val results = mutableMapOf<String, Map<String, Any>>()
        val completed = mutableSetOf<String>()
        var current = input

        // Simple sequential execution (topological order implied by dependsOn)
        for (step in steps) {
            if (step.dependsOn.all { it in completed }) {
                val result = step.action(current)
                results[step.name] = result
                completed.add(step.name)
                current = result
            }
        }

        val fp = Fingerprint.compute(results)
        return WorkflowResult(results, current, fp, completed.size == steps.size)
    }
}
