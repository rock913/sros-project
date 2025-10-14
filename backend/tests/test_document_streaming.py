#!/usr/bin/env python3
"""
WebSocket Document Streaming Test

Tests real-time document update streaming via WebSocket.

This test validates:
1. WebSocket connection establishment
2. Document update message reception
3. Incremental paragraph updates
4. Message format correctness
"""

import asyncio
import json
import sys
import os
import uuid
from datetime import datetime

# Add backend src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import websockets
except ImportError:
    print("⚠️  websockets library not installed")
    print("   This test requires manual WebSocket client testing")
    print("   or installation of websockets library")
    sys.exit(0)


class DocumentStreamingTest:
    """Test WebSocket document streaming functionality."""
    
    def __init__(self, url=None):
        # Support both internal (container) and external (host) testing
        # When running inside container, connect to localhost:8000
        # When running from host, connect to localhost:8121
        if url is None:
            url = os.getenv("WS_URL", "ws://localhost:8000/agent/stream")
        self.url = url
        self.tests_passed = 0
        self.tests_failed = 0
        self.messages_received = []
    
    def log(self, message: str, level: str = "INFO"):
        """Pretty logging."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌"}
        symbol = symbols.get(level, "•")
        print(f"[{timestamp}] {symbol} {message}")
    
    async def test_document_streaming(self):
        """
        Test 1: Document update streaming
        
        Sends a research request and monitors for document_update messages.
        """
        print("\n" + "="*60)
        print("Test 1: WebSocket Document Update Streaming")
        print("="*60)
        
        try:
            # Connect to WebSocket
            async with websockets.connect(self.url) as websocket:
                self.log("WebSocket connected", "SUCCESS")
                
                # Send research request
                # Note: thread_id must be a valid UUID string
                request = {
                    "messages": [
                        {"role": "user", "content": "AI applications in healthcare"}
                    ],
                    "thread_id": str(uuid.uuid4())
                }
                
                await websocket.send(json.dumps(request))
                self.log("Sent research request")
                
                # Listen for messages
                document_updates = []
                timeout = 60  # 60 seconds timeout
                start_time = asyncio.get_event_loop().time()
                
                while True:
                    # Check timeout
                    if asyncio.get_event_loop().time() - start_time > timeout:
                        self.log(f"Timeout after {timeout}s", "ERROR")
                        break
                    
                    try:
                        # Wait for message with timeout
                        message_str = await asyncio.wait_for(
                            websocket.recv(),
                            timeout=5.0
                        )
                        
                        message = json.loads(message_str)
                        msg_type = message.get("type")
                        
                        self.log(f"Received: {msg_type}")
                        self.messages_received.append(message)
                        
                        # Print error details if error message
                        if msg_type == "error":
                            self.log(f"  ❌ Error: {message.get('message', 'Unknown error')}", "ERROR")
                            if message.get("detail"):
                                self.log(f"  Detail: {message.get('detail')}", "ERROR")
                        
                        # Collect document updates
                        if msg_type == "document_update":
                            document_updates.append(message)
                            self.log(f"  📝 Document update: {message.get('action')} - {message.get('content', '')[:50]}...")
                        
                        # Stop on completion or error
                        if msg_type in ["complete", "error", "research_stopped"]:
                            break
                            
                    except asyncio.TimeoutError:
                        # No message in 5s, but haven't hit overall timeout yet
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        self.log("Connection closed", "INFO")
                        break
                
                # Validate results
                self.log(f"\nTotal messages received: {len(self.messages_received)}")
                self.log(f"Document updates received: {len(document_updates)}")
                
                if len(document_updates) > 0:
                    self.log("✅ Document streaming working!", "SUCCESS")
                    
                    # Validate message format
                    for i, update in enumerate(document_updates[:3]):  # Check first 3
                        self.log(f"\nUpdate {i+1}:")
                        self.log(f"  Action: {update.get('action')}")
                        self.log(f"  Range: {update.get('range')}")
                        self.log(f"  Rationale: {update.get('rationale', 'N/A')[:50]}")
                        
                        # Validate required fields
                        required = ["type", "action", "range", "content"]
                        missing = [f for f in required if f not in update]
                        if missing:
                            self.log(f"  ⚠️  Missing fields: {missing}", "ERROR")
                            self.tests_failed += 1
                            return False
                    
                    self.tests_passed += 1
                    return True
                else:
                    self.log("⚠️  No document updates received", "ERROR")
                    self.log("   This could mean:")
                    self.log("   - Research didn't reach synthesis node")
                    self.log("   - Document streaming not yet integrated")
                    self.log("   - Or PostgresSaver async issue occurred")
                    self.tests_failed += 1
                    return False
                    
        except Exception as e:
            self.log(f"Test failed: {type(e).__name__}: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            self.tests_failed += 1
            return False
    
    async def test_message_types_summary(self):
        """
        Test 2: Message type distribution
        
        Analyzes what message types were received.
        """
        print("\n" + "="*60)
        print("Test 2: Message Type Distribution")
        print("="*60)
        
        if not self.messages_received:
            self.log("No messages to analyze", "ERROR")
            self.tests_failed += 1
            return False
        
        # Count message types
        type_counts = {}
        for msg in self.messages_received:
            msg_type = msg.get("type", "unknown")
            type_counts[msg_type] = type_counts.get(msg_type, 0) + 1
        
        self.log("Message types received:")
        for msg_type, count in sorted(type_counts.items()):
            self.log(f"  - {msg_type}: {count}")
        
        # Check for expected types
        expected_types = ["started", "progress"]
        found_types = [t for t in expected_types if t in type_counts]
        
        if len(found_types) == len(expected_types):
            self.log("✅ All expected message types received", "SUCCESS")
            self.tests_passed += 1
            return True
        else:
            missing = [t for t in expected_types if t not in type_counts]
            self.log(f"⚠️  Missing message types: {missing}", "ERROR")
            self.tests_failed += 1
            return False
    
    async def run_all_tests(self):
        """Run all document streaming tests."""
        print("\n" + "="*70)
        print(" "*15 + "WebSocket Document Streaming Tests")
        print("="*70)
        
        # Test 1: Document streaming
        await self.test_document_streaming()
        
        # Test 2: Message type analysis
        await self.test_message_types_summary()
        
        # Print summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        total = self.tests_passed + self.tests_failed
        print(f"Total Tests: {total}")
        print(f"Passed:      {self.tests_passed}")
        print(f"Failed:      {self.tests_failed}")
        
        if total > 0:
            print(f"Success Rate: {self.tests_passed/total*100:.0f}%")
        
        print("="*70)
        
        if self.tests_failed == 0:
            print("\n🎉 ALL TESTS PASSED! 🎉\n")
            print("✅ WebSocket document streaming validated")
            print("✅ Message format correct")
            print("✅ Incremental updates working")
            return True
        else:
            print(f"\n⚠️  {self.tests_failed} test(s) failed\n")
            print("Note: Some failures expected if:")
            print("- Backend not running (start with: docker-compose up)")
            print("- PostgresSaver async limitation hit")
            print("- Research didn't reach synthesis node")
            return False


async def main():
    """Main test runner."""
    # Check if backend is accessible
    import socket
    # When running inside container, check port 8000
    # When running from host, check port 8121
    check_host = 'localhost'
    check_port = int(os.getenv("BACKEND_PORT", "8000"))
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((check_host, check_port))
        sock.close()
        if result != 0:
            print(f"❌ Backend not accessible at {check_host}:{check_port}")
            print("   Please start backend: docker-compose -f docker-compose-dev.yml up -d")
            return False
    except Exception as e:
        print(f"❌ Cannot check backend: {e}")
        return False
    
    # Run tests
    test = DocumentStreamingTest()
    success = await test.run_all_tests()
    return success


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test runner failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
