from __future__ import annotations

import time

from sros.utils.task_manager import get_task_manager


def test_task_manager_success():
    tm = get_task_manager()

    rec = tm.start(kind="unit", name="ok", args={"x": 1}, run=lambda: {"y": 2})
    assert rec.id

    deadline = time.time() + 2
    while time.time() < deadline:
        got = tm.get(rec.id)
        assert got is not None
        if got.state in {"succeeded", "failed"}:
            break
        time.sleep(0.01)

    got = tm.get(rec.id)
    assert got is not None
    assert got.state == "succeeded"
    assert got.result == {"y": 2}
    assert got.error is None


def test_task_manager_failure():
    tm = get_task_manager()

    def boom():
        raise RuntimeError("nope")

    rec = tm.start(kind="unit", name="boom", args={}, run=boom)

    deadline = time.time() + 2
    while time.time() < deadline:
        got = tm.get(rec.id)
        assert got is not None
        if got.state in {"succeeded", "failed"}:
            break
        time.sleep(0.01)

    got = tm.get(rec.id)
    assert got is not None
    assert got.state == "failed"
    assert isinstance(got.error, str) and "nope" in got.error
