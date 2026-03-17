from __future__ import annotations

import ast
import importlib.util
import os
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class PluginInfo:
    # `name` is the stable plugin id (filename stem) used for addressing.
    name: str
    description: str
    path: Path
    display_name: Optional[str] = None
    input_schema: Optional[Dict[str, Any]] = None


class PluginLoadError(RuntimeError):
    pass


def _literal_or_none(node: ast.AST) -> Any:
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def parse_plugin_metadata(path: Path) -> PluginInfo:
    """Parse plugin metadata without executing plugin code.

    Best-effort: reads SKILL_NAME, SKILL_DESCRIPTION, SKILL_INPUT_SCHEMA via AST.
    """
    name = path.stem
    description = ""
    display_name: Optional[str] = None
    input_schema: Optional[Dict[str, Any]] = None

    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.Assign) or not node.targets:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            key = target.id
            if key == "SKILL_NAME":
                v = _literal_or_none(node.value)
                if isinstance(v, str) and v.strip():
                    display_name = v.strip()
            elif key == "SKILL_DESCRIPTION":
                v = _literal_or_none(node.value)
                if v is None:
                    continue
                description = v if isinstance(v, str) else str(v)
            elif key == "SKILL_INPUT_SCHEMA":
                v = _literal_or_none(node.value)
                if isinstance(v, dict):
                    input_schema = v
    except Exception:
        # Ignore parse errors; fall back to defaults.
        pass

    return PluginInfo(
        name=name,
        description=description,
        path=path,
        display_name=display_name,
        input_schema=input_schema,
    )


def get_workspace_dir() -> Path:
    workspace_env = os.getenv("SROS_WORKSPACE_DIR")
    if not workspace_env:
        raise PluginLoadError("SROS_WORKSPACE_DIR is not set")
    return Path(workspace_env).expanduser().resolve()


def get_plugins_dir(workspace_dir: Optional[Path] = None) -> Path:
    ws = (workspace_dir or get_workspace_dir()).resolve()
    return (ws / ".sros" / "plugins").resolve()


def discover_plugins(workspace_dir: Optional[Path] = None) -> List[PluginInfo]:
    plugins_dir = get_plugins_dir(workspace_dir)
    if not plugins_dir.exists() or not plugins_dir.is_dir():
        return []

    plugins: List[PluginInfo] = []
    for path in sorted(plugins_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        plugins.append(parse_plugin_metadata(path))
    return plugins


def _load_module_from_path(module_name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise PluginLoadError(f"Failed to load plugin module: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def load_plugin(name: str, workspace_dir: Optional[Path] = None) -> tuple[PluginInfo, ModuleType]:
    plugins_dir = get_plugins_dir(workspace_dir)
    path = (plugins_dir / f"{name}.py").resolve()

    # Prevent traversal / loading outside workspace
    try:
        path.relative_to(plugins_dir)
    except ValueError:
        raise PluginLoadError("Invalid plugin name/path")

    if not path.exists():
        raise PluginLoadError(f"Plugin not found: {name}")

    module = _load_module_from_path(f"sros_plugin_{name}", path)

    skill_name = getattr(module, "SKILL_NAME", name)
    if not isinstance(skill_name, str) or not skill_name.strip():
        raise PluginLoadError("Plugin SKILL_NAME must be a non-empty string")

    desc = getattr(module, "SKILL_DESCRIPTION", "")
    if desc is None:
        desc = ""
    if not isinstance(desc, str):
        desc = str(desc)

    schema = getattr(module, "SKILL_INPUT_SCHEMA", None)
    if schema is not None and not isinstance(schema, dict):
        # Allow string-encoded schema as a convenience
        if isinstance(schema, str):
            try:
                import json

                schema = json.loads(schema)
            except Exception:
                schema = None
        else:
            schema = None

    plugin = PluginInfo(
        name=name,
        display_name=str(skill_name).strip(),
        description=desc,
        path=path,
        input_schema=schema if isinstance(schema, dict) else None,
    )
    return plugin, module


def run_plugin(name: str, args: Dict[str, Any], workspace_dir: Optional[Path] = None) -> Any:
    plugin, module = load_plugin(name, workspace_dir=workspace_dir)

    run_fn = getattr(module, "run", None)
    if not callable(run_fn):
        raise PluginLoadError("Plugin must define callable: run(args: dict) -> Any")

    return run_fn(dict(args or {}))
