#!/usr/bin/env python3
"""
Demo script for Zotero Expert MCP Server
Shows the enhanced functionality including local library reading and AI note synchronization.
"""

import os
import sys
import json
from server import ZoteroExpertServer
from mcp_handler import ZoteroExpertMCPHandler

def demo_zotero_expert():
    """Demonstrate the enhanced Zotero Expert functionality."""
    print("=== Zotero Expert MCP Server Demo ===\n")
    
    # Initialize server and handler
    server = ZoteroExpertServer()
    handler = ZoteroExpertMCPHandler()
    
    # Show capabilities
    print("1. Server Capabilities:")
    init_result = handler.handle_request("initialize", {})
    if "result" in init_result:
        capabilities = init_result["result"]["capabilities"]
        for cap, enabled in capabilities.items():
            print(f"   - {cap}: {'✓' if enabled else '✗'}")
    print()
    
    # Demonstrate library statistics (if configured)
    print("2. Library Statistics:")
    stats_result = handler.handle_request("get_library_statistics", {})
    if "result" in stats_result:
        stats = stats_result["result"]
        print(f"   - Total Items: {stats.get('total_items', 'N/A')}")
        print(f"   - Total Collections: {stats.get('total_collections', 'N/A')}")
        print(f"   - Item Types: {stats.get('item_types', 'N/A')}")
    else:
        print("   - Library not configured or accessible")
    print()
    
    # Demonstrate local library reading
    print("3. Local Library Reading:")
    library_result = handler.handle_request("read_local_library", {"limit": 5})
    if "result" in library_result:
        library = library_result["result"]
        print(f"   - Retrieved {library.get('count', 0)} items")
        print(f"   - Limit: {library.get('limit', 'N/A')}")
        items = library.get('items', [])
        if items:
            print("   - Sample items:")
            for i, item in enumerate(items[:3]):
                data = item.get('data', {})
                title = data.get('title', 'No Title')[:50] + "..." if len(data.get('title', '')) > 50 else data.get('title', 'No Title')
                print(f"     {i+1}. {title}")
    else:
        print("   - Library not configured or accessible")
    print()
    
    # Demonstrate citation key validation
    print("4. Citation Key Validation:")
    sample_items = [
        {"key": "item1", "data": {"citationKey": "smith2020"}},
        {"key": "item2", "data": {"citationKey": "jones2021"}},
        {"key": "item3", "data": {"citationKey": "smith2020"}},  # Duplicate
    ]
    validation_result = handler.handle_request("validate_citation_keys", {"items": sample_items})
    if "result" in validation_result:
        validation = validation_result["result"]
        print(f"   - Valid: {validation.get('valid', 'N/A')}")
        print(f"   - Conflicts: {len(validation.get('conflicts', []))}")
        print(f"   - Unique Keys: {validation.get('unique_citation_keys', 0)}")
    print()
    
    # Demonstrate smart bibliography generation
    print("5. Smart Bibliography Generation:")
    bib_result = handler.handle_request("generate_smart_bibliography", {
        "item_keys": ["item1", "item2"],
        "style": "apa",
        "format_options": {"locale": "en-US"}
    })
    if "result" in bib_result:
        bib = bib_result["result"]
        print(f"   - Style: {bib.get('style', 'N/A')}")
        print(f"   - Item Count: {bib.get('item_count', 0)}")
        print("   - Bibliography generated successfully")
    else:
        print("   - Bibliography generation requires valid configuration")
    print()
    
    # Demonstrate AI note synchronization
    print("6. AI Note Synchronization:")
    ai_notes = [
        {"title": "Research Summary", "content": "This paper presents novel findings in AI research."},
        {"title": "Key Insights", "content": "The methodology demonstrates significant improvements over baseline approaches."}
    ]
    sync_result = handler.handle_request("sync_ai_notes", {
        "item_key": "sample-item-key",
        "ai_notes": ai_notes
    })
    if "result" in sync_result:
        sync = sync_result["result"]
        print(f"   - Synced: {sync.get('synced', 0)} notes")
        print(f"   - Errors: {sync.get('errors', 0)}")
    else:
        print("   - Note synchronization requires valid configuration")
    print()
    
    print("=== Demo Complete ===")

if __name__ == "__main__":
    # Add current directory to path for imports
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    demo_zotero_expert()