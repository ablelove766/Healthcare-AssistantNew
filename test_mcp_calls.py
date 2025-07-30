#!/usr/bin/env python3
"""
Test script to call MCP server tools directly.
This simulates how Claude Desktop would call the MCP server.
"""

import asyncio
from mcp_server import list_tools, getpatientlist

async def test_mcp_calls():
    """Test MCP server tool calls."""
    
    print("🚀 Testing MCP Server Tool Calls")
    print("=" * 50)
    
    # Test 1: List all available tools
    print("\n1. Listing all available tools:")
    try:
        tools_result = await list_tools()
        print(tools_result)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Get all patients (no filter)
    print("\n2. Getting all patients (no filter):")
    try:
        patients_result = await getpatientlist(limit=5)
        print(patients_result)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Get patients filtered by name
    print("\n3. Getting patients filtered by name 'John':")
    try:
        filtered_result = await getpatientlist(patient_name="John", limit=3)
        print(filtered_result)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Get patients with different name filter
    print("\n4. Getting patients filtered by name 'Smith':")
    try:
        smith_result = await getpatientlist(patient_name="Smith", limit=2)
        print(smith_result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ MCP Server testing completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_calls())
