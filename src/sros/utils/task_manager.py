from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


TaskState = str  # "queued" | "running" | "succeeded" | "failed"


@dataclass
class TaskRecord:
    id: str
    state: TaskState
    kind: str
    name: str
    args: Dict[str, Any]
    created_at: float
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    result: Any = None
    error: Optional[str] = None


Notifier = Callable[[Dict[str, Any]], None]


class TaskManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tasks: Dict[str, TaskRecord] = {}
        self._notifier: Optional[Notifier] = None

    def set_notifier(self, notifier: Optional[Notifier]) -> None:
        """Set an optional notifier called on task completion.

        The notifier must be fast and must not raise.
        """
        self._notifier = notifier

    def start(
        self,
        *,
        kind: str,
        name: str,
        args: Dict[str, Any],
        run: Callable[[], Any],
    ) -> TaskRecord:
        task_id = uuid.uuid4().hex
        record = TaskRecord(
            id=task_id,
            state="queued",
            kind=str(kind),
            name=str(name),
            args=dict(args or {}),
            created_at=time.time(),
        )

        with self._lock:
            self._tasks[task_id] = record

        def _runner() -> None:
            self._set_state(task_id, "running")
            try:
                value = run()
                self._set_result(task_id, value)
            except Exception as e:  # noqa: BLE001
                self._set_error(task_id, str(e))

        t = threading.Thread(target=_runner, name=f"sros-task-{kind}-{name}-{task_id[:8]}", daemon=True)
        t.start()
        return record

    def get(self, task_id: str) -> Optional[TaskRecord]:
        with self._lock:
            return self._tasks.get(task_id)

    def list(self) -> Dict[str, TaskRecord]:
        with self._lock:
            return dict(self._tasks)

    def _set_state(self, task_id: str, state: TaskState) -> None:
        with self._lock:
            rec = self._tasks.get(task_id)
            if rec is None:
                return
            rec.state = state
            if state == "running":
                rec.started_at = time.time()

    def _set_result(self, task_id: str, result: Any) -> None:
        payload: Optional[Dict[str, Any]] = None
        with self._lock:
            rec = self._tasks.get(task_id)
            if rec is None:
                return
            rec.state = "succeeded"
            rec.finished_at = time.time()
            rec.result = result
            payload = {
                "event": "task.completed",
                "task": self._as_dict(rec),
            }

        self._notify(payload)

    def _set_error(self, task_id: str, error: str) -> None:
        payload: Optional[Dict[str, Any]] = None
        with self._lock:
            rec = self._tasks.get(task_id)
            if rec is None:
                return
            rec.state = "failed"
            rec.finished_at = time.time()
            rec.error = error
            payload = {
                "event": "task.completed",
                "task": self._as_dict(rec),
            }

        self._notify(payload)

    def _notify(self, payload: Optional[Dict[str, Any]]) -> None:
        notifier = self._notifier
        if notifier is None or payload is None:
            return
        try:
            notifier(payload)
        except Exception:
            # Never allow notification failure to break task completion.
            return

    @staticmethod
    def _as_dict(rec: TaskRecord) -> Dict[str, Any]:
        return {
            "id": rec.id,
            "state": rec.state,
            "kind": rec.kind,
            "name": rec.name,
            "args": rec.args,
            "created_at": rec.created_at,
            "started_at": rec.started_at,
            "finished_at": rec.finished_at,
            "result": rec.result,
            "error": rec.error,
        }


_GLOBAL_TASK_MANAGER: Optional[TaskManager] = None


def get_task_manager() -> TaskManager:
    global _GLOBAL_TASK_MANAGER
    if _GLOBAL_TASK_MANAGER is None:
        _GLOBAL_TASK_MANAGER = TaskManager()
    return _GLOBAL_TASK_MANAGER
