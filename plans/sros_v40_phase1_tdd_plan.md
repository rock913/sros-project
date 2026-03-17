# SROS V4.0 Phase 1（Lit-Pack）TDD 开发计划

目标：以 [doc/SROS V4.0 Phase 1: 文献与知识合成闭环 MVP 测试指南.md](../doc/SROS%20V4.0%20Phase%201:%20%E6%96%87%E7%8C%AE%E4%B8%8E%E7%9F%A5%E8%AF%86%E5%90%88%E6%88%90%E9%97%AD%E7%8E%AF%20MVP%20%E6%B5%8B%E8%AF%95%E6%8C%87%E5%8D%97.md) 的 Omni-Prompt 作为唯一验收口径，完成可回归的端到端闭环。

## Phase 1 必须交付的 Skills（最小集合）

- `ext.web-scrape`：网页抓取 + 最小正文提取（mock/离线可测）
- `scholar.search`：检索入口（兼容别名），内部复用 `scholar.federated-search`
- `scholar.zotero-sync`：把 citekeys 写入本地 `references/`（bib + 可选 pdf 占位）并入库
- `rag.build` / `rag.query`：构建 `document_chunks`，支持 query 返回 top-k chunks（MVP lexical scoring）
- `manuscript.refactor`：面向章节的“可控重写”，并对引用做校验 + 写入 `CITES` 边

## 数据落盘与可验证性（Acceptance）

- Workspace 物理产物：
  - `references/zotero_library.bib` 必须存在并包含传入 citekeys
  - `references/pdfs/`（可选）
- DuckDB `.sros/graph.db`：
  - `citations` 表含 citekey（复用现有 zotero handler）
  - `edges` 表包含 `relationship='CITES'` 的边
  - `document_chunks` 表存在且 chunk_count > 0
- `draft.md`：
  - `Related Work` 章节存在（不存在则创建）
  - 内容包含 `[@citekey]`
  - 若 citekey 不存在于本 workspace，则拒绝写入（防幻觉引用）

## TDD 分解（按测试驱动的提交顺序）

### 1) 先写集成测试（定义“Done”）

新增：`tests/integration/test_v4_phase1_lit_pack_mvp.py`

- 使用 `tmp_path` 构造工作区：
  - `materials/raw_notes/idea_brainstorm.md`（含 URL）
  - `draft.md`（含或不含 `# Related Work`）
- 依次调用（Typer CLI runner or rpc dispatch）：
  - `ext web-scrape`（对 requests 做 monkeypatch，返回固定正文）
  - `scholar search`（mock backend，返回固定 3 篇论文 with citekeys）
  - `scholar zotero-sync`（写 bib + citations 表）
  - `rag build`（source=materials/,references/ 写 document_chunks）
  - `rag query`（query 返回至少 1 chunk）
  - `manuscript refactor`（写入 Related Work + CITES edges）
- 最终断言：文件存在、duckdb 表存在与行数、draft.md 内容。

这一步先失败（红），用来锁定接口。

### 2) ext.web-scrape（单元测试 -> 实现）

新增：
- `src/sros/servers/ext/handler.py`
- `src/sros/skills/cli.py` 增加 `ext` typer 子命令
- `src/sros/skills/rpc.py` 增加 `ext.web_scrape`（RPC 名称建议用 snake_case 与 CLI 对齐）

测试：`tests/unit/test_v4_ext_web_scrape.py`

- requests.get monkeypatch
- 返回 `{ok:true,text:...}` 且错误时 `{ok:false,error:...}`

### 3) scholar.search（兼容层）

改动：
- `src/sros/skills/cli.py` 增加 `scholar search`（内部调用现有 handler）
- 可保留 `federated-search` 作为底层/高级入口

测试：`tests/unit/test_v4_scholar_search_alias.py`

### 4) scholar.zotero-sync（本地落盘 + citations 入库）

改动：
- 复用 `src/sros/servers/zotero/handler.py`（citations 表）
- 新增 `src/sros/servers/scholar/zotero_sync.py`（把 citekeys -> Citation 记录 + bibtex 渲染 + 写文件）
- `src/sros/skills/cli.py` 增加 `scholar zotero-sync`

测试：`tests/unit/test_v4_scholar_zotero_sync.py`

- 断言：`references/zotero_library.bib` 生成；duckdb citations 表插入成功。

### 5) rag.build / rag.query（lexical MVP）

新增：
- `src/sros/servers/rag/handler.py`
- `src/sros/skills/cli.py` 增加 `rag` 子命令
- 表：`document_chunks`

MVP 算法建议：
- build：遍历 source 下的 `.md/.txt/.bib`，按段落或固定字符数切 chunk
- query：对 chunk 做简单 token overlap 计分（`score = sum(token in chunk)`），返回 top-k

测试：`tests/unit/test_v4_rag_build_query.py`

- build 后表存在且 chunk_count>0
- query 返回按 score 排序的 chunks

### 6) manuscript.refactor（章节重写 + 引用校验 + CITES 入库）

新增/改动：
- `src/sros/servers/manuscript/handler.py` 增加 `refactor_section(...)`
- 引用校验：读取 citations 表（或 paper 节点）验证 citekeys
- 写入：复用已有 `_persist_citation_mapping` 或扩展为 section->paper 的 CITES edges（最终落在 edges 表）
- `src/sros/skills/cli.py` 增加 `manuscript refactor`

测试：`tests/unit/test_v4_manuscript_refactor.py`

- citekeys 存在：成功写入并产生 CITES edges
- citekeys 不存在：拒绝写入并返回 `{ok:false,error:...}`

### 7) 回归与兼容性

- 跑：`pytest -q tests/unit/test_v4_*.py tests/integration/test_v4_phase1_lit_pack_mvp.py`
- 在文档中固化 Golden commands（禁止 raw python 逃逸）

## 产出文件清单（建议）

- 代码：
  - `src/sros/servers/ext/handler.py`
  - `src/sros/servers/rag/handler.py`
  - `src/sros/servers/scholar/zotero_sync.py`
  - `src/sros/skills/cli.py`（新增子命令）
  - `src/sros/skills/rpc.py`（新增 dispatch 分支）
- 测试：
  - `tests/integration/test_v4_phase1_lit_pack_mvp.py`
  - `tests/unit/test_v4_ext_web_scrape.py`
  - `tests/unit/test_v4_scholar_search_alias.py`
  - `tests/unit/test_v4_scholar_zotero_sync.py`
  - `tests/unit/test_v4_rag_build_query.py`
  - `tests/unit/test_v4_manuscript_refactor.py`

## 备注

- Phase 1 以可回归为第一优先，所有联网能力必须可被 mock（默认离线也能跑）。
- vss/embedding 作为增强项放到 Phase 1+ 或 Phase 2，不阻塞 Phase 1 MVP。
