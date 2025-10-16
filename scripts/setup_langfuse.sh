#!/bin/bash
# LangFuse 配置助手
# 帮助用户快速配置 LangFuse API 密钥

set -e

echo "============================================================================"
echo "🔧 LangFuse 配置助手 (Phase 4.1)"
echo "============================================================================"
echo ""

# 检查 LangFuse 服务是否运行
echo "📡 步骤 1: 检查 LangFuse 服务状态..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo "✅ LangFuse 服务运行中: http://localhost:3000"
    LANGFUSE_RUNNING=true
else
    echo "⚠️  LangFuse 服务未运行"
    echo ""
    echo "快速启动 LangFuse:"
    echo "  1. mkdir -p langfuse && cd langfuse"
    echo "  2. curl -o docker-compose.yml https://raw.githubusercontent.com/langfuse/langfuse/main/docker-compose.yml"
    echo "  3. docker-compose up -d"
    echo "  4. 访问 http://localhost:3000 并注册账号"
    echo ""
    LANGFUSE_RUNNING=false
fi
echo ""

if [ "$LANGFUSE_RUNNING" = true ]; then
    echo "📋 步骤 2: 获取 LangFuse API 密钥"
    echo ""
    echo "请按照以下步骤操作:"
    echo "  1. 打开浏览器访问: http://localhost:3000"
    echo "  2. 登录您的账号（如果还没注册，请先注册）"
    echo "  3. 点击左侧菜单 'Settings' → 'API Keys'"
    echo "  4. 点击 'Create new API key' 按钮"
    echo "  5. 复制生成的 Public Key (pk-lf-...) 和 Secret Key (sk-lf-...)"
    echo ""
    echo "按 Enter 继续（当您已经获取到密钥后）..."
    read -r
    echo ""
    
    echo "🔑 步骤 3: 输入您的 LangFuse API 密钥"
    echo ""
    
    # 读取 Public Key
    while true; do
        echo -n "请输入 Public Key (pk-lf-...): "
        read -r PUBLIC_KEY
        
        if [[ $PUBLIC_KEY =~ ^pk-lf- ]]; then
            break
        else
            echo "❌ 格式错误！Public Key 应以 'pk-lf-' 开头，请重新输入"
        fi
    done
    
    # 读取 Secret Key
    while true; do
        echo -n "请输入 Secret Key (sk-lf-...): "
        read -r SECRET_KEY
        
        if [[ $SECRET_KEY =~ ^sk-lf- ]]; then
            break
        else
            echo "❌ 格式错误！Secret Key 应以 'sk-lf-' 开头，请重新输入"
        fi
    done
    
    echo ""
    echo "✅ 密钥格式验证通过！"
    echo ""
    
    # 更新 .env 文件
    echo "📝 步骤 4: 更新 .env 文件..."
    
    # 备份原文件
    cp .env .env.backup
    echo "   已创建备份: .env.backup"
    
    # 使用 sed 替换占位符
    sed -i "s|LANGFUSE_PUBLIC_KEY=pk-lf-placeholder.*|LANGFUSE_PUBLIC_KEY=$PUBLIC_KEY|g" .env
    sed -i "s|LANGFUSE_SECRET_KEY=sk-lf-placeholder.*|LANGFUSE_SECRET_KEY=$SECRET_KEY|g" .env
    
    echo "   ✅ .env 文件已更新"
    echo ""
    
    # 验证配置
    echo "🔍 步骤 5: 验证配置..."
    if grep -q "$PUBLIC_KEY" .env && grep -q "$SECRET_KEY" .env; then
        echo "   ✅ 配置已成功写入 .env 文件"
    else
        echo "   ❌ 配置写入失败，请手动编辑 .env 文件"
        exit 1
    fi
    echo ""
    
    # 显示下一步操作
    echo "============================================================================"
    echo "🎉 配置完成！"
    echo "============================================================================"
    echo ""
    echo "下一步操作:"
    echo "  1. 重新构建并启动后端服务:"
    echo "     docker-compose -f docker-compose-dev.yml build langgraph-api"
    echo "     docker-compose -f docker-compose-dev.yml up -d"
    echo ""
    echo "  2. 运行连接测试:"
    echo "     docker exec -it langgraph-api python /deps/backend/test_langfuse_connection.py"
    echo ""
    echo "  3. 查看 LangFuse Dashboard:"
    echo "     http://localhost:3000"
    echo ""
    echo "📚 详细文档: QUICKSTART_LANGFUSE.md"
    echo ""
else
    echo "============================================================================"
    echo "⚠️  请先启动 LangFuse 服务，然后重新运行此脚本"
    echo "============================================================================"
    exit 1
fi
