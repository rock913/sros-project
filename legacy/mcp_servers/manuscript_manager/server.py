#!/usr/bin/env python3
"""
Manuscript Manager MCP Server
Core server for manuscript operations and atomic editing capabilities.
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import markdown
from markdown.extensions.toc import TocExtension

class ManuscriptManagerServer:
    """Manuscript Manager MCP Server implementation."""
    
    def __init__(self, manuscript_path: str = "draft.md"):
        """
        Initialize the Manuscript Manager server.
        
        Args:
            manuscript_path: Path to the manuscript file
        """
        self.manuscript_path = manuscript_path
        self._ensure_manuscript_exists()
    
    def _ensure_manuscript_exists(self):
        """Ensure the manuscript file exists."""
        manuscript_file = Path(self.manuscript_path)
        manuscript_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not manuscript_file.exists():
            # Create a basic manuscript template
            template = """# Research Draft

## Introduction

TODO: Write introduction

## Related Work

TODO: Review related work

## Methodology

TODO: Describe methodology

## Results

TODO: Present results

## Conclusion

TODO: Write conclusion

## References
"""
            manuscript_file.write_text(template)
    
    def get_structure(self) -> Dict[str, any]:
        """
        Get the current manuscript structure tree.
        
        Returns:
            Dictionary representing the manuscript structure with headers and their positions
        """
        if not os.path.exists(self.manuscript_path):
            return {"error": "Manuscript file not found"}
        
        with open(self.manuscript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse markdown structure
        lines = content.split('\n')
        structure = {
            "file": self.manuscript_path,
            "headers": [],
            "sections": {}
        }
        
        current_headers = []
        header_stack = []
        
        for i, line in enumerate(lines):
            # Match markdown headers (## Header)
            header_match = re.match(r'^(#{1,6})\s+(.+)', line.strip())
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                # Adjust header stack based on level
                while len(header_stack) >= level:
                    header_stack.pop()
                
                # Create header path
                header_path = header_stack + [title]
                header_key = ' > '.join(header_path)
                
                header_info = {
                    "level": level,
                    "title": title,
                    "line_number": i + 1,
                    "path": header_key
                }
                
                structure["headers"].append(header_info)
                structure["sections"][header_key] = {
                    "start_line": i + 1,
                    "content": ""
                }
                
                header_stack.append(title)
                current_headers = header_path[:]
        
        # Extract content for each section
        header_titles = [h["path"] for h in structure["headers"]]
        
        for i, header_title in enumerate(header_titles):
            start_line = structure["headers"][i]["line_number"]
            
            # Find end line (next header or end of file)
            if i + 1 < len(structure["headers"]):
                end_line = structure["headers"][i + 1]["line_number"] - 1
            else:
                end_line = len(lines)
            
            # Extract content between headers
            section_content = '\n'.join(lines[start_line:end_line])
            structure["sections"][header_title]["content"] = section_content.strip()
        
        return structure
    
    def detect_gaps(self) -> List[Dict[str, any]]:
        """
        Detect explicit and implicit gaps in the manuscript.
        
        Returns:
            List of detected gaps with their locations and descriptions
        """
        if not os.path.exists(self.manuscript_path):
            return [{"error": "Manuscript file not found"}]
        
        with open(self.manuscript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        gaps = []
        
        # Explicit gaps (TODO markers)
        for i, line in enumerate(lines):
            if 'TODO:' in line.upper():
                # Extract TODO content
                todo_match = re.search(r'TODO:\s*(.+)', line, re.IGNORECASE)
                if todo_match:
                    todo_content = todo_match.group(1).strip()
                else:
                    todo_content = "Complete this section"
                
                gaps.append({
                    "type": "explicit",
                    "description": todo_content,
                    "line_number": i + 1,
                    "section": self._get_section_for_line(i + 1, lines),
                    "priority": 1
                })
        
        # Implicit gaps (short sections, logic jumps, lack of citations)
        structure = self.get_structure()
        if "headers" in structure:
            for header_info in structure["headers"]:
                section_path = header_info["path"]
                if section_path in structure["sections"]:
                    section_content = structure["sections"][section_path]["content"]
                    
                    # Check for short sections
                    if len(section_content.strip()) < 50 and "TODO" not in section_content.upper():
                        gaps.append({
                            "type": "implicit",
                            "description": "Section appears too short and may need expansion",
                            "line_number": header_info["line_number"],
                            "section": section_path,
                            "priority": 2
                        })
                    
                    # Check for lack of citations
                    if not re.search(r'\[@\w+\]', section_content):
                        # Only flag sections that should have citations (not TODO sections)
                        if "TODO" not in section_content.upper() and len(section_content.strip()) > 100:
                            gaps.append({
                                "type": "implicit",
                                "description": "Section lacks citations and may need academic references",
                                "line_number": header_info["line_number"],
                                "section": section_path,
                                "priority": 3
                            })
        
        # Sort gaps by priority
        gaps.sort(key=lambda x: x.get("priority", 999))
        return gaps
    
    def _get_section_for_line(self, line_number: int, lines: List[str]) -> str:
        """
        Get the section name for a given line number.
        
        Args:
            line_number: Line number (1-based)
            lines: List of lines in the document
            
        Returns:
            Section name
        """
        # Find the last header before this line
        current_section = "Unknown"
        for i in range(line_number - 1, -1, -1):
            if i < len(lines):
                header_match = re.match(r'^(#{1,6})\s+(.+)', lines[i].strip())
                if header_match:
                    current_section = header_match.group(2).strip()
                    break
        
        return current_section
    
    def edit_section(self, section_path: str, content: str, mode: str = "append") -> bool:
        """
        Atomically edit a section in the manuscript.
        
        Args:
            section_path: Path to the section (e.g., "Introduction > Background")
            content: Content to insert/replace
            mode: Edit mode ("append", "prepend", "replace")
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(self.manuscript_path):
            return False
        
        # Read current content
        with open(self.manuscript_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find the section
        section_start, section_end = self._find_section_range(section_path, lines)
        if section_start is None:
            return False
        
        # Perform the edit based on mode
        if mode == "replace":
            # Replace the entire section content
            new_lines = lines[:section_start] + [content + '\n'] + lines[section_end:]
        elif mode == "append":
            # Append to the end of the section
            new_lines = lines[:section_end] + [content + '\n'] + lines[section_end:]
        elif mode == "prepend":
            # Prepend to the beginning of the section
            new_lines = lines[:section_start] + [content + '\n'] + lines[section_start:]
        else:
            return False
        
        # Write back to file
        with open(self.manuscript_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return True
    
    def _find_section_range(self, section_path: str, lines: List[str]) -> Tuple[Optional[int], Optional[int]]:
        """
        Find the start and end line numbers for a section.
        
        Args:
            section_path: Path to the section (can be simple name or hierarchical)
            lines: List of lines in the document
            
        Returns:
            Tuple of (start_line, end_line) or (None, None) if not found
        """
        # Handle both simple section names and hierarchical paths
        target_title = section_path
        if ' > ' in section_path:
            section_parts = section_path.split(' > ')
            target_title = section_parts[-1]
        
        section_start = None
        section_end = None
        
        # Find start of section
        for i, line in enumerate(lines):
            header_match = re.match(r'^(#{1,6})\s+(.+)', line.strip())
            if header_match:
                title = header_match.group(2).strip()
                
                # Check if this is our target section (match by title only)
                if title == target_title:
                    section_start = i + 1  # Start after the header line
                    target_level = len(header_match.group(1))
                    break
        
        if section_start is None:
            return None, None
        
        # Find end of section (next header of same or higher level, or end of file)
        for i in range(section_start, len(lines)):
            header_match = re.match(r'^(#{1,6})\s+(.+)', lines[i].strip())
            if header_match:
                level = len(header_match.group(1))
                if level <= target_level:
                    section_end = i
                    break
        
        if section_end is None:
            section_end = len(lines)
        
        return section_start, section_end
    
    def insert_content(self, section_path: str, content: str, citation_keys: List[str] = None) -> bool:
        """
        Insert cited content at a specified location in the manuscript.
        
        Args:
            section_path: Path to the section where content should be inserted
            content: Content to insert
            citation_keys: List of citation keys to include
            
        Returns:
            True if successful, False otherwise
        """
        if citation_keys:
            # Format citations in markdown style
            citation_str = " ".join([f"[@{key}]" for key in citation_keys])
            content = f"{content} {citation_str}"
        
        return self.edit_section(section_path, content, mode="append")
    
    def get_section_content(self, section_path: str) -> Optional[str]:
        """
        Get the content of a specific section.
        
        Args:
            section_path: Path to the section (can be simple name or hierarchical)
            
        Returns:
            Section content or None if not found
        """
        structure = self.get_structure()
        if "sections" not in structure:
            return None
            
        # First try exact match
        if section_path in structure["sections"]:
            return structure["sections"][section_path]["content"]
            
        # If not found, try to find by simple name matching
        target_title = section_path
        if ' > ' in section_path:
            target_title = section_path.split(' > ')[-1]
            
        # Look for any section that ends with this title
        for section_key, section_data in structure["sections"].items():
            if section_key.endswith(f" > {target_title}") or section_key == target_title:
                return section_data["content"]
                
        return None

# Server initialization for MCP
def create_server(manuscript_path: str = "draft.md") -> ManuscriptManagerServer:
    """
    Create and initialize the Manuscript Manager server.
    
    Args:
        manuscript_path: Path to the manuscript file
        
    Returns:
        Initialized ManuscriptManagerServer instance
    """
    return ManuscriptManagerServer(manuscript_path)

if __name__ == "__main__":
    # Example usage
    server = create_server()
    print("Manuscript Manager Server initialized successfully!")
    
    # Show structure
    structure = server.get_structure()
    print(f"Manuscript structure: {structure}")
    
    # Detect gaps
    gaps = server.detect_gaps()
    print(f"Detected gaps: {gaps}")