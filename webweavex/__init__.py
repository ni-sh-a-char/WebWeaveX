"""
WebWeaveX - Universal Extraction Library

Core: run() function
Optional Plugin System: Intelligence Layer
"""

from webweavex.api.api import run
from webweavex.api.schemas import validate_request, validate_response

__version__ = "1.0.5"

# Plugin system exports
from webweavex.plugins import (
    Plugin,
    register_plugin,
    get_plugin,
    list_plugins,
    execute_plugins,
    run_task,
    build_graph,
    generate_actions,
    load_provider,
    TASK_REGISTRY,
)

__all__ = [
    "run",
    "validate_request",
    "validate_response",
    "Plugin",
    "register_plugin",
    "get_plugin",
    "list_plugins",
    "execute_plugins",
    "run_task",
    "build_graph",
    "generate_actions",
    "load_provider",
    "TASK_REGISTRY",
    "__version__",
]