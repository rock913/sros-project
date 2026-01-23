# Phase 4.2: MCP Infrastructure & Hexagonal Migration - 实施计划

**创建时间**: 2026-01-22  
**状态**: 🚧 In Progress  
**预计完成**: 2026-02-12 (3周)  
**负责人**: AI-Native Architect (Copilot) + Builder (Aider)

---

## 📋 概述

### 目标
完成MCP（Model Context Protocol）基础设施构建，并迁移剩余工具到六边形架构（Hexagonal Architecture）。

### 背景
- Phase 4.1已完成：MPA架构建立，LangFuse可观测性集成
- 当前状态：部分工具已迁移（Unpaywall, Arxiv, Zotero），但MCP基础设施不完整
- 遗留问题：`tools_and_schemas.py`需要重构，FastAPI MCP适配器需要实现

---

## 🎯 核心交付物

### 1. MCP基础架构 (Week 1)
- ✅ **MCP SDK集成**: `mcp`包安装和配置
- ✅ **McpServer Protocol**: 定义标准接口
- ✅ **FastAPIMcpServerAdapter**: 实现FastAPI适配器
- ✅ **动态工具注册**: 标准入口点实现

### 2. 工具迁移 - 大重构 (Week 2-3)
- ✅ **Arxiv迁移**: `ArxivAdapter`实现`PaperSearcher` Protocol
- ✅ **Zotero迁移**: `ZoteroAdapter`实现`ReferenceManager` Protocol  
- ✅ **遗留代码清理**: 废弃`backend/src/agent/tools_and_schemas.py`
- ✅ **测试覆盖**: 所有迁移组件100%测试覆盖率

### 3. 文档与验证 (Week 3)
- ✅ **API文档**: 更新OpenAPI规范
- ✅ **架构文档**: 六边形架构说明
- ✅ **验证测试**: E2E测试确保向后兼容

---

## 📁 文件结构变更

### 新增文件
```
backend/src/agent/domain/ports/mcp_server.py          # McpServer Protocol
backend/src/agent/infrastructure/mcp/fastapi_adapter.py # FastAPI适配器
backend/src/agent/infrastructure/mcp/entrypoint.py    # 动态工具注册
backend/src/agent/infrastructure/mcp/config.py        # MCP配置
```

### 修改文件
```
backend/src/agent/infrastructure/mcp/simple_mcp_server.py # 扩展实现
backend/src/agent/infrastructure/mcp/tools/__init__.py    # 工具工厂
backend/pyproject.toml                                    # 依赖更新
docker-compose-dev.yml                                    # 环境变量
```

### 废弃文件
```
backend/src/agent/tools_and_schemas.py                   # 遗留代码
```

---

## 🔧 技术实施细节

### 1. MCP Server Protocol 设计

```python
# backend/src/agent/domain/ports/mcp_server.py
from typing import Protocol, List, Optional
from agent.domain.schemas.mcp import McpTool, McpResource

class McpServer(Protocol):
    """MCP服务器协议 - 定义标准MCP服务器接口"""
    
    @property
    def name(self) -> str:
        """服务器名称"""
        ...
    
    @property
    def version(self) -> str:
        """服务器版本"""
        ...
    
    def get_tools(self) -> List[McpTool]:
        """获取所有可用工具"""
        ...
    
    def get_resources(self) -> List[McpResource]:
        """获取所有可用资源"""
        ...
    
    def initialize(self) -> None:
        """初始化服务器"""
        ...
    
    def shutdown(self) -> None:
        """关闭服务器"""
        ...
```

### 2. FastAPI MCP适配器实现

```python
# backend/src/agent/infrastructure/mcp/fastapi_adapter.py
from fastapi import FastAPI, APIRouter
from agent.domain.ports.mcp_server import McpServer

class FastAPIMcpServerAdapter:
    """FastAPI MCP服务器适配器"""
    
    def __init__(self, mcp_server: McpServer, prefix: str = "/mcp"):
        self.mcp_server = mcp_server
        self.prefix = prefix
        self.router = APIRouter(prefix=prefix)
        
    def register_routes(self, app: FastAPI) -> None:
        """注册MCP路由到FastAPI应用"""
        
        @self.router.get("/tools")
        async def list_tools():
            return self.mcp_server.get_tools()
        
        @self.router.get("/resources")
        async def list_resources():
            return self.mcp_server.get_resources()
        
        @self.router.post("/tools/{tool_name}/execute")
        async def execute_tool(tool_name: str, arguments: dict):
            # 工具执行逻辑
            pass
        
        app.include_router(self.router)
```

### 3. 动态工具注册入口点

```python
# backend/src/agent/infrastructure/mcp/entrypoint.py
from typing import Dict, Callable
from agent.domain.schemas.mcp import McpTool

class ToolRegistry:
    """工具注册表 - 支持动态工具注册"""
    
    _tools: Dict[str, Callable[[], McpTool]] = {}
    
    @classmethod
    def register(cls, name: str, factory: Callable[[], McpTool]):
        """注册工具工厂"""
        cls._tools[name] = factory
    
    @classmethod
    def get_tool(cls, name: str) -> Optional[McpTool]:
        """获取工具实例"""
        if name in cls._tools:
            return cls._tools[name]()
        return None
    
    @classmethod
    def get_all_tools(cls) -> Dict[str, McpTool]:
        """获取所有工具"""
        return {name: factory() for name, factory in cls._tools.items()}
```

### 4. 工具迁移模式

```python
# 迁移前 - 遗留工具
from backend.src.agent.tools_and_schemas import search_arxiv

# 迁移后 - MCP工具
from agent.infrastructure.mcp.tools.arxiv import ArxivAdapter
from agent.domain.ports.paper_searcher import PaperSearcher

class ArxivMcpTool(McpTool):
    def __init__(self):
        self.adapter = ArxivAdapter()
    
    def execute(self, arguments: dict) -> dict:
        # 调用适配器
        return self.adapter.search(arguments)
```

---

## 📊 实施时间表

### Week 1: MCP基础架构 (2026-01-22 至 2026-01-28)

| 任务 | 负责人 | 状态 | 预计工时 |
|------|--------|------|----------|
| 1.1 安装MCP SDK依赖 | Aider | ⏳ | 1小时 |
| 1.2 实现McpServer Protocol | Copilot | ⏳ | 2小时 |
| 1.3 实现FastAPIMcpServerAdapter | Copilot | ⏳ | 4小时 |
| 1.4 创建动态工具注册入口点 | Copilot | ⏳ | 3小时 |
| 1.5 更新Docker配置 | Aider | ⏳ | 1小时 |
| 1.6 编写单元测试 | Aider | ⏳ | 4小时 |
| **Week 1总计** | | | **15小时** |

### Week 2: 工具迁移 - Arxiv & Zotero (2026-01-29 至 2026-02-04)

| 任务 | 负责人 | 状态 | 预计工时 |
|------|--------|------|----------|
| 2.1 分析现有Arxiv实现 | Copilot | ⏳ | 2小时 |
| 2.2 创建ArxivAdapter | Copilot | ⏳ | 4小时 |
| 2.3 创建Arxiv MCP工具 | Aider | ⏳ | 3小时 |
| 2.4 分析现有Zotero实现 | Copilot | ⏳ | 2小时 |
| 2.5 创建ZoteroAdapter | Copilot | ⏳ | 4小时 |
| 2.6 创建Zotero MCP工具 | Aider | ⏳ | 3小时 |
| 2.7 更新工具注册表 | Aider | ⏳ | 2小时 |
| **Week 2总计** | | | **20小时** |

### Week 3: 测试、清理与文档 (2026-02-05 至 2026-02-11)

| 任务 | 负责人 | 状态 | 预计工时 |
|------|--------|------|----------|
| 3.1 编写集成测试 | Aider | ⏳ | 6小时 |
| 3.2 E2E测试验证 | Aider | ⏳ | 4小时 |
| 3.3 废弃tools_and_schemas.py | Copilot | ⏳ | 2小时 |
| 3.4 更新所有导入引用 | Aider | ⏳ | 4小时 |
| 3.5 更新OpenAPI文档 | Copilot | ⏳ | 3小时 |
| 3.6 编写架构迁移文档 | Copilot | ⏳ | 3小时 |
| 3.7 性能测试与优化 | Aider | ⏳ | 4小时 |
| **Week 3总计** | | | **26小时** |

### 总预计工时: 61小时 (约1.5人周)

---

## 🧪 测试策略

### 1. 单元测试
```bash
# 测试MCP基础架构
pytest backend/tests/agent/infrastructure/mcp/test_mcp_server.py
pytest backend/tests/agent/infrastructure/mcp/test_fastapi_adapter.py

# 测试迁移工具
pytest backend/tests/agent/infrastructure/tools/test_arxiv_adapter.py
pytest backend/tests/agent/infrastructure/tools/test_zotero_adapter.py
```

### 2. 集成测试
```bash
# 测试MCP服务器集成
pytest backend/tests/agent/infrastructure/mcp/test_integration.py

# 测试向后兼容性
pytest backend/tests/agent/test_backward_compatibility.py
```

### 3. E2E测试
```bash
# 完整研究流程测试
./scripts/test-e2e-mcp.sh
```

### 测试覆盖率目标
- 单元测试: >90%
- 集成测试: >80%  
- E2E测试: 关键路径100%

---

## 🔄 迁移风险与缓解

### 风险1: 向后兼容性破坏
**影响**: 现有API客户端可能失效
**缓解措施**:
1. 保持现有API端点不变
2. 使用适配器模式桥接新旧实现
3. 分阶段迁移，先并行运行再切换

### 风险2: 性能下降
**影响**: MCP层增加可能影响响应时间
**缓解措施**:
1. 性能基准测试（迁移前后对比）
2. 实现缓存机制
3. 异步工具执行

### 风险3: 工具功能缺失
**影响**: 迁移过程中可能丢失某些功能
**缓解措施**:
1. 详细的功能对比清单
2. 回归测试覆盖所有功能点
3. 分工具逐步迁移，而非一次性

---

## 📚 文档要求

### 1. 技术文档
- [ ] `doc/architecture/MCP_ARCHITECTURE.md` - MCP架构说明
- [ ] `doc/development/TOOL_MIGRATION_GUIDE.md` - 工具迁移指南
- [ ] `backend/API_DOCUMENTATION.md` - 更新API文档

### 2. 开发者文档
- [ ] `CONTRIBUTING.md` - 更新贡献指南
- [ ] `README.md` - 更新项目说明
- [ ] `doc/development/PHASE_4.2_COMPLETION_REPORT.md` - 完成报告

### 3. 用户文档
- [ ] `doc/user/MCP_TOOLS.md` - MCP工具使用指南
- [ ] `doc/user/HEXAGONAL_ARCHITECTURE.md` - 架构变更说明

---

## 🚀 部署计划

### 阶段1: 开发环境 (Week 1)
- 在开发分支实现MCP基础架构
- 开发环境测试通过

### 阶段2: 测试环境 (Week 2)
- 合并到测试分支
- 运行完整测试套件
- 性能基准测试

### 阶段3: 生产环境 (Week 3)
- 代码审查通过
- 所有测试通过
- 部署到生产环境
- 监控和验证

---

## 📈 成功指标

### 技术指标
- ✅ MCP服务器响应时间 < 100ms
- ✅ 工具迁移覆盖率 100%
- ✅ 测试覆盖率 > 85%
- ✅ 零回归缺陷

### 业务指标  
- ✅ 向后兼容性保持 100%
- ✅ 用户无感知迁移
- ✅ 开发效率提升（新工具集成时间减少50%）

### 质量指标
- ✅ 代码审查通过率 100%
- ✅ 文档完整性 100%
- ✅ 部署成功率 100%

---

## 👥 团队协作

### 角色分工
- **AI-Native Architect (Copilot)**: 架构设计、协议定义、代码审查
- **Builder (Aider)**: 代码实现、测试编写、文档更新
- **Tester (Automated)**: 测试执行、质量保证

### 沟通机制
- 每日进度更新在`.ai-sessions/development/`
- 代码审查通过GitHub PR
- 问题跟踪在GitHub Issues

### 决策记录
所有架构决策记录在：
- `.ai-sessions/development/2026-01-22-phase-4.2-decisions.md`
- `doc/architecture/DECISION_LOG.md`

---

## 🔗 相关文档

### 参考文档
- [Model Context Protocol (MCP) Specification](https://spec.modelcontextprotocol.io/)
- [Phase 4.1 完成报告](doc/verification/PHASE_4.1.md)
- [ROADMAP.md](ROADMAP.md) - 项目路线图
- [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md) - 开发状态

### 技术资源
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Hexagonal Architecture Pattern](https://alistair.cockburn.us/hexagonal-architecture/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 🎯 验收标准

### 必须完成 (MUST)
- [ ] MCP服务器可通过FastAPI访问
- [ ] 所有工具迁移到MCP架构
- [ ] `tools_and_schemas.py`完全废弃
- [ ] 测试覆盖率 > 85%
- [ ] 向后兼容性保持

### 应该完成 (SHOULD)
- [ ] 性能基准测试完成
- [ ] 完整文档更新
- [ ] 开发者指南编写

### 可以完成 (COULD)
- [ ] 性能优化（缓存、异步）
- [ ] 监控仪表板
- [ ] 自动化部署脚本

---

## 📝 更新日志

| 日期 | 版本 | 更新内容 | 负责人 |
|------|------|----------|--------|
| 2026-01-22 | v1.0 | 初始实施计划创建 | Copilot |
| 2026-01-23 | v1.1 | 添加详细技术设计 | Copilot |
| 2026-01-24 | v1.2 | 更新时间表和风险评估 | Copilot |

---

## ✅ 完成检查清单

### 启动前检查
- [ ] 环境准备完成（Docker、Python环境）
- [ ] 代码库最新状态
- [ ] 备份现有实现
- [ ] 团队沟通完成

### 实施中检查
- [ ] 每日进度更新
- [ ] 代码审查通过
- [ ] 测试通过
- [ ] 文档同步更新

### 完成后检查
- [ ] 所有验收标准满足
- [ ] 生产部署成功
- [ ] 用户验证通过
- [ ] 项目状态更新

---

**计划批准**: 待批准  
**下一步**: 开始Week 1实施 - MCP基础架构
