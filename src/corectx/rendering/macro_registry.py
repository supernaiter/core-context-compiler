from __future__ import annotations

DEFAULT_MACROS = {
    "P0": "ja+direct+sepEGU+noUnsourced",
}


class MacroRegistry:
    def __init__(self, macros: dict[str, str] | None = None) -> None:
        self.macros = dict(DEFAULT_MACROS)
        if macros:
            self.macros.update(macros)

    def get(self, key: str) -> str:
        return self.macros[key]

    def render_definitions(self, used: set[str] | None = None) -> list[str]:
        keys = sorted(used or set(self.macros))
        return [f"{key}={self.macros[key]}" for key in keys if key in self.macros]
