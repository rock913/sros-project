# Cline + Aider MCP 容器化实战指南 (v2026)

本指南旨在建立一个独立于具体项目的、可复用的 Aider MCP 执行引擎。通过容器化技术，Cline 可以像调用远程服务一样驱动 Aider 完成 TDD 闭环。

## 1. 架构定位：谁在做什么？

- **Cline (VS Code)**: 总指挥 (Architect)。负责解析需求、设计 Protocol、下达指令。
- **DeepSeek-R1 / Claude 4.5**: 大脑 (Intelligence)。提供推理、代码审查。
- **Aider MCP Container**: 执行车间 (Builder)。封装了 Aider CLI、Pytest、Ruff。
- **MCP Protocol**: 通信桥梁。Cline 通过 JSON-RPC 结构化参数驱动 Container。

## 2. 顶级模型选型 (2026 矩阵)

| 角色 | 推荐模型 | 关键参数 | API Provider |
| :--- | :--- | :--- | :--- |
| **指挥官 (Cline)** | claude-3.5/4.5 (首选) / deepseek-reasoner | Max Tokens: 8192 | Anthropic / DeepSeek |
| **执行员 (Aider)** | **dashscope/qwen-max** | High Performance/Cost Ratio | DashScope (Aliyun) |

## 3. 部署独立 Aider MCP 容器

### 第一步：准备 Dockerfile

建议新建文件: `backend/Dockerfile.aider`

```dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y git curl build-essential && rm -rf /var/lib/apt/lists/*

# 安装 Aider, MCP SDK 和常用工具
RUN pip install --no-cache-dir aider-chat mcp[cli] ruff pytest pydantic-ai

# 设置工作目录
WORKDIR /app

# 复制 MCP 服务脚本 (假设脚本位于backend/src下)
COPY backend/src/aider_mcp_launcher.py /usr/local/bin/aider_mcp_launcher.py

# 设置 PYTHONPATH
ENV PYTHONPATH=/app/backend/src

# 默认命令 (可被 docker-compose 覆盖)
CMD ["tail", "-f", "/dev/null"]
```

### 第二步：编写通用 MCP 启动脚本

建议新建文件: `backend/src/aider_mcp_launcher.py`

```python
import asyncio
import os
import sys
from mcp.server.fastmcp import FastMCP

# 初始化 MCP Server
mcp = FastMCP("Aider-Factory")

@mcp.tool()
async def execute_tdd_loop(
    project_root: str,
    interface_file: str,
    impl_file: str,
    test_file: str,
    instructions: str,
    model: str = "dashscope/qwen-max"
) -> str:
    """
    在指定项目中执行 Aider TDD 闭环。
    
    Args:
        project_root: 项目在容器内的挂载路径 (通常为 /app)
        interface_file: 接口文件路径 (例如 backend/src/agent/domain/ports/xyz.py)
        impl_file: 实现类文件路径
        test_file: 测试文件路径
        instructions: Aider 任务描述
        model: Aider 使用的模型，默认为 dashscope/qwen-max (参考 .clinerules)
    """
    # 切换到项目根目录
    if os.path.isabs(project_root):
        os.chdir(project_root)
    else:
        os.chdir(os.path.abspath(project_root))
        
    print(f"Working directory: {os.getcwd()}", file=sys.stderr)

    # 构建 Aider 命令
    # 注意: --yes 自动确认, --no-suggest-shell-commands 减少干扰
    # 使用 .clinerules 中推荐的参数配置
    cmd = [
        "aider", 
        "--model", model, 
        "--yes", 
        "--no-suggest-shell-commands",
        "--read", interface_file,
        "--file", impl_file, 
        "--file", test_file,
        "--lint-cmd", f"ruff check {impl_file} {test_file} --fix",
        "--test-cmd", f"pytest {test_file}",
        "--message", instructions
    ]
    
    # 环境变量传递 (确保容器已注入 KEYS)
    env = os.environ.copy()

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd, 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE,
            env=env
        )
        stdout, stderr = await process.communicate()
        
        output = f"## Execution Result\n\n### STDOUT\n{stdout.decode()}\n\n### STDERR\n{stderr.decode()}"
        return output
    except Exception as e:
        return f"Error executing Aider: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

## 4. 整合到 docker-compose-dev.yml

将 Aider MCP 作为一个长期运行的服务加入开发环境。

**添加到 `services` 部分:**

```yaml
  aider-agent:
    build:
      context: .
      dockerfile: backend/Dockerfile.aider
    container_name: aider-agent
    # 挂载整个项目到 /app，确保 Aider 能修改宿主机代码
    volumes:
      - .:/app
    environment:
      # 注入必要的 API Keys
      QWEN_API_KEY: ${QWEN_API_KEY}
      DASHSCOPE_API_KEY: ${DASHSCOPE_API_KEY:-}
      OPENAI_API_KEY: ${OPENAI_API_KEY:-}
      # 确保中文编码支持
      LANG: C.UTF-8
    # 保持容器运行，等待 Cline 调用
    command: tail -f /dev/null
```

## 5. 在 Cline 中配置 (cline_mcp_settings.json)

配置 Cline 连接到 Docker 容器内部执行 MCP 脚本。我们使用 `docker exec` 模式，这样不需要映射额外的端口，且能直接在已挂载好环境的容器中运行。

**操作步骤：**
1. 在 VS Code 中打开 Cline 侧边栏。
2. 点击输入框上方的 **MCP Servers** 图标（通常是一个插头形状）。
3. 选择 **"Configure MCP Servers"**。这将打开全局的 `cline_mcp_settings.json` 文件。
4. 将以下配置添加到 `mcpServers` 对象中：

```json
{
  "mcpServers": {
    "aider-container": {
      "command": "docker",
      "args": [
        "exec",
        "-i",           
        "aider-agent",  /* 对应 docker-compose service name 或 container_name */
        "python",
        "/usr/local/bin/aider_mcp_launcher.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**配置说明：**
- `command`: 使用 `docker` 命令。
- `args`: 使用 `exec -i` 进入正在运行的容器。
- `aider-agent`: 必须与 `docker-compose.yml` 中的容器名称一致。

## 总结

1. **构建镜像**: `docker-compose -f docker-compose-dev.yml build aider-agent`
2. **启动环境**: `docker-compose -f docker-compose-dev.yml up -d aider-agent`
3. **Cline 调用**: 配置好 MCP 后，Cline 即可通过 `execute_tdd_loop` 工具直接指挥容器内的 Aider 修改代码。
