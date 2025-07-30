#!/usr/bin/env python3
"""
A simple MCP (Model Context Protocol) server implementation.
This server provides healthcare-related tools for AI assistants.

Available Tools:
1. getpatientlist(patient_name, limit) - Get a list of patients filtered by patient name

Usage:
- Run: python mcp_server.py
- Configure in Claude Desktop with stdio transport
"""

from mcp.server.fastmcp import FastMCP
from api_client import patient_api_client

# Initialize FastMCP server
mcp = FastMCP("healthcare-mcp-server")



@mcp.tool()
async def getpatientlist(patient_name: str = None, limit: int = 10) -> str:
    """Get a list of patients filtered by patient name.

    Args:
        patient_name: Filter by patient name (optional, partial matches supported)
        limit: Maximum number of patients to return (1-100, default: 10)
    """
    # Call the API client to get patient list
    return await patient_api_client.get_patient_list(patient_name=patient_name, limit=limit)

if __name__ == "__main__":
    # Run the server using stdio transport
    mcp.run(transport="stdio")
