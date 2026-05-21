from __future__ import annotations

from typing import Any, Callable, Dict


class SemanticFunctionRegistry:
    def __init__(self) -> None:
        self._functions: Dict[str, Callable[..., Any]] = {}

    def register(
        self,
        name: str,
        fn: Callable[..., Any],
    ) -> None:

        self._functions[name] = fn

    def call(
        self,
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:

        return self._functions[name](
            *args,
            **kwargs,
        )
