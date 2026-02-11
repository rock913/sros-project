#!/usr/bin/env python3
"""
MVP Smoke Test
验证 SROS V2.3.2 MVP 是否满足验收标准
"""

import sys
import os
import tempfile
from pathlib import Path
import json

# 添加 src 到 Python 路径
sys.path.insert(0, 'src')

def test_mvp_requirements():
    """测试 MVP 的所有要求"""
    print("=== SROS V2.3.2 MVP Smoke Test ===\n")
    
    # 1. 测试 CLI 安装和帮助
    print("1. Testing CLI installation and help...")
    try:
        from sros.cli import app
        print("   ✓ CLI module imported successfully")
    except Exception as e:
        print(f"   ✗ Failed to import CLI: {e}")
        return False
    
    # 2. 测试协议定义
    print("2. Testing protocol definitions...")
    try:
        from sros.domain.ports.manuscript_protocol import ManuscriptProtocol
        from sros.domain.ports.scholar_protocol import ScholarProtocol
        from sros.domain.ports.memory_protocol import MemoryProtocol
        from sros.domain.ports.zotero_protocol import ZoteroProtocol
        print("   ✓ All protocols imported successfully")
        
        # 检查 find_gaps 方法
        if hasattr(ManuscriptProtocol, 'find_gaps'):
            print("   ✓ find_gaps method defined in ManuscriptProtocol")
        else:
            print("   ✗ find_gaps method missing from ManuscriptProtocol")
            return False
            
    except Exception as e:
        print(f"   ✗ Failed to import protocols: {e}")
        return False
    
    # 3. 测试服务实现
    print("3. Testing service implementations...")
    try:
        from sros.servers.manuscript.handler import ManuscriptHandler
        from sros.servers.scholar.handler import ScholarHandler
        from sros.servers.memory.handler import MemoryHandler
        from sros.servers.zotero.handler import ZoteroHandler
        
        # 测试 find_gaps 方法
        handler = ManuscriptHandler()
        if hasattr(handler, 'find_gaps') and callable(getattr(handler, 'find_gaps')):
            print("   ✓ ManuscriptHandler.find_gaps implemented")
        else:
            print("   ✗ ManuscriptHandler.find_gaps not properly implemented")
            return False
            
        print("   ✓ All service handlers created successfully")
        
    except Exception as e:
        print(f"   ✗ Failed to create service handlers: {e}")
        return False
    
    # 4. 测试网关功能
    print("4. Testing gateway functionality...")
    try:
        from sros.gateway.main import SROSGateway
        from fastapi.testclient import TestClient
        gateway = SROSGateway()
        print("   ✓ Gateway initialized successfully")
        
        # 检查路由
        routes = [route.path for route in gateway.app.routes]
        required_routes = ["/", "/health", "/tools", "/sse"]
        for route in required_routes:
            if route in routes:
                print(f"   ✓ Route {route} exists")
            else:
                print(f"   ⚠ Route {route} missing")

        # Verify /sse is real SSE (HTTP GET, text/event-stream)
        # Use one-shot mode to avoid hanging on an infinite stream during tests.
        client = TestClient(gateway.app)
        response = client.get("/sse?once=1")
        content_type = response.headers.get("content-type", "")
        if response.status_code == 200 and content_type.startswith("text/event-stream"):
            print("   ✓ /sse is SSE (text/event-stream)")
        else:
            print(f"   ✗ /sse is not SSE (status={response.status_code}, content-type={content_type})")
            return False
        if "event: ready" in response.text:
            print("   ✓ SSE stream yields initial ready event")
        else:
            print("   ⚠ SSE stream did not yield expected initial event")
                
    except Exception as e:
        print(f"   ✗ Failed to initialize gateway: {e}")
        return False
    
    # 5. 测试工作区初始化
    print("5. Testing workspace initialization...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            from sros.cli import init as cli_init

            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                cli_init("test_paper")
            finally:
                os.chdir(old_cwd)

            project_path = Path(tmpdir) / "test_paper"
            expected_paths = [
                project_path / ".roo" / "mcp.json",
                project_path / ".sros" / "graph.db",
                project_path / "draft.md",
                project_path / "ideas.md",
                project_path / "materials",
                project_path / "references",
            ]
            for p in expected_paths:
                if not p.exists():
                    print(f"   ✗ Missing expected path: {p}")
                    return False

            mcp_path = project_path / ".roo" / "mcp.json"
            mcp_config = json.loads(mcp_path.read_text(encoding="utf-8"))
            if "mcpServers" in mcp_config and "sros-gateway" in mcp_config.get("mcpServers", {}):
                print("   ✓ .roo/mcp.json uses mcpServers schema")
            else:
                print("   ✗ .roo/mcp.json schema invalid (expected mcpServers.sros-gateway)")
                return False

            gateway_cfg = mcp_config["mcpServers"]["sros-gateway"]
            if gateway_cfg.get("url") == "http://localhost:8000/sse" and gateway_cfg.get("type") == "sse":
                print("   ✓ Roo gateway config points to /sse and type=sse")
            else:
                print("   ✗ Roo gateway config incorrect (url/type mismatch)")
                return False

            print("   ✓ Workspace initialization via sros init works")
            
    except Exception as e:
        print(f"   ✗ Failed to create workspace: {e}")
        return False
    
    print("\n=== All MVP Requirements Passed ===")
    return True

if __name__ == "__main__":
    success = test_mvp_requirements()
    sys.exit(0 if success else 1)