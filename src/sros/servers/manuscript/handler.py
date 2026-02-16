from typing import List, Dict, Any
import re
import os
from pathlib import Path
from sros.domain.ports import ManuscriptProtocol
from sros.domain.schemas import GapAnalysisResult, OutlineNode

def resolve_workspace_path(file_path: str) -> Path:
    """
    Resolve a workspace-relative file path.
    Enforces that file_path is relative to SROS_WORKSPACE_DIR and prevents path traversal.
    """
    workspace = Path(os.environ["SROS_WORKSPACE_DIR"])
    
    rel = Path(file_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("file_path must be workspace-relative (no absolute paths or '..')")
    
    resolved_path = (workspace / rel).resolve()
    
    # Verify the resolved path is still within the workspace
    try:
        resolved_path.relative_to(workspace.resolve())
    except ValueError:
        raise ValueError(f"file_path resolves outside workspace: {resolved_path}")
    
    return resolved_path

class ManuscriptHandler(ManuscriptProtocol):
    """稿件管理器实现"""
    
    def find_gaps(self, file_path: str = "draft.md") -> List[GapAnalysisResult]:
        """
        基于规则识别待办项
        """
        gaps = []
        
        try:
            # Resolve workspace-relative path
            path = resolve_workspace_path(file_path)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找 TODO 标记
            todo_pattern = r'\[TODO:\s*(.*?)\]'
            for match in re.finditer(todo_pattern, content):
                gaps.append(GapAnalysisResult(
                    section=f"Line {content[:match.start()].count(chr(10))+1}",
                    type="Task Pending",
                    confidence=0.9,
                    suggestions=[match.group(1)]
                ))
            
            # 查找短段落（可能需要扩展）
            paragraphs = content.split('\n\n')
            for i, para in enumerate(paragraphs):
                if len(para.strip()) > 0 and len(para.strip()) < 50:  # 少于50字符的段落
                    gaps.append(GapAnalysisResult(
                        section=f"Paragraph {i+1}",
                        type="Elaboration Needed",
                        confidence=0.7,
                        suggestions=["Expand this section with more details"]
                    ))
            
            # 查找缺少引用的部分
            if content.count('[@') == 0 and content.count('()]') == 0:  # 没有引用标记
                gaps.append(GapAnalysisResult(
                    section="Entire Document",
                    type="Citation Needed",
                    confidence=0.8,
                    suggestions=["Add relevant citations to support claims"]
                ))
                
        except FileNotFoundError:
            gaps.append(GapAnalysisResult(
                section="File Error",
                type="File Not Found",
                confidence=1.0,
                suggestions=[f"File {file_path} does not exist in workspace"]
            ))
        except KeyError:
            gaps.append(GapAnalysisResult(
                section="Environment Error",
                type="SROS_WORKSPACE_DIR not set",
                confidence=1.0,
                suggestions=["Please set SROS_WORKSPACE_DIR environment variable"]
            ))
        except ValueError as e:
            gaps.append(GapAnalysisResult(
                section="Path Security Error",
                type="Invalid path",
                confidence=1.0,
                suggestions=[str(e)]
            ))
        except Exception as e:
            gaps.append(GapAnalysisResult(
                section="Processing Error",
                type="Error",
                confidence=1.0,
                suggestions=[f"Error processing file: {str(e)}"]
            ))
            
        return gaps
    
    def get_outline_tree(self, file_path: str = "draft.md") -> OutlineNode:
        """
        返回 Markdown/AST 的树状结构
        """
        try:
            # Resolve workspace-relative path
            path = resolve_workspace_path(file_path)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 Markdown 标题来构建大纲
            lines = content.split('\n')
            root = OutlineNode(id="root", title="Document", level=0, content="", children=[])
            stack = [(root, -1)]  # (node, level)
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if line.startswith('#'):
                    # 计算标题级别
                    level = 0
                    for char in line:
                        if char == '#':
                            level += 1
                        elif char == ' ':
                            break
                        else:
                            break
                    
                    if level > 0:  # 有效标题
                        title = line[level:].strip()  # 移除 # 和空格
                        node_id = f"heading-{line_num}"
                        
                        # 找到合适的父节点
                        while stack and stack[-1][1] >= level:
                            stack.pop()
                        
                        new_node = OutlineNode(
                            id=node_id,
                            title=title,
                            level=level,
                            content="",
                            children=[]
                        )
                        
                        if stack:
                            parent, parent_level = stack[-1]
                            parent.children.append(new_node)
                        
                        stack.append((new_node, level))
            
            return root
        except KeyError:
            return OutlineNode(
                id="root",
                title="Environment Error",
                level=0,
                content="SROS_WORKSPACE_DIR not set",
                children=[]
            )
        except ValueError as e:
            return OutlineNode(
                id="root",
                title="Path Security Error",
                level=0,
                content=str(e),
                children=[]
            )
        except Exception:
            return OutlineNode(
                id="root",
                title="Document",
                level=0,
                content="Error reading document",
                children=[]
            )
    
    def insert_section(self, target: str, content: str, citations: List[str], file_path: str = "draft.md") -> bool:
        """
        带引用的增量写入
        """
        try:
            # Resolve workspace-relative path
            path = resolve_workspace_path(file_path)
            
            # 读取当前文件
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    current_content = f.read()
            else:
                current_content = ""
            
            # 添加内容和引用
            new_content = current_content + f"\n\n{content}"
            
            # 添加引用标记
            if citations:
                citation_text = " ".join([f"[@{cite}]" for cite in citations])
                new_content += f"\n\n{citation_text}"
            
            # 写回文件
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        except Exception:
            return False
    
    def patch_draft(self, patches: List[Dict[str, Any]], file_path: str = "draft.md") -> bool:
        """
        批量更新稿件内容
        """
        try:
            # Resolve workspace-relative path
            path = resolve_workspace_path(file_path)
            
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = ""
            
            # 应用补丁（简化实现：追加内容）
            for patch in patches:
                if patch.get('action') == 'append':
                    content += f"\n\n{patch.get('content', '')}"
                elif patch.get('action') == 'prepend':
                    content = f"{patch.get('content', '')}\n\n{content}"
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception:
            return False
