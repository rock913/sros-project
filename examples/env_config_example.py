#!/usr/bin/env python3
"""
Example script demonstrating environment configuration usage
"""

import os
from pathlib import Path

def demonstrate_env_setup():
    """Demonstrate different ways to set up environment configuration"""
    
    print("=" * 60)
    print("Environment Configuration Examples")
    print("=" * 60)
    
    # Method 1: Manual environment variable setup
    print("\n1. Manual Environment Variable Setup:")
    print("   You can set environment variables directly in your shell:")
    print("   ")
    print("   export OPENALEX_EMAIL=your.email@example.com")
    print("   export UNPAYWALL_EMAIL=your.email@example.com")
    print("   export SEMANTIC_SCHOLAR_API_KEY=your_s2_api_key")
    print("   export ZOTERO_API_KEY=your_zotero_api_key")
    print("   export DUCKDB_PATH=./my_research.db")
    print("   ")
    print("   Then run your servers:")
    print("   python run_servers.py")
    
    # Method 2: Using .env file
    print("\n2. Using .env File (Recommended):")
    print("   Create a .env file in your project root with your configuration:")
    print("   ")
    print("   # .env file contents:")
    print("   OPENALEX_EMAIL=your.email@example.com")
    print("   UNPAYWALL_EMAIL=your.email@example.com")
    print("   SEMANTIC_SCHOLAR_API_KEY=your_s2_api_key")
    print("   ZOTERO_API_KEY=your_zotero_api_key")
    print("   DUCKDB_PATH=./my_research.db")
    print("   ")
    print("   Note: You'll need to install python-dotenv:")
    print("   pip install python-dotenv")
    
    # Show current .env.example
    env_example_path = Path(".env.example")
    if env_example_path.exists():
        print("\n3. Current .env.example Template:")
        print("   Here's the template you can use as a starting point:")
        print("   " + "-" * 50)
        with open(env_example_path, 'r') as f:
            for line in f:
                print(f"   {line.rstrip()}")
        print("   " + "-" * 50)
    
    print("\n" + "=" * 60)
    print("Configuration Tips:")
    print("• Never commit your .env file to version control")
    print("• Add .env to your .gitignore file")
    print("• Use .env.example as a template for other developers")
    print("• Environment variables take precedence over defaults")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_env_setup()