#!/usr/bin/env python3
"""
MCP Handler for Context Ingester
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, List
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class ContextIngesterMCPHandler:
    """MCP Handler for context ingestion"""
    
    def __init__(self):
        self.workspace_path = None
        
    def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        try:
            if method == "initialize":
                return self._handle_initialize(params)
            elif method == "ingest_materials":
                return self._handle_ingest_materials(params)
            elif method == "get_context_summary":
                return self._handle_get_context_summary(params)
            elif method == "search_soft_knowledge":
                return self._handle_search_soft_knowledge(params)
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not found"
                    }
                }
        except Exception as e:
            logger.error(f"Error handling request {method}: {e}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            
    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize the context ingester"""
        self.workspace_path = params.get("workspace_path", ".")
        logger.info(f"Context Ingester initialized with workspace: {self.workspace_path}")
        
        return {
            "result": {
                "capabilities": {
                    "methods": [
                        "ingest_materials",
                        "get_context_summary", 
                        "search_soft_knowledge"
                    ],
                    "version": "1.0.0"
                },
                "workspace": self.workspace_path
            }
        }
        
    def _handle_ingest_materials(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest materials from workspace"""
        workspace_path = params.get("workspace_path", self.workspace_path)
        materials_dir = Path(workspace_path) / "materials"
        ideas_file = Path(workspace_path) / "ideas.md"
        
        all_content = {}
        
        # Process ideas.md
        if ideas_file.exists():
            content = ideas_file.read_text(encoding='utf-8')
            all_content["ideas.md"] = self._parse_markdown_structure(content)
            
        # Process materials directory
        if materials_dir.exists():
            for file_path in materials_dir.glob("**/*.md"):
                content = file_path.read_text(encoding='utf-8')
                rel_path = file_path.relative_to(materials_dir)
                all_content[str(rel_path)] = self._parse_markdown_structure(content)
                
        # Process other material types
        for file_path in materials_dir.glob("**/*"):
            if file_path.suffix.lower() in ['.txt', '.pdf', '.docx']:
                rel_path = file_path.relative_to(materials_dir)
                content = self._extract_text_from_file(file_path)
                all_content[str(rel_path)] = self._parse_text_structure(content)
                
        # Store in knowledge graph (would connect to duckdb_memory in real implementation)
        summary = self._store_in_graph(all_content)
        
        return {"result": summary}
        
    def _parse_markdown_structure(self, content: str) -> Dict[str, Any]:
        """Parse markdown content into structured format"""
        lines = content.split('\n')
        structure = {
            "headers": [],
            "paragraphs": [],
            "lists": [],
            "tables": [],
            "code_blocks": [],
            "metadata": {}
        }
        
        # Extract headers
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                header_text = line.strip()[level:].strip()
                structure["headers"].append({
                    "level": level,
                    "text": header_text,
                    "line": i
                })
                
        # Extract paragraphs and other content
        current_paragraph = ""
        for line in lines:
            stripped = line.strip()
            if not stripped.startswith('#') and stripped:
                if stripped.startswith('- ') or stripped.startswith('* '):
                    structure["lists"].append(stripped)
                elif stripped.startswith('|'):
                    structure["tables"].append(stripped)
                elif stripped.startswith('```'):
                    structure["code_blocks"].append(stripped)
                else:
                    current_paragraph += stripped + " "
            else:
                if current_paragraph:
                    structure["paragraphs"].append(current_paragraph.strip())
                    current_paragraph = ""
                    
        if current_paragraph:
            structure["paragraphs"].append(current_paragraph.strip())
            
        return structure
        
    def _extract_text_from_file(self, file_path: Path) -> str:
        """Extract text from various file formats"""
        if file_path.suffix.lower() == '.txt':
            return file_path.read_text(encoding='utf-8')
        elif file_path.suffix.lower() == '.pdf':
            # Would use PyPDF2 or similar in real implementation
            return f"[PDF content from {file_path.name}]"
        elif file_path.suffix.lower() == '.docx':
            # Would use python-docx in real implementation  
            return f"[DOCX content from {file_path.name}]"
        else:
            return f"[Content from {file_path.name}]"
            
    def _parse_text_structure(self, content: str) -> Dict[str, Any]:
        """Parse plain text into structured format"""
        lines = content.split('\n')
        structure = {
            "sections": [],
            "paragraphs": [],
            "keywords": [],
            "entities": []
        }
        
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Filter short words
                word_freq[word] = word_freq.get(word, 0) + 1
                
        # Get top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        structure["keywords"] = [word for word, freq in sorted_words[:20]]
        
        # Split into paragraphs
        current_para = ""
        for line in lines:
            if line.strip():
                current_para += line.strip() + " "
            else:
                if current_para:
                    structure["paragraphs"].append(current_para.strip())
                    current_para = ""
                    
        if current_para:
            structure["paragraphs"].append(current_para.strip())
            
        return structure
        
    def _store_in_graph(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Store parsed content in knowledge graph"""
        total_items = 0
        for file_data in content.values():
            if isinstance(file_data, dict):
                total_items += len(file_data.get("headers", []))
                total_items += len(file_data.get("paragraphs", []))
                total_items += len(file_data.get("lists", []))
                
        summary = {
            "files_processed": len(content),
            "total_items_extracted": total_items,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        logger.info(f"Ingested {summary['files_processed']} files with {summary['total_items_extracted']} items")
        return summary
        
    def _handle_get_context_summary(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get summary of ingested context"""
        # Would query the knowledge graph in real implementation
        return {
            "result": {
                "summary": "Context summary would be retrieved from knowledge graph",
                "last_ingestion": "2026-02-04T06:00:00Z",
                "total_nodes": 150,
                "total_relationships": 45
            }
        }
        
    def _handle_search_soft_knowledge(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search for soft knowledge in ingested materials"""
        query = params.get("query", "")
        limit = params.get("limit", 10)
        
        # Would perform actual search in knowledge graph
        results = [
            {
                "source_file": "materials/deep_research.md",
                "section": "Introduction",
                "content": f"Relevant content related to '{query}'...",
                "confidence": 0.85,
                "relevance_score": 0.92
            }
        ][:limit]
        
        return {"result": {"results": results, "query": query, "limit": limit}}