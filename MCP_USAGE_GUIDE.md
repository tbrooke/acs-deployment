# 🚀 MCP Server Usage Guide

Your Alfresco MCP server is now installed and running! Here are the different ways to test and use it:

## 🧪 **Testing Methods**

### **1. Direct Python Testing (What we just did)**
```bash
cd /Users/tombrooke/Code/trust-server/alfresco/acs-deployment/python-alfresco-mcp-server
uv run python ../demo_queries.py
```

### **2. HTTP API Testing**
```bash
# Start HTTP server
uv run python-alfresco-mcp-server --transport http --port 3001

# Test via curl (example)
curl -X POST http://localhost:3001/mcp/sessions \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'
```

### **3. Claude Desktop Integration (Recommended for daily use)**
```bash
# Start in STDIO mode for Claude Desktop
uv run python-alfresco-mcp-server --transport stdio
```

## 📋 **Available Queries/Operations**

### **Search Operations:**
- `search_content` - Find documents by content/metadata
- `advanced_search` - Advanced search with filtering
- `search_by_metadata` - Search by specific metadata fields
- `cmis_search` - Database-level SQL queries

### **Repository Operations:**
- `browse_repository` - Navigate folder structures
- `get_node_properties` - Get document/folder metadata
- `update_node_properties` - Update metadata
- `get_repository_info_tool` - Server information

### **Document Management:**
- `upload_document` - Upload new files
- `download_document` - Download existing files
- `create_folder` - Create new folders
- `delete_node` - Delete files/folders

### **Document Lifecycle:**
- `checkout_document` - Lock for editing
- `checkin_document` - Save changes and unlock
- `cancel_checkout` - Cancel edit session

## 🌐 **Integration Options**

### **Option 1: Share Integration (Custom)**
The MCP server is NOT built into Alfresco Share by default. To add queries to Share, you would need to:

1. **Create custom Share dashlets** that call the MCP server
2. **Build custom web scripts** in Share that proxy to MCP
3. **Add JavaScript extensions** to Share UI

### **Option 2: Claude Desktop (Easiest)**
1. Configure Claude Desktop to use the MCP server
2. Ask Claude natural language questions about your documents
3. Claude will automatically use the MCP server to query Alfresco

### **Option 3: Custom Applications**
Build your own apps that use the MCP server as a backend API.

## 🎯 **Example Queries You Can Make**

### **In Python/Code:**
```python
# Search for PDFs
await client.call_tool("search_content", {
    "query": "*.pdf",
    "max_results": 20
})

# Browse a specific folder
await client.call_tool("browse_repository", {
    "parent_id": "some-folder-id",
    "max_items": 50
})
```

### **With Claude Desktop (Natural Language):**
- "Show me all PDF files in the repository"
- "List the contents of the Company Home folder"
- "Find all documents modified in the last week"
- "Upload this document to the Marketing folder"

## 🔗 **Current Status**

✅ **MCP Server:** Running at http://localhost:3001/mcp/  
✅ **Alfresco:** Available at http://localhost:8080  
✅ **Share:** Available at http://localhost:8080/share  
✅ **Connection:** MCP ↔ Alfresco working perfectly  

## 🚀 **Next Steps**

1. **Test in Claude Desktop:** Configure it to use your MCP server
2. **Explore queries:** Try different search patterns and operations
3. **Build custom tools:** Create your own applications using the MCP API
4. **Scale up:** Add Solr search service for advanced full-text search capabilities

Your Alfresco MCP integration is ready for AI-powered document management! 🎉