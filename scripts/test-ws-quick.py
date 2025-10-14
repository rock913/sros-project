#!/usr/bin/env python3
"""Quick test for WebSocket streaming endpoint"""

import asyncio
import websockets
import json
import sys

async def test_websocket():
    uri = 'ws://localhost:8121/agent/stream'
    print(f"🔌 Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as ws:
            print("✅ WebSocket connected\n")
            
            # Send research request
            request = {
                'messages': [{'role': 'user', 'content': 'Test quantum computing'}]
            }
            await ws.send(json.dumps(request))
            print(f"📤 Sent: {request['messages'][0]['content']}\n")
            
            # Receive messages
            count = 0
            async for message in ws:
                data = json.loads(message)
                msg_type = data.get('type')
                count += 1
                
                if msg_type == 'started':
                    print(f"🚀 Research started")
                    print(f"   Session: {data.get('session_id', 'N/A')[:8]}...")
                    print(f"   Thread:  {data.get('thread_id', 'N/A')[:8]}...\n")
                
                elif msg_type == 'progress':
                    node = data.get('node', '?')
                    print(f"⚙️  Processing: {node}")
                
                elif msg_type == 'complete':
                    print(f"\n✅ Completed! ({count} messages received)")
                    return True
                
                elif msg_type == 'error':
                    print(f"❌ Error: {data.get('message')}")
                    return False
        
        return False
    
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(test_websocket())
    sys.exit(0 if result else 1)
