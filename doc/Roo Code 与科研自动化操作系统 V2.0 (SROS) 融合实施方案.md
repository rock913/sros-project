Roo Code 与科研自动化操作系统 V2.0 (SROS) 融合实施方案

本方案旨在通过 Roo Code 的自定义模式（Custom Modes）和 MCP 架构，实现文档中定义的“首席研究员”、“图书管理员”、“分析师”和“撰稿人”四位一体的自动化科研流。

1. 核心架构映射 (Mapping)

SROS V2.0 概念

Roo Code 实现方式

融合价值

交互平面 (Interaction Plane)

Roo Code VS Code Extension UI

提供决策卡片 (HITL)、多模态聊天和思维链可视化。

智能编排平面 (Orchestrator)

Roo Code Custom Modes + Qwen3-Coder

利用 custom_modes.yaml 定义学术思维链 (Academic CoT)。

能力供给平面 (MCP Servers)

Roo Code MCP Settings

挂载 Zotero、Academic Fetch、GraphRAG 等专用服务器。

2. 实施步骤一：定义科研专属模式 (Custom Modes)

在 Roo Code 的配置文件（通常在 ~/Library/Application Support/Code/User/globalStorage/roocode.roo-code/settings/custom_modes.yaml）中注入文档定义的角色。

- slug: research-librarian
  name: 图书管理员 (Librarian)
  roleDefinition: |
    你是一名专业的科研文献检索专家。你负责广度优先搜索，从 Zotero 本地库、arXiv、Semantic Scholar 获取文献。
    你的目标是生成候选文献清单，执行去重和初步筛选。
  groups:
    - ["read", "browser", "mcp"]
  customInstructions: |
    优先使用 `zotero_search_semantic` 查找本地库。
    若本地不足，调用 `arxiv_search` 补充。
    输出格式应包含：标题、年份、引用数、AI推荐理由。

- slug: research-analyst
  name: 文献分析师 (Analyst)
  roleDefinition: |
    你是一名深度的学术内容分析师。你负责阅读全文，提取关键声明 (Claims)、证据 (Evidence) 和方法论。
    你负责将提取的知识点通过 MCP 写入 Neo4j 知识图谱。
  groups:
    - ["read", "edit", "mcp"]
  customInstructions: |
    使用 `pdf_fulltext_extract` 读取全文。
    依据 CiTO (Citation Typing Ontology) 本体提取引用意图。
    必须向用户确认提取的“三元组”是否准确。

- slug: research-scribe
  name: 学术撰稿人 (Scribe)
  roleDefinition: |
    你是一名严谨的学术论文撰写专家。你负责基于知识图谱生成带有规范引用的 Markdown/LaTeX 文本。
    你必须执行 Reflexion (反思) 机制以消除幻觉引用。
  groups:
    - ["read", "edit", "terminal"]
  customInstructions: |
    遵循 Reflexion 引文验证循环：
    1. 生成草稿 -> 2. 检查 Zotero Key 存在性 -> 3. 事实核查 -> 4. 修正。
    禁止生成库中不存在的引用。


3. 实施步骤二：挂载专用 MCP Servers

按照文档 3.1.3 节的要求，在 Roo Code 的 MCP 设置中配置以下服务器。

{
  "mcpServers": {
    "zotero-expert": {
      "command": "node",
      "args": ["/path/to/enhanced-zotero-mcp/dist/index.js"],
      "env": { "ZOTERO_API_KEY": "your_key" }
    },
    "academic-fetch": {
      "command": "python",
      "args": ["-m", "academic_fetch_server"],
      "env": { "SEMANTIC_SCHOLAR_API_KEY": "your_key" }
    },
    "graph-rag-neo4j": {
      "command": "node",
      "args": ["/path/to/graphrag-mcp/index.js"],
      "env": { "NEO4J_URI": "bolt://localhost:7687" }
    }
  }
}


4. 实施步骤三：注入“学术思维链”指令 (Instruction Tuning)

为了让 Qwen3-Coder 展现出文档要求的“外脑”特质，需在 Roo Code 的 Settings -> Custom Instructions 中添加以下全局约束：

逻辑优先：在阅读文献时，不仅关注结论，更要识别“citesAsAuthority”或“critiques”等引用关系。

证据导向：所有生成的论点必须关联到 zotero_key。

人机回环 (HITL)：在执行以下操作前必须弹出决策卡片：

筛选后的文献清单确认。

论文层级大纲修改。

知识图谱三元组写入。

5. 关键流程融合：Reflexion 验证闭环

在 Roo Code 的撰稿模式下，通过以下 System Prompt 实现文档 4.2 节的流程：

Reflexion 协议执行命令：
每当你完成一个章节的写作，请自动触发：
list_citations -> zotero_check_citation -> report_hallucinations。
若发现无效引用，立即在当前文件中标注 [ERROR: Invalid Citation] 并根据 zotero_search 的结果进行重写。

6. 预期效果：科研操作系统的具体表现

打破孤岛：你在 Roo Code 侧边栏输入“总结最近关于数字孪生鲁棒性的论文”，Agent 会自动打开 Zotero 扫描 PDF、查询 arXiv 补全缺失，最后在 VS Code 编辑器生成文档。

动态图谱：随着研究深入，Agent 会通过 MCP 将新发现的关系写入 Neo4j，Roo Code 能够利用 GraphRAG 进行跨文献的深度问答。

自动化验证：告别虚假文献，所有引用均经过本地 Zotero 数据库的实时校对。