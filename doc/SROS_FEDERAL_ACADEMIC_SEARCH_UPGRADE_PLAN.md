# SROS联邦学术搜索升级完整开发计划

## 1. 项目概述

本计划详细描述了将现有的Semantic Scholar MCP服务器升级为支持OpenAlex + Unpaywall + Semantic Scholar联邦架构的完整开发方案。该升级将保持与现有接口的兼容性，同时提供更丰富的学术资源访问能力和更高的性能。

## 2. 设计目标

### 2.1 核心目标
- 使用OpenAlex作为主要的学术搜索引擎
- 使用Unpaywall专门负责开放获取PDF的下载
- 保留Semantic Scholar作为语义增强层
- 保持与现有Semantic Scholar API相似的接口
- 实现高性能、高可用的学术搜索服务

### 2.2 功能目标
- 论文搜索（关键词、作者、标题）
- 论文详细信息获取
- 引用上下文检索
- 参考文献获取
- 开放获取PDF下载
- TLDR摘要获取
- 缓存管理和统计

## 3. 系统架构设计

### 3.1 联邦架构图示

```
┌─────────────────┐    ┌──────────────┐    ┌────────────────┐
│   OpenAlex API  │    │ Unpaywall API│    │ Semantic Scholar│
│  (主搜索引擎)   │    │ (PDF获取服务)│    │ (语义增强层)    │
└─────────┬───────┘    └──────┬───────┘    └───────┬────────┘
          │                   │                    │
          └─────────┬─────────┴────────────────────┘
                    │
    ┌───────────────▼──────────────────────────────┐
    │          AcademicSearchManager               │
    │  • OpenAlexSearchProvider (核心检索)          │
    │  • UnpaywallPDFProvider (路由下载)            │
    │  • S2EnrichmentProvider (语义补充)            │
    │  • ResultTransformer (模型映射与兼容)         │
    │  • CacheManager (持久化缓存)                  │
    │  • RateLimiter (速率控制)                     │
    │  • CircuitBreaker (熔断器)                    │
    └───────────────┬──────────────────────────────┘
                    │
          ┌──────────▼──────────┐
          │     MCP Handler      │
          │  (保持原S2接口签名)  │
          └─────────────────────┘
```

### 3.2 核心组件说明

#### 3.2.1 联邦 Provider 集成
- **OpenAlexSearchProvider**: 负责 90% 的检索任务，包括关键词、作者、标题搜索
- **UnpaywallPDFProvider**: 专门负责根据 DOI 寻找最佳开放获取（OA）链接
- **S2EnrichmentProvider**: 按需调用。仅在用户请求 tldr 或 citationContext 时触发

#### 3.2.2 ResultTransformer (兼容性核心)
负责将不同源的数据映射到统一的内部模型，并输出兼容原 S2 接口的格式：

- `id` (OpenAlex ID) -> `paperId`
- `display_name` -> `title`
- `cited_by_count` -> `citationCount`
- `best_oa_location.url` -> `openAccessPdf`

#### 3.2.3 CacheManager (持久化缓存)
使用 SQLite 存储已检索的元数据和 PDF 链接，实现零延迟响应和API配额节省。

#### 3.2.4 RateLimiter (速率控制)
控制各数据源的API调用频率，避免触发限制。

#### 3.2.5 CircuitBreaker (熔断器)
当某个数据源出现问题时，自动切换到降级模式。

## 4. 核心代码实现框架

```python
import asyncio
import aiohttp
from typing import List, Optional, Dict

class AcademicSearchManager:
    def __init__(self, email: str, s2_key: str = ""):
        self.email = email
        self.s2_key = s2_key
        self.headers = {"User-Agent": f"SROS-MCP (mailto:{email})"}

    async def search_papers(self, query: str, limit: int = 10):
        """
        核心逻辑：联邦检索
        1. OpenAlex 获取基础列表
        2. 并发从 Unpaywall 获取 PDF，从 S2 获取 TLDR
        """
        # 1. OpenAlex 搜索
        works = await self._call_openalex(query, limit)
        
        # 2. 并发增强数据
        tasks = [self._enrich_work(work) for work in works]
        return await asyncio.gather(*tasks)

    async def _enrich_work(self, work: Dict) -> Dict:
        doi = work.get("doi")
        # 并发执行：Unpaywall 找 PDF + S2 找 TLDR
        pdf_task = self._call_unpaywall(doi)
        s2_task = self._call_s2_enrichment(doi)
        
        pdf_url, s2_data = await asyncio.gather(pdf_task, s2_task)
        
        return {
            "paperId": work.get("id"),
            "title": work.get("display_name"),
            "doi": doi,
            "abstract": work.get("abstract"),
            "citationCount": work.get("cited_by_count"),
            "openAccessPdf": pdf_url or work.get("best_oa_location", {}).get("url_for_pdf"),
            "tldr": s2_data.get("tldr"),
            "year": work.get("publication_year")
        }
```

## 5. 数据模型映射表

| 内部统一字段 | OpenAlex 来源 | Unpaywall 来源 | Semantic Scholar 来源 |
|-------------|---------------|----------------|----------------------|
| paperId | id | - | paperId |
| title | display_name | - | title |
| pdf_url | best_oa_location.url | best_oa_location.url_for_pdf | - |
| tldr | - | - | tldr.text |
| citations | cited_by_count | - | citationCount |

## 6. 接口设计与映射

保持与现有Semantic Scholar MCP服务器相同的接口签名：

- `search_papers(query, limit, fields)`
- `get_paper_details(paper_id, fields)`
- `get_citation_context(paper_id, limit)`
- `download_pdf(paper_id, output_path)`
- `search_by_author(author_name, limit, fields)`
- `search_by_title(title, limit, fields)`
- `get_paper_references(paper_id, limit, fields)`

## 7. 性能与稳定性策略

### 7.1 延迟加载与按需增强 (On-demand Enrichment)
**策略**：在初始 search_papers 列表请求时，不强制等待 S2 返回结果。
**实现**：如果 S2 在 2 秒内未响应，则直接返回 OpenAlex 结果。

### 7.2 熔断与优雅降级 (Graceful Degradation)
**策略**：当 S2 触发 429 (Too Many Requests) 时，系统进入 5 分钟的"熔断期"。
**表现**：熔断期内所有请求仅由 OpenAlex + Unpaywall 提供支持。

### 7.3 数据对齐与回退机制
**缺失处理**：若 OpenAlex 返回的论文在 S2 中不存在，系统自动利用 OpenAlex 的 abstract 进行本地简单摘要生成。

### 7.4 缓存优先策略
**策略**：所有 S2 的 tldr 数据在 SQLite 中永久保存。
**收益**：对于热门论文，SROS 重复检索时将实现"零延迟"响应。

## 8. 完整开发路线图

### 8.1 第一阶段：基础架构搭建 (Week 4: Feb 10-16)

#### 任务清单
- [ ] 创建新的学术搜索服务器目录结构
- [ ] 设计统一的数据模型和接口
- [ ] 实现OpenAlexSearchProvider类
- [ ] 实现UnpaywallPDFProvider类
- [ ] 实现S2EnrichmentProvider类
- [ ] 实现基本的HTTP客户端和配置管理
- [ ] 实现结果转换器

#### 交付物
- 新的服务器目录结构
- 基础Provider类实现
- 配置管理模块
- 数据模型定义

#### 验收标准
- Provider类能够正确初始化
- 配置能够正确加载
- 数据模型定义完整

### 8.2 第二阶段：核心搜索功能实现 (Week 4: Feb 10-16)

#### 任务清单
- [ ] 实现论文搜索功能 (search_papers)
- [ ] 实现论文详情获取 (get_paper_details)
- [ ] 实现作者搜索 (search_by_author)
- [ ] 实现标题搜索 (search_by_title)
- [ ] 实现参考文献获取 (get_paper_references)
- [ ] 实现数据格式转换和标准化
- [ ] 添加基本的日志记录

#### 交付物
- 完整的搜索功能实现
- 数据转换和标准化逻辑
- 基本日志记录

#### 验收标准
- 所有搜索功能能够正确返回结果
- 数据格式符合预期
- 日志记录完整

### 8.3 第三阶段：增强功能实现 (Week 5: Feb 17-23)

#### 任务清单
- [ ] 实现引用上下文获取 (get_citation_context)
- [ ] 实现PDF下载功能 (download_pdf)
- [ ] 实现TLDR摘要获取功能
- [ ] 实现按需增强机制
- [ ] 添加增强功能错误处理

#### 交付物
- 完整的增强功能实现
- 按需增强机制
- 错误处理机制

#### 验收标准
- 增强功能能够正确工作
- 按需增强机制有效
- 错误处理完善

### 8.4 第四阶段：性能优化和稳定性 (Week 5: Feb 17-23)

#### 任务清单
- [ ] 实现缓存管理器 (CacheManager)
- [ ] 添加速率限制器 (Rate Limiter)
- [ ] 实现熔断机制
- [ ] 实现优雅降级策略
- [ ] 性能优化
- [ ] 编写单元测试

#### 交付物
- 完整的缓存管理机制
- 速率限制和熔断机制
- 优雅降级策略
- 性能优化后的代码
- 完整的测试套件

#### 验收标准
- 缓存机制工作正常
- 速率限制和熔断机制有效
- 优雅降级策略完善
- 性能达到预期
- 测试覆盖率达标

### 8.5 第五阶段：测试和完善 (Week 6: Feb 24-Mar 2)

#### 任务清单
- [ ] 编写集成测试
- [ ] 进行兼容性测试
- [ ] 进行压力测试
- [ ] 完善文档
- [ ] 添加监控和统计功能

#### 交付物
- 完整的测试套件
- 兼容性测试报告
- 压力测试报告
- 完善的文档
- 监控和统计功能

#### 验收标准
- 所有测试通过
- 兼容性良好
- 性能满足要求
- 文档齐全
- 监控功能完整

## 9. 时间安排和里程碑

### 9.1 详细时间表
```
Week 4 (Feb 10-16): 基础架构和核心功能
  - 周一至周三: 第一阶段 - 基础架构搭建
  - 周四至周五: 第二阶段 - 核心搜索功能实现

Week 5 (Feb 17-23): 增强功能和性能优化
  - 周一至周三: 第三阶段 - 增强功能实现
  - 周四至周五: 第四阶段 - 性能优化和稳定性

Week 6 (Feb 24-Mar 2): 测试和完善
  - 周一至周三: 第五阶段 - 测试和完善
  - 周四至周五: 最终测试和部署准备
```

### 9.2 关键里程碑
- **里程碑1** (Feb 12): 基础架构完成
- **里程碑2** (Feb 15): 核心搜索功能完成
- **里程碑3** (Feb 19): 增强功能完成
- **里程碑4** (Feb 24): 性能优化完成
- **里程碑5** (Feb 26): 所有功能完成并测试通过
- **里程碑6** (Mar 2): 正式发布

## 10. 配置管理

### 10.1 环境变量
```bash
# OpenAlex配置
OPENALEX_BASE_URL=https://api.openalex.org
OPENALEX_EMAIL=your-email@example.com
OPENALEX_TIMEOUT=30

# Unpaywall配置
UNPAYWALL_BASE_URL=https://api.unpaywall.org/v2
UNPAYWALL_EMAIL=your-email@example.com
UNPAYWALL_TIMEOUT=30

# Semantic Scholar配置
SEMANTIC_SCHOLAR_API_KEY=your_api_key_here
SEMANTIC_SCHOLAR_TIMEOUT=30

# 缓存配置
ACADEMIC_SEARCH_CACHE_ENABLED=true
ACADEMIC_SEARCH_CACHE_DB_PATH=.cache/academic_search.db
```

## 11. 资源需求

### 11.1 人力资源
- 1名后端开发工程师
- 1名测试工程师

### 11.2 技术资源
- OpenAlex API访问权限
- Unpaywall API访问权限
- Semantic Scholar API访问权限
- 开发和测试环境
- CI/CD流水线

### 11.3 工具需求
- Python开发环境
- Git版本控制
- 单元测试框架
- 性能测试工具

## 12. 风险管理

### 12.1 技术风险
- **API变更风险**: 各API可能发生变更
  - 应对措施: 实现API版本兼容，定期检查API更新
- **性能风险**: 大量并发请求可能导致性能问题
  - 应对措施: 实现请求限流和缓存机制
- **数据质量风险**: 不同数据源的数据质量可能不一致
  - 应对措施: 实现数据质量监控和清洗机制

### 12.2 进度风险
- **依赖延迟**: 第三方API响应慢可能影响开发进度
  - 应对措施: 实现模拟数据和离线测试
- **技术难题**: 可能遇到未预见的技术挑战
  - 应对措施: 预留缓冲时间，及时调整方案

## 13. 质量保证

### 13.1 代码质量
- 遵循PEP 8编码规范
- 实现完整的单元测试覆盖
- 代码审查机制
- 静态代码分析

### 13.2 测试策略
- 单元测试覆盖率不低于80%
- 集成测试覆盖所有核心功能
- 性能测试确保响应时间符合要求
- 兼容性测试确保向后兼容

### 13.3 监控和运维
- 实现详细的日志记录
- 监控API调用成功率和响应时间
- 实现健康检查端点
- 建立告警机制

## 14. 部署计划

### 14.1 部署环境
- 开发环境: 用于日常开发和测试
- 测试环境: 用于集成测试和用户验收
- 生产环境: 对外提供服务

### 14.2 部署流程
1. 代码提交到版本控制系统
2. 自动化构建和测试
3. 部署到测试环境
4. 手动验收测试
5. 部署到生产环境

### 14.3 回滚策略
- 保留最近5个版本的部署包
- 实现一键回滚功能
- 建立回滚测试流程

## 15. 验收标准

### 15.1 功能验收
- 所有API接口按设计文档实现
- 功能测试全部通过
- 性能指标达到预期
- 向后兼容性得到保证

### 15.2 质量验收
- 代码审查通过
- 测试覆盖率达标
- 安全扫描无高危漏洞
- 文档齐全且准确

### 15.3 运维验收
- 部署流程顺畅
- 监控告警配置完成
- 运维文档齐全
- 回滚机制有效

## 16. 后续计划

### 16.1 短期计划 (1个月内)
- 收集用户反馈并持续优化
- 监控系统运行状态
- 修复发现的问题

### 16.2 中期计划 (3个月内)
- 扩展支持更多的学术数据库
- 增强搜索算法和排序机制
- 优化用户体验

### 16.3 长期计划 (6个月以上)
- 实现分布式部署架构
- 支持更多语言和国际化
- 增加AI辅助搜索功能