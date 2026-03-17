SROS V3.0-Beta 进展分析与端到端测试指南

1. 当前进展深度分析：真正的“无头实验室 (Headless Lab)”已上线

根据 MVP 测试结果，SROS 已经完美实现了《V3.0 战略规划》中定义的 Phase 2 (突破纯文本 —— 数据、计算与全息图谱)。这具有以下几个深远的架构意义：

1.1 “黄金主线”的维度扩张 (From Text to Modality)

之前的 SROS 只能处理文本（Gap -> 找论文 -> 插入文字）。现在的 SROS 具备了处理**“物质/数据”**的能力（CSV 数据 -> 运算 -> 图表 -> 插入论文）。这条扩展后的黄金主线，让 SROS 真正覆盖了科研的核心中段——“实验与分析”。

1.2 异构图谱的觉醒 (Heterogeneous Provenance Graph)

测试日志中提到 Script 节点、Figure 节点 和 GENERATES 边 已成功写入 DuckDB。这是科研界的一大痛点（科研不可复现）的终极解法：数据血缘追踪 (Data Provenance)。
大模型不仅改了文章，SROS 还在底层账本上清晰地记录了：“这篇文章里的图B，是由脚本A基于数据集C生成的”。

1.3 sros-skill 确立了最佳的 Agent UI 形态

data.preview (返回行列信息和样本) 和 data.run-script (自动拦截产物并落盘) 的成功，证明了 “把复杂的环境操作封装成原子化的 CLI Skill” 是绝对正确的路线。Claude Code 只需要像敲击键盘一样调用这些命令，就能在毫无痛感的情况下完成复杂的科研任务。

2. 基于 Claude Code 的端到端 (E2E) 测试指南

为了验证这个数据闭环，我们需要让 Claude Code 扮演“双手”，SROS 扮演“实验室”。以下是完整的沙盒测试流。

步骤一：准备“无头实验室”环境

首先，打开您的终端（Terminal），初始化一个全新的 V3.0 工作区。

# 1. 创建并初始化 V3.0 工作区（推荐同时生成 Roo/Claude 配置）
sros init e2e-data-test --target both
cd e2e-data-test

# 2. 准备一份测试用的 mock 数据 (模拟真实的科研 raw 数据)
mkdir -p data/raw
cat << 'EOF' > data/raw/experiment_scores.csv
subject_id,group,score
sub-01,control,85
sub-02,control,88
sub-03,treatment,95
sub-04,treatment,92
sub-05,control,82
sub-06,treatment,98
EOF


步骤二：唤醒 Claude Code 并注入系统提示

在 e2e-data-test 目录下启动 Claude Code。如果您在 sros init 时已经自动生成了 .clauderc，Claude Code 启动时会自动加载 SROS 的技能说明。

claude


步骤三：输入“魔法指令 (The Golden Prompt)”

在 Claude Code 的交互提示符下，输入以下包含完整意图的 Prompt：

User Prompt 给 Claude Code:
"你是一个数据分析师。请按照以下步骤操作：

使用 sros-skill 查看 data/raw/experiment_scores.csv 的数据结构。

编写一个 Python 脚本（保存到 scripts/plot_scores.py），使用 matplotlib 绘制 control 和 treatment 两组的 score 箱线图（boxplot），并将图片保存到 figures/ 目录（例如 figures/scores_boxplot.png）。

使用 sros-skill 执行这个脚本。

最后，使用 sros-skill manuscript insert，将实验结论和生成的图表路径写入到 draft.md 的末尾（比如新建一个 'Results' 章节）。"

步骤四：观察 Agent 的“自动驾驶”过程

此时，您将体验到“端到端可视化”的极致快感。您会在终端看到 Claude Code 进行如下推理和操作：

[Tool Use] 调用 sros-skill --raw data preview --file data/raw/experiment_scores.csv。

Claude 思考：获取到了列名 subject_id, group, score。

[File Write] 自动在 scripts/plot_scores.py 写入 Python 画图代码。

[Tool Use] 调用 sros-skill --raw data run-script --script scripts/plot_scores.py。

SROS 拦截：SROS 会执行脚本，检测到 figures/ 下新增图片，并在 DuckDB 中建立图谱关联（Script -GENERATES-> Figure），然后返回最终图片路径给 Claude。

[Tool Use] 调用 sros-skill manuscript insert。

Claude 思考：将分析结论和 ![箱线图](figures/xxx.png) 语法插入到 draft.md。

步骤五：验证闭环产物 (Verification Checklist)

测试结束后，请在 VS Code 或终端中检查以下三个“单一事实来源”是否正确更新：

✅ 1. 检查文件树 (Workspace)
您应该看到：

e2e-data-test/
├── scripts/plot_scores.py
└── figures/xxxx_plot.png  <-- SROS 自动捕获并归档的图片


✅ 2. 检查稿件 (draft.md)
打开 draft.md，您应该看到类似下面的内容，并且在 VS Code 预览模式下能直接看到图片：

## Results
实验数据分析表明，Treatment 组的得分显著高于 Control 组。详情如下图所示：
![Scores Boxplot](figures/xxxx_plot.png)


✅ 3. 检查全息图谱 (DuckDB)
如果您想验证数据血缘，可以在终端使用 sqlite/duckdb CLI 工具或通过 Python 脚本快速查询：

# 进入 python 环境简单验证
python -c "
import duckdb
con = duckdb.connect('.sros/graph.db')
print(con.execute("SELECT * FROM edges WHERE relationship = 'GENERATES'").df())
"


预期结果：应看到一条从 scripts/plot_scores.py 指向 figures/xxxx_plot.png 的记录。

3. 下一步迭代建议 (Towards V3.0-GA)

当上述基于 Claude Code 的端到端测试能够 100% 稳定跑通后，SROS 的骨架就已经大成了。下一步建议直接切入 Phase 3 (插件系统与垂直领域扩展)：

固化自动化集成测试 (E2E Tests)：将上面这一套流程用 Python subprocess 或 pytest 写成一个自动化的回归测试脚本（不需要外接真实 Claude API，可以 mock Claude 的命令行调用序列），确保未来重构不会破坏“黄金主线”。

研发 SROS-Neuro-Pack MVP：不要再画简单的散点图了。尝试封装一个真实的轻量级医学影像处理脚本（比如用 nilearn 画一个大脑默认网络图），将其封装成 sros-skill neuro.plot-network，让大模型直接调用。这将形成降维打击 GraphMRI 的初步演示 Demo。