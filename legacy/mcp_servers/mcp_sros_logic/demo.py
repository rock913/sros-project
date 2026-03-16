#!/usr/bin/env python3
"""
Demo script for SROS Logic Server enhanced functionality.
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the server directly
from server import SROSLogicServer

def create_sample_manuscript(workspace_path: str):
    """Create a sample manuscript for testing."""
    draft_path = Path(workspace_path) / "draft.md"
    with open(draft_path, 'w') as f:
        f.write("""# Research on Artificial Intelligence in Healthcare

## Abstract
This paper explores the applications of artificial intelligence in healthcare.

## Introduction
Artificial intelligence has become increasingly important in healthcare.

## Related Work
Previous studies have shown various applications.

## Methodology
We conducted a comprehensive review.

## Results
Our findings indicate significant potential.

## Discussion
The implications are profound.

## Conclusion
AI will transform healthcare delivery.

## References
No references cited yet.
""")

def main():
    """Demonstrate enhanced SROS Logic Server functionality."""
    print("=== SROS Logic Server Enhanced Demo ===\n")
    
    # Create a temporary workspace for testing
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary workspace: {temp_dir}\n")
    
    try:
        # Create sample manuscript
        create_sample_manuscript(temp_dir)
        
        # Initialize server
        server = SROSLogicServer(temp_dir)
        
        # 1. Initialize workspace
        print("1. Initializing workspace...")
        init_result = server.init_workspace()
        if init_result["success"]:
            print(f"   ✓ {init_result['message']}")
            print(f"   ✓ Directories: {len(init_result['directories_created'])}")
            print(f"   ✓ Files: {len(init_result['files_created'])}")
        else:
            print(f"   ✗ Failed: {init_result['error']}")
        print()
        
        # 2. Detect academic gaps
        print("2. Detecting academic gaps...")
        gaps_result = server.detect_academic_gaps()
        if gaps_result["success"]:
            print(f"   ✓ {gaps_result['analysis']}")
            print(f"   ✓ Quality Score: {gaps_result['quality_score']}/100")
            gaps = gaps_result["gaps"]
            if gaps:
                print(f"   ✓ Found {len(gaps)} gaps:")
                high_priority = [g for g in gaps if g.get('priority') == 'high']
                medium_priority = [g for g in gaps if g.get('priority') == 'medium']
                low_priority = [g for g in gaps if g.get('priority') == 'low']
                info_priority = [g for g in gaps if g.get('priority') == 'info']
                
                if high_priority:
                    print(f"     🔴 {len(high_priority)} High Priority:")
                    for i, gap in enumerate(high_priority[:2], 1):
                        print(f"       {i}. {gap['description']}")
                        print(f"           Section: {gap['section']}")
                        if 'suggestion' in gap:
                            print(f"           Suggestion: {gap['suggestion']}")
                
                if medium_priority:
                    print(f"     🟡 {len(medium_priority)} Medium Priority:")
                    for i, gap in enumerate(medium_priority[:2], 1):
                        print(f"       {i}. {gap['description']}")
                        print(f"           Section: {gap['section']}")
                        if 'suggestion' in gap:
                            print(f"           Suggestion: {gap['suggestion']}")
            else:
                print("   ✓ No gaps detected")
            
            # Show analysis report highlights
            analysis = gaps_result.get("analysis_report", {})
            if analysis:
                print(f"   ✓ Analysis Report:")
                print(f"     - Structure Analysis: {analysis.get('structure_analysis', {}).get('total_sections', 0)} sections")
                print(f"     - Content Gaps: {analysis.get('content_analysis', {}).get('manuscript_gaps', 0)} from manuscript manager")
                print(f"     - Citation Gaps: {analysis.get('citation_analysis', {}).get('citation_gaps', 0)} from citation analysis")
        else:
            print(f"   ✗ Failed: {gaps_result['error']}")
        print()
        
        # 3. Research coordination
        print("3. Coordinating research activities...")
        coord_result = server.research_coordination()
        if coord_result["success"]:
            print(f"   ✓ {coord_result['message']}")
            results = coord_result.get("results", {})
            print(f"   ✓ Coordination Results:")
            print(f"     - Manuscript Sections: {results.get('manuscript_sections', 'N/A')}")
            print(f"     - Open Gaps: {results.get('open_gaps', 'N/A')}")
            print(f"     - Coordination Plan: {len(results.get('coordination_plan', []))} tasks")
            executed = results.get('executed_tasks', {})
            print(f"     - Executed Tasks: {executed.get('success_count', 0)}/{executed.get('total_count', 0)}")
        else:
            print(f"   ✗ Failed: {coord_result['error']}")
        print()
        
        # 4. Workflow management
        print("4. Managing research workflow...")
        workflow_result = server.workflow_management()
        if workflow_result["success"]:
            print(f"   ✓ {workflow_result['message']}")
            print(f"   ✓ Quality Score: {workflow_result['quality_score']}/100")
            print(f"   ✓ Gaps Found: {workflow_result['gaps_found']}")
            
            # Show workflow results summary
            results = workflow_result.get("results", {})
            summary = results.get("summary", {})
            if summary:
                print(f"   ✓ Workflow Summary:")
                print(f"     - Status: {summary.get('overall_status', 'unknown')}")
                recommendations = summary.get('recommendations', [])
                if recommendations:
                    print(f"     - Recommendations: {len(recommendations)}")
                    for rec in recommendations[:2]:
                        print(f"       • {rec}")
                next_steps = summary.get('next_steps', [])
                if next_steps:
                    print(f"     - Next Steps: {len(next_steps)}")
                    for step in next_steps[:2]:
                        print(f"       • {step}")
        else:
            print(f"   ✗ Failed: {workflow_result['error']}")
        print()
        
        print("=== Demo Complete ===")
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print(f"Cleaned up temporary workspace: {temp_dir}")

if __name__ == "__main__":
    main()