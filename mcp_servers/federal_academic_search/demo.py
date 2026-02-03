#!/usr/bin/env python3
"""
Demo script for Federal Academic Search MCP Server
"""
import sys
import os
import asyncio

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_servers.federal_academic_search.core.manager import AcademicSearchManager
from mcp_servers.federal_academic_search.config import FederalAcademicSearchConfig


async def demo_search():
    """Demonstrate basic search functionality."""
    print("=== Federal Academic Search Demo ===\n")
    
    # Initialize configuration
    config = FederalAcademicSearchConfig()
    
    # Initialize search manager
    manager = AcademicSearchManager(config)
    
    # Demo 1: Basic paper search
    print("1. Searching for papers on 'machine learning'...")
    search_results = await manager.search_papers("machine learning", limit=5, enrich=True)
    
    if "error" in search_results:
        print(f"   Error: {search_results['error']}")
    else:
        print(f"   Found {search_results.get('total', 0)} papers")
        if search_results.get('results'):
            for i, paper in enumerate(search_results['results'][:3], 1):
                print(f"   {i}. {paper.get('title', 'No title')}")
                if paper.get('authors'):
                    print(f"      Authors: {paper['authors']}")
                if paper.get('year'):
                    print(f"      Year: {paper['year']}")
                if paper.get('citationCount'):
                    print(f"      Citations: {paper['citationCount']}")
                print()
    
    # Demo 2: Search by author
    print("2. Searching for papers by author 'Yann LeCun'...")
    author_results = await manager.search_by_author("Yann LeCun", limit=3, enrich=True)
    
    if "error" in author_results:
        print(f"   Error: {author_results['error']}")
    else:
        print(f"   Found {author_results.get('total', 0)} papers")
        if author_results.get('results'):
            for i, paper in enumerate(author_results['results'], 1):
                print(f"   {i}. {paper.get('title', 'No title')}")
                if paper.get('year'):
                    print(f"      Year: {paper['year']}")
                print()
    
    # Demo 3: Get paper details
    print("3. Getting details for a specific paper...")
    # Use a known paper ID for demo
    paper_details = await manager.get_paper_details("https://openalex.org/W2024384345", enrich=True)
    
    if "error" in paper_details:
        print(f"   Error: {paper_details['error']}")
    else:
        print(f"   Title: {paper_details.get('title', 'No title')}")
        if paper_details.get('abstract'):
            abstract = paper_details['abstract']
            if len(abstract) > 200:
                abstract = abstract[:200] + "..."
            print(f"   Abstract: {abstract}")
        if paper_details.get('authors'):
            print(f"   Authors: {paper_details['authors']}")
        if paper_details.get('citationCount'):
            print(f"   Citations: {paper_details['citationCount']}")
        if paper_details.get('openAccessPdf'):
            print(f"   PDF: {paper_details['openAccessPdf']}")
        print()
    
    # Demo 4: Cache statistics
    print("4. Cache statistics:")
    cache_stats = manager.get_cache_stats()
    print(f"   Total entries: {cache_stats.get('total_entries', 0)}")
    print(f"   Active entries: {cache_stats.get('active_entries', 0)}")
    print(f"   Recently accessed: {cache_stats.get('recently_accessed', 0)}")


def main():
    """Main entry point."""
    print("Setting up environment variables for demo...")
    
    # Set required environment variables for demo
    os.environ.setdefault('OPENALEX_EMAIL', 'demo@example.com')
    os.environ.setdefault('UNPAYWALL_EMAIL', 'demo@example.com')
    
    # Run async demo
    try:
        asyncio.run(demo_search())
        print("\n=== Demo completed successfully! ===")
    except Exception as e:
        print(f"\n=== Demo failed: {e} ===")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())