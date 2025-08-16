#!/usr/bin/env python3
"""
Demo script showing how to make queries to the MCP server
"""
import asyncio
import os
from fastmcp import Client
from alfresco_mcp_server.fastmcp_server import mcp

async def demo_queries():
    """Demonstrate various query capabilities"""
    print("🚀 MCP Server Query Demo")
    print("=" * 50)
    
    try:
        async with Client(mcp) as client:
            
            # Query 1: Search for all documents
            print("\n📋 Query 1: Find all documents")
            print("-" * 30)
            result = await client.call_tool("search_content", {
                "query": "*",
                "max_results": 10
            })
            print("✅ Found documents in repository")
            
            # Query 2: Browse the root directory
            print("\n📁 Query 2: Browse repository root")  
            print("-" * 35)
            result = await client.call_tool("browse_repository", {
                "parent_id": "-root-",
                "max_items": 10
            })
            print("✅ Listed root directory contents")
            
            # Query 3: Browse user's home space
            print("\n🏠 Query 3: Browse user home space")
            print("-" * 35)
            result = await client.call_tool("browse_repository", {
                "parent_id": "-my-",  # User's personal space
                "max_items": 10
            })
            print("✅ Listed user home directory")
            
            # Query 4: Get repository information
            print("\n🔍 Query 4: Get repository info")
            print("-" * 32)
            result = await client.call_tool("get_repository_info_tool", {})
            print("✅ Retrieved Alfresco repository information")
            
            print(f"\n🎉 All queries completed successfully!")
            print(f"🌐 MCP Server is ready for AI interactions at http://localhost:3001/mcp/")
            
    except Exception as e:
        print(f"❌ Query failed: {e}")

if __name__ == "__main__":
    # Set environment variables
    os.environ["ALFRESCO_URL"] = "http://localhost:8080"
    os.environ["ALFRESCO_USERNAME"] = "admin" 
    os.environ["ALFRESCO_PASSWORD"] = "admin"
    
    print("🔗 Connecting to Alfresco at http://localhost:8080")
    print("👤 Using admin credentials")
    
    asyncio.run(demo_queries())