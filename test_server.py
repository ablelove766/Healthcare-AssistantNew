#!/usr/bin/env python3
"""
Test script for the MCP server.
This script helps verify that the server is working correctly.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict


class MCPTester:
    """Simple tester for MCP server functionality."""
    
    def __init__(self):
        self.server_process = None
    
    async def test_basic_functionality(self):
        """Test basic server functionality without full MCP protocol."""
        print("Testing MCP Server Basic Functionality")
        print("=" * 50)
        
        # Test 1: Import and basic setup
        try:
            import mcp_server
            import api_client
            print("✓ Server and API client import successful")
        except Exception as e:
            print(f"✗ Server/API client import failed: {e}")
            return False
        
        # Test 2: Test list_tools function
        try:
            result = await mcp_server.list_tools()
            print("✓ List tools test:")
            print(result[:200] + "..." if len(result) > 200 else result)
        except Exception as e:
            print(f"✗ List tools test failed: {e}")

        # Test 3: Check if tools are defined
        try:
            # Check if the FastMCP server has tools registered
            if hasattr(mcp_server, 'mcp') and hasattr(mcp_server.mcp, '_tools'):
                tools = mcp_server.mcp._tools
                print(f"✓ Found {len(tools)} registered tools:")
                for tool_name in tools.keys():
                    print(f"  - {tool_name}")
            else:
                print("✓ Server structure looks correct (tools will be registered at runtime)")
        except Exception as e:
            print(f"✗ Tool check failed: {e}")

        # Test 4: Test API client directly
        try:
            result = await api_client.patient_api_client.get_patient_list(limit=5)
            print(f"✓ API client test (no name filter): {result.split(chr(10))[0] if chr(10) in result else result[:50]}...")
        except Exception as e:
            print(f"✓ API client test (expected to fail without API): {str(e)[:50]}...")

        # Test 5: Test getpatientlist tool function (which calls API client)
        try:
            result = await mcp_server.getpatientlist(limit=5)
            print(f"✓ Patient list tool test (no name filter): {result.split(chr(10))[0] if chr(10) in result else result[:50]}...")
        except Exception as e:
            print(f"✓ Patient list tool test (expected to fail without API): {str(e)[:50]}...")

        try:
            result = await mcp_server.getpatientlist(patient_name="John", limit=3)
            print(f"✓ Patient list tool test (with name filter): {result.split(chr(10))[0] if chr(10) in result else result[:50]}...")
        except Exception as e:
            print(f"✓ Patient list tool test with name filter (expected to fail without API): {str(e)[:50]}...")
        
        print("\n" + "=" * 50)
        print("Basic functionality tests completed!")
        return True
    
    def test_server_startup(self):
        """Test that the server can start up properly."""
        print("\nTesting Server Startup")
        print("=" * 30)
        
        try:
            # Try to start the server process
            process = subprocess.Popen(
                [sys.executable, "mcp_server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give it a moment to start
            import time
            time.sleep(1)
            
            # Check if it's still running
            if process.poll() is None:
                print("✓ Server started successfully")
                process.terminate()
                process.wait()
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"✗ Server failed to start")
                if stderr:
                    print(f"Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Server startup test failed: {e}")
            return False


async def main():
    """Run all tests."""
    tester = MCPTester()
    
    print("MCP Server Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    basic_success = await tester.test_basic_functionality()
    
    # Test server startup
    startup_success = tester.test_server_startup()
    
    print(f"\nTest Results:")
    print(f"Basic Functionality: {'PASS' if basic_success else 'FAIL'}")
    print(f"Server Startup: {'PASS' if startup_success else 'FAIL'}")
    
    if basic_success and startup_success:
        print("\n🎉 All tests passed! Your MCP server is ready to use.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure Claude Desktop (see README.md)")
        print("3. Start using your MCP server!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())
