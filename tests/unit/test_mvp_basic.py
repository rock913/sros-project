"""MVP 基本功能测试"""

from pathlib import Path
import pytest
from sros.cli import app
from typer.testing import CliRunner
from sros.gateway.main import SROSGateway
from sros.domain.ports.manuscript_protocol import ManuscriptProtocol
from sros.domain.ports.scholar_protocol import ScholarProtocol
from sros.domain.ports.memory_protocol import MemoryProtocol
from sros.domain.ports.zotero_protocol import ZoteroProtocol

def test_cli_help():
    """测试 CLI 帮助命令"""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output

def test_gateway_import(monkeypatch, tmp_path):
    """测试网关可以被导入"""
    # 这应该不会引发异常
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
    gateway = SROSGateway()
    assert gateway is not None

def test_protocols_exist():
    """测试所有协议都存在"""
    # 测试 ManuscriptProtocol
    assert hasattr(ManuscriptProtocol, 'find_gaps')
    assert hasattr(ManuscriptProtocol, 'get_outline_tree')
    assert hasattr(ManuscriptProtocol, 'insert_section')
    assert hasattr(ManuscriptProtocol, 'patch_draft')
    
    # 测试 ScholarProtocol
    assert hasattr(ScholarProtocol, 'brainstorm_perspectives')
    assert hasattr(ScholarProtocol, 'find_critiques')
    assert hasattr(ScholarProtocol, 'federated_search')
    
    # 测试 MemoryProtocol
    assert hasattr(MemoryProtocol, 'store_knowledge')
    assert hasattr(MemoryProtocol, 'query_knowledge')
    assert hasattr(MemoryProtocol, 'get_citation_map')
    
    # 测试 ZoteroProtocol
    assert hasattr(ZoteroProtocol, 'add_citation')
    assert hasattr(ZoteroProtocol, 'get_citation')
    assert hasattr(ZoteroProtocol, 'search_citations')

def test_find_gaps_exists():
    """测试 find_gaps 方法存在"""
    # 通过导入验证方法存在
    from sros.servers.manuscript.handler import ManuscriptHandler
    handler = ManuscriptHandler()
    assert hasattr(handler, 'find_gaps')
    assert callable(getattr(handler, 'find_gaps'))

def test_sse_endpoint_available(monkeypatch, tmp_path):
    """测试 SSE 端点可用"""
    # 简单测试网关路由是否正确设置
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
    gateway = SROSGateway()
    assert gateway.app is not None
    # 检查是否有健康检查端点
    routes = [route.path for route in gateway.app.routes]
    assert "/health" in routes
    assert "/tools" in routes
    assert "/sse" in routes

if __name__ == "__main__":
    pytest.main([__file__, "-v"])