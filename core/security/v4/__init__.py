from core.security.remote_target import is_safe_remote_target
from core.security.resource_budget import enforce_resource_budget

enforce_resource_budget_v4 = enforce_resource_budget

__all__ = ["is_safe_remote_target", "enforce_resource_budget", "enforce_resource_budget_v4"]
