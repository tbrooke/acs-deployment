#!/usr/bin/env python3
"""
Simple test script to verify MCP server connection to Alfresco
"""
import asyncio
import os
from fastmcp import Client
from alfresco_mcp_server.fastmcp_server import mcp

async def test_connection():
    """Test basic MCP server functionality"""
    print("🧪 Testing MCP Server Connection to Alfresco")
    print("=" * 50)
    
    try:
        async with Client(mcp) as client:
            # Test search functionality
            print("\n🔍 Testing search functionality...")
            search_result = await client.call_tool("search_content", {
                "query": "*",
                "max_results": 3
            })
            print(f"✅ Search completed successfully")
            
            # Test browse functionality  
            print("\n📁 Testing browse functionality...")
            browse_result = await client.call_tool("browse_repository", {
                "parent_id": "-root-",
                "max_items": 5
            })
            print(f"✅ Browse completed successfully")
            
            # Test repository info tool
            print("\n📋 Getting repository information...")
            repo_info = await client.call_tool("get_repository_info_tool", {})
            print(f"✅ Repository info retrieved successfully")
            
            print("\n🎉 All tests passed! MCP server is working correctly.")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Set environment variables if not already set
    if not os.getenv("ALFRESCO_URL"):
        os.environ["ALFRESCO_URL"] = "http://localhost:8080"
    if not os.getenv("ALFRESCO_USERNAME"):
        os.environ["ALFRESCO_USERNAME"] = "admin"
    if not os.getenv("ALFRESCO_PASSWORD"):
        os.environ["ALFRESCO_PASSWORD"] = "admin"
    
    asyncio.run(test_connection())