#!/usr/bin/env python3
"""
LangFuse Connection Test Script

This script verifies that LangFuse is properly configured and can connect
to your LangFuse instance.

Usage:
    # Run inside the container
    docker exec -it langgraph-api python /deps/backend/test_langfuse_connection.py
    
    # Or copy to container and run
    docker cp test_langfuse_connection.py langgraph-api:/tmp/
    docker exec -it langgraph-api python /tmp/test_langfuse_connection.py
"""

import os
import sys
from datetime import datetime

def test_langfuse_connection():
    """Test LangFuse connection and create a test trace."""
    
    print("=" * 70)
    print("LangFuse Connection Test")
    print("=" * 70)
    print()
    
    # Step 1: Check environment variables
    print("📋 Step 1: Checking environment variables...")
    
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
    
    if not public_key:
        print("❌ LANGFUSE_PUBLIC_KEY is not set")
        print("   Please set it in your .env file or docker-compose-dev.yml")
        return False
    else:
        print(f"✅ LANGFUSE_PUBLIC_KEY: {public_key[:15]}...")
    
    if not secret_key:
        print("❌ LANGFUSE_SECRET_KEY is not set")
        print("   Please set it in your .env file or docker-compose-dev.yml")
        return False
    else:
        print(f"✅ LANGFUSE_SECRET_KEY: {secret_key[:15]}...")
    
    print(f"✅ LANGFUSE_HOST: {host}")
    print()
    
    # Step 2: Import LangFuse
    print("📦 Step 2: Importing LangFuse SDK...")
    try:
        from langfuse import Langfuse
        print("✅ LangFuse SDK imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import LangFuse: {e}")
        print("   Run: pip install langfuse")
        return False
    print()
    
    # Step 3: Initialize LangFuse client
    print("🔌 Step 3: Initializing LangFuse client...")
    try:
        langfuse = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=host
        )
        print("✅ LangFuse client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize LangFuse client: {e}")
        return False
    print()
    
    # Step 4: Create a test trace
    print("📊 Step 4: Creating test trace...")
    try:
        trace = langfuse.trace(
            name="Connection Test",
            input={
                "message": "Testing LangFuse connection",
                "timestamp": datetime.utcnow().isoformat(),
                "test_type": "automated_connection_test"
            },
            tags=["test", "connection", "automated"]
        )
        print("✅ Test trace created")
        print(f"   Trace ID: {trace.id if hasattr(trace, 'id') else 'N/A'}")
    except Exception as e:
        print(f"❌ Failed to create trace: {e}")
        return False
    print()
    
    # Step 5: Add a test span
    print("🔍 Step 5: Creating test span...")
    try:
        span = trace.span(
            name="Test Span",
            input={
                "operation": "test_operation",
                "data": "sample_data"
            },
            tags=["test", "span"]
        )
        span.end(output={
            "status": "success",
            "message": "Test span completed successfully"
        })
        print("✅ Test span created and completed")
    except Exception as e:
        print(f"❌ Failed to create span: {e}")
        return False
    print()
    
    # Step 6: Update trace output
    print("📝 Step 6: Updating trace output...")
    try:
        trace.update(output={
            "status": "success",
            "message": "LangFuse connection test completed successfully!",
            "timestamp": datetime.utcnow().isoformat(),
            "test_results": {
                "environment_variables": "OK",
                "sdk_import": "OK",
                "client_initialization": "OK",
                "trace_creation": "OK",
                "span_creation": "OK"
            }
        })
        print("✅ Trace output updated")
    except Exception as e:
        print(f"❌ Failed to update trace: {e}")
        return False
    print()
    
    # Step 7: Flush (ensure data is sent)
    print("🚀 Step 7: Flushing data to LangFuse...")
    try:
        langfuse.flush()
        print("✅ Data flushed to LangFuse")
    except Exception as e:
        print(f"⚠️  Warning: Failed to flush data: {e}")
        print("   Data may still be sent asynchronously")
    print()
    
    # Success summary
    print("=" * 70)
    print("✅ LangFuse Connection Test PASSED!")
    print("=" * 70)
    print()
    print("📊 Next Steps:")
    print(f"   1. Visit your LangFuse Dashboard: {host}")
    print("   2. Go to the 'Traces' page")
    print("   3. Look for a trace named 'Connection Test'")
    print("   4. Verify the trace has:")
    print("      - Input: message, timestamp, test_type")
    print("      - Output: status, message, test_results")
    print("      - Tags: test, connection, automated")
    print("      - 1 Span: 'Test Span'")
    print()
    print("🎉 If you can see the trace, LangFuse is working correctly!")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = test_langfuse_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
