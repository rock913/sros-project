SROS V2.2 架构实施总蓝图：聚合网关与上下文增强

版本: V2.2 (Gateway Edition)
状态: 🚀 Ready for Implementation
核心哲学: 以稿件为中心，以网关为枢纽，以“软知识”预热加速科研冷启动。

1. 核心愿景与架构演进

1.1 解决的核心痛点

连接数物理墙: 彻底解决 VS Code/Electron 环境下 SSE 连接数限制（Max 6）的问题，实现工具链的无限扩展。

科研冷启动: 通过解析用户已有的笔记、Deep Research 报告，让 Agent “带薪进组”，不再从零开始检索。

部署复杂度: 从多端口管理（8001-8006）简化为单端口（8000）一键启动。

1.2 系统架构：双平面 + 轮毂模型 (Hub-and-Spoke)

SROS V2.2 采用 MCP Gateway 模式：

前端 (Roo Code): 只与 Gateway (Port 8000) 建立 1 个 SSE 连接。

后端 (Sub-servers): Gateway 通过 Stdio (标准输入输出) 启动并管理所有子服务进程。

graph TD
    User[Roo Code / User] <-->|SSE (Port 8000)| Gateway[SROS Gateway]
    
    subgraph "Capabilities Plane (Stdio Pipes)"
        Gateway <-->|Stdio| Search[Federal Academic Search]
        Gateway <-->|Stdio| MsMgr[Manuscript Manager]
        Gateway <-->|Stdio| Graph[DuckDB Memory]
        Gateway <-->|Stdio| Context[Context Ingester]
        Gateway <-->|Stdio| Zotero[Zotero Expert]
    end
    
    subgraph "Data Plane (Local FS)"
        MsMgr --> Draft[draft.md]
        Context --> Materials[materials/*.md]
        Graph --> DB[.sros/graph.db]
    end


2. 核心组件清单 (MCP Servers)

所有服务位于 mcp_servers/ 目录下：

sros_gateway (New): 核心聚合器。负责请求路由、工具命名空间管理（如 federal_search_paper）和子进程生命周期管理。

context_ingester (New): 非结构化材料解析器。读取 materials/ 下的 Deep Research 报告、网页剪藏，转化为知识节点。

federal_academic_search: 联邦学术搜索 (OpenAlex + Semantic Scholar)。

manuscript_manager: 稿件原子化操作（基于 AST 的增量写入）。

duckdb_memory: 本地知识图谱存储（存储引文关系 + 软知识）。

zotero_expert: 本地文献库管理。

3. 生产环境拓扑 (Production Topology)

为了防止上下文污染，严格区分 代码库 与 科研项目。

3.1 推荐的项目文件结构

用户应直接在 VS Code 中打开具体的 项目子文件夹：

/My_PhD_Thesis_Project/  <-- VS Code Root
├── .sros/                 # [自动生成] 隐藏状态目录
│   ├── graph.db           # 本地知识图谱 (DuckDB)
│   └── research_log.jsonl # 检索足迹
├── .roomodes              # [复制/软链] 定义 SROS-Writer 等模式
├── .env                   # [复制] 环境变量 (API Keys)
├── draft.md               # [核心] 论文初稿 (Single Source of Truth)
├── ideas.md               # [可选] 初始想法与核心假设
├── materials/             # [新增] 辅助参考材料 (Context Ingester 扫描区)
│   ├── deep_research.md   # Gemini 生成的 50页调研报告
│   ├── web_clips.txt      # 网页剪藏
│   └── meeting_notes.md   # 导师会议记录
└── references/            # [正式] 仅存放 Zotero 链接的 PDF 附件


4. 核心工作流：上下文增强型科研循环

Step 0: 预热 (Warm-up / Ingest)

启动项目时，context_ingester 自动扫描 ideas.md 和 materials/。

提取关键概念与论据，注入 .sros/graph.db，标记为“软知识 (Soft Knowledge)”。

Step 1: 观察与检测 (Observe & Detect)

Agent 扫描 draft.md，发现 [TODO: 补充 Transformer 架构对比]。

优先查询: Agent 先查询本地 Graph。如果 deep_research.md 中已有相关对比表格，直接提取使用。

Step 2: 联邦检索 (Federal Retrieve)

如果本地无答案，Gateway 路由请求至 federal_academic_search 进行外部检索。

Step 3: 原子化写入 (Atomic Write)

Agent 调用 manuscript_manager 将综合后的内容插入指定章节。

5. 关键代码实现指南

5.1 Gateway 配置 (mcp_servers/sros_gateway/config.json)

{
  "servers": {
    "federal": {
      "command": "python",
      "args": ["-m", "mcp_servers.federal_academic_search.main"],
      "env": { "PYTHONUNBUFFERED": "1" }
    },
    "manuscript": {
      "command": "python",
      "args": ["-m", "mcp_servers.manuscript_manager.main"],
      "env": { "PYTHONUNBUFFERED": "1" }
    },
    "memory": {
      "command": "python",
      "args": ["-m", "mcp_servers.duckdb_memory.main"],
      "env": { "PYTHONUNBUFFERED": "1" }
    },
    "context": {
      "command": "python",
      "args": ["-m", "mcp_servers.context_ingester.main"],
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}


5.2 统一启动脚本 (run_servers.py)

import sys
import subprocess
import os

def main():
    print("🚀 Starting SROS Gateway (V2.2 Hub-and-Spoke Mode)...")
    print("   - Port: 8000 (SSE)")
    print("   - Transport: Stdio for sub-services")
    
    # 只需要启动 Gateway，它会自动拉起 config.json 里的所有子服务
    cmd = [
        sys.executable, "-m", "mcp_servers.sros_gateway.main"
    ]
    
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    
    try:
        # Check port 8000 availability logic here (omitted for brevity)
        subprocess.run(cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Gateway stopped. All sub-processes cleaned up.")

if __name__ == "__main__":
    main()


5.3 Roo Code 配置 (.roomodes)

name: SROS-Writer
groups:
  - read
  - edit
  - browser
  - mcp
systemPrompt: |
  你是一个专业的学术论文写作助手。你的目标是消除 draft.md 中的 [TODO]。
  
  核心规则：
  1. **上下文优先**：在去外部搜索前，必须先查询 `duckdb_memory`，检查用户的 `materials/` 中是否已有答案。
  2. **原子写入**：严禁重写整个文件。必须使用 `manuscript_manager` 的 `edit_section` 工具。
  3. **工具调用**：所有工具现在通过 Gateway 暴露，名称带有前缀（如 `federal_search_paper`）。


6. 实施路线图 (Execution Roadmap)

Phase 1: Gateway 基础设施 (Days 1-2)

[ ] 创建 mcp_servers/sros_gateway。

[ ] 实现基于 mcp.ClientSession 的 Stdio 聚合逻辑。

[ ] 调整所有子服务的 main.py，确保支持 python -m 直接启动 Stdio 模式。

Phase 2: 上下文引擎 (Days 3-4)

[ ] 实现 context_ingester：解析 Markdown 标题层级，存入 DuckDB。

[ ] 编写测试用例：放入一份 Deep Research 报告，验证 Agent 能否回答其中细节。

Phase 3: 全链路集成测试 (Day 5)

[ ] 启动 run_servers.py。

[x] 在 Roo Code 连接 http://localhost:8000/sse。

[ ] 执行 "Warm-up -> Gap Detect -> Write" 完整闭环。

7. 避坑指南

子服务入口: 确保每个子服务的 if __name__ == "__main__": 块使用的是 app.run() (自动检测模式) 而不是强制 transport='sse'。

错误透传: Gateway 应当捕获子服务的 stderr 并打印到主控制台，否则子服务报错时你会看到一片死寂。

流式传输: 在 MVP 阶段，Gateway 可以暂不支持流式透传（即等待子服务返回完整结果后再返回给 Roo），以降低实现难度。