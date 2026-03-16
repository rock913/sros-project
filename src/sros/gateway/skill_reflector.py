from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class SkillCallResult:
    ok: bool
    value: Any


class SkillReflector:
    """In-process reflection to skills RPC.

    This keeps the gateway thin (no business logic in gateway) while avoiding
    the large latency of spawning a new Python interpreter per tool call.
    """

    def call(self, tool_name: str, arguments: Dict[str, Any]) -> SkillCallResult:
        from sros.skills.rpc import dispatch_tool

        try:
            value = dispatch_tool(tool_name, arguments or {})
            return SkillCallResult(ok=True, value=value)
        except Exception as e:
            return SkillCallResult(ok=False, value={"ok": False, "error": str(e), "tool": tool_name})
