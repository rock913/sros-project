from __future__ import annotations

from typing import Any, Dict, Optional

from sros.utils.task_manager import get_task_manager


class TasksHandler:
    """Minimal long-running task API.

    Tasks run in-process (threaded). When invoked through the gateway, completion
    may be broadcast via SSE as a JSON-RPC notification.
    """

    def run_plugin_async(self, plugin: str, args: Dict[str, Any]) -> Dict[str, Any]:
        from sros.utils.plugin_loader import run_plugin

        tm = get_task_manager()
        rec = tm.start(
            kind="plugin",
            name=str(plugin),
            args=dict(args or {}),
            run=lambda: run_plugin(plugin, dict(args or {})),
        )
        return {"ok": True, "task_id": rec.id}

    def get_task(self, task_id: str) -> Dict[str, Any]:
        tm = get_task_manager()
        rec = tm.get(str(task_id))
        if rec is None:
            return {"ok": False, "error": "Task not found", "task_id": str(task_id)}
        return {"ok": True, "task": tm._as_dict(rec)}

    def list_tasks(self) -> Dict[str, Any]:
        tm = get_task_manager()
        tasks = [tm._as_dict(t) for t in tm.list().values()]
        # Most recent first
        tasks.sort(key=lambda t: float(t.get("created_at") or 0), reverse=True)
        return {"ok": True, "tasks": tasks, "count": len(tasks)}

    def wait_task(self, task_id: str, timeout_s: float = 30.0, poll_interval_s: float = 0.05) -> Dict[str, Any]:
        import time

        deadline = time.time() + float(timeout_s)
        while time.time() < deadline:
            got = self.get_task(task_id)
            if not got.get("ok"):
                return got
            state = (got.get("task") or {}).get("state")
            if state in {"succeeded", "failed"}:
                return got
            time.sleep(float(poll_interval_s))
        return {"ok": False, "error": "Timeout", "task_id": str(task_id)}
