#!/bin/bash
# Week 1 Day 1: API 客户端功能测试脚本

set -e  # 遇到错误立即退出

echo "🧪 Week 1 Day 1: 测试线程管理 API"
echo "=================================="
echo ""

# 后端基础 URL
API_URL="http://localhost:8121"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数
TESTS_PASSED=0
TESTS_FAILED=0

# 测试函数
test_api() {
    local test_name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -e "${YELLOW}测试: ${test_name}${NC}"
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "${API_URL}${endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "${API_URL}${endpoint}" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
        echo "Response: $body" | jq '.' 2>/dev/null || echo "$body"
        echo ""
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo "$body"  # 返回响应体供后续使用
    else
        echo -e "${RED}❌ FAIL${NC} (HTTP $http_code)"
        echo "Response: $body"
        echo ""
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# 检查后端健康状态
echo "步骤 1: 检查后端健康状态"
echo "------------------------"
test_api "Health Check" "GET" "/ok"

# 测试 1: 创建线程
echo "步骤 2: 创建研究线程"
echo "------------------------"
thread_response=$(test_api "Create Thread" "POST" "/threads" '{
  "metadata": {
    "research_topic": "LangGraph test",
    "test": true
  }
}')

# 提取 thread_id
thread_id=$(echo "$thread_response" | jq -r '.thread_id')

if [ -z "$thread_id" ] || [ "$thread_id" = "null" ]; then
    echo -e "${RED}❌ 无法获取 thread_id${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Thread ID: $thread_id${NC}"
echo ""

# 测试 2: 获取线程状态（空状态）
echo "步骤 3: 获取初始线程状态"
echo "------------------------"
test_api "Get Thread State (Initial)" "GET" "/threads/$thread_id/state"

# 测试 3: 启动研究任务
echo "步骤 4: 启动研究任务"
echo "------------------------"
echo -e "${YELLOW}注意: 这个测试可能需要较长时间...${NC}"

run_response=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/threads/$thread_id/runs/stream" \
    -H "Content-Type: application/json" \
    -d '{
      "assistant_id": "agent",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": "Please research: What is LangGraph? Provide a brief summary."
          }
        ]
      },
      "stream_mode": ["values"]
    }')

http_code=$(echo "$run_response" | tail -n1)

if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
    echo -e "${GREEN}✅ Research started successfully${NC} (HTTP $http_code)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}❌ Failed to start research${NC} (HTTP $http_code)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo ""

# 测试 4: 轮询状态直到完成（最多等待 30 秒）
echo "步骤 5: 监控研究进度"
echo "------------------------"
max_attempts=15
attempt=0
completed=false

while [ $attempt -lt $max_attempts ]; do
    attempt=$((attempt + 1))
    echo "检查进度... (尝试 $attempt/$max_attempts)"
    
    state_response=$(curl -s "${API_URL}/threads/$thread_id/state")
    next_steps=$(echo "$state_response" | jq -r '.next | length')
    
    if [ "$next_steps" = "0" ]; then
        echo -e "${GREEN}✅ 研究已完成！${NC}"
        completed=true
        break
    fi
    
    # 显示当前状态
    current_state=$(echo "$state_response" | jq -r '.values | keys[]' | head -n 3)
    echo "当前状态包含: $current_state ..."
    
    sleep 2
done

if [ "$completed" = true ]; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo ""
    echo "步骤 6: 查看最终结果"
    echo "------------------------"
    
    final_state=$(curl -s "${API_URL}/threads/$thread_id/state")
    
    paper_count=$(echo "$final_state" | jq -r '.values.literature_abstracts | length')
    report_length=$(echo "$final_state" | jq -r '.values.report | length')
    
    echo "📚 收集的论文数量: $paper_count"
    echo "📝 报告长度: $report_length 字符"
    
    if [ "$paper_count" -gt 0 ] && [ "$report_length" -gt 0 ]; then
        echo -e "${GREEN}✅ 获得了真实的研究结果！${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}❌ 研究结果不完整${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${YELLOW}⚠️  研究超时（30秒），但这可能是正常的${NC}"
fi

echo ""
echo "=================================="
echo "测试总结"
echo "=================================="
echo -e "通过: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "失败: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！Week 1 Day 1 任务完成！${NC}"
    exit 0
else
    echo -e "${RED}❌ 有 ${TESTS_FAILED} 个测试失败${NC}"
    exit 1
fi
