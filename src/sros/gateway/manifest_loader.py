"""Manifest Loader — 读取并校验子应用 mcp_tools.json manifest。

SROS 启动时扫描 config/sub_apps/ 目录下的 JSON manifest，
校验后注入 Gateway 工具列表。实现 "内核纯净" 原则：
SROS 自身代码不含任何领域特定词汇（医学/天文），
所有领域工具通过 manifest 动态挂载。

Proposal: meta-docs/proposals/pending/SROS-Dynamic-Skill-Registration.md (Ω4)
"""

import json
import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)


class ToolManifestItem(BaseModel):
    """单个 MCP tool 的 manifest 条目。"""

    name: str  # e.g. "omnineuro.mri.fMRIPrep_submit"
    description: str
    inputSchema: dict = Field(default_factory=dict)
    handler: str  # CLI command with {placeholder} args
    handler_type: str = "cli"  # "cli" | "http"
    timeout_ms: int = 300_000  # 5 min default


class SubAppManifest(BaseModel):
    """子应用 manifest — 对应一个 mcp_tools.json 文件。"""

    name: str  # e.g. "omnineuro"
    version: str  # e.g. "9.0.0"
    compatible_sros_version: str = ">=4.0"
    description: str = ""
    tools: list[ToolManifestItem] = Field(default_factory=list)


class ManifestLoader:
    """加载并校验子应用 manifest JSON 文件。

    用法:
        loader = ManifestLoader(manifests_dir=Path("config/sub_apps"))
        loader.set_static_tool_names({"sros.db.ingest", ...})
        manifests = loader.load_all()  # -> dict[str, SubAppManifest]
    """

    def __init__(self, manifests_dir: Path | None = None):
        self.manifests_dir = manifests_dir or Path("config/sub_apps")
        self.static_tool_names: set[str] = set()

    def set_static_tool_names(self, names: set[str]) -> None:
        """注入静态工具名称集，用于冲突检测。"""
        self.static_tool_names = names

    def load_all(self) -> dict[str, SubAppManifest]:
        """扫描 manifests_dir 下所有 .json 文件，返回 {app_name: manifest}。

        加载失败不阻止 SROS 启动 — 告警 + 跳过该 manifest。
        """
        if not self.manifests_dir.exists():
            logger.info("Manifest directory not found: %s — skipping dynamic tools", self.manifests_dir)
            return {}

        manifests: dict[str, SubAppManifest] = {}
        all_tool_names: set[str] = set()

        for manifest_path in sorted(self.manifests_dir.glob("*.json")):
            try:
                manifest = self._load_one(manifest_path)
                if manifest is None:
                    continue

                # Detect tool name conflicts
                for tool in manifest.tools:
                    if tool.name in self.static_tool_names:
                        logger.error(
                            "Tool name conflict with static tool: %s (from %s) — REJECTED",
                            tool.name, manifest.name,
                        )
                        continue
                    if tool.name in all_tool_names:
                        logger.error(
                            "Tool name conflict between manifests: %s (from %s) — REJECTED",
                            tool.name, manifest.name,
                        )
                        continue
                    all_tool_names.add(tool.name)

                manifests[manifest.name] = manifest
                logger.info(
                    "Loaded manifest: %s v%s — %d tools",
                    manifest.name, manifest.version, len(manifest.tools),
                )

            except Exception:
                logger.exception("Failed to load manifest: %s", manifest_path)

        return manifests

    def _load_one(self, path: Path) -> Optional[SubAppManifest]:
        """加载单个 manifest 文件。"""
        if not path.is_file():
            return None

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in manifest %s: %s", path.name, e)
            return None

        try:
            return SubAppManifest(**data)
        except ValidationError as e:
            logger.error("Schema validation failed for manifest %s: %s", path.name, e)
            return None

    def get_all_tools(self, manifests: dict[str, SubAppManifest]) -> list[ToolManifestItem]:
        """从所有 loaded manifests 中提取扁平 tool 列表（已去重）。"""
        tools: list[ToolManifestItem] = []
        seen: set[str] = set()
        for manifest in manifests.values():
            for tool in manifest.tools:
                if tool.name not in seen:
                    tools.append(tool)
                    seen.add(tool.name)
        return tools
