"""
WebWeaveX Intelligence Engine

Optional AI execution layer with fail-safe design.
Note: This module only loads AI providers when explicitly requested.
"""

import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Prompt builder for different tasks
def build_prompt(task: str, data: Dict[str, Any]) -> str:
    """Build prompts for different tasks"""

    structured = data.get("structured_data", {})
    human = data.get("human_readable", "")
    text = structured.get("text", human)
    summary = structured.get("summary", "")

    prompts = {
        "summarize": f"Summarize this content concisely:\n{summary or text[:1000]}",
        "explain": f"Explain this clearly:\n{text[:1000]}",
        "generate_code": f"Generate working Python code from:\n{structured.get('files', [])}\n{text[:500]}",
        "analyze": f"Analyze this content:\n{text[:1000]}",
        "extract_entities": f"Extract entities, actions, and relationships from:\n{text[:1000]}"
    }

    return prompts.get(task, text[:500])


def run_ai_task(data: Dict[str, Any], task: str, provider_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Run AI task with specified provider"""

    if provider_name == "mock":
        return _mock_ai_response(task, data)

    try:
        provider = _load_provider(provider_name)
    except ImportError as e:
        logger.warning(f"Provider {provider_name} not available: {e}")
        return _fallback_to_rule(task, data)

    try:
        prompt = build_prompt(task, data)
        response = provider.generate(prompt, config)

        return {
            "ai_output": response,
            "task": task,
            "provider": provider_name,
            "success": True
        }
    except Exception as e:
        logger.warning(f"AI task failed: {e}")
        return _fallback_to_rule(task, data)


def _fallback_to_rule(task: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback to rule-based task when AI fails"""

    task_map = {
        "summarize": lambda d: {"summary": d.get("human_readable", "")[:200]},
        "explain": lambda d: {"explanation": "Content analyzed based on structure"},
        "analyze": lambda d: {"analysis": "Rule-based analysis complete"},
    }

    func = task_map.get(task, lambda d: {"result": "completed"})
    return {"ai_output": func(data), "task": task, "provider": "rule-based", "success": False, "fallback": True}


def _mock_ai_response(task: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Mock AI response for testing"""

    responses = {
        "summarize": "This code provides a calculator app implementation.",
        "explain": "This is a functional application that performs calculations.",
        "analyze": "The code structure shows good organization.",
        "extract_entities": "Main entity: Calculator, Actions: calculate, display"
    }

    return {
        "ai_output": responses.get(task, "Task completed"),
        "task": task,
        "provider": "mock",
        "success": True
    }


def _load_provider(provider_name: str):
    """Lazy load AI provider"""

    provider_map = {
        "openai": "openai",
        "ollama": "ollama",
        "groq": "groq",
        "anthropic": "anthropic",
    }

    if provider_name not in provider_map:
        raise ValueError(f"Unknown provider: {provider_name}")

    # Try to import provider module
    try:
        module_name = f"webweavex.plugins.providers.{provider_name}"
        import importlib
        return importlib.import_module(module_name)
    except ImportError:
        raise ImportError(f"Provider {provider_name} not installed")


# Enhanced task execution with AI support
def enhanced_task_runner(data: Dict[str, Any], task: str, provider: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run task with optional AI provider"""

    if config is None:
        config = {}

    # If no provider, use rule-based
    if not provider:
        from webweavex.plugins import run_task
        return run_task(data, task)

    # Try AI task
    try:
        return run_ai_task(data, task, provider, config)
    except Exception as e:
        logger.warning(f"AI execution failed: {e}")
        # Fallback to rule-based
        from webweavex.plugins import run_task
        return run_task(data, task)