# Dev Container 配置说明

本项目使用多重 Dev Container 配置，支持前端和后端分离的开发环境。

## 配置结构

```
.devcontainer/
├── frontend/
│   └── devcontainer.json    # 前端开发环境
├── backend/
│   └── devcontainer.json    # 后端开发环境
└── README.md
```

## 使用方法

### 1. 选择开发环境

在 VS Code 中：
1. 按 `F1` 或 `Ctrl+Shift+P`
2. 输入 "Dev Containers: Open Folder in Container"
3. 选择要使用的配置：
   - **Frontend Dev** - 前端开发（Node.js、ESLint、Prettier）
   - **Backend Dev** - 后端开发（Python、LangGraph、FastAPI）

### 2. 环境说明

#### Frontend Dev
- **服务**: vscode-dev
- **工作目录**: `/workspaces/gemini-fullstack-langgraph-quickstart`
- **包含扩展**: ESLint, Prettier, Docker, Gemini
- **适用于**: 前端界面开发、样式调整

#### Backend Dev
- **服务**: langgraph-api
- **工作目录**: `/deps/backend`
- **包含扩展**: Python, Docker, Gemini
- **端口映射**: 8000 (容器) → 8121 (主机)
- **适用于**: API 开发、Agent 逻辑开发

## 故障排除

### 问题：连接 Backend Dev 时长期卡在 "Installing server"

**原因分析**：
1. VS Code Server 下载缓慢（网络问题）
2. postCreateCommand 执行耗时过长
3. Docker 镜像构建不完整

**解决方案**：

#### 方案 1：预构建 Docker 镜像
```bash
# 先构建镜像，确保所有依赖都已安装
docker compose -f docker-compose-dev.yml build langgraph-api
```

#### 方案 2：配置 Docker 镜像加速
编辑 `/etc/docker/daemon.json`（Linux）或 Docker Desktop 设置（Windows/Mac）：
```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com"
  ]
}
```

#### 方案 3：使用代理
如果有代理服务，在 devcontainer.json 中添加：
```json
{
  "containerEnv": {
    "HTTP_PROXY": "http://your-proxy:port",
    "HTTPS_PROXY": "http://your-proxy:port"
  }
}
```

#### 方案 4：跳过 VS Code Server 预安装
如果 Dockerfile.dev 中的 VS Code Server 预安装失败，可以临时注释掉：
```dockerfile
# RUN curl -fsSL https://aka.ms/install-vscode-server/setup.sh | sh
```

### 问题：容器内 Python 依赖缺失

**原因**：Docker 镜像构建时依赖安装失败

**解决方案**：
```bash
# 进入容器后手动安装
docker exec -it langgraph-api bash
cd /deps/backend
uv pip install --system -e .
```

### 问题：端口冲突

**原因**：8121 端口已被占用

**解决方案**：
```bash
# 检查端口占用
sudo lsof -i :8121
# 或修改 docker-compose-dev.yml 中的端口映射
```

## 最佳实践

1. **首次使用前**：先运行 `docker compose -f docker-compose-dev.yml build` 构建镜像
2. **网络环境差**：考虑使用镜像加速或离线安装包
3. **频繁切换**：关闭当前 Dev Container 后再打开另一个
4. **依赖更新**：修改 requirements 后，重新构建镜像

## 常用命令

```bash
# 构建所有服务
docker compose -f docker-compose-dev.yml build

# 启动所有服务
docker compose -f docker-compose-dev.yml up -d

# 查看日志
docker compose -f docker-compose-dev.yml logs -f langgraph-api

# 停止所有服务
docker compose -f docker-compose-dev.yml down

# 重建并启动
docker compose -f docker-compose-dev.yml up -d --build --force-recreate
```
