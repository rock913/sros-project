SROS V4.0 Phase 1: 文献与知识合成闭环 MVP 测试指南

1. 测试目标与架构验证点

本指南旨在通过 Claude Code 端到端验证 SROS V4.0 Phase 1 的核心基建能力。您将扮演一名拥有零散灵感的天文学/AI交叉领域研究员，让 Agent 帮您完成从“混沌”到“秩序”的知识重构。

核心验证点：

Omni-Ingestion & CLI-Anything：Agent 能否自主调用扩展工具（如 ext.web_scrape）抓取外部散乱资料，并提炼成“检索种子”。

Scholar & Zotero 闭环：Agent 能否利用种子线索去 OpenAlex 检索，并调用 Zotero 技能将文献（PDF/元数据）沉淀为标准资产。

本地 RAG 知识合成：Agent 能否触发 DuckDB 的 VSS（向量空间搜索）构建命令，并在写作前进行精准的 RAG 查询。

Draft AST 重构：Agent 能否基于 RAG 返回的真实上下文，重构 draft.md 并写入标准引用（消除幻觉）。

2. 测试环境准备 (The Headless Lab Setup)

首先，在您的终端初始化一个全新的 V4.0 工作区，并人为制造一些“散乱的前期调研材料”。

# 1. 初始化 V4 工作区
sros init v4-lit-test --target claude
cd v4-lit-test

# 2. 准备零散的灵感笔记 (Omni-Ingestion 目标)
mkdir -p materials/raw_notes
cat << 'EOF' > materials/raw_notes/idea_brainstorm.md
# 关于大模型在天文领域的应用想法

我昨天和导师开会，想到可以用 Transformer 来处理天文巡天（如 SDSS）的光变曲线数据。
不知道现在有没有人做过这个？

我还看到了一篇网上的博客提到 PINN (Physics-Informed Neural Networks) 在天体物理里的应用。
链接是：[https://example.com/mock-astro-blog-post](https://example.com/mock-astro-blog-post)

[TODO] 帮我调研一下：
1. Transformer 在天文光变曲线 (light curves) 的最新应用。
2. 结合上面的博客，看看这几年有没有顶会论文在做类似的事情。
EOF

# 3. 启动 Gateway (如果使用 MCP 代理模式)
export SROS_WORKSPACE_DIR="$PWD"
sros start -w . -p 8000


3. The Omni-Prompt (全链路魔法指令)

在 v4-lit-test 目录下启动 claude，将以下精心设计的 Prompt 发送给它。这个 Prompt 将强迫 Agent 走完 V4 设定的每一层漏斗。

User Prompt 给 Claude Code:

"你是一个高级 AI 科研助理。请严格使用 sros-skill --raw 执行以下端到端文献综述闭环：

泛在摄入 (Omni-Ingestion)：读取 materials/raw_notes/idea_brainstorm.md。如果发现有 URL，请调用 sros-skill --raw ext web_scrape --url <URL> 提取网页正文。总结出我的核心假设。

定向检索与资产沉淀 (Scholar & Zotero)：使用 sros-skill --raw scholar search 检索至少 3 篇关于 'Transformer astronomy light curve' 的最新核心论文。然后，使用 sros-skill --raw scholar zotero-sync --citekeys <keys> 将它们同步到本地文献库（假装下载了 PDF）。

知识向量化与合成 (RAG)：调用 sros-skill --raw rag build --source materials/,references/，把我的灵感笔记和新下载的论文切块建索引。随后，调用 sros-skill --raw rag query --query 'Transformer 在光变曲线上的具体模型架构差异' 获取上下文。

大纲重构写回 (Refactor)：基于 RAG 返回的内容，使用 sros-skill --raw manuscript refactor --target 'heading:Related Work' 在 draft.md 中重构生成一段严谨的文献综述，必须包含清晰的引用标记（如 [@citekey]），并在 DuckDB 记录图谱关系。"

4. 观察 Agent 自动驾驶的“交响乐”

如果 V4 的 CLI Skills 设计得足够宽容且符合标准输出，您将欣赏到 Claude Code 完美的推理链：

[文件读取] Agent 读取了 idea_brainstorm.md。

[Tool Use: CLI-Anything] Agent 发现了 https://example.com...，聪明地调用了 sros-skill --raw ext web_scrape（SROS 内部可能是对 curl 或 trafilatura 的简单包装）。

Claude 思考：我抓取到了 PINN 的知识，结合 Transformer，提取出了核心搜索关键词。

[Tool Use: Scholar] Agent 调用 sros-skill --raw scholar search "Transformer astronomy light curves PINN"。

[Tool Use: Zotero] Agent 调用 sros-skill --raw scholar zotero-sync。

SROS 拦截：SROS 在后台通过 Zotero API 建立条目，并在 DuckDB 记录 Paper 实体。

[Tool Use: RAG Build] Agent 调用 rag build。

SROS 拦截：SROS 触发 DuckDB vss 扩展，计算 embedding 并落盘。

[Tool Use: RAG Query] Agent 调用 rag query 拿到了精确的文本片段。

[Tool Use: Refactor] Agent 调用 manuscript refactor。

SROS 拦截：SROS 解析 Markdown AST，无损插入包含引用的综述，并写入图谱。

5. 验收标准与验证清单 (Verification Checklist)

当 Claude Code 报告“任务已完成”后，请通过以下步骤对 Phase 1 成果进行“冷酷无情”的硬核校验。

✅ 5.1 验证物理资产沉淀 (Workspace)

确认 SROS 成功把云端的非结构化知识变成了本地的标准资产：

# 检查 references 目录是否自动生成了结构化的 BibTeX 或元数据
ls -la references/

# 预期输出应包含类似：
# zotero_library.bib
# pdfs/xxx_transformer_astro.pdf (或 mock 的文件)


✅ 5.2 验证大纲重构 (Draft AST)

打开 draft.md，检查 Related Work 章节是否被完美创建，并且没有破坏其他已有章节。重点检查大模型是否按照 RAG 给定的知识，输出了带有明确 citekey 的学术语言，而非自己的幻觉。

## Related Work

近期研究表明，Transformer 架构在处理天文巡天的大规模光变曲线时表现出显著优势。例如，[模型名称]通过引入自注意力机制，有效解决了非均匀采样问题 [@smith2024transformer]。此外，结合我们在前期调研中提及的 PINN 网络...


✅ 5.3 验证异构知识图谱与向量索引 (DuckDB VSS)

这是 V4.0 Phase 1 最硬核的底层验收。在终端使用 Python 查询 DuckDB 数据库：

python - <<'PY'
import duckdb

con = duckdb.connect('.sros/graph.db')

# 1. 验证 CITES 关系是否成功写入
print("=== Citation Edges ===")
print(con.execute("SELECT source, target FROM edges WHERE relationship = 'CITES'").df())

# 2. 验证 V4 新增的 RAG Vector Table 是否建立
try:
    print("\n=== Vector Store Stats ===")
    print(con.execute("SELECT count(*) as chunk_count FROM document_chunks").df())
    # 如果集成了 vss 扩展，甚至可以检查维度
    # print(con.execute("SELECT typeof(embedding) FROM document_chunks LIMIT 1").df())
except duckdb.CatalogException:
    print("\n[Warning] document_chunks 表未找到，请检查 RAG Build 模块是否正确落库。")
PY


预期结果：

CITES 表中应该看到从 draft_section 指向刚才 Agent 同步的真实论文 citekey 的关系边。

document_chunks 表应存在且包含若干条切割好的文本记录（代表 Omni-Ingestion 的笔记和 PDF 都已被向量化）。

6. 常见失败场景与 V4 迭代优化建议

在早期测试阶段，如果您发现本测试失败，通常会是以下原因（这正是开发阶段需要迭代改进的重点）：

ext web_scrape 失败：说明 CLI-Anything 的动态包装机制不够鲁棒，遇到网络超时或反爬时抛出了堆栈错误。改进方案：在 Skill Wrapper 层捕获所有异常，返回标准化的 {ok: false, error: "..."} 让 Claude 重试。

rag build Context 超限：当 PDF 过大时，如果在本地调 embedding 模型导致 OOM 或耗时过长，可能导致 Agent 超时断开。改进方案：Phase 2 需引入基于 SSE 的长任务异步事件钩子（Event Hooks），让 rag build 成为后台任务。

幻觉引用：Agent 生成的 [@citekey] 在 DuckDB 里查不到。改进方案：在 manuscript refactor 技能内部增加一层鉴权，如果检测到传入的 citations 在当前 workspace 的 graph.db 中不存在，则直接拒接写入并报错提醒 Agent 同步 Zotero。