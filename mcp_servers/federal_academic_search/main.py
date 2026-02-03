"""
Main entry point for Federal Academic Search MCP Server
"""
import sys
import logging
from typing import Dict, Any

from .server import FederalAcademicSearchServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main entry point for the Federal Academic Search MCP Server.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        logger.info("Starting Federal Academic Search MCP Server...")
        
        # Create server instance
        server = FederalAcademicSearchServer()
        
        # Initialize server
        logger.info("Initializing server...")
        init_result = server.initialize()
        
        if "error" in init_result:
            logger.error(f"Failed to initialize server: {init_result['error']}")
            return 1
            
        logger.info("Server initialized successfully")
        logger.info("Federal Academic Search MCP Server is ready to serve requests")
        
        # Keep server running (in a real implementation, this would be a service loop)
        try:
            # For demonstration, we'll just show that the server is ready
            print("Federal Academic Search MCP Server is running...")
            print("Press Ctrl+C to stop the server")
            
            # In a real implementation, this would be replaced with actual server loop
            # For now, we'll just exit gracefully
            return 0
            
        except KeyboardInterrupt:
            logger.info("Server shutdown requested by user")
            return 0
            
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())