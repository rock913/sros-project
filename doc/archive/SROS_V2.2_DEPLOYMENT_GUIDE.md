# SROS V2.2 部署和使用指南

## 1. 概述

SROS V2.2 引入了全新的 Gateway 架构，解决了连接数限制、科研冷启动和部署复杂度问题。本文档介绍如何部署和使用 SROS V2.2。

## 2. 架构概览

### 2.1 双平面 + 轮毂模型 (Hub-and-Spoke)
```
Roo Code / User <--> SSE (Port 8000) <--> SROS Gateway
                                           |
    ----------------------------------------
    |        |        |        |        |
Stdio    Stdio   Stdio   Stdio   Stdio
    |        |        |        |        |
FedAcad  Manuscr  DuckDB  Context  Zotero
Search   Mgr      Mem     Ingester Expert
```

### 2.2 核心优势
- **连接数突破**: 从 6 个 SSE 连接限制 → 无限扩展
- **冷启动加速**: 通过 context_ingester 预处理材料实现 "带薪进组"
- **简化部署**: 从 6 个端口管理 → 1 个端口一键启动

## 3. 部署步骤

### 3.1 环境要求
- Python 3.6+
- VS Code with Roo Code/Cline extension
- Git for version control

### 3.2 安装依赖
```bash
# 安装核心依赖
pip install -r requirements.txt

# 安装可选依赖（推荐）
pip install duckdb  # 本地知识图谱存储
```

### 3.3 配置环境变量
```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件配置 API 密钥
vim .env
```

## 4. 启动方式

### 4.1 启动 SROS V2.2 Gateway 模式（推荐）
```bash
# 启动 Gateway 模式（默认）
python run_servers.py gateway

# 指定端口
python run_servers.py gateway --port 8000

# 自动寻找可用端口
python run_servers.py gateway --auto-port
```

### 4.2 启动传统模式（兼容）
```bash
# 启动所有传统服务器
python run_servers.py all

# 启动单个服务器
python run_servers.py federal-academic-search
python run_servers.py manuscript-manager
python run_servers.py duckdb-memory
python run_servers.py zotero-expert
python run_servers.py sros-logic
```

## 5. 项目结构

### 5.1 推荐的科研项目结构
```
/My_Research_Project/          # VS Code 打开此目录
├── .sros/                    # [自动生成] 隐藏状态目录
│   ├── graph.db              # 本地知识图谱 (DuckDB)
│   └── research_log.jsonl    # 检索足迹
├── .roomodes                 # [复制/软链] 项目特定的行为定义
├── .env                      # [复制] 环境变量配置
├── draft.md                  # [核心] 单一事实来源
├── ideas.md                  # [可选] 初始想法与核心假设
├── materials/                # [新增] 辅助参考材料
│   ├── deep_research.md      # Gemini/Perplexity 生成的调研报告
│   ├── web_clips.txt         # 网页剪藏
│   └── notes.md              # 随手笔记
└── references/               # [正式] 仅存放 Zotero 链接的正式 PDF 附件
```

## 6. 工作流程

### 6.1 上下文增强型科研循环

#### Step 0: 预热 (Warm-up / Ingest)
```python
# Context Ingester 自动扫描
ctx_ingest_materials({
    "workspace_path": "/path/to/project"
})
```

#### Step 1: 观察与检测 (Observe & Detect)
```python
# Agent 扫描 draft.md，发现 [TODO: 补充 Transformer 架构对比]
ms_parse_structure({"file_path": "draft.md"})
```

#### Step 2: 本地查询优先
```python
# 优先查询本地 Graph
ctx_search_soft_knowledge({
    "query": "Transformer 架构对比",
    "limit": 5
})
```

#### Step 3: 联邦检索 (Federal Retrieve)
```python
# 如果本地无答案，使用联邦搜索
federal_search_paper({
    "query": "Transformer vs RNN architecture comparison",
    "limit": 10
})
```

#### Step 4: 原子化写入 (Atomic Write)
```python
# 使用稿件管理器插入内容
ms_edit_section({
    "section": "Related Work",
    "content": "Detailed comparison content...",
    "operation": "insert"
})
```

## 7. 工具命名空间

### 7.1 Gateway 模式下的工具前缀
- `federal_*` - 联邦学术搜索相关
  - `federal_search_paper` - 论文搜索
  - `federal_get_paper_details` - 论文详情获取

- `ms_*` - 稿件管理相关
  - `ms_parse_structure` - 解析稿件结构
  - `ms_edit_section` - 编辑章节
  - `ms_validate_draft` - 验证稿件

- `mem_*` - 内存/知识图谱相关
  - `mem_store_knowledge` - 存储知识
  - `mem_query_graph` - 查询图谱
  - `mem_get_relationships` - 获取关系

- `ctx_*` - 上下文处理相关
  - `ctx_ingest_materials` - 摄入材料
  - `ctx_search_soft_knowledge` - 搜索软知识
  - `ctx_get_context_summary` - 获取上下文摘要

- `zot_*` - Zotero 专家相关
  - `zot_manage_references` - 管理参考文献
  - `zot_sync_library` - 同步文献库

## 8. 配置文件

### 8.1 .roo/mcp.json (Gateway 模式)
```json
{
  "mcpServers": {
    "sros-gateway": {
      "name": "SROS Gateway",
      "url": "http://localhost:8000/sse",
      "type": "sse",
      "description": "SROS V2.2 Gateway - Unified MCP Server Aggregator",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

### 8.2 Gateway 配置 (mcp_servers/sros_gateway/config.json)
```json
{
  "servers": {
    "federal": {
      "command": "python",
      "args": ["-m", "mcp_servers.federal_academic_search.main", "--mode", "stdio"],
      "env": { "PYTHONUNBUFFERED": "1" },
      "namespace_prefix": "federal_"
    },
    "manuscript": {
      "command": "python", 
      "args": ["-m", "mcp_servers.manuscript_manager.main", "--mode", "stdio"],
      "env": { "PYTHONUNBUFFERED": "1" },
      "namespace_prefix": "ms_"
    },
    "memory": {
      "command": "python",
      "args": ["-m", "mcp_servers.duckdb_memory.main", "--mode", "stdio"], 
      "env": { "PYTHONUNBUFFERED": "1" },
      "namespace_prefix": "mem_"
    },
    "context": {
      "command": "python",
      "args": ["-m", "mcp_servers.context_ingester.main", "--mode", "stdio"],
      "env": { "PYTHONUNBUFFERED": "1" },
      "namespace_prefix": "ctx_"
    },
    "zotero": {
      "command": "python",
      "args": ["-m", "mcp_servers.zotero_expert.main", "--mode", "stdio"],
      "env": { "PYTHONUNBUFFERED": "1" },
      "namespace_prefix": "zot_"
    }
  }
}
```

## 9. .roomodes 配置示例

```yaml
name: SROS-Writer-V2.2
groups:
  - read
  - edit
  - browser
  - mcp
systemPrompt: |
  你是一个专业的学术论文写作助手，使用 SROS V2.2 Gateway 架构。你的目标是消除 draft.md 中的 [TODO]。

  核心规则：
  1. **上下文优先**：在去外部搜索前，必须先调用 `mem_query_graph` 检查软知识库。
  2. **原子写入**：严禁重写整个文件。必须使用 `ms_edit_section` 工具。
  3. **工具调用**：所有工具现在通过 Gateway 暴露，名称带有前缀：
     - `federal_search_paper` - 联邦学术搜索
     - `ms_parse_structure` - 稿件结构分析
     - `ms_edit_section` - 稿件编辑
     - `mem_store_knowledge` - 知识图谱存储
     - `mem_query_graph` - 知识图谱查询
     - `ctx_ingest_materials` - 上下文材料摄入
     - `ctx_search_soft_knowledge` - 软知识搜索
     - `zot_manage_references` - 文献管理

  工作流程：
  1. **预热**：调用 `ctx_ingest_materials` 处理 materials/ 和 ideas.md
  2. **观察**：调用 `ms_parse_structure` 分析 draft.md
  3. **检测**：识别 [TODO] 和逻辑缺口
  4. **查询**：先调用 `ctx_search_soft_knowledge` 和 `mem_query_graph` 检查本地材料
  5. **检索**：如本地无答案，调用 `federal_search_paper`
  6. **存储**：使用 `mem_store_knowledge` 存储新知识
  7. **写入**：使用 `ms_edit_section` 插入内容
```

## 10. 故障排除

### 10.1 常见问题
1. **端口占用**: 使用 `--auto-port` 参数自动寻找可用端口
2. **依赖缺失**: 确保安装了所有必需的 Python 包
3. **配置错误**: 检查 `.env` 文件中的 API 密钥配置
4. **Gateway 启动失败**: 检查 `mcp_servers/sros_gateway/config.json` 配置

### 10.2 调试技巧
- 查看 Gateway 日志: `tail -f .sros/logs/gateway.log`
- 检查子服务状态: 确认各子服务能单独启动
- 网络连接测试: `curl -X POST http://localhost:8000/sse`

### 10.3 稳定性修复说明（V2.2.1）
**问题**：Gateway 冷启动时并行拉起多个 Python 子进程会导致 CPU/I/O 峰值，触发客户端超时（Cold Start Storm）。

**解决**：
1. 引入健康检查 `/health`，仅在所有子服务准备就绪后标记为 ready。
2. 启动预热（preheat）：Gateway 启动时初始化所有子服务。
3. `run_servers.py` 启动后轮询健康检查，直到就绪再返回成功。

**使用方式**：
```bash
# 启动并等待健康检查通过
python run_servers.py gateway

# 跳过健康检查（调试用途）
python run_servers.py gateway --no-health-check
```

**排查建议**：
- 如果健康检查超时，检查 `config.json` 子服务配置与依赖是否完整。
- 如启动耗时过长，可临时提高 `wait_for_gateway_health()` 的超时时间。

**补充说明**：
- 健康检查会返回 `unhealthy_servers` 以定位未就绪的子服务。
- HTTP Keep-Alive 超时建议设置为 300 秒以避免长耗时请求被断开。

## 11. 性能优化

### 11.1 Gateway 性能
- 子服务进程复用，减少启动开销
- 请求路由缓存，提高响应速度
- 连接池管理，优化资源使用

### 11.2 内存管理
- 智能缓存策略，平衡速度和内存使用
- 定期清理临时文件，避免磁盘空间耗尽

## 12. 升级指南

### 12.1 从 V2.1.5 升级到 V2.2
1. 备份现有项目数据
2. 更新配置文件 `.roo/mcp.json` (已更新为使用 /sse 端点)
3. 修改 `.roomodes` 中的工具调用前缀
4. 启动 Gateway 模式

### 12.2 回滚到 V2.1.5
```bash
# 启动传统模式
python run_servers.py all
```

## 13. 最佳实践

1. **项目隔离**: 每个研究项目使用独立目录
2. **材料组织**: 合理组织 `materials/` 目录结构
3. **定期备份**: 定期备份 `.sros/` 目录
4. **渐进式写作**: 使用 `[TODO:]` 标记待研究内容
5. **版本控制**: 使用 Git 管理项目变更