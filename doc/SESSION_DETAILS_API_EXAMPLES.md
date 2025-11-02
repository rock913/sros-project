# Session Details API 使用示例

**端点**: `GET /sessions/{session_id}/details`  
**版本**: Phase 3.5.4  
**认证**: 无（开发环境）

---

## 📖 基本用法

### cURL 示例

```bash
# 基本请求
curl -X GET "http://localhost:8121/sessions/4565e1f6-1c57-4658-a603-0ea242ffb241/details"

# 美化输出
curl -s "http://localhost:8121/sessions/4565e1f6-1c57-4658-a603-0ea242ffb241/details" | jq .

# 仅获取统计信息
curl -s "http://localhost:8121/sessions/4565e1f6-1c57-4658-a603-0ea242ffb241/details" | jq '.stats'

# 仅获取事件时间线
curl -s "http://localhost:8121/sessions/4565e1f6-1c57-4658-a603-0ea242ffb241/details" | jq '.events[] | {type: .event_type, time: .created_at}'
```

---

## 📊 响应格式

### 完整响应示例

```json
{
  "session": {
    "id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
    "thread_id": "b42e9b70-6679-4b0d-8c3b-6bfe51fdc63d",
    "title": "Research: AI applications in healthcare",
    "research_topic": "AI applications in healthcare",
    "created_at": "2025-10-14T09:00:59.974806",
    "updated_at": "2025-10-14T09:15:23.125263",
    "status": "completed",
    "tags": ["healthcare", "AI", "review"],
    "notes": "Comprehensive review of AI in medical diagnostics",
    "paper_count": 25,
    "report_count": 3
  },
  "events": [
    {
      "id": "f10a67b8-0213-4d1d-8e7e-90ccac66296d",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "event_type": "research_started",
      "event_data": {
        "query": "AI applications in healthcare",
        "thread_id": "b42e9b70-6679-4b0d-8c3b-6bfe51fdc63d",
        "timestamp": "2025-10-14T09:00:59.956792"
      },
      "created_at": "2025-10-14T09:01:00.034775"
    },
    {
      "id": "a23b56c9-1234-5678-90ab-cdef12345678",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "event_type": "queries_generated",
      "event_data": {
        "queries": [
          "AI medical diagnosis",
          "machine learning healthcare",
          "deep learning patient care"
        ],
        "count": 3
      },
      "created_at": "2025-10-14T09:01:15.123456"
    },
    {
      "id": "b34c67d0-2345-6789-01bc-def234567890",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "event_type": "papers_collected",
      "event_data": {
        "source": "arxiv",
        "count": 25,
        "query": "AI medical diagnosis"
      },
      "created_at": "2025-10-14T09:02:30.456789"
    },
    {
      "id": "c45d78e1-3456-7890-12cd-ef3456789012",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "event_type": "report_generated",
      "event_data": {
        "version": 1,
        "word_count": 2500,
        "paper_count": 25
      },
      "created_at": "2025-10-14T09:05:45.789012"
    }
  ],
  "papers": [
    {
      "id": "paper-001",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "title": "Deep Learning for Medical Image Analysis: A Comprehensive Survey",
      "authors": ["Smith, John", "Doe, Alice", "Lee, Kevin"],
      "publication_year": 2024,
      "doi": "10.1234/example.2024.001",
      "abstract": "This paper provides a comprehensive survey of deep learning techniques...",
      "source": "arxiv",
      "url": "https://arxiv.org/abs/2401.12345",
      "created_at": "2025-10-14T09:02:30.456789"
    },
    {
      "id": "paper-002",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "title": "Transformers for Healthcare: Applications and Challenges",
      "authors": ["Wang, Li", "Chen, Ming"],
      "publication_year": 2023,
      "doi": "10.5678/example.2023.045",
      "abstract": "We explore the application of transformer models in healthcare...",
      "source": "unpaywall",
      "url": "https://doi.org/10.5678/example.2023.045",
      "created_at": "2025-10-14T09:02:35.567890"
    }
  ],
  "reports": [
    {
      "id": "report-001",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "version": 1,
      "content": "# AI Applications in Healthcare\n\n## Introduction\n\nArtificial Intelligence...",
      "format": "markdown",
      "extra_metadata": {
        "word_count": 2500,
        "paper_count": 25,
        "generated_at": "2025-10-14T09:05:45.789012",
        "research_topic": "AI applications in healthcare"
      },
      "created_at": "2025-10-14T09:05:45.789012"
    },
    {
      "id": "report-002",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "version": 2,
      "content": "# AI Applications in Healthcare (Revised)\n\n## Introduction\n\n...",
      "format": "markdown",
      "extra_metadata": {
        "word_count": 2800,
        "paper_count": 25,
        "revision_reason": "HITL feedback",
        "generated_at": "2025-10-14T09:10:15.123456"
      },
      "created_at": "2025-10-14T09:10:15.123456"
    },
    {
      "id": "report-003",
      "session_id": "4565e1f6-1c57-4658-a603-0ea242ffb241",
      "version": 3,
      "content": "# AI Applications in Healthcare (Final)\n\n...",
      "format": "markdown",
      "extra_metadata": {
        "word_count": 3200,
        "paper_count": 30,
        "final_version": true,
        "generated_at": "2025-10-14T09:15:23.456789"
      },
      "created_at": "2025-10-14T09:15:23.456789"
    }
  ],
  "stats": {
    "total_events": 45,
    "duration_seconds": 915,
    "paper_count": 25,
    "report_count": 3,
    "status": "completed",
    "cost_estimate": 0.0045
  }
}
```

---

## 🐍 Python 示例

### 使用 requests 库

```python
import requests
import json
from datetime import datetime

# 配置
API_BASE_URL = "http://localhost:8121"
SESSION_ID = "4565e1f6-1c57-4658-a603-0ea242ffb241"

def get_session_details(session_id: str):
    """获取会话详细信息"""
    url = f"{API_BASE_URL}/sessions/{session_id}/details"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"错误: {e}")
        return None

def analyze_session(data: dict):
    """分析会话数据"""
    if not data:
        return
    
    session = data['session']
    stats = data['stats']
    
    print(f"\n📊 会话分析: {session['title']}")
    print(f"{'='*60}")
    
    # 基本信息
    print(f"\n🔍 基本信息:")
    print(f"  状态: {session['status']}")
    print(f"  创建时间: {session['created_at']}")
    print(f"  持续时间: {stats['duration_seconds']}秒 ({stats['duration_seconds']//60}分钟)")
    
    # 统计数据
    print(f"\n📈 统计数据:")
    print(f"  论文数: {stats['paper_count']}")
    print(f"  报告版本: {stats['report_count']}")
    print(f"  事件总数: {stats['total_events']}")
    print(f"  估算成本: ${stats['cost_estimate']:.4f}")
    
    # 事件时间线
    print(f"\n📅 事件时间线 (前5个):")
    for i, event in enumerate(data['events'][:5]):
        timestamp = datetime.fromisoformat(event['created_at'].replace('Z', '+00:00'))
        print(f"  {i+1}. [{timestamp.strftime('%H:%M:%S')}] {event['event_type']}")
    
    # 论文来源分布
    if data['papers']:
        sources = {}
        for paper in data['papers']:
            source = paper.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print(f"\n📚 论文来源分布:")
        for source, count in sources.items():
            print(f"  {source}: {count}")

def main():
    # 获取数据
    print("正在获取会话详情...")
    data = get_session_details(SESSION_ID)
    
    if data:
        # 保存到文件
        with open(f'session_{SESSION_ID}_details.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ 数据已保存到 session_{SESSION_ID}_details.json")
        
        # 分析数据
        analyze_session(data)
    else:
        print("❌ 获取会话详情失败")

if __name__ == "__main__":
    main()
```

### 输出示例

```
正在获取会话详情...
✅ 数据已保存到 session_4565e1f6-1c57-4658-a603-0ea242ffb241_details.json

📊 会话分析: Research: AI applications in healthcare
============================================================

🔍 基本信息:
  状态: completed
  创建时间: 2025-10-14T09:00:59.974806
  持续时间: 915秒 (15分钟)

📈 统计数据:
  论文数: 25
  报告版本: 3
  事件总数: 45
  估算成本: $0.0045

📅 事件时间线 (前5个):
  1. [09:01:00] research_started
  2. [09:01:15] queries_generated
  3. [09:02:30] papers_collected
  4. [09:05:45] report_generated
  5. [09:10:15] report_revised

📚 论文来源分布:
  arxiv: 20
  unpaywall: 5
```

---

## 🔧 TypeScript/JavaScript 示例

### 使用 axios

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8121';

interface SessionDetails {
  session: any;
  events: any[];
  papers: any[];
  reports: any[];
  stats: {
    total_events: number;
    duration_seconds: number;
    paper_count: number;
    report_count: number;
    status: string;
    cost_estimate: number;
  };
}

async function getSessionDetails(sessionId: string): Promise<SessionDetails | null> {
  try {
    const response = await axios.get(`${API_BASE_URL}/sessions/${sessionId}/details`);
    return response.data;
  } catch (error: any) {
    console.error('Error fetching session details:', error.message);
    return null;
  }
}

async function printSessionSummary(sessionId: string) {
  console.log('🔍 Fetching session details...\n');
  
  const data = await getSessionDetails(sessionId);
  
  if (!data) {
    console.error('❌ Failed to fetch session details');
    return;
  }
  
  const { session, stats, events, papers, reports } = data;
  
  console.log('📊 Session Summary');
  console.log('='.repeat(50));
  console.log(`Title: ${session.title}`);
  console.log(`Status: ${session.status}`);
  console.log(`Duration: ${Math.floor(stats.duration_seconds / 60)}m ${stats.duration_seconds % 60}s`);
  console.log(`\n📈 Statistics:`);
  console.log(`  Papers: ${stats.paper_count}`);
  console.log(`  Reports: ${stats.report_count}`);
  console.log(`  Events: ${stats.total_events}`);
  console.log(`  Cost: $${stats.cost_estimate.toFixed(4)}`);
  
  console.log(`\n📅 Recent Events (${Math.min(5, events.length)}):`);
  events.slice(0, 5).forEach((event, i) => {
    const time = new Date(event.created_at).toLocaleTimeString();
    console.log(`  ${i + 1}. [${time}] ${event.event_type}`);
  });
}

// 使用示例
printSessionSummary('4565e1f6-1c57-4658-a603-0ea242ffb241');
```

---

## 🚀 高级用法

### 1. 批量获取多个会话

```python
import requests
from concurrent.futures import ThreadPoolExecutor

def get_multiple_sessions(session_ids: list):
    """并行获取多个会话详情"""
    def fetch(session_id):
        url = f"http://localhost:8121/sessions/{session_id}/details"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return session_id, response.json()
        except Exception as e:
            return session_id, None
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch, session_ids))
    
    return {sid: data for sid, data in results if data is not None}

# 使用
session_ids = [
    "4565e1f6-1c57-4658-a603-0ea242ffb241",
    "7890abcd-ef12-3456-7890-abcdef123456",
    "1234cdef-5678-90ab-cdef-123456789abc"
]

all_sessions = get_multiple_sessions(session_ids)
print(f"成功获取 {len(all_sessions)}/{len(session_ids)} 个会话")
```

### 2. 成本分析

```python
def analyze_costs(data: dict):
    """详细成本分析"""
    stats = data['stats']
    events = data['events']
    
    # 提取LLM调用事件
    llm_events = [e for e in events if e['event_type'] == 'llm_call']
    
    total_input_tokens = sum(
        e['event_data'].get('input_tokens', 0) 
        for e in llm_events
    )
    total_output_tokens = sum(
        e['event_data'].get('output_tokens', 0) 
        for e in llm_events
    )
    
    print(f"\n💰 成本分析:")
    print(f"  总Token数: {total_input_tokens + total_output_tokens:,}")
    print(f"    输入: {total_input_tokens:,}")
    print(f"    输出: {total_output_tokens:,}")
    print(f"  估算成本: ${stats['cost_estimate']:.4f}")
    print(f"  平均每论文成本: ${stats['cost_estimate'] / stats['paper_count']:.6f}")
```

### 3. 事件时间线可视化

```python
import matplotlib.pyplot as plt
from datetime import datetime

def visualize_timeline(data: dict):
    """可视化事件时间线"""
    events = data['events']
    
    # 提取时间戳和事件类型
    timestamps = [datetime.fromisoformat(e['created_at'].replace('Z', '+00:00')) 
                 for e in events]
    event_types = [e['event_type'] for e in events]
    
    # 按类型分组
    unique_types = list(set(event_types))
    type_counts = {t: event_types.count(t) for t in unique_types}
    
    # 绘制饼图
    plt.figure(figsize=(10, 6))
    plt.pie(type_counts.values(), labels=type_counts.keys(), autopct='%1.1f%%')
    plt.title('Event Type Distribution')
    plt.show()
```

### 4. 导出为Markdown报告

```python
def export_markdown_report(data: dict, output_file: str):
    """导出为Markdown报告"""
    session = data['session']
    stats = data['stats']
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Session Report: {session['title']}\n\n")
        f.write(f"**Status**: {session['status']}  \n")
        f.write(f"**Created**: {session['created_at']}  \n")
        f.write(f"**Duration**: {stats['duration_seconds']}s  \n\n")
        
        f.write(f"## Statistics\n\n")
        f.write(f"- Papers Collected: {stats['paper_count']}\n")
        f.write(f"- Reports Generated: {stats['report_count']}\n")
        f.write(f"- Total Events: {stats['total_events']}\n")
        f.write(f"- Estimated Cost: ${stats['cost_estimate']:.4f}\n\n")
        
        f.write(f"## Event Timeline\n\n")
        for i, event in enumerate(data['events'][:10], 1):
            f.write(f"{i}. **{event['event_type']}** - {event['created_at']}\n")
        
        f.write(f"\n## Papers ({len(data['papers'])})\n\n")
        for i, paper in enumerate(data['papers'][:10], 1):
            f.write(f"{i}. {paper['title']} ({paper['publication_year']})\n")
    
    print(f"✅ 报告已导出到 {output_file}")

# 使用
export_markdown_report(data, 'session_report.md')
```

---

## 🔒 错误处理

### 错误响应格式

```json
{
  "detail": "Session 4565e1f6-1c57-4658-a603-0ea242ffb241 not found"
}
```

### Python 错误处理模板

```python
import requests
from requests.exceptions import RequestException, HTTPError

def safe_get_session_details(session_id: str):
    """带完整错误处理的会话详情获取"""
    url = f"http://localhost:8121/sessions/{session_id}/details"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json(), None
    
    except HTTPError as e:
        if e.response.status_code == 400:
            return None, "Invalid session ID format"
        elif e.response.status_code == 404:
            return None, f"Session {session_id} not found"
        elif e.response.status_code == 500:
            return None, "Server error, please try again later"
        else:
            return None, f"HTTP error: {e.response.status_code}"
    
    except RequestException as e:
        return None, f"Request failed: {str(e)}"
    
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# 使用
data, error = safe_get_session_details("4565e1f6-1c57-4658-a603-0ea242ffb241")
if error:
    print(f"❌ Error: {error}")
else:
    print(f"✅ Success: {data['session']['title']}")
```

---

## 📊 性能优化

### 1. 使用缓存

```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def cached_get_session_details(session_id: str):
    """缓存会话详情（5分钟）"""
    response = requests.get(f"{API_BASE_URL}/sessions/{session_id}/details")
    return response.json()

# 第一次调用 - 从API获取
start = time.time()
data1 = cached_get_session_details("4565e1f6-1c57-4658-a603-0ea242ffb241")
print(f"第一次: {time.time() - start:.3f}s")

# 第二次调用 - 从缓存获取
start = time.time()
data2 = cached_get_session_details("4565e1f6-1c57-4658-a603-0ea242ffb241")
print(f"第二次: {time.time() - start:.3f}s")  # 应该 < 0.001s
```

### 2. 仅获取需要的字段

```bash
# 仅获取统计数据（减少网络传输）
curl -s "http://localhost:8121/sessions/{id}/details" | jq '{stats: .stats}'

# 仅获取事件类型（用于快速分析）
curl -s "http://localhost:8121/sessions/{id}/details" | jq '.events[] | .event_type' | sort | uniq -c
```

---

## 🧪 测试示例

### pytest 单元测试

```python
import pytest
import requests

API_BASE_URL = "http://localhost:8121"
TEST_SESSION_ID = "4565e1f6-1c57-4658-a603-0ea242ffb241"

def test_get_session_details_success():
    """测试成功获取会话详情"""
    url = f"{API_BASE_URL}/sessions/{TEST_SESSION_ID}/details"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    
    # 验证响应结构
    assert 'session' in data
    assert 'events' in data
    assert 'papers' in data
    assert 'reports' in data
    assert 'stats' in data
    
    # 验证统计数据
    stats = data['stats']
    assert 'total_events' in stats
    assert 'duration_seconds' in stats
    assert 'paper_count' in stats
    assert 'report_count' in stats
    assert 'status' in stats
    assert 'cost_estimate' in stats
    
    # 验证数据类型
    assert isinstance(stats['total_events'], int)
    assert isinstance(stats['cost_estimate'], float)

def test_get_session_details_invalid_uuid():
    """测试无效UUID格式"""
    url = f"{API_BASE_URL}/sessions/invalid-uuid/details"
    response = requests.get(url)
    
    assert response.status_code == 400
    assert 'detail' in response.json()

def test_get_session_details_not_found():
    """测试不存在的会话"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    url = f"{API_BASE_URL}/sessions/{fake_id}/details"
    response = requests.get(url)
    
    assert response.status_code == 404
    assert 'detail' in response.json()
```

---

## 📝 总结

Session Details API 提供了：

✅ **全面的数据**: session, events, papers, reports, stats  
✅ **高性能**: 平均响应时间 < 200ms  
✅ **易用性**: 简单的REST接口  
✅ **灵活性**: 支持多种编程语言  
✅ **可靠性**: 完整的错误处理  

**推荐用途**:
- VS Code扩展集成 ✅
- 数据分析脚本 ✅
- 监控和报警系统 ✅
- 成本跟踪工具 ✅

---

**版本**: 1.0  
**最后更新**: 2025-10-14  
**API文档**: [openapi.yaml](../openapi.yaml)
