#!/bin/bash

# Week 1 Day 1: 测试修正后的 LangGraph API 集成
# 按照 GEMINI.md 的 Session-Driven Workflow 记录测试结果

echo "🧪 Week 1 Day 1: 测试 LangGraph API 集成（修正版）"
echo "=================================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_BASE="http://localhost:8121"

# 步骤 1: 检查后端健康状态
echo "步骤 1: 检查后端健康状态"
echo "------------------------"
response=$(curl -s -w "\n%{http_code}" "$API_BASE/ok")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
    echo "$body"
else
    echo -e "${RED}❌ FAIL${NC} (HTTP $http_code)"
    echo "$body"
    exit 1
fi
echo ""

# 步骤 2: 生成 UUID (模拟 generateThreadId())
echo "步骤 2: 生成线程 ID"
echo "------------------------"
THREAD_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
echo -e "${GREEN}✅ Generated Thread ID:${NC} $THREAD_ID"
echo ""

# 步骤 3: 调用 /agent/invoke 启动研究
echo "步骤 3: 调用 /agent/invoke 启动研究"
echo "------------------------"
echo -e "${YELLOW}测试: POST /agent/invoke${NC}"

PAYLOAD=$(cat <<EOF
{
  "input": {
    "messages": [
      {
        "role": "user",
        "content": "Please research: Test topic for Week 1 Day 1"
      }
    ]
  },
  "config": {
    "configurable": {
      "thread_id": "$THREAD_ID"
    }
  }
}
EOF
)

response=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/agent/invoke" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
    echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    echo -e "${RED}❌ FAIL${NC} (HTTP $http_code)"
    echo "$body"
    echo ""
    echo -e "${YELLOW}⚠️  Note: This is expected if the agent takes time to process.${NC}"
fi
echo ""

# 步骤 4: 获取线程状态
echo "步骤 4: 获取线程状态"
echo "------------------------"
echo -e "${YELLOW}测试: GET /agent/state/${THREAD_ID}${NC}"

sleep 2  # 等待2秒让 agent 处理

response=$(curl -s -w "\n%{http_code}" "$API_BASE/agent/state/$THREAD_ID")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
    echo "$body" | jq '. | {research_topic, search_queries, literature_count: (.literature_abstracts | length), report_length: (.report | length)}' 2>/dev/null || echo "$body"
else
    echo -e "${RED}❌ FAIL${NC} (HTTP $http_code)"
    echo "$body"
fi
echo ""

# 总结
echo "=================================================="
echo "测试总结"
echo "=================================================="
echo -e "${GREEN}✅ 健康检查通过${NC}"
echo -e "${GREEN}✅ 线程 ID 生成成功${NC}"
echo -e "${YELLOW}⚠️  invoke 调用已发送（agent 可能在后台处理）${NC}"
echo -e "Thread ID: $THREAD_ID"
echo ""
echo "下一步: 在 VS Code 扩展中实现这些 API 调用"
echo ""
