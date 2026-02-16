from typing import List, Dict, Any
import duckdb
import json
import os
from pathlib import Path
from sros.domain.ports import MemoryProtocol
from sros.domain.schemas import KnowledgeEdge

class MemoryHandler(MemoryProtocol):
    """记忆服务实现 - 使用 DuckDB 持久化存储"""
    
    def __init__(self):
        # 使用工作区中的 graph.db 文件
        workspace_dir = os.getenv("SROS_WORKSPACE_DIR", ".")
        db_path = Path(workspace_dir) / ".sros" / "graph.db"
        
        # 确保目录存在
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = duckdb.connect(str(db_path))
        self._initialize_schema()
    
    def _initialize_schema(self):
        """初始化数据库表结构"""
        # 创建节点表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id VARCHAR PRIMARY KEY,
                type VARCHAR,
                title VARCHAR,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建边表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                id VARCHAR PRIMARY KEY,
                source VARCHAR,
                target VARCHAR,
                relationship VARCHAR,
                confidence FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_relationship ON edges(relationship)")
    
    def store_knowledge(self, nodes: List[Dict[str, Any]], edges: List[KnowledgeEdge]) -> bool:
        """
        存储知识节点和关系
        """
        try:
            # 插入或更新节点
            for node in nodes:
                node_id = node.get('id')
                if node_id:
                    self.conn.execute("""
                        INSERT OR REPLACE INTO nodes (id, type, title, content, updated_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, [
                        node_id,
                        node.get('type', ''),
                        node.get('title', ''),
                        json.dumps(node.get('content', {}), ensure_ascii=False)
                    ])
            
            # 插入或更新边
            for edge in edges:
                edge_id = f"edge_{hash(edge.source + edge.target + edge.relationship) % 1000000}"
                self.conn.execute("""
                    INSERT OR REPLACE INTO edges (id, source, target, relationship, confidence, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, [
                    edge_id,
                    edge.source,
                    edge.target,
                    edge.relationship,
                    edge.confidence
                ])
            
            return True
        except Exception as e:
            print(f"Error storing knowledge: {str(e)}")
            return False
    
    def query_knowledge(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        查询知识图谱
        """
        try:
            # 简单的全文搜索
            results = self.conn.execute("""
                SELECT id, type, title, content, created_at
                FROM nodes
                WHERE LOWER(title) LIKE LOWER(?) OR LOWER(content) LIKE LOWER(?)
                ORDER BY created_at DESC
                LIMIT ?
            """, [f'%{query}%', f'%{query}%', limit]).fetchall()
            
            return [
                {
                    "id": row[0],
                    "type": row[1],
                    "title": row[2],
                    "content": row[3],
                    "created_at": row[4].isoformat() if row[4] else None
                }
                for row in results
            ]
        except Exception as e:
            print(f"Error querying knowledge: {str(e)}")
            return []
    
    def get_citation_map(self, section_id: str) -> List[KnowledgeEdge]:
        """
        获取特定章节的引用关系图
        """
        try:
            results = self.conn.execute("""
                SELECT source, target, relationship, confidence
                FROM edges
                WHERE source = ? OR target = ?
                ORDER BY confidence DESC
            """, [section_id, section_id]).fetchall()
            
            return [
                KnowledgeEdge(
                    source=row[0],
                    target=row[1],
                    relationship=row[2],
                    confidence=row[3]
                )
                for row in results
            ]
        except Exception as e:
            print(f"Error getting citation map: {str(e)}")
            return []
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'conn'):
            self.conn.close()