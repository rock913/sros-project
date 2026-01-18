# Phase 3.5.3 Week 2 实施计划

**日期**: 2025-10-14  
**任务**: Week 2 - Backend Analytics APIs  
**预计完成**: 2025-10-21  
**依赖**: Week 1 (Phase 3 WebSocket) ✅  

---

## 目标概述

实现4个分析统计API端点，为Week 3的前端Dashboard提供数据支持。

---

## API端点规划

### 1. GET /analytics/sessions

**功能**: 获取所有研究会话列表（分页支持）

**请求参数**:
```yaml
parameters:
  - name: limit
    in: query
    schema:
      type: integer
      default: 50
      maximum: 200
    description: Maximum number of sessions to return
  
  - name: offset
    in: query
    schema:
      type: integer
      default: 0
    description: Number of sessions to skip
  
  - name: status
    in: query
    schema:
      type: string
      enum: [running, completed, failed]
    description: Filter by session status
  
  - name: user_id
    in: query
    schema:
      type: string
    description: Filter by user ID
  
  - name: sort_by
    in: query
    schema:
      type: string
      enum: [created_at, duration, papers_count]
      default: created_at
    description: Sort field
  
  - name: order
    in: query
    schema:
      type: string
      enum: [asc, desc]
      default: desc
    description: Sort order
```

**响应格式**:
```json
{
  "sessions": [
    {
      "session_id": "uuid",
      "thread_id": "uuid",
      "user_id": "string",
      "research_topic": "string",
      "status": "completed",
      "created_at": "2025-10-14T10:00:00Z",
      "completed_at": "2025-10-14T10:15:00Z",
      "duration_seconds": 900,
      "papers_count": 15,
      "queries_count": 5,
      "loops_count": 3,
      "events_count": 42
    }
  ],
  "total": 100,
  "limit": 50,
  "offset": 0,
  "has_more": true
}
```

**数据库查询**:
```sql
SELECT 
    s.id as session_id,
    s.thread_id,
    s.user_id,
    s.research_topic,
    s.status,
    s.created_at,
    s.completed_at,
    EXTRACT(EPOCH FROM (s.completed_at - s.created_at)) as duration_seconds,
    s.metadata->>'papers_count' as papers_count,
    s.metadata->>'queries_count' as queries_count,
    (SELECT COUNT(*) FROM session_events WHERE session_id = s.id) as events_count
FROM sessions s
WHERE ($status IS NULL OR s.status = $status)
  AND ($user_id IS NULL OR s.user_id = $user_id)
ORDER BY 
    CASE WHEN $sort_by = 'created_at' THEN s.created_at END DESC,
    CASE WHEN $sort_by = 'duration' THEN (s.completed_at - s.created_at) END DESC
LIMIT $limit OFFSET $offset;
```

**实现文件**: `backend/src/database/analytics.py` (新建)

---

### 2. GET /analytics/sessions/{session_id}

**功能**: 获取单个会话的详细信息，包括所有事件

**路径参数**:
- `session_id`: UUID

**响应格式**:
```json
{
  "session": {
    "session_id": "uuid",
    "thread_id": "uuid",
    "user_id": "string",
    "research_topic": "string",
    "status": "completed",
    "created_at": "2025-10-14T10:00:00Z",
    "completed_at": "2025-10-14T10:15:00Z",
    "duration_seconds": 900,
    "metadata": {
      "papers_count": 15,
      "queries_count": 5,
      "loops_count": 3
    }
  },
  "events": [
    {
      "event_id": "uuid",
      "event_type": "agent_start",
      "node_name": "researcher",
      "timestamp": "2025-10-14T10:00:05Z",
      "metadata": {
        "message": "Starting research"
      }
    }
  ],
  "timeline": {
    "total_duration": 900,
    "phases": [
      {
        "phase": "initialization",
        "duration_seconds": 10,
        "percentage": 1.1
      },
      {
        "phase": "research",
        "duration_seconds": 600,
        "percentage": 66.7
      },
      {
        "phase": "report_generation",
        "duration_seconds": 290,
        "percentage": 32.2
      }
    ]
  }
}
```

**数据库查询**:
```sql
-- Session info
SELECT * FROM sessions WHERE id = $session_id;

-- Events
SELECT * FROM session_events 
WHERE session_id = $session_id 
ORDER BY created_at ASC;

-- Timeline phases (calculated in Python)
```

**实现文件**: `backend/src/database/analytics.py`

---

### 3. GET /analytics/sessions/stats

**功能**: 获取会话统计数据（聚合指标）

**请求参数**:
```yaml
parameters:
  - name: time_range
    in: query
    schema:
      type: string
      enum: [24h, 7d, 30d, all]
      default: 7d
    description: Time range for statistics
  
  - name: user_id
    in: query
    schema:
      type: string
    description: Filter by user ID
```

**响应格式**:
```json
{
  "time_range": "7d",
  "stats": {
    "total_sessions": 150,
    "completed_sessions": 120,
    "failed_sessions": 10,
    "running_sessions": 20,
    "success_rate": 80.0,
    "total_papers_collected": 2250,
    "total_queries_generated": 750,
    "avg_papers_per_session": 15.0,
    "avg_queries_per_session": 5.0,
    "avg_duration_seconds": 890,
    "avg_loops_per_session": 2.8
  },
  "daily_breakdown": [
    {
      "date": "2025-10-14",
      "sessions": 25,
      "completed": 20,
      "failed": 2,
      "avg_duration": 850
    }
  ],
  "top_topics": [
    {
      "topic": "quantum computing",
      "count": 15,
      "avg_papers": 18
    }
  ]
}
```

**数据库查询**:
```sql
-- Basic stats
SELECT 
    COUNT(*) as total_sessions,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_sessions,
    COUNT(*) FILTER (WHERE status = 'failed') as failed_sessions,
    COUNT(*) FILTER (WHERE status = 'running') as running_sessions,
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) as avg_duration_seconds,
    AVG((metadata->>'papers_count')::int) as avg_papers_per_session
FROM sessions
WHERE created_at > NOW() - INTERVAL $time_range;

-- Daily breakdown
SELECT 
    DATE(created_at) as date,
    COUNT(*) as sessions,
    COUNT(*) FILTER (WHERE status = 'completed') as completed,
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) as avg_duration
FROM sessions
WHERE created_at > NOW() - INTERVAL $time_range
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

**实现文件**: `backend/src/database/analytics.py`

---

### 4. GET /analytics/papers/trends

**功能**: 获取论文收集趋势数据

**请求参数**:
```yaml
parameters:
  - name: time_range
    in: query
    schema:
      type: string
      enum: [24h, 7d, 30d, all]
      default: 7d
```

**响应格式**:
```json
{
  "time_range": "7d",
  "trends": {
    "total_papers": 2250,
    "unique_papers": 1800,
    "avg_papers_per_day": 321,
    "papers_by_day": [
      {
        "date": "2025-10-14",
        "papers_count": 350
      }
    ],
    "top_venues": [
      {
        "venue": "arXiv",
        "papers_count": 1200,
        "percentage": 66.7
      }
    ],
    "papers_by_year": [
      {
        "year": 2024,
        "count": 800
      },
      {
        "year": 2023,
        "count": 600
      }
    ]
  }
}
```

**数据库查询** (需要papers表):
```sql
-- Note: 需要先在database schema中添加papers表
CREATE TABLE IF NOT EXISTS papers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id),
    title TEXT NOT NULL,
    authors TEXT[],
    venue TEXT,
    year INTEGER,
    doi TEXT,
    url TEXT,
    abstract TEXT,
    collected_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(session_id, doi)
);

-- Trends query
SELECT 
    DATE(p.collected_at) as date,
    COUNT(*) as papers_count
FROM papers p
JOIN sessions s ON p.session_id = s.id
WHERE p.collected_at > NOW() - INTERVAL $time_range
GROUP BY DATE(p.collected_at)
ORDER BY date DESC;
```

**实现文件**: `backend/src/database/analytics.py`

---

## 实施步骤

### Day 6: 数据模型设计与准备

**任务**:
1. ✅ Review现有database schema (`backend/src/database/models.py`)
2. ⏳ 设计papers表schema
3. ⏳ 创建migration script
4. ⏳ 创建`analytics.py`模块

**文件**:
- `backend/src/database/models.py` (review)
- `backend/src/database/analytics.py` (new)
- `backend/migrations/add_papers_table.sql` (new)

---

### Day 7-8: 实现Analytics APIs

**任务**:
1. ⏳ 实现`get_sessions_list()` function
2. ⏳ 实现`get_session_details()` function
3. ⏳ 实现`get_sessions_stats()` function
4. ⏳ 实现`get_papers_trends()` function
5. ⏳ 添加FastAPI endpoints到`app.py`

**文件**:
- `backend/src/database/analytics.py`
- `backend/src/agent/app.py`

---

### Day 9: OpenAPI文档与测试

**任务**:
1. ⏳ 更新`openapi.yaml`
2. ⏳ 创建测试脚本
3. ⏳ Manual E2E testing

**文件**:
- `openapi.yaml`
- `scripts/test-analytics-api.sh` (new)
- `scripts/test-analytics.py` (new)

---

### Day 10: Code Review与优化

**任务**:
1. ⏳ Code review
2. ⏳ Performance optimization (add indexes)
3. ⏳ Error handling improvement
4. ⏳ Documentation update

---

## 数据库优化

### 新增索引
```sql
-- Sessions table indexes
CREATE INDEX idx_sessions_created_at ON sessions(created_at DESC);
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);

-- Session events table indexes
CREATE INDEX idx_session_events_session_id ON session_events(session_id);
CREATE INDEX idx_session_events_created_at ON session_events(created_at);

-- Papers table indexes (new)
CREATE INDEX idx_papers_session_id ON papers(session_id);
CREATE INDEX idx_papers_collected_at ON papers(collected_at DESC);
CREATE INDEX idx_papers_year ON papers(year);
```

---

## 技术栈

- **ORM**: SQLAlchemy (already in use)
- **Database**: PostgreSQL 16
- **Query Builder**: Raw SQL + SQLAlchemy Core
- **Pagination**: Offset-based
- **Caching**: Redis (optional, for stats)

---

## 验收标准

- [ ] 4个API端点全部实现
- [ ] OpenAPI文档完整
- [ ] 测试脚本通过
- [ ] 响应时间 < 500ms (p95)
- [ ] 错误处理完善
- [ ] TypeScript类型定义生成 (openapi-typescript)

---

## 风险与依赖

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| Papers表数据缺失 | High | 从sessions metadata回填 |
| 查询性能慢 | Medium | 添加索引，使用缓存 |
| Schema变更影响现有功能 | Low | 使用migration，向后兼容 |

---

## 下一步

完成Week 2后，进入Week 3: Frontend Analytics Dashboard

**预计交付时间**: 2025-10-21
