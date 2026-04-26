"""
Extractor Registry for WebWeaveX
Allows pluggable extractors
"""

_registry = {}


def register_extractor(name, extractor_cls):
    """Register an extractor by name and class."""
    _registry[name] = extractor_cls


def get_extractor(name):
    """Get an extractor by name."""
    return _registry.get(name)


def get_registry_copy():
    return dict(_registry)

def get_extractors():
    """Get all registered extractors as instances."""
    return [cls() for cls in get_registry_copy().values()]


def list_extractors():
    """List all registered extractor names."""
    return list(_registry.keys())


def clear_registry():
    """Clear all registered extractors."""
    _registry.clear()


# Default registrations will be done by the API initialization
__all__ = ["register_extractor", "get_extractor", "get_extractors", "list_extractors", "clear_registry"]