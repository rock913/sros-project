# 会话: 增强 Library 和 Document 历史数据展示功能

**日期**: 2025-10-12  
**状态**: ✅ 需求分析完成，已整合到项目文档  
**相关文件**: 
- [ROADMAP.md](../../ROADMAP.md) - Phase 3.5 已添加
- [DEVELOPMENT_STATUS.md](../../DEVELOPMENT_STATUS.md) - 完整进度追踪
- [GEMINI.md](../../GEMINI.md) - 已添加会话示例引用
- [README.md](../../README.md) - 已更新功能列表

**目标**: 
系统化地设计并实现 VS Code Extension 中的历史 Library（文献库）和 Document（文档/报告）的详细展示功能，包括：
1. 梳理完整的 OpenAPI 接口需求 ✅
2. 设计前端界面结构 ✅
3. 制定分阶段开发计划 ✅
4. 整合到项目文档以便追踪 ✅

---

## 文档整合状态

### ✅ 已更新的文档

1. **ROADMAP.md**
   - 添加了完整的 Phase 3.5: Historical Data Management and Advanced Analytics
   - 包含 4 个子阶段的详细计划（7周时间线）
   - 定义了 4 个里程碑 (M1-M4)
   - 列出了 16 个新 API 端点和 4 个数据模型

2. **DEVELOPMENT_STATUS.md** (新建)
   - 全面的开发进度追踪文档
   - 包含所有阶段的完成状态
   - Phase 3.5 的详细任务清单（可勾选）
   - 每周里程碑和验收标准
   - 开发资源和命令参考

3. **GEMINI.md**
   - 更新了"示例调试场景"章节
   - 添加了本会话文档作为"特性规划"示例
   - 补充了开发工作流说明

4. **README.md**
   - 添加了历史数据管理功能说明
   - 添加了研究分析仪表板功能说明
   - 添加了 DEVELOPMENT_STATUS.md 链接

---

## 第一阶段：需求分析与功能设计

### 1.1 当前状态分析

#### 现有前端界面组件
1. **Asset Library View** (资产库视图)
   - 当前功能：展示 `literature_abstracts` 列表
   - 数据源：`GET /agent/state` → `AgentState.literature_abstracts`
   - 展示内容：
     - 论文标题
     - 作者列表（描述）
     - 摘要（tooltip）
   - 限制：
     - ❌ 无历史版本管理
     - ❌ 无详细元数据（DOI, URL, 发布日期等）
     - ❌ 无分类/标签/筛选功能
     - ❌ 无关联研究任务信息

2. **Manuscript View** (手稿视图)
   - 当前功能：展示最新的 `report`
   - 数据源：`GET /agent/state` → `AgentState.report`
   - 展示内容：
     - 完整报告文本（单一 TreeItem）
   - 限制：
     - ❌ 无历史报告版本
     - ❌ 无结构化展示（章节、引用等）
     - ❌ 无编辑/导出功能
     - ❌ 无版本对比功能

3. **Control Panel** (控制面板)
   - 当前功能：展示研究状态摘要
   - 数据源：`GET /agent/state` → 完整 `AgentState`
   - 展示内容：
     - 后端状态
     - 关键指标（论文数、查询数、循环数、字数）
     - 研究详情（主题、知识缺口、查询列表）
   - 限制：
     - ❌ 无历史数据趋势
     - ❌ 无任务列表/时间线

#### 现有后端 API 端点
```
GET  /ok                        - 健康检查
GET  /agent/state               - 获取最新状态（无会话隔离）
GET  /agent/state/{thread_id}   - 获取特定会话状态（需实现 checkpointer）
POST /agent/invoke              - 启动/继续研究任务
```

**关键问题**:
- ✅ 可以获取"当前"状态
- ❌ 无法获取"历史"数据
- ❌ 无会话/任务管理机制
- ❌ 无时间序列数据

---

### 1.2 增强需求定义

#### 核心功能需求

**FR1: 历史文献库管理**
- FR1.1: 展示所有已收集的文献（跨多次研究）
- FR1.2: 按研究任务/会话分组展示
- FR1.3: 文献详细信息（标题、作者、摘要、DOI、URL、收集时间、来源）
- FR1.4: 文献筛选（按关键词、作者、日期、任务）
- FR1.5: 文献排序（时间、相关性、引用次数）
- FR1.6: 文献导出（BibTeX, RIS, JSON）

**FR2: 历史报告/文档管理**
- FR2.1: 展示所有生成的报告（版本历史）
- FR2.2: 按研究任务/会话分组
- FR2.3: 报告元数据（生成时间、字数、关联文献数）
- FR2.4: 报告结构化展示（章节、引用）
- FR2.5: 报告版本对比
- FR2.6: 报告导出（Markdown, PDF, HTML）

**FR3: 研究任务/会话管理**
- FR3.1: 任务列表（所有历史研究）
- FR3.2: 任务详情（主题、状态、创建时间、完成时间）
- FR3.3: 任务时间线（关键事件记录）
- FR3.4: 任务切换（查看不同任务的数据）
- FR3.5: 任务删除/归档

**FR4: 数据统计与可视化**
- FR4.1: 总体统计（总论文数、总报告数、总任务数）
- FR4.2: 趋势分析（每日/每周活动）
- FR4.3: 关键词云图
- FR4.4: 作者网络图

---

## 第二阶段：OpenAPI 接口需求梳理

### 2.1 数据模型设计

#### 核心实体

**1. ResearchSession (研究会话)**
```yaml
ResearchSession:
  type: object
  properties:
    session_id:
      type: string
      format: uuid
      description: 会话唯一标识
    research_topic:
      type: string
      description: 研究主题
    status:
      type: string
      enum: [pending, in_progress, completed, failed]
      description: 会话状态
    created_at:
      type: string
      format: date-time
      description: 创建时间
    updated_at:
      type: string
      format: date-time
      description: 最后更新时间
    completed_at:
      type: string
      format: date-time
      nullable: true
      description: 完成时间
    metadata:
      type: object
      properties:
        total_papers:
          type: integer
        total_queries:
          type: integer
        loop_count:
          type: integer
        is_sufficient:
          type: boolean
```

**2. Paper (文献)**
```yaml
Paper:
  type: object
  properties:
    paper_id:
      type: string
      format: uuid
      description: 文献唯一标识
    session_id:
      type: string
      format: uuid
      description: 所属会话ID
    title:
      type: string
      description: 论文标题
    authors:
      type: array
      items:
        type: string
      description: 作者列表
    abstract:
      type: string
      description: 摘要
    summary:
      type: string
      nullable: true
      description: AI 生成的摘要
    doi:
      type: string
      nullable: true
      description: DOI
    url:
      type: string
      format: uri
      nullable: true
      description: 论文链接
    arxiv_id:
      type: string
      nullable: true
      description: ArXiv ID
    published_date:
      type: string
      format: date
      nullable: true
      description: 发布日期
    source:
      type: string
      enum: [arxiv, pubmed, semantic_scholar, manual]
      description: 来源
    collected_at:
      type: string
      format: date-time
      description: 收集时间
    tags:
      type: array
      items:
        type: string
      description: 标签
    relevance_score:
      type: number
      format: float
      nullable: true
      description: 相关性评分
```

**3. Report (报告)**
```yaml
Report:
  type: object
  properties:
    report_id:
      type: string
      format: uuid
      description: 报告唯一标识
    session_id:
      type: string
      format: uuid
      description: 所属会话ID
    version:
      type: integer
      description: 版本号
    content:
      type: string
      description: 报告内容（Markdown）
    word_count:
      type: integer
      description: 字数
    paper_count:
      type: integer
      description: 引用文献数
    generated_at:
      type: string
      format: date-time
      description: 生成时间
    metadata:
      type: object
      properties:
        structure:
          type: object
          description: 报告结构（章节信息）
        citations:
          type: array
          items:
            type: string
          description: 引用的 paper_id 列表
```

**4. SessionEvent (会话事件)**
```yaml
SessionEvent:
  type: object
  properties:
    event_id:
      type: string
      format: uuid
    session_id:
      type: string
      format: uuid
    event_type:
      type: string
      enum: [session_created, query_generated, search_executed, paper_collected, report_generated, session_completed]
    timestamp:
      type: string
      format: date-time
    details:
      type: object
      description: 事件详情（动态内容）
```

---

### 2.2 完整 API 端点设计

#### 2.2.1 会话管理接口

**1. 获取所有会话列表**
```yaml
GET /sessions
summary: "获取所有研究会话列表"
tags: [Sessions]
parameters:
  - name: status
    in: query
    schema:
      type: string
      enum: [pending, in_progress, completed, failed]
    description: "按状态筛选"
  - name: limit
    in: query
    schema:
      type: integer
      default: 20
    description: "返回数量限制"
  - name: offset
    in: query
    schema:
      type: integer
      default: 0
    description: "分页偏移"
  - name: sort_by
    in: query
    schema:
      type: string
      enum: [created_at, updated_at]
      default: created_at
    description: "排序字段"
  - name: order
    in: query
    schema:
      type: string
      enum: [asc, desc]
      default: desc
    description: "排序方向"
responses:
  '200':
    description: "成功返回会话列表"
    content:
      application/json:
        schema:
          type: object
          properties:
            sessions:
              type: array
              items:
                $ref: '#/components/schemas/ResearchSession'
            total:
              type: integer
            limit:
              type: integer
            offset:
              type: integer
```

**2. 获取单个会话详情**
```yaml
GET /sessions/{session_id}
summary: "获取特定会话的详细信息"
tags: [Sessions]
parameters:
  - name: session_id
    in: path
    required: true
    schema:
      type: string
      format: uuid
responses:
  '200':
    description: "成功返回会话详情"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ResearchSession'
  '404':
    description: "会话不存在"
```

**3. 创建新会话**
```yaml
POST /sessions
summary: "创建新的研究会话"
tags: [Sessions]
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        properties:
          research_topic:
            type: string
        required:
          - research_topic
responses:
  '201':
    description: "会话创建成功"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ResearchSession'
```

**4. 删除会话**
```yaml
DELETE /sessions/{session_id}
summary: "删除指定会话及其所有关联数据"
tags: [Sessions]
parameters:
  - name: session_id
    in: path
    required: true
    schema:
      type: string
      format: uuid
responses:
  '204':
    description: "删除成功"
  '404':
    description: "会话不存在"
```

---

#### 2.2.2 文献管理接口

**5. 获取文献列表**
```yaml
GET /papers
summary: "获取文献列表（支持多维度筛选）"
tags: [Papers]
parameters:
  - name: session_id
    in: query
    schema:
      type: string
      format: uuid
    description: "按会话ID筛选"
  - name: search
    in: query
    schema:
      type: string
    description: "搜索关键词（标题、作者、摘要）"
  - name: source
    in: query
    schema:
      type: string
      enum: [arxiv, pubmed, semantic_scholar, manual]
    description: "按来源筛选"
  - name: date_from
    in: query
    schema:
      type: string
      format: date
    description: "发布日期起始"
  - name: date_to
    in: query
    schema:
      type: string
      format: date
    description: "发布日期结束"
  - name: tags
    in: query
    schema:
      type: array
      items:
        type: string
    description: "按标签筛选（逗号分隔）"
  - name: limit
    in: query
    schema:
      type: integer
      default: 50
  - name: offset
    in: query
    schema:
      type: integer
      default: 0
  - name: sort_by
    in: query
    schema:
      type: string
      enum: [collected_at, published_date, relevance_score, title]
      default: collected_at
  - name: order
    in: query
    schema:
      type: string
      enum: [asc, desc]
      default: desc
responses:
  '200':
    description: "成功返回文献列表"
    content:
      application/json:
        schema:
          type: object
          properties:
            papers:
              type: array
              items:
                $ref: '#/components/schemas/Paper'
            total:
              type: integer
            limit:
              type: integer
            offset:
              type: integer
```

**6. 获取单个文献详情**
```yaml
GET /papers/{paper_id}
summary: "获取特定文献的详细信息"
tags: [Papers]
parameters:
  - name: paper_id
    in: path
    required: true
    schema:
      type: string
      format: uuid
responses:
  '200':
    description: "成功返回文献详情"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Paper'
  '404':
    description: "文献不存在"
```

**7. 导出文献**
```yaml
GET /papers/export
summary: "导出文献列表为指定格式"
tags: [Papers]
parameters:
  - name: session_id
    in: query
    schema:
      type: string
      format: uuid
    description: "导出特定会话的文献"
  - name: paper_ids
    in: query
    schema:
      type: array
      items:
        type: string
        format: uuid
    description: "导出指定文献（逗号分隔）"
  - name: format
    in: query
    required: true
    schema:
      type: string
      enum: [bibtex, ris, json, csv]
    description: "导出格式"
responses:
  '200':
    description: "成功导出"
    content:
      application/x-bibtex:
        schema:
          type: string
      application/x-research-info-systems:
        schema:
          type: string
      application/json:
        schema:
          type: array
          items:
            $ref: '#/components/schemas/Paper'
      text/csv:
        schema:
          type: string
```

---

#### 2.2.3 报告管理接口

**8. 获取报告列表**
```yaml
GET /reports
summary: "获取报告列表"
tags: [Reports]
parameters:
  - name: session_id
    in: query
    schema:
      type: string
      format: uuid
    description: "按会话ID筛选"
  - name: limit
    in: query
    schema:
      type: integer
      default: 20
  - name: offset
    in: query
    schema:
      type: integer
      default: 0
  - name: sort_by
    in: query
    schema:
      type: string
      enum: [generated_at, version]
      default: generated_at
  - name: order
    in: query
    schema:
      type: string
      enum: [asc, desc]
      default: desc
responses:
  '200':
    description: "成功返回报告列表"
    content:
      application/json:
        schema:
          type: object
          properties:
            reports:
              type: array
              items:
                $ref: '#/components/schemas/Report'
            total:
              type: integer
```

**9. 获取单个报告详情**
```yaml
GET /reports/{report_id}
summary: "获取特定报告的详细内容"
tags: [Reports]
parameters:
  - name: report_id
    in: path
    required: true
    schema:
      type: string
      format: uuid
responses:
  '200':
    description: "成功返回报告详情"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Report'
  '404':
    description: "报告不存在"
```

**10. 获取会话的最新报告**
```yaml
GET /sessions/{session_id}/reports/latest
summary: "获取指定会话的最新报告"
tags: [Reports]
parameters:
  - name: session_id
    in: path
    required: true
    schema:
      type: string
      format: uuid
responses:
  '200':
    description: "成功返回最新报告"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Report'
  '404':
    description: "报告不存在"
```

**11. 对比两个报告版本**
```yaml
GET /reports/{report_id1}/compare/{report_id2}
summary: "对比两个报告的差异"
tags: [Reports]
parameters:
  - name: report_id1
    in: path
    required: true
    schema:
      type: string
      format: uuid
  - name: report_id2
    in: path
    required: true
    schema:
      type: string
      format: uuid
responses:
  '200':
    description: "成功返回差异信息"
    content:
      application/json:
        schema:
          type: object
          properties:
            diff:
              type: string
              description: "差异（unified diff 格式）"
            added_lines:
              type: integer
            removed_lines:
              type: integer
            modified_sections:
              type: array
              items:
                type: string
```

**12. 导出报告**
```yaml
GET /reports/{report_id}/export
summary: "导出报告为指定格式"
tags: [Reports]
parameters:
  - name: report_id
    in: path
    required: true
    schema:
      type: string
      format: uuid
  - name: format
    in: query
    required: true
    schema:
      type: string
      enum: [markdown, html, pdf, docx]
responses:
  '200':
    description: "成功导出"
    content:
      text/markdown:
        schema:
          type: string
      text/html:
        schema:
          type: string
      application/pdf:
        schema:
          type: string
          format: binary
      application/vnd.openxmlformats-officedocument.wordprocessingml.document:
        schema:
          type: string
          format: binary
```

---

#### 2.2.4 会话事件与时间线接口

**13. 获取会话事件时间线**
```yaml
GET /sessions/{session_id}/events
summary: "获取指定会话的事件时间线"
tags: [Sessions, Events]
parameters:
  - name: session_id
    in: path
    required: true
    schema:
      type: string
      format: uuid
  - name: event_type
    in: query
    schema:
      type: string
      enum: [session_created, query_generated, search_executed, paper_collected, report_generated, session_completed]
    description: "按事件类型筛选"
  - name: limit
    in: query
    schema:
      type: integer
      default: 100
  - name: offset
    in: query
    schema:
      type: integer
      default: 0
responses:
  '200':
    description: "成功返回事件列表"
    content:
      application/json:
        schema:
          type: object
          properties:
            events:
              type: array
              items:
                $ref: '#/components/schemas/SessionEvent'
            total:
              type: integer
```

---

#### 2.2.5 统计与分析接口

**14. 获取全局统计**
```yaml
GET /stats/global
summary: "获取全局统计信息"
tags: [Statistics]
responses:
  '200':
    description: "成功返回统计信息"
    content:
      application/json:
        schema:
          type: object
          properties:
            total_sessions:
              type: integer
            total_papers:
              type: integer
            total_reports:
              type: integer
            active_sessions:
              type: integer
            completed_sessions:
              type: integer
            total_queries_executed:
              type: integer
            avg_papers_per_session:
              type: number
              format: float
            avg_report_length:
              type: integer
```

**15. 获取趋势数据**
```yaml
GET /stats/trends
summary: "获取活动趋势数据"
tags: [Statistics]
parameters:
  - name: period
    in: query
    schema:
      type: string
      enum: [day, week, month]
      default: week
    description: "统计周期"
  - name: metric
    in: query
    schema:
      type: string
      enum: [sessions, papers, reports]
      default: sessions
    description: "统计指标"
responses:
  '200':
    description: "成功返回趋势数据"
    content:
      application/json:
        schema:
          type: object
          properties:
            data_points:
              type: array
              items:
                type: object
                properties:
                  date:
                    type: string
                    format: date
                  count:
                    type: integer
```

**16. 获取关键词分析**
```yaml
GET /stats/keywords
summary: "获取高频关键词统计"
tags: [Statistics]
parameters:
  - name: limit
    in: query
    schema:
      type: integer
      default: 50
    description: "返回关键词数量"
responses:
  '200':
    description: "成功返回关键词列表"
    content:
      application/json:
        schema:
          type: object
          properties:
            keywords:
              type: array
              items:
                type: object
                properties:
                  word:
                    type: string
                  count:
                    type: integer
                  weight:
                    type: number
                    format: float
```

---

### 2.3 API 端点总结

| 编号 | 方法 | 端点 | 功能 | 优先级 |
|------|------|------|------|--------|
| 1 | GET | `/sessions` | 获取所有会话列表 | 🔴 高 |
| 2 | GET | `/sessions/{session_id}` | 获取单个会话详情 | 🔴 高 |
| 3 | POST | `/sessions` | 创建新会话 | 🔴 高 |
| 4 | DELETE | `/sessions/{session_id}` | 删除会话 | 🟡 中 |
| 5 | GET | `/papers` | 获取文献列表（多维筛选） | 🔴 高 |
| 6 | GET | `/papers/{paper_id}` | 获取单个文献详情 | 🟡 中 |
| 7 | GET | `/papers/export` | 导出文献 | 🟢 低 |
| 8 | GET | `/reports` | 获取报告列表 | 🔴 高 |
| 9 | GET | `/reports/{report_id}` | 获取单个报告详情 | 🔴 高 |
| 10 | GET | `/sessions/{session_id}/reports/latest` | 获取会话最新报告 | 🔴 高 |
| 11 | GET | `/reports/{id1}/compare/{id2}` | 对比报告版本 | 🟢 低 |
| 12 | GET | `/reports/{report_id}/export` | 导出报告 | 🟡 中 |
| 13 | GET | `/sessions/{session_id}/events` | 获取会话事件时间线 | 🟡 中 |
| 14 | GET | `/stats/global` | 获取全局统计 | 🟡 中 |
| 15 | GET | `/stats/trends` | 获取趋势数据 | 🟢 低 |
| 16 | GET | `/stats/keywords` | 获取关键词分析 | 🟢 低 |

---

## 第三阶段：前端界面设计

### 3.1 界面结构重构

#### 当前布局
```
Sidebar (Activity Bar):
├── Asset Library (TreeView)
└── Manuscript (TreeView)
```

#### 增强后的布局
```
Sidebar (Activity Bar): Auto-Researcher
├── 📚 Sessions (TreeView - 新增)
│   ├── 📁 Active Sessions
│   │   ├── Session 1 (expandable)
│   │   │   ├── 📄 Papers (5)
│   │   │   ├── 📝 Reports (2)
│   │   │   └── ⏱️  Timeline
│   │   └── Session 2
│   └── 📁 Completed Sessions
│       └── Session 3
├── 📖 Library (TreeView - 增强)
│   ├── 📁 By Session
│   │   ├── Session 1 Papers (5)
│   │   └── Session 2 Papers (3)
│   ├── 📁 By Source
│   │   ├── ArXiv (6)
│   │   └── PubMed (2)
│   └── 📁 By Date
│       ├── This Week (4)
│       └── Last Month (4)
├── 📄 Documents (TreeView - 增强)
│   ├── 📁 By Session
│   │   ├── Session 1 Reports (2)
│   │   └── Session 2 Reports (1)
│   └── 📁 Recent Reports
│       ├── Report v2 (Latest)
│       └── Report v1
└── 📊 Analytics (Webview - 新增)
    └── Dashboard
```

### 3.2 详细视图设计

#### 3.2.1 Sessions View (会话视图)

**功能**:
- 展示所有研究会话（活跃/已完成）
- 可展开查看会话详情（论文、报告、时间线）
- 右键菜单：查看详情、切换到会话、删除会话

**TreeView 数据结构**:
```typescript
interface SessionTreeItem {
  type: 'session' | 'papers_group' | 'reports_group' | 'timeline_link';
  session?: ResearchSession;
  count?: number;
}
```

**交互**:
- 单击会话：展开/折叠
- 双击会话：在 Webview 中打开会话详情
- 点击 "Papers (5)"：打开该会话的论文列表
- 点击 "Reports (2)"：打开该会话的报告列表
- 点击 "Timeline"：打开该会话的事件时间线

#### 3.2.2 Enhanced Library View (增强文献库视图)

**功能**:
- 多维度分组（会话、来源、日期）
- 文献详情悬浮提示（tooltip）
- 点击打开详情 Webview
- 右键菜单：导出选中、添加标签、查看相关报告

**TreeView 数据结构**:
```typescript
interface LibraryTreeItem {
  type: 'group' | 'paper';
  groupName?: string;
  paper?: Paper;
}
```

**文献详情 Webview**:
```
┌─────────────────────────────────────┐
│ 📄 Paper Details                    │
├─────────────────────────────────────┤
│ Title: [Paper Title]                │
│ Authors: [Author List]              │
│ Published: 2024-01-15               │
│ Source: ArXiv (arXiv:2401.12345)    │
│ DOI: 10.1234/example                │
│ URL: [Link]                         │
│                                     │
│ Abstract:                           │
│ [Full Abstract Text...]             │
│                                     │
│ AI Summary:                         │
│ [AI Generated Summary...]           │
│                                     │
│ Collected: 2025-01-20 10:30 AM      │
│ Session: "AI in Climate Change"     │
│ Tags: [machine-learning, climate]   │
│                                     │
│ [Open URL] [Export] [Add Tags]      │
└─────────────────────────────────────┘
```

#### 3.2.3 Enhanced Documents View (增强文档视图)

**功能**:
- 按会话分组展示报告
- 显示版本号和生成时间
- 点击打开报告内容（只读编辑器或 Webview）
- 右键菜单：导出、对比版本、查看引用文献

**TreeView 数据结构**:
```typescript
interface DocumentTreeItem {
  type: 'group' | 'report';
  groupName?: string;
  report?: Report;
}
```

**报告详情 Webview**:
```
┌─────────────────────────────────────┐
│ 📝 Report Details                   │
├─────────────────────────────────────┤
│ Session: "AI in Climate Change"     │
│ Version: 2 (Latest)                 │
│ Generated: 2025-01-20 11:45 AM      │
│ Word Count: 3,245                   │
│ Citations: 15 papers                │
│                                     │
│ [View Previous Version] [Export]    │
│ [Compare with v1] [View Citations]  │
├─────────────────────────────────────┤
│ Content:                            │
│                                     │
│ # Research Report                   │
│                                     │
│ ## Introduction                     │
│ [Report content in Markdown...]     │
│                                     │
│ ## Methodology                      │
│ ...                                 │
└─────────────────────────────────────┘
```

#### 3.2.4 Analytics Dashboard (分析仪表板)

**Webview 内容**:
```
┌─────────────────────────────────────┐
│ 📊 Auto-Researcher Analytics        │
├─────────────────────────────────────┤
│ 📈 Global Statistics                │
│ ├─ Total Sessions: 12               │
│ ├─ Total Papers: 156                │
│ ├─ Total Reports: 18                │
│ └─ Active Sessions: 2               │
├─────────────────────────────────────┤
│ 📉 Activity Trend (Last 7 Days)     │
│ [Line Chart: Papers collected/day]  │
├─────────────────────────────────────┤
│ ☁️  Top Keywords                     │
│ [Word Cloud Visualization]          │
├─────────────────────────────────────┤
│ 👥 Top Authors                      │
│ 1. Author A (12 papers)             │
│ 2. Author B (8 papers)              │
│ 3. Author C (6 papers)              │
└─────────────────────────────────────┘
```

---

## 第四阶段：分阶段开发计划

### Phase 1: 基础数据持久化与会话管理 (2 周)

**目标**: 建立数据库基础设施，实现会话和历史数据的持久化

#### 后端任务
1. **数据库设计与迁移** (3 天)
   - [ ] 设计数据库 Schema（PostgreSQL）
   - [ ] 创建表：`sessions`, `papers`, `reports`, `session_events`
   - [ ] 编写数据库迁移脚本（Alembic）
   - [ ] 测试数据库连接和迁移

2. **实现核心数据模型** (2 天)
   - [ ] 创建 SQLAlchemy 模型（`ResearchSession`, `Paper`, `Report`, `SessionEvent`）
   - [ ] 实现 CRUD 操作（Database Repository 层）
   - [ ] 编写单元测试

3. **实现会话管理 API** (3 天)
   - [ ] `GET /sessions` - 会话列表
   - [ ] `GET /sessions/{session_id}` - 会话详情
   - [ ] `POST /sessions` - 创建会话
   - [ ] `DELETE /sessions/{session_id}` - 删除会话
   - [ ] 编写 API 测试

4. **集成 LangGraph 与会话管理** (4 天)
   - [ ] 修改 `graph.compile()` 添加 `SqliteSaver` 或 `PostgresSaver`
   - [ ] 在 `POST /agent/invoke` 中自动创建/更新 Session
   - [ ] 在研究流程中自动记录 Papers
   - [ ] 在报告生成时自动创建 Report 记录
   - [ ] 记录 SessionEvents（关键节点）
   - [ ] 测试完整流程

#### 前端任务
5. **创建 Sessions TreeView** (2 天)
   - [ ] 创建 `SessionsProvider` 实现
   - [ ] 调用 `GET /sessions` API
   - [ ] 展示会话列表（基础版）
   - [ ] 注册命令：刷新会话列表
   - [ ] 编写前端测试

**验收标准**:
- ✅ 数据库正确存储所有会话、论文、报告
- ✅ 启动新研究任务时自动创建 Session
- ✅ 前端能显示历史会话列表
- ✅ 所有 API 测试通过

---

### Phase 2: 文献库与报告历史管理 (2 周)

**目标**: 实现文献和报告的完整 CRUD 和展示

#### 后端任务
1. **实现文献管理 API** (4 天)
   - [ ] `GET /papers` - 文献列表（支持筛选、排序、分页）
   - [ ] `GET /papers/{paper_id}` - 文献详情
   - [ ] `GET /papers/export` - 导出文献（BibTeX, JSON）
   - [ ] 实现高级搜索（全文搜索）
   - [ ] 编写 API 测试

2. **实现报告管理 API** (3 天)
   - [ ] `GET /reports` - 报告列表
   - [ ] `GET /reports/{report_id}` - 报告详情
   - [ ] `GET /sessions/{session_id}/reports/latest` - 最新报告
   - [ ] `GET /reports/{report_id}/export` - 导出报告（Markdown, HTML）
   - [ ] 编写 API 测试

3. **实现会话事件 API** (2 天)
   - [ ] `GET /sessions/{session_id}/events` - 事件时间线
   - [ ] 在关键节点记录事件
   - [ ] 编写 API 测试

#### 前端任务
4. **增强 Library TreeView** (3 天)
   - [ ] 重构 `AssetLibraryProvider`
   - [ ] 调用 `GET /papers` API
   - [ ] 实现多维度分组（会话、来源、日期）
   - [ ] 创建文献详情 Webview
   - [ ] 右键菜单：导出、查看详情
   - [ ] 编写前端测试

5. **增强 Documents TreeView** (3 天)
   - [ ] 重构 `ManuscriptProvider`
   - [ ] 调用 `GET /reports` API
   - [ ] 按会话分组展示报告
   - [ ] 创建报告详情 Webview（Markdown 渲染）
   - [ ] 右键菜单：导出、对比版本
   - [ ] 编写前端测试

**验收标准**:
- ✅ 可以查看所有历史文献（跨会话）
- ✅ 可以查看所有历史报告（带版本）
- ✅ 可以导出文献和报告
- ✅ 前端测试覆盖率 > 80%

---

### Phase 3: 高级功能与统计分析 (1.5 周)

**目标**: 实现高级功能和数据分析

#### 后端任务
1. **实现统计分析 API** (3 天)
   - [ ] `GET /stats/global` - 全局统计
   - [ ] `GET /stats/trends` - 趋势数据
   - [ ] `GET /stats/keywords` - 关键词分析
   - [ ] 实现后台数据聚合任务
   - [ ] 编写 API 测试

2. **实现报告对比功能** (2 天)
   - [ ] `GET /reports/{id1}/compare/{id2}` - 版本对比
   - [ ] 使用 difflib 或类似库生成 diff
   - [ ] 编写 API 测试

#### 前端任务
3. **创建 Analytics Dashboard** (3 天)
   - [ ] 创建分析仪表板 Webview
   - [ ] 调用统计 API
   - [ ] 集成图表库（Chart.js 或 D3.js）
   - [ ] 展示趋势、关键词云图、作者统计
   - [ ] 注册命令：打开分析面板

4. **完善 Sessions TreeView** (2 天)
   - [ ] 可展开显示会话下的论文/报告/时间线
   - [ ] 实现会话切换功能
   - [ ] 右键菜单：查看详情、删除
   - [ ] 集成到现有界面

**验收标准**:
- ✅ 可以查看全局统计数据
- ✅ 可以对比不同版本的报告
- ✅ Analytics Dashboard 正常展示图表
- ✅ Sessions TreeView 功能完整

---

### Phase 4: 优化与完善 (1 周)

**目标**: 性能优化、用户体验优化、文档完善

#### 任务
1. **性能优化** (2 天)
   - [ ] 数据库查询优化（添加索引）
   - [ ] API 响应时间优化（缓存）
   - [ ] 前端数据加载优化（懒加载、虚拟滚动）
   - [ ] 性能测试

2. **用户体验优化** (2 天)
   - [ ] 添加加载状态指示器
   - [ ] 添加错误处理和友好提示
   - [ ] 优化界面布局和交互
   - [ ] 添加键盘快捷键

3. **文档与测试完善** (2 天)
   - [ ] 更新 `openapi.yaml`
   - [ ] 更新 `API_DOCUMENTATION.md`
   - [ ] 更新 VS Code Extension README
   - [ ] 完善单元测试和集成测试
   - [ ] 编写用户手册

4. **E2E 测试** (1 天)
   - [ ] 编写完整的 E2E 测试场景
   - [ ] 运行并修复发现的问题
   - [ ] 记录测试结果

**验收标准**:
- ✅ 所有 API 响应时间 < 500ms
- ✅ 前端交互流畅，无明显卡顿
- ✅ 测试覆盖率 > 85%
- ✅ 文档完整且准确
- ✅ E2E 测试全部通过

---

## 第五阶段：总结与交付

### 开发时间线

```
Week 1-2:  Phase 1 - 基础数据持久化与会话管理
Week 3-4:  Phase 2 - 文献库与报告历史管理
Week 5-6:  Phase 3 - 高级功能与统计分析
Week 7:    Phase 4 - 优化与完善
```

**总计**: 7 周（约 1.5 个月）

### 关键里程碑

- **M1 (Week 2)**: 会话管理基础设施完成
- **M2 (Week 4)**: 文献和报告历史展示完成
- **M3 (Week 6)**: 所有高级功能实现完成
- **M4 (Week 7)**: 系统优化并准备发布

### 风险与依赖

**风险**:
1. 数据库迁移可能影响现有数据
2. LangGraph Checkpointer 集成可能复杂
3. 前端图表库性能问题

**缓解措施**:
1. 提供数据备份和迁移脚本
2. 充分的集成测试
3. 选择轻量级图表库，实现懒加载

---

## 附录：技术栈建议

### 后端
- **数据库**: PostgreSQL + pgvector（已有）
- **ORM**: SQLAlchemy
- **迁移**: Alembic
- **Checkpointer**: `langgraph.checkpoint.postgres.PostgresSaver`
- **导出**: 
  - BibTeX: `bibtexparser`
  - PDF: `WeasyPrint` 或 `ReportLab`
  - Diff: `difflib` (Python 标准库)

### 前端
- **图表**: Chart.js（轻量）或 D3.js（强大）
- **Markdown 渲染**: `marked` + `highlight.js`
- **Diff 展示**: `diff2html`
- **虚拟滚动**: VS Code API 内置支持

---

**会话状态**: ✅ 需求分析完成，已整合到项目文档，准备开始实施

---

## 下一步行动

### 准备工作检查清单

在开始 Phase 3.5.1 实施前，需确认以下准备工作：

- [x] 完整的 OpenAPI 接口需求梳理
- [x] 数据模型设计（4个核心实体）
- [x] 前端界面结构规划
- [x] 分阶段开发计划（7周时间线）
- [x] 项目文档更新（ROADMAP.md, DEVELOPMENT_STATUS.md, GEMINI.md, README.md）
- [ ] 用户/利益相关者确认需求
- [ ] 技术栈选型确认（SQLAlchemy, Alembic, Chart.js）
- [ ] 开发环境准备（Docker, PostgreSQL, 依赖安装）
- [ ] 分支策略确认（是否创建 feature/phase-3.5 分支）

### 实施启动流程

1. **用户确认**: 等待用户批准开始实施
2. **环境准备**: 确保开发环境就绪
3. **创建开发分支**: 
   ```bash
   git checkout -b feature/phase-3.5-historical-data-management
   ```
4. **启动 Phase 3.5.1**: 从数据库设计开始
5. **持续更新**: 在 DEVELOPMENT_STATUS.md 中勾选完成的任务

### 建议的实施会话

为了保持 Session-Driven Workflow，建议为每个 Phase 创建独立的开发会话日志：

- `.ai-sessions/development/2025-10-12-phase-3.5.1-database-foundation.md`
- `.ai-sessions/development/2025-10-XX-phase-3.5.2-literature-report-history.md`
- `.ai-sessions/development/2025-10-XX-phase-3.5.3-analytics-visualization.md`
- `.ai-sessions/development/2025-10-XX-phase-3.5.4-optimization-production.md`

每个会话日志应包含：
- 任务清单（从 DEVELOPMENT_STATUS.md 复制）
- 实施细节和代码更改记录
- 测试结果验证
- 遇到的问题和解决方案

---

## 文档资源汇总

本次规划会话已完成以下文档的创建和更新：

### 新建文档
1. **DEVELOPMENT_STATUS.md** - 完整的开发状态追踪文档
   - 所有阶段的进度总览
   - Phase 3.5 的详细任务清单
   - 每周里程碑和验收标准
   - 开发命令和资源引用

2. **doc/PHASE_3.5_QUICK_REFERENCE.md** - Phase 3.5 快速参考指南
   - 数据架构可视化
   - 16 个 API 端点总览
   - 4 个前端组件详细说明
   - 实施时间线和测试策略
   - 依赖和数据库schema

### 更新文档
1. **ROADMAP.md**
   - 添加完整的 Phase 3.5 章节
   - 包含 4 个子阶段的详细计划
   - 定义了 4 个里程碑 (M1-M4)

2. **README.md**
   - 更新了功能列表（添加历史数据管理和分析仪表板）
   - 添加了 DEVELOPMENT_STATUS.md 链接

3. **GEMINI.md**
   - 更新了"示例调试场景"章节
   - 添加了本会话作为"特性规划"示例

### 参考结构

```
gemini-fullstack-langgraph-quickstart/
├── README.md                              # ✅ 已更新 - 添加新功能说明
├── ROADMAP.md                             # ✅ 已更新 - 添加 Phase 3.5
├── GEMINI.md                              # ✅ 已更新 - 添加会话引用
├── DEVELOPMENT_STATUS.md                  # 🆕 新建 - 进度追踪
├── openapi.yaml                           # ⏳ 待更新 (Phase 3.5.4)
├── doc/
│   ├── WORKFLOW_STRATEGY.md               # 现有 - 开发工作流
│   ├── PHASE_3.5_QUICK_REFERENCE.md       # 🆕 新建 - 快速参考
│   └── ...
├── .ai-sessions/
│   └── development/
│       ├── 2025-10-12-enhance-library-document-display.md  # 本会话
│       ├── 2025-10-12-phase-3.5.1-database-foundation.md   # ⏳ 待创建
│       └── ...
└── backend/
    └── API_DOCUMENTATION.md               # ⏳ 待更新 (Phase 3.5.4)
```

---

**等待用户指令**: 需要我立即开始 Phase 3.5.1 的实施吗？或者您想先审查计划并进行调整？
