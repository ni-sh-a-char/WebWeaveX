"""
WebWeaveX Plugin System

Simple, extensible plugin architecture for WebWeaveX.
All plugins are optional and fail-safe.
"""

from typing import Dict, Any, Optional
import logging
import traceback

logger = logging.getLogger(__name__)

# Plugin Registry
PLUGIN_REGISTRY: Dict[str, Any] = {}


class Plugin:
    """Base plugin class"""

    name: str = "base"
    version: str = "1.0.0"

    def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute plugin on data"""
        return data


def register_plugin(name: str, plugin: Plugin) -> None:
    """Register a plugin"""
    PLUGIN_REGISTRY[name] = plugin


def get_plugin(name: str) -> Optional[Plugin]:
    """Get a registered plugin"""
    return PLUGIN_REGISTRY.get(name)


def list_plugins() -> list:
    """List all registered plugins"""
    return list(PLUGIN_REGISTRY.keys())


def execute_plugins(data: Dict[str, Any], plugins: list, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute multiple plugins in sequence"""
    if config is None:
        config = {}

    result = data
    for plugin_name in plugins:
        try:
            plugin = get_plugin(plugin_name)
            if plugin:
                result = plugin.execute(result, config.get(plugin_name, {}))
        except Exception:
            logger.warning(f"Plugin {plugin_name} failed: {traceback.format_exc()}")
            # Fail-safe: continue with base result

    return result


# Base task functions (no AI required)
def task_summarize(data: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based summarization"""
    text = data.get("structured_data", {}).get("text", "")
    if len(text) > 200:
        return {"summary": text[:200] + "..."}
    return {"summary": text}


def task_explain(data: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based explanation"""
    return {"explanation": "Content analyzed based on structure"}


def task_analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based analysis"""
    return {"analysis": {"has_structure": bool(data.get("structured_data")), "confidence": data.get("confidence", 0)}}


# Task registry (rule-based tasks)
TASK_REGISTRY = {
    "summarize": task_summarize,
    "explain": task_explain,
    "analyze": task_analyze,
}


def run_task(data: Dict[str, Any], task: str, provider: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run a task with optional AI provider"""

    if config is None:
        config = {}

    # Unknown task
    if task not in TASK_REGISTRY:
        return {"error": f"Unknown task: {task}"}

    # If provider specified, use AI engine
    if provider and provider != "rule":
        try:
            from webweavex.plugins.intelligence_engine import run_ai_task
            return run_ai_task(data, task, provider, config)
        except Exception as e:
            logger.warning(f"AI task failed, using rule-based: {e}")

    # Fallback to rule-based task
    task_func = TASK_REGISTRY[task]
    return task_func(data)


# Knowledge graph builder (lightweight)
def build_graph(data: Dict[str, Any]) -> Dict[str, Any]:
    """Build simple knowledge graph without external dependencies"""

    nodes = []
    edges = []
    seen_ids = set()

    structured = data.get("structured_data", {})
    semantics = structured.get("semantics", {}) if structured else {}

    entities = semantics.get("entities", [])
    actions = semantics.get("actions", [])
    relationships = semantics.get("relationships", [])

    for entity in entities:
        entity_id = entity.get("text", "")
        if entity_id and entity_id not in seen_ids:
            nodes.append({
                "id": entity_id,
                "type": "entity",
                "label": entity_id,
                "category": entity.get("category", "unknown")
            })
            seen_ids.add(entity_id)

    for action in actions:
        action_id = action.get("text", "")
        if action_id and action_id not in seen_ids:
            nodes.append({
                "id": action_id,
                "type": "action",
                "label": action_id,
                "category": action.get("category", "unknown")
            })
            seen_ids.add(action_id)

    for rel in relationships:
        from_node = rel.get("from", "")
        to_node = rel.get("to", "")
        rel_type = rel.get("type", "relates_to")

        if from_node and to_node:
            edges.append({
                "from": from_node,
                "to": to_node,
                "relation": rel_type
            })
        elif from_node:
            edges.append({
                "from": from_node,
                "to": rel.get("action", "acts"),
                "relation": "performs"
            })

    for key, value in structured.items():
        if key == "semantics":
            continue
        if isinstance(value, str) and value and value not in seen_ids:
            nodes.append({"id": key, "type": "attribute", "label": value})
            seen_ids.add(value)

    for i, node in enumerate(nodes):
        if i > 0:
            edges.append({"from": nodes[i-1]["id"], "to": node["id"], "relation": "follows"})

    return {
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges)
    }


# Action generator (rule-based with DAG)
def generate_actions(data: Dict[str, Any]) -> list:
    """Generate actions based on data and semantics with dependencies"""
    import sys

    actions = []
    structured = data.get("structured_data", {})
    semantics = structured.get("semantics", {}) if structured else {}
    reasoning = structured.get("reasoning", {}) if structured else {}
    entities = semantics.get("entities", [])
    action_pairs = semantics.get("action_pairs", [])
    all_actions = semantics.get("actions", [])
    approach = reasoning.get("approach", [])

    action_id = 1

    if approach:
        approach_to_action = {
            "install": "install_dependencies",
            "build": "create_project", 
            "run": "run_command",
            "deploy": "deploy_service",
            "verify": "validate"
        }

        for i, step in enumerate(approach):
            if step in approach_to_action:
                action_item = {
                    "id": action_id,
                    "type": approach_to_action[step],
                    "depends_on": [action_id - 1] if i > 0 else []
                }
                if step == "install":
                    action_item["items"] = [e.get("text", "") for e in entities[:3]]
                elif step == "build":
                    action_item["target"] = reasoning.get("strategy", "default")
                elif step == "run":
                    action_item["command"] = "python main.py"
                actions.append(action_item)
                action_id += 1

    for pair in action_pairs:
        action_type = pair.get("normalized_action", "")
        entity = pair.get("entity", "")

        if action_type in ["build", "create", "make"]:
            actions.append({
                "id": action_id,
                "type": "create_project",
                "target": entity,
                "depends_on": []
            })
        elif action_type == "install":
            actions.append({
                "id": action_id,
                "type": "install_dependencies",
                "items": [entity],
                "depends_on": []
            })
        elif action_type in ["execute", "run"]:
            actions.append({
                "id": action_id,
                "type": "run_command",
                "command": f"python {entity}.py",
                "depends_on": [action_id - 1] if action_id > 1 else []
            })
        elif action_type == "deploy":
            actions.append({
                "id": action_id,
                "type": "deploy_service",
                "target": entity,
                "depends_on": [action_id - 1] if action_id > 1 else []
            })
        action_id += 1

    files = data.get("reconstructed_project", [])
    for f in files:
        actions.append({
            "id": action_id,
            "type": "create_file",
            "path": f.get("path", "untitled"),
            "content": f.get("content", ""),
            "depends_on": []
        })
        action_id += 1

    if len(actions) < 3:
        base_steps = [
            ("create_project", "install_dependencies"),
            ("install_dependencies", "build_project"),
            ("build_project", "run_command")
        ]
        
        for step_type, step_name in base_steps:
            actions.append({
                "id": action_id,
                "type": step_type,
                "name": step_name,
                "depends_on": [action_id - 1] if action_id > 1 else []
            })
            action_id += 1

    return actions


# LLM Provider loader (lazy, no hardcoded dependencies)
def load_provider(provider_name: str) -> Any:
    """Dynamically load LLM provider"""

    provider_map = {
        "openai": "webweavex.plugins.providers.openai",
        "ollama": "webweavex.plugins.providers.ollama",
        "groq": "webweavex.plugins.providers.groq",
    }

    if provider_name not in provider_map:
        raise ValueError(f"Unknown provider: {provider_name}")

    try:
        import importlib
        return importlib.import_module(provider_map[provider_name])
    except ImportError:
        raise ImportError(f"Provider {provider_name} not installed. Install with: pip install {provider_name}")


# Register context plugin
class ContextPlugin(Plugin):
    name = "context"

    def execute(self, data, config):
        context = config.get("context", {})
        if context and "structured_data" in data:
            data["structured_data"]["context"] = context
        return data


register_plugin("context", ContextPlugin())