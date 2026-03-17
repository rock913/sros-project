from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


PID_FILE_RELATIVE = Path(".sros") / "gateway.pid"


@dataclass(frozen=True)
class PortOwner:
    pid: Optional[int]
    name: Optional[str]


def pid_file_path(workspace_dir: str | Path) -> Path:
    return Path(workspace_dir).expanduser().resolve() / PID_FILE_RELATIVE


def read_pid_file(workspace_dir: str | Path) -> Optional[Dict[str, Any]]:
    path = pid_file_path(workspace_dir)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        return data
    except Exception:
        return None


def write_pid_file(workspace_dir: str | Path, pid: int, port: int) -> Optional[Path]:
    try:
        workspace = Path(workspace_dir).expanduser().resolve()
        path = workspace / PID_FILE_RELATIVE
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "pid": int(pid),
            "port": int(port),
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
    except Exception:
        return None


def remove_pid_file(workspace_dir: str | Path) -> None:
    try:
        path = pid_file_path(workspace_dir)
        path.unlink(missing_ok=True)
    except Exception:
        return


def is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False

    try:
        import psutil  # type: ignore

        return bool(psutil.pid_exists(pid))
    except Exception:
        # Fallback: POSIX-only best-effort
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False


def cleanup_zombie_pid_file(workspace_dir: str | Path) -> bool:
    """Remove pid file if it points to a non-existing process.

    Returns True if a zombie pid file was removed.
    """
    data = read_pid_file(workspace_dir)
    if not data:
        return False

    pid = data.get("pid")
    try:
        pid_int = int(pid)
    except Exception:
        remove_pid_file(workspace_dir)
        return True

    if not is_pid_alive(pid_int):
        remove_pid_file(workspace_dir)
        return True

    return False


def find_port_owner(port: int) -> PortOwner:
    """Best-effort: identify process that is LISTENing on a TCP port."""
    if port <= 0:
        return PortOwner(pid=None, name=None)

    try:
        import psutil  # type: ignore

        try:
            conns = psutil.net_connections(kind="inet")
        except TypeError:
            conns = psutil.net_connections()

        for c in conns:
            try:
                laddr = getattr(c, "laddr", None)
                if not laddr:
                    continue
                if getattr(laddr, "port", None) != port:
                    continue
                if getattr(c, "status", "") != "LISTEN":
                    continue

                pid = getattr(c, "pid", None)
                name: Optional[str] = None
                if pid:
                    try:
                        name = psutil.Process(pid).name()
                    except Exception:
                        name = None
                return PortOwner(pid=int(pid) if pid else None, name=name)
            except Exception:
                continue
    except Exception:
        pass

    return PortOwner(pid=None, name=None)


def terminate_process(pid: int, timeout_s: float = 3.0) -> Tuple[bool, str]:
    """Terminate a process by pid.

    Returns: (terminated, message)
    """
    if pid <= 0:
        return False, "Invalid PID"

    # Prefer psutil when available (more reliable cross-platform).
    try:
        import psutil  # type: ignore

        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            return False, "Process already dead"

        try:
            proc.terminate()
            proc.wait(timeout=timeout_s)
            return True, "Terminated gracefully"
        except psutil.TimeoutExpired:
            proc.kill()
            return True, "Force killed"
        except psutil.AccessDenied:
            return False, "Access denied"
    except Exception:
        # Fallback to signals (POSIX best-effort)
        try:
            os.kill(pid, 15)
            return True, "Terminated (signal)"
        except ProcessLookupError:
            return False, "Process already dead"
        except PermissionError:
            return False, "Access denied"
        except Exception as e:
            return False, f"Failed to terminate: {e}"
