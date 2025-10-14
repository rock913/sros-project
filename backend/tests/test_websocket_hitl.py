#!/usr/bin/env python3
"""
Phase 3.6 WebSocket HITL Notification Test

Tests the WebSocket real-time HITL notification system:
1. Connect to WebSocket
2. Send research request
3. Monitor for HITL notifications
4. Verify message format

This validates the real-time communication layer.
"""

import asyncio
import json
import websockets
from datetime import datetime


class WebSocketHITLTest:
    """Test WebSocket HITL notification system"""
    
    def __init__(self):
        # Use 127.0.0.1:8000 for internal container access
        self.ws_url = "ws://127.0.0.1:8000/agent/stream"
        self.received_messages = []
        self.hitl_requests = []
        
    def log(self, message: str, level: str = "INFO"):
        """Pretty logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        symbol = symbols.get(level, "•")
        print(f"[{timestamp}] {symbol} {message}")
    
    async def test_websocket_connection(self):
        """Test 1: Basic WebSocket connection"""
        self.log("Testing WebSocket connection...")
        
        try:
            async with websockets.connect(self.ws_url) as websocket:
                self.log("WebSocket connected successfully", "SUCCESS")
                return True
        except Exception as e:
            self.log(f"WebSocket connection failed: {e}", "ERROR")
            return False
    
    async def test_hitl_notification(self):
        """Test 2: HITL notification delivery"""
        self.log("Testing HITL notification delivery...")
        
        try:
            async with websockets.connect(self.ws_url) as websocket:
                # Send research request
                request = {
                    "messages": [
                        {"role": "user", "content": "Research quantum computing"}
                    ]
                }
                
                self.log("Sending research request...")
                await websocket.send(json.dumps(request))
                
                # Monitor messages
                message_count = 0
                hitl_received = False
                timeout = 30  # 30 second timeout
                
                try:
                    async with asyncio.timeout(timeout):
                        while True:
                            message = await websocket.recv()
                            data = json.loads(message)
                            message_count += 1
                            
                            self.received_messages.append(data)
                            msg_type = data.get("type", "unknown")
                            
                            self.log(f"Received: {msg_type}", "INFO")
                            
                            # Check for HITL request
                            if msg_type == "hitl_request":
                                hitl_received = True
                                self.hitl_requests.append(data)
                                self.log(f"HITL request detected!", "SUCCESS")
                                self.log(f"  Request ID: {data.get('request_id')}", "INFO")
                                self.log(f"  Type: {data.get('decision_type')}", "INFO")
                                self.log(f"  Prompt: {data.get('prompt', '')[:50]}...", "INFO")
                                
                                # Validate message structure
                                required_fields = [
                                    "request_id", "decision_type", "prompt", 
                                    "options", "session_id", "thread_id"
                                ]
                                missing = [f for f in required_fields if f not in data]
                                
                                if missing:
                                    self.log(f"Missing fields: {missing}", "ERROR")
                                    return False
                                else:
                                    self.log("All required fields present", "SUCCESS")
                                    return True  # Success!
                            
                            # Exit on completion or error
                            if msg_type in ["complete", "error", "research_stopped"]:
                                self.log(f"Session ended: {msg_type}", "INFO")
                                break
                            
                            # Safety: limit messages
                            if message_count > 100:
                                self.log("Too many messages, stopping", "WARNING")
                                break
                                
                except asyncio.TimeoutError:
                    self.log(f"Timeout after {timeout}s", "WARNING")
                
                if hitl_received:
                    self.log("HITL notification test passed!", "SUCCESS")
                    return True
                else:
                    self.log("No HITL notification received", "ERROR")
                    self.log(f"Received {message_count} messages", "INFO")
                    return False
                    
        except Exception as e:
            self.log(f"Test failed: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_message_format(self):
        """Test 3: Validate HITL message format"""
        self.log("Validating HITL message format...")
        
        if not self.hitl_requests:
            self.log("No HITL requests to validate", "ERROR")
            return False
        
        request = self.hitl_requests[0]
        
        # Validate structure
        checks = {
            "request_id": isinstance(request.get("request_id"), str),
            "decision_type": request.get("decision_type") in [
                "query_approval", "paper_selection", "report_revision"
            ],
            "prompt": isinstance(request.get("prompt"), str) and len(request.get("prompt", "")) > 0,
            "options": isinstance(request.get("options"), list) and len(request.get("options", [])) > 0,
            "context": isinstance(request.get("context"), dict),
            "session_id": isinstance(request.get("session_id"), str),
            "thread_id": isinstance(request.get("thread_id"), str),
            "timeout_seconds": isinstance(request.get("timeout_seconds"), int)
        }
        
        all_passed = True
        for field, passed in checks.items():
            status = "✅" if passed else "❌"
            self.log(f"  {status} {field}: {passed}", "INFO")
            if not passed:
                all_passed = False
        
        if all_passed:
            self.log("Message format validation passed!", "SUCCESS")
            return True
        else:
            self.log("Message format validation failed", "ERROR")
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("WebSocket Test Summary")
        print("="*60)
        print(f"Total messages received: {len(self.received_messages)}")
        print(f"HITL requests received: {len(self.hitl_requests)}")
        
        if self.received_messages:
            print("\nMessage types:")
            types = {}
            for msg in self.received_messages:
                msg_type = msg.get("type", "unknown")
                types[msg_type] = types.get(msg_type, 0) + 1
            
            for msg_type, count in sorted(types.items()):
                print(f"  - {msg_type}: {count}")
        
        if self.hitl_requests:
            print("\nHITL Requests:")
            for i, req in enumerate(self.hitl_requests, 1):
                print(f"  {i}. {req.get('request_id')} ({req.get('decision_type')})")
                print(f"     Prompt: {req.get('prompt', '')[:60]}...")
                print(f"     Options: {req.get('options', [])}")
        
        print("="*60 + "\n")
    
    async def run_all_tests(self):
        """Run all WebSocket tests"""
        print("\n" + "="*60)
        print("Phase 3.6 WebSocket HITL Notification Tests")
        print("="*60 + "\n")
        
        results = []
        
        # Test 1: Connection
        self.log("=" * 50)
        self.log("Test 1: WebSocket Connection")
        self.log("=" * 50)
        result1 = await self.test_websocket_connection()
        results.append(("Connection", result1))
        print()
        
        if not result1:
            self.log("Connection failed, skipping remaining tests", "ERROR")
            return False
        
        # Test 2: HITL Notification
        self.log("=" * 50)
        self.log("Test 2: HITL Notification Delivery")
        self.log("=" * 50)
        self.log("⚠️  This test will trigger actual graph execution", "WARNING")
        self.log("⚠️  May take 10-30 seconds depending on LLM response", "WARNING")
        print()
        
        result2 = await self.test_hitl_notification()
        results.append(("HITL Notification", result2))
        print()
        
        # Test 3: Message Format (only if test 2 passed)
        if result2:
            self.log("=" * 50)
            self.log("Test 3: Message Format Validation")
            self.log("=" * 50)
            result3 = await self.test_message_format()
            results.append(("Message Format", result3))
            print()
        
        # Print summary
        self.print_summary()
        
        # Final results
        print("=" * 60)
        print("TEST RESULTS")
        print("=" * 60)
        
        for test_name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{status:12s} - {test_name}")
        
        print("-" * 60)
        total = len(results)
        passed_count = sum(1 for _, p in results if p)
        print(f"Total: {passed_count}/{total} passed ({passed_count/total*100:.0f}%)")
        print("=" * 60 + "\n")
        
        return all(p for _, p in results)


async def main():
    """Main test entry point"""
    test = WebSocketHITLTest()
    success = await test.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
