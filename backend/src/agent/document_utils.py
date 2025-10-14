"""
Document Streaming Utilities for Real-time Collaboration

This module provides utilities for:
1. Paragraph-level diff generation
2. Document conflict detection
3. WebSocket message payload creation
4. Incremental document updates

Used by the synthesis node to stream report generation in real-time.
"""

import hashlib
import difflib
from typing import Dict, List, Optional, Any, Tuple
import re


class DocumentDiffer:
    """
    Handles document comparison and incremental update generation.
    
    Uses Python's difflib for efficient paragraph-level comparison.
    Operates at paragraph level for optimal UX (not too fine, not too coarse).
    """
    
    def __init__(self):
        pass
    
    def extract_paragraphs(self, text: str) -> List[str]:
        """
        Split Markdown text into paragraphs.
        
        Paragraphs are separated by double newlines (\n\n).
        Preserves code blocks and other Markdown structures.
        
        Args:
            text: Full Markdown document
            
        Returns:
            List of paragraph strings (without separator)
        """
        if not text:
            return []
        
        # Split by double newline, filter empty strings
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return paragraphs
    
    def calculate_line_range(
        self, 
        full_text: str, 
        paragraph_index: int
    ) -> Dict[str, int]:
        """
        Convert paragraph index to line numbers in full document.
        
        Args:
            full_text: Complete document text
            paragraph_index: Index of paragraph (0-based)
            
        Returns:
            Dictionary with startLine, endLine, startColumn, endColumn
        """
        paragraphs = self.extract_paragraphs(full_text)
        
        if paragraph_index >= len(paragraphs):
            # Return end of document
            lines = full_text.split('\n')
            return {
                "startLine": len(lines),
                "startColumn": 0,
                "endLine": len(lines),
                "endColumn": 0
            }
        
        # Find the paragraph in original text
        target_para = paragraphs[paragraph_index]
        
        # Calculate lines up to this paragraph
        lines_before = 0
        current_text = ""
        for i, para in enumerate(paragraphs):
            if i < paragraph_index:
                current_text += para + "\n\n"
                lines_before = current_text.count('\n')
        
        # Paragraph starts at lines_before
        # Paragraph ends at lines_before + lines in paragraph
        para_lines = target_para.count('\n') + 1
        
        return {
            "startLine": lines_before,
            "startColumn": 0,
            "endLine": lines_before + para_lines,
            "endColumn": 0
        }
    
    def generate_paragraph_diff(
        self, 
        old_text: str, 
        new_text: str
    ) -> List[Dict[str, Any]]:
        """
        Generate paragraph-level diffs between two document versions.
        
        Uses difflib.SequenceMatcher for accurate diff generation.
        
        Args:
            old_text: Previous version of document
            new_text: New version of document
            
        Returns:
            List of diff operations with action, content, and range
        """
        old_paras = self.extract_paragraphs(old_text)
        new_paras = self.extract_paragraphs(new_text)
        
        diffs = []
        
        # Use difflib to compare sequences
        matcher = difflib.SequenceMatcher(None, old_paras, new_paras)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                # Unchanged paragraphs
                for i in range(j1, j2):
                    diffs.append({
                        "action": "unchanged",
                        "paragraph_index": i,
                        "content": new_paras[i],
                        "range": self.calculate_line_range(new_text, i)
                    })
                    
            elif tag == 'replace':
                # Modified paragraphs
                for i in range(max(i2-i1, j2-j1)):
                    old_idx = i1 + i if (i1 + i) < i2 else None
                    new_idx = j1 + i if (j1 + i) < j2 else None
                    
                    if old_idx is not None and new_idx is not None:
                        diffs.append({
                            "action": "replace",
                            "paragraph_index": new_idx,
                            "content": new_paras[new_idx],
                            "old_content": old_paras[old_idx],
                            "range": self.calculate_line_range(new_text, new_idx)
                        })
                    elif new_idx is not None:
                        diffs.append({
                            "action": "insert",
                            "paragraph_index": new_idx,
                            "content": new_paras[new_idx],
                            "range": self.calculate_line_range(new_text, new_idx)
                        })
                    elif old_idx is not None:
                        diffs.append({
                            "action": "delete",
                            "paragraph_index": old_idx,
                            "content": old_paras[old_idx],
                            "range": self.calculate_line_range(old_text, old_idx)
                        })
                        
            elif tag == 'delete':
                # Deleted paragraphs
                for i in range(i1, i2):
                    diffs.append({
                        "action": "delete",
                        "paragraph_index": i,
                        "content": old_paras[i],
                        "range": self.calculate_line_range(old_text, i)
                    })
                    
            elif tag == 'insert':
                # Inserted paragraphs
                for i in range(j1, j2):
                    diffs.append({
                        "action": "insert",
                        "paragraph_index": i,
                        "content": new_paras[i],
                        "range": self.calculate_line_range(new_text, i)
                    })
        
        return diffs
    
    def generate_update_message(
        self, 
        diff: Dict[str, Any],
        rationale: str = ""
    ) -> Dict[str, Any]:
        """
        Create WebSocket message payload for a document update.
        
        Args:
            diff: Diff operation from generate_paragraph_diff()
            rationale: Human-readable explanation of why this change was made
            
        Returns:
            WebSocket message dictionary ready to send
        """
        return {
            "type": "document_update",
            "action": diff["action"],
            "range": diff["range"],
            "content": diff["content"],
            "rationale": rationale or f"AI {diff['action']} paragraph {diff['paragraph_index']}"
        }


class ConflictDetector:
    """
    Detects conflicts between user edits and AI edits.
    
    Uses document version hashing to track changes.
    Identifies overlapping edits that require user resolution.
    """
    
    @staticmethod
    def calculate_hash(text: str) -> str:
        """Calculate SHA-256 hash of document content."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def detect_conflict(
        base_text: str,
        user_text: str,
        ai_text: str
    ) -> Dict[str, Any]:
        """
        Detect if user and AI have conflicting edits.
        
        Three-way comparison:
        - base_text: Last known version before any edits
        - user_text: User's current version
        - ai_text: AI's proposed version
        
        Args:
            base_text: Original version
            user_text: User-edited version
            ai_text: AI-generated version
            
        Returns:
            {
                "is_conflict": bool,
                "conflict_type": "none" | "non_overlapping" | "overlapping",
                "user_changes": List[diff],
                "ai_changes": List[diff],
                "overlapping_ranges": List[range]
            }
        """
        differ = DocumentDiffer()
        
        # Get user's changes from base
        user_diffs = differ.generate_paragraph_diff(base_text, user_text)
        user_changed_paras = {
            d["paragraph_index"] 
            for d in user_diffs 
            if d["action"] != "unchanged"
        }
        
        # Get AI's changes from base
        ai_diffs = differ.generate_paragraph_diff(base_text, ai_text)
        ai_changed_paras = {
            d["paragraph_index"] 
            for d in ai_diffs 
            if d["action"] != "unchanged"
        }
        
        # Check for overlapping edits
        overlapping = user_changed_paras & ai_changed_paras
        
        if not overlapping:
            # No conflict - changes are in different paragraphs
            return {
                "is_conflict": False,
                "conflict_type": "none" if not user_changed_paras else "non_overlapping",
                "user_changes": [d for d in user_diffs if d["action"] != "unchanged"],
                "ai_changes": [d for d in ai_diffs if d["action"] != "unchanged"],
                "overlapping_ranges": []
            }
        
        # Conflict detected - both edited same paragraphs
        overlapping_ranges = []
        for para_idx in overlapping:
            # Find the range in original document
            user_diff = next((d for d in user_diffs if d["paragraph_index"] == para_idx), None)
            if user_diff:
                overlapping_ranges.append(user_diff["range"])
        
        return {
            "is_conflict": True,
            "conflict_type": "overlapping",
            "user_changes": [d for d in user_diffs if d["paragraph_index"] in overlapping],
            "ai_changes": [d for d in ai_diffs if d["paragraph_index"] in overlapping],
            "overlapping_ranges": overlapping_ranges
        }
    
    @staticmethod
    def generate_conflict_message(
        conflict: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Create WebSocket message for conflict notification.
        
        Args:
            conflict: Result from detect_conflict()
            session_id: Research session ID
            
        Returns:
            WebSocket message dictionary
        """
        return {
            "type": "document_conflict",
            "session_id": session_id,
            "conflict_type": conflict["conflict_type"],
            "overlapping_ranges": conflict["overlapping_ranges"],
            "user_changes": conflict["user_changes"],
            "ai_changes": conflict["ai_changes"],
            "resolution_options": [
                "keep_user",
                "keep_ai",
                "manual_merge"
            ]
        }


def merge_non_overlapping_edits(
    base_text: str,
    user_text: str,
    ai_text: str
) -> str:
    """
    Automatically merge non-overlapping edits from user and AI.
    
    When user and AI edit different paragraphs, combine both changes.
    This is safe because there's no conflict.
    
    Args:
        base_text: Original version
        user_text: User-edited version
        ai_text: AI-edited version
        
    Returns:
        Merged text with both user and AI changes
    """
    differ = DocumentDiffer()
    detector = ConflictDetector()
    
    # Check for conflicts first
    conflict = detector.detect_conflict(base_text, user_text, ai_text)
    
    if conflict["is_conflict"]:
        # Cannot auto-merge overlapping edits
        raise ValueError("Cannot auto-merge: overlapping edits detected")
    
    # Get all changes
    base_paras = differ.extract_paragraphs(base_text)
    user_paras = differ.extract_paragraphs(user_text)
    ai_paras = differ.extract_paragraphs(ai_text)
    
    # Start with base
    merged_paras = base_paras.copy()
    
    # Apply user changes
    user_diffs = differ.generate_paragraph_diff(base_text, user_text)
    for diff in user_diffs:
        if diff["action"] == "insert":
            merged_paras.insert(diff["paragraph_index"], diff["content"])
        elif diff["action"] == "replace":
            if diff["paragraph_index"] < len(merged_paras):
                merged_paras[diff["paragraph_index"]] = diff["content"]
        elif diff["action"] == "delete":
            if diff["paragraph_index"] < len(merged_paras):
                merged_paras.pop(diff["paragraph_index"])
    
    # Apply AI changes (to merged result)
    ai_diffs = differ.generate_paragraph_diff(base_text, ai_text)
    for diff in ai_diffs:
        if diff["action"] == "insert":
            merged_paras.insert(diff["paragraph_index"], diff["content"])
        elif diff["action"] == "replace":
            if diff["paragraph_index"] < len(merged_paras):
                merged_paras[diff["paragraph_index"]] = diff["content"]
        elif diff["action"] == "delete":
            if diff["paragraph_index"] < len(merged_paras):
                merged_paras.pop(diff["paragraph_index"])
    
    # Rejoin paragraphs
    return "\n\n".join(merged_paras)


# Convenience exports
__all__ = [
    "DocumentDiffer",
    "ConflictDetector",
    "merge_non_overlapping_edits"
]
