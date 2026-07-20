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
    val success: Boolean,
    val executionOrder: List<String>,
    val diagnostics: List<String> = emptyList()
)

object WorkflowEngine {
    fun execute(steps: List<WorkflowStep>, input: Map<String, Any>): WorkflowResult {
        val diagnostics = mutableListOf<String>()
        
        // Cycle detection
        val adj = steps.associate { it.name to it.dependsOn }
        if (hasCycle(adj)) {
            return WorkflowResult(emptyMap(), input, "", false, emptyList(), listOf("Cycle detected in workflow"))
        }
        
        // Duplicate detection
        val names = steps.map { it.name }
        val dupes = names.groupBy { it }.filter { it.value.size > 1 }.keys
        if (dupes.isNotEmpty()) {
            return WorkflowResult(emptyMap(), input, "", false, emptyList(), listOf("Duplicate steps: $dupes"))
        }
        
        // Topological sort
        val orderSteps = topologicalSort(steps); val order = orderSteps.map { it.name }
        val results = mutableMapOf<String, Map<String, Any>>()
        var current = input
        
        for (step in orderSteps) {
            val result = step.action(current)
            results[step.name] = result
            current = result
        }
        
        val fp = Fingerprint.compute(results)
        return WorkflowResult(results, current, fp, true, order)
    }
    
    private fun hasCycle(adj: Map<String, List<String>>): Boolean {
        val visited = mutableSetOf<String>()
        val stack = mutableSetOf<String>()
        fun dfs(node: String): Boolean {
            if (node in stack) return true
            if (node in visited) return false
            stack.add(node)
            for (dep in adj[node] ?: emptyList()) {
                if (dfs(dep)) return true
            }
            stack.remove(node)
            visited.add(node)
            return false
        }
        return adj.keys.any { dfs(it) }
    }
    
    private fun topologicalSort(steps: List<WorkflowStep>): List<WorkflowStep> {
        val adj = steps.associate { it.name to it.dependsOn }
        val inDegree = mutableMapOf<String, Int>()
        steps.forEach { inDegree[it.name] = 0 }
        adj.values.flatten().forEach { inDegree[it] = (inDegree[it] ?: 0) + 1 }
        
        val queue = ArrayDeque<String>()
        steps.forEach { if ((inDegree[it.name] ?: 0) == 0) queue.add(it.name) }
        
        val order = mutableListOf<String>()
        while (queue.isNotEmpty()) {
            val node = queue.removeFirst()
            order.add(node)
            for (dep in adj.keys.filter { adj[it]!!.contains(node) }) {
                inDegree[dep] = inDegree[dep]!! - 1
                if (inDegree[dep] == 0) queue.add(dep)
            }
        }
        
        return order.map { name -> steps.first { it.name == name } }
    }
}
