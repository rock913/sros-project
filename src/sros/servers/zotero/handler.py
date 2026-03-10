from typing import List
import duckdb
import json
import os
from pathlib import Path
from sros.domain.ports import ZoteroProtocol
from sros.domain.schemas import Citation

class ZoteroHandler(ZoteroProtocol):
    """Zotero 服务实现 - 使用 DuckDB 持久化存储"""
    
    def __init__(self):
        # 使用工作区中的 graph.db 文件
        workspace_dir = os.getenv("SROS_WORKSPACE_DIR", ".")
        db_path = Path(workspace_dir) / ".sros" / "graph.db"
        
        # 确保目录存在
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = duckdb.connect(str(db_path))
        self._initialize_schema()
    
    def _initialize_schema(self):
        """初始化引用表结构"""
        # 创建引用表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                citekey VARCHAR PRIMARY KEY,
                title VARCHAR,
                authors JSON,
                year INTEGER,
                journal VARCHAR,
                url VARCHAR,
                bibtex TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self._migrate_citations_schema()
        
        # 创建索引
        try:
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_citations_year ON citations(year)")
        except Exception:
            # Migration should have added the column; don't block startup if index creation fails.
            pass

        try:
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_citations_journal ON citations(journal)")
        except Exception:
            pass

    def _migrate_citations_schema(self) -> None:
        """Best-effort schema migration for older graph.db files.

        Older workspaces may have a `citations` table missing newer columns
        (e.g. `year`). DuckDB will throw a Binder Error when we query/index
        missing columns.
        """
        try:
            rows = self.conn.execute("PRAGMA table_info('citations')").fetchall()
        except Exception:
            # If PRAGMA fails, there's nothing safe we can do.
            return

        existing_cols = {str(r[1]) for r in (rows or []) if len(r) > 1}

        # Minimum columns required by our queries and inserts.
        required_additions = [
            ("title", "VARCHAR"),
            ("authors", "JSON"),
            ("year", "INTEGER"),
            ("journal", "VARCHAR"),
            ("url", "VARCHAR"),
            ("bibtex", "TEXT"),
            ("created_at", "TIMESTAMP"),
            ("updated_at", "TIMESTAMP"),
        ]

        for col_name, col_type in required_additions:
            if col_name in existing_cols:
                continue
            try:
                self.conn.execute(f"ALTER TABLE citations ADD COLUMN {col_name} {col_type}")
            except Exception:
                # Keep migration best-effort; if the column can't be added we leave Zotero optional.
                continue
    
    def add_citation(self, citation: Citation) -> bool:
        """
        添加引用到数据库
        """
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO citations
                (citekey, title, authors, year, journal, url, bibtex, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, [
                citation.citekey,
                citation.title,
                json.dumps(citation.authors, ensure_ascii=False),
                citation.year,
                citation.journal,
                citation.url,
                citation.bibtex
            ])
            return True
        except Exception as e:
            print(f"Error adding citation: {str(e)}")
            return False
    
    def get_citation(self, citekey: str) -> Citation:
        """
        根据 citekey 获取引用信息
        """
        try:
            result = self.conn.execute("""
                SELECT citekey, title, authors, year, journal, url, bibtex
                FROM citations
                WHERE citekey = ?
            """, [citekey]).fetchone()
            
            if result:
                return Citation(
                    citekey=result[0],
                    title=result[1],
                    authors=json.loads(result[2]),
                    year=result[3],
                    journal=result[4],
                    url=result[5],
                    bibtex=result[6]
                )
            else:
                # 返回默认值或抛出异常
                raise ValueError(f"Citation with key '{citekey}' not found")
        except Exception as e:
            print(f"Error getting citation: {str(e)}")
            raise
    
    def search_citations(self, query: str) -> List[Citation]:
        """
        搜索引用
        """
        try:
            results = self.conn.execute("""
                SELECT citekey, title, authors, year, journal, url, bibtex
                FROM citations
                WHERE LOWER(title) LIKE LOWER(?)
                   OR LOWER(journal) LIKE LOWER(?)
                   OR citekey LIKE ?
                ORDER BY year DESC
            """, [f'%{query}%', f'%{query}%', f'%{query}%']).fetchall()
            
            citations = []
            for row in results:
                citations.append(Citation(
                    citekey=row[0],
                    title=row[1],
                    authors=json.loads(row[2]),
                    year=row[3],
                    journal=row[4],
                    url=row[5],
                    bibtex=row[6]
                ))
            
            return citations
        except Exception as e:
            print(f"Error searching citations: {str(e)}")
            return []
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'conn'):
            self.conn.close()