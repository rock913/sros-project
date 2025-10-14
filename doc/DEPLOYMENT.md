# 🚀 部署指南

**版本**: Phase 3.5.4  
**最后更新**: 2025-10-14  
**目标环境**: 生产环境 / 预发布环境

---

## 📋 目录

- [部署前准备](#部署前准备)
- [环境配置](#环境配置)
- [数据库迁移](#数据库迁移)
- [Docker部署](#docker部署)
- [验证部署](#验证部署)
- [回滚方案](#回滚方案)
- [监控和维护](#监控和维护)
- [故障排除](#故障排除)

---

## 🔧 部署前准备

### 1. 系统要求

**硬件要求**:
- CPU: 4核心以上
- 内存: 8GB以上（推荐16GB）
- 磁盘: 50GB可用空间（数据库和日志）

**软件要求**:
- Docker: 20.10+
- Docker Compose: 2.0+
- Git: 2.30+
- PostgreSQL Client: 14+（用于数据库管理）

### 2. 检查依赖

```bash
# 检查Docker版本
docker --version

# 检查Docker Compose版本
docker-compose --version

# 检查PostgreSQL客户端
psql --version

# 验证Docker服务运行
docker ps
```

### 3. 获取代码

```bash
# 克隆仓库
git clone https://github.com/AutoBrainLab/gemini-fullstack-langgraph-quickstart.git
cd gemini-fullstack-langgraph-quickstart

# 切换到稳定分支（生产环境）
git checkout main

# 或使用特定版本标签
git checkout tags/v3.5.4
```

---

## ⚙️ 环境配置

### 1. 创建环境变量文件

```bash
# 复制示例文件
cp .env.example .env

# 编辑环境变量
nano .env  # 或使用 vim/code
```

### 2. 必需的环境变量

```bash
# ============================================================================
# 生产环境最小配置
# ============================================================================

# AI服务 (必需)
GEMINI_API_KEY=your-actual-gemini-api-key-here

# 数据库 (必需)
POSTGRES_URI="postgresql://postgres:your-secure-password@langgraph-postgres:5432/postgres"

# 文献检索 (必需)
UNPAYWALL_EMAIL=your-production-email@example.com

# 可观测性 (强烈推荐)
LANGSMITH_API_KEY=your-langsmith-api-key-here
LANGSMITH_PROJECT=gemini-production

# 环境标识
ENVIRONMENT=production

# 安全配置
POSTGRES_SSL_MODE=require
CORS_ORIGINS=https://your-frontend-domain.com

# 性能配置
WEBSOCKET_HEARTBEAT_INTERVAL=30
SESSION_DETAILS_EVENT_LIMIT=50
API_REQUEST_TIMEOUT=300

# 日志级别
LOG_LEVEL=INFO
```

### 3. 验证配置

```bash
# 使用内置脚本验证环境变量
make check-env

# 或手动验证
python backend/src/check_env.py
```

**预期输出**:
```
✓ GEMINI_API_KEY: 已设置
✓ POSTGRES_URI: 已设置
✓ UNPAYWALL_EMAIL: 已设置
✓ LANGSMITH_API_KEY: 已设置
✅ 所有必需环境变量已配置
```

---

## 🗄️ 数据库迁移

### 1. 执行迁移脚本

Phase 3.5.4 包含数据库性能优化索引，需要在首次部署时执行：

```bash
# 启动PostgreSQL容器
docker-compose up -d langgraph-postgres

# 等待数据库就绪
sleep 10

# 执行索引迁移
docker exec -i langgraph-postgres psql -U postgres -d postgres < backend/migrations/001_add_indexes.sql
```

**预期输出**:
```
================================================
开始创建数据库性能优化索引...
================================================

📄 Papers 表索引...
  ✓ 创建 idx_papers_session_id
  ✓ 创建 idx_papers_doi
  ✓ 创建 idx_papers_created_at

📊 Reports 表索引...
  ✓ 创建 idx_reports_session_id
  ✓ 创建 idx_reports_session_version

...

✅ 所有索引创建成功！
```

### 2. 验证索引

```bash
# 检查索引数量
docker exec langgraph-postgres psql -U postgres -d postgres -c \
  "SELECT schemaname, tablename, COUNT(*) as index_count 
   FROM pg_indexes 
   WHERE schemaname = 'public' 
   GROUP BY schemaname, tablename 
   ORDER BY tablename;"
```

**预期结果**:
```
 schemaname |   tablename    | index_count 
------------+----------------+-------------
 public     | papers         | 4+
 public     | reports        | 3+
 public     | session_events | 5+
 public     | sessions       | 4+
```

### 3. 备份数据库（生产环境）

```bash
# 创建备份目录
mkdir -p backups

# 导出数据库
docker exec langgraph-postgres pg_dump -U postgres -d postgres > backups/pre_deployment_$(date +%Y%m%d_%H%M%S).sql

# 验证备份
ls -lh backups/
```

---

## 🐳 Docker部署

### 1. 构建镜像

```bash
# 生产环境构建
docker-compose -f docker-compose.yml build

# 查看构建的镜像
docker images | grep gemini
```

### 2. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps
```

**预期输出**:
```
NAME                    STATUS              PORTS
langgraph-postgres      Up 10 seconds       0.0.0.0:5433->5432/tcp
langgraph-api           Up 8 seconds        0.0.0.0:8123->8000/tcp
vscode-dev              Up 5 seconds        0.0.0.0:8121->8121/tcp
```

### 3. 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f vscode-dev

# 查看最近100行
docker-compose logs --tail=100 vscode-dev
```

---

## ✅ 验证部署

### 1. 健康检查

```bash
# 基础健康检查
curl http://localhost:8121/ok
# 预期: {"status":"ok"}

# 完整健康检查
curl http://localhost:8121/health | jq .
```

**预期响应**:
```json
{
  "status": "healthy",
  "version": "3.5.4",
  "timestamp": "2025-10-14T10:30:00.123456",
  "dependencies": {
    "database": {
      "status": "healthy",
      "response_time_ms": 15.23,
      "type": "postgresql"
    },
    "langgraph": {
      "status": "healthy",
      "response_time_ms": 8.45,
      "url": "http://localhost:8123"
    },
    "environment": {
      "status": "healthy",
      "configured_variables": 2
    },
    "filesystem": {
      "status": "healthy",
      "response_time_ms": 1.12
    }
  },
  "performance": {
    "total_response_time_ms": 45.67,
    "healthy_dependencies": 4,
    "total_dependencies": 4,
    "health_percentage": 100.0
  }
}
```

### 2. API功能测试

```bash
# 测试会话列表
curl http://localhost:8121/sessions?limit=10 | jq '.[] | {id, title, status}'

# 测试论文列表
curl http://localhost:8121/papers?limit=5 | jq '.[] | {title, authors}'

# 测试报告列表
curl http://localhost:8121/reports?limit=3 | jq '.[] | {id, version}'
```

### 3. 性能基准测试

```bash
# 运行完整基准测试
cd backend/tests
./benchmark_phase_3.5.4.sh

# 查看报告
cat benchmark_report_*.md
```

### 4. 集成测试

```bash
# 运行Phase 3.5.4集成测试
cd backend/tests
./test_phase_3.5.4.sh
```

**预期输出**: 7/7 测试通过

---

## 🔄 回滚方案

### 场景1: 索引导致性能问题

```bash
# 回滚索引
docker exec -i langgraph-postgres psql -U postgres -d postgres < backend/migrations/001_add_indexes_rollback.sql

# 重启服务
docker-compose restart vscode-dev
```

### 场景2: 应用代码问题

```bash
# 停止服务
docker-compose down

# 切换到上一个稳定版本
git checkout tags/v3.5.3

# 重新构建和启动
docker-compose build
docker-compose up -d

# 恢复数据库（如果需要）
docker exec -i langgraph-postgres psql -U postgres -d postgres < backups/pre_deployment_20251014_103000.sql
```

### 场景3: 数据库损坏

```bash
# 停止数据库
docker-compose stop langgraph-postgres

# 恢复备份
docker exec -i langgraph-postgres psql -U postgres -d postgres < backups/latest_backup.sql

# 重启服务
docker-compose up -d
```

---

## 📊 监控和维护

### 1. 日志管理

**日志位置**:
- 应用日志: `logs/e2e_test_*.log`
- Docker日志: `docker-compose logs`
- 数据库日志: 容器内 `/var/log/postgresql/`

**日志轮转**:
```bash
# 配置logrotate (Linux)
sudo nano /etc/logrotate.d/gemini-langgraph

# 内容示例:
/path/to/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

### 2. 数据库维护

**定期备份** (cron任务):
```bash
# 编辑crontab
crontab -e

# 每天凌晨3点备份
0 3 * * * docker exec langgraph-postgres pg_dump -U postgres -d postgres > /backups/daily_$(date +\%Y\%m\%d).sql
```

**性能监控**:
```bash
# 查看慢查询
docker exec langgraph-postgres psql -U postgres -d postgres -c \
  "SELECT query, calls, total_time, mean_time 
   FROM pg_stat_statements 
   ORDER BY mean_time DESC 
   LIMIT 10;"
```

### 3. 应用监控

**健康检查定时任务**:
```bash
# 每5分钟检查一次
*/5 * * * * curl -f http://localhost:8121/health || echo "Health check failed" | mail -s "Alert" admin@example.com
```

**Prometheus指标** (未来实现):
```bash
# 访问指标端点
curl http://localhost:8121/metrics
```

### 4. 容器资源监控

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
docker system df

# 清理未使用资源
docker system prune -a
```

---

## 🐛 故障排除

### 问题1: 数据库连接失败

**症状**:
```
Error: could not connect to server: Connection refused
```

**解决方案**:
```bash
# 检查容器运行状态
docker-compose ps

# 查看数据库日志
docker-compose logs langgraph-postgres

# 重启数据库
docker-compose restart langgraph-postgres

# 验证连接
docker exec langgraph-postgres psql -U postgres -c '\l'
```

### 问题2: API响应缓慢

**症状**: 请求响应时间 > 1秒

**诊断**:
```bash
# 运行性能测试
./backend/tests/benchmark_phase_3.5.4.sh

# 检查数据库索引
docker exec langgraph-postgres psql -U postgres -d postgres -c \
  "SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;"

# 查看容器资源
docker stats --no-stream
```

**解决方案**:
- 如果索引未使用 → 检查查询是否正确使用索引
- 如果CPU/内存高 → 增加容器资源限制
- 如果磁盘I/O高 → 考虑SSD或增加缓存

### 问题3: WebSocket连接断开

**症状**: 长时间研究任务中断

**检查**:
```bash
# 查看心跳配置
grep WEBSOCKET_HEARTBEAT_INTERVAL .env

# 查看WebSocket日志
docker-compose logs vscode-dev | grep "heartbeat"
```

**解决方案**:
```bash
# 调整心跳间隔（.env）
WEBSOCKET_HEARTBEAT_INTERVAL=20

# 重启服务
docker-compose restart vscode-dev
```

### 问题4: 环境变量未生效

**症状**: 应用使用默认值而非.env配置

**检查**:
```bash
# 验证容器环境变量
docker exec vscode-dev env | grep GEMINI

# 验证.env文件
cat .env | grep GEMINI
```

**解决方案**:
```bash
# 重新构建镜像（包含.env）
docker-compose down
docker-compose up -d --build
```

---

## 📞 支持和文档

### 相关文档
- [用户指南](./SESSION_DETAILS_VIEW_USER_GUIDE.md)
- [API示例](./SESSION_DETAILS_API_EXAMPLES.md)
- [OpenAPI规范](../openapi.yaml)
- [开发文档](../.ai-sessions/development/PHASE_3.5.4_COMPLETION_SUMMARY.md)

### 获取帮助
- GitHub Issues: https://github.com/AutoBrainLab/gemini-fullstack-langgraph-quickstart/issues
- 健康检查: `curl http://localhost:8121/health`
- 日志: `docker-compose logs -f`

### 版本历史
- **v3.5.4** (2025-10-14): 生产就绪 - 性能优化、Session Details View
- **v3.5.3** (2025-10-08): 增强测试、Analytics Dashboard
- **v3.5.2** (2025-09-29): 核心功能稳定版

---

## ✅ 部署检查清单

**部署前**:
- [ ] 服务器硬件满足要求
- [ ] Docker和Docker Compose已安装
- [ ] 代码已拉取到目标分支/标签
- [ ] .env文件已配置所有必需变量
- [ ] 环境变量已验证（`make check-env`）
- [ ] 数据库备份已创建

**部署中**:
- [ ] 数据库迁移已执行
- [ ] 索引创建已验证（25个索引）
- [ ] Docker镜像已构建
- [ ] 所有容器已启动
- [ ] 容器状态为"Up"

**部署后**:
- [ ] 基础健康检查通过（`/ok`）
- [ ] 完整健康检查通过（`/health`）
- [ ] API功能测试通过
- [ ] 性能基准测试通过（<500ms）
- [ ] 集成测试通过（7/7）
- [ ] 日志无严重错误
- [ ] 监控和告警已配置

**生产环境额外检查**:
- [ ] SSL证书已配置
- [ ] CORS已正确设置
- [ ] 日志轮转已配置
- [ ] 定时备份已设置
- [ ] 监控面板可访问
- [ ] 回滚方案已测试

---

**祝部署顺利！** 🎉

如有问题，请查看[故障排除](#故障排除)章节或提交GitHub Issue。
