# SROS V2.2.1 Stability Fix Documentation

## Problem Statement

The MCP error -32001: Request timed out issue was caused by the "Cold Start Storm" phenomenon. When the Gateway starts, it attempts to simultaneously launch multiple Python sub-processes. During this process, the OS process creation and Python interpreter initialization consume significant CPU and I/O resources. When 3-5 interpreters initialize simultaneously, the CPU becomes saturated, causing response times to linearly increase beyond Roo Code's hard timeout threshold.

## Solution Overview

We implemented a system-wide solution that decouples "Gateway startup time" from "Client connection timeout" by introducing:

1. **Health Check Mechanism**: A robust health endpoint that reports system readiness
2. **Preheating Phase**: Gateway initializes all sub-servers before accepting external requests
3. **Polling Script**: Enhanced `run_servers.py` that waits for system readiness before reporting success

## Key Changes Made

### 1. Enhanced `run_servers.py`

- Added `requests` library dependency for health checking
- Implemented `wait_for_gateway_health()` function that polls the `/health` endpoint
- Added `--no-health-check` flag for bypassing health checks
- Updated main gateway startup logic to wait for system readiness

### 2. Enhanced `mcp_servers/sros_gateway/main.py`

- Added `SubProcessManager` enhancements for tracking server readiness
- Implemented `_preheat_servers()` method that sends initialization requests to all sub-servers
- Added `_handle_health_check()` method to respond to health requests
- Updated `health_status` to track system readiness
- Added `is_ready()` and `mark_ready()` methods for server status tracking
- **Fixed race condition in health status reporting**: Implemented synchronization to ensure all servers are fully initialized before marking system ready
- **Added integration test coverage**: Implemented `test_health_endpoint_sync()` in test_gateway.py to validate health endpoint behavior during server initialization delays and timeout scenarios
- **Enhanced health check reporting**: Added `unhealthy_servers` field to health endpoint to provide visibility into which specific servers are not ready
- **Improved environment variable handling**: Added automatic `.env` file loading in `run_servers.py` to ensure proper API key propagation to sub-servers
- **Uvicorn timeout configuration**: Documented that HTTP Keep-Alive timeout is set to 300 seconds (5 minutes) to prevent connection drops during slow operations

### 3. Optimized `mcp_servers/federal_academic_search/main.py`

- Implemented lazy loading of `FederalAcademicSearchMCPHandler` 
- Created `get_handler_instance()` helper function to defer expensive imports
- Applied lazy loading to both stdio and SSE modes to prevent cold start delays

## Startup Sequence

1. **User runs**: `python run_servers.py`
2. **Script starts Gateway**: `python -m mcp_servers.sros_gateway.main`
3. **Gateway begins**: Starts all sub-processes
4. **Gateway preheats**: Sends initialization requests to all sub-servers
5. **Gateway updates health**: Marks system as ready when all servers are initialized
6. **Script polls health**: Continuously checks `/health` endpoint until ready
7. **System ready**: Prints `✅ SYSTEM READY!` and allows Roo Code connection

## Usage Instructions

### Normal Operation
```bash
python run_servers.py
```

### Skip Health Check (for debugging)
```bash
python run_servers.py --no-health-check
```

### Custom Port
```bash
python run_servers.py --port 8080
```

## Troubleshooting

### Issue: "❌ Gateway health check timeout!"
**Cause**: Sub-servers took too long to initialize (over 60 seconds)
**Solution**: 
1. Check if sub-servers are properly configured in `config.json`
2. Verify that required dependencies are installed
3. Increase timeout in `wait_for_gateway_health()` function if needed

### Issue: "❌ Port 8000 is already in use!"
**Cause**: Another instance is running
**Solution**: 
1. Kill existing processes: `killall python`
2. Or use auto-port detection: `python run_servers.py --auto-port`

### Issue: "Failed to start [server] server"
**Cause**: Missing dependencies or incorrect configuration
**Solution**:
1. Install required dependencies: `pip install -r mcp_servers/[server]/requirements.txt`
2. Check server configuration in `config.json`

## Verification Steps

1. Run `python run_servers.py`
2. Observe the startup sequence:
   ```
   🔌 Connecting to federal...
   ⏳ Waiting for Gateway to warm up...
   ✅ SYSTEM READY!
   ```
3. Connect to Roo Code only after seeing `✅ SYSTEM READY!`
4. Verify that Roo Code connects successfully without timeouts

## Technical Details

The solution works by:
- **Decoupling startup time**: Sub-process initialization happens in the background
- **Pre-warming**: All sub-servers are initialized before the health check passes
- **Graceful degradation**: If one server fails to initialize, others continue
- **Real-time monitoring**: Health endpoint provides live status information