#!/bin/bash
# Test WebSocket streaming endpoint

set -e

BASE_URL="ws://localhost:8121"
TOPIC="${1:-What are the latest advancements in quantum computing?}"

echo "=== WebSocket Stream Test ==="
echo "Topic: $TOPIC"
echo ""

# Use Python for WebSocket testing
python3 << EOF
import asyncio
import websockets
import json
import sys

async def test_stream():
    uri = '${BASE_URL}/agent/stream'
    print(f"Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as ws:
            print("✅ WebSocket connected")
            
            # Send research request
            request = {
                'messages': [{'role': 'user', 'content': '${TOPIC}'}]
            }
            await ws.send(json.dumps(request))
            print(f"📤 Sent request: {request['messages'][0]['content'][:50]}...")
            print("")
            
            # Receive and print messages
            message_count = 0
            async for message in ws:
                data = json.loads(message)
                message_count += 1
                
                msg_type = data.get('type', 'unknown')
                
                if msg_type == 'started':
                    print(f"🚀 [{msg_type}] Session started")
                    print(f"   Session ID: {data.get('session_id', 'N/A')}")
                    print(f"   Thread ID:  {data.get('thread_id', 'N/A')}")
                    print("")
                
                elif msg_type == 'progress':
                    node = data.get('node', 'unknown')
                    print(f"⚙️  [{msg_type}] Processing node: {node}")
                
                elif msg_type == 'complete':
                    print("")
                    print(f"✅ [{msg_type}] Research completed!")
                    print(f"   Session ID: {data.get('session_id', 'N/A')}")
                    print(f"   Total messages received: {message_count}")
                    break
                
                elif msg_type == 'error':
                    print(f"❌ [{msg_type}] Error: {data.get('message', 'Unknown error')}")
                    sys.exit(1)
                
                else:
                    print(f"📨 [{msg_type}] {json.dumps(data)[:100]}...")
            
            print("")
            print("✅ WebSocket test completed successfully")
    
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

asyncio.run(test_stream())
EOF

echo ""
echo "=== Test completed ==="
