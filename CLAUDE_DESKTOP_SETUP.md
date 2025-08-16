# 🎯 Claude Desktop + Alfresco MCP Server Setup

## ✅ Configuration Complete!

Your Claude Desktop has been configured to use the Alfresco MCP server! Here's what was done:

### **📝 Configuration Added**
Updated: `/Users/tombrooke/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "globalShortcut": "Ctrl+Space",
  "mcpServers": {
    "context7": {
      "command": "npx",
       "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "alfresco": {
      "command": "/Users/tombrooke/.local/bin/uv",
      "args": ["run", "python-alfresco-mcp-server", "--transport", "stdio"],
      "cwd": "/Users/tombrooke/Code/trust-server/alfresco/acs-deployment/python-alfresco-mcp-server",
      "env": {
        "ALFRESCO_URL": "http://localhost:8080",
        "ALFRESCO_USERNAME": "admin", 
        "ALFRESCO_PASSWORD": "admin"
      }
    }
  }
}
```

## 🚀 **Next Steps:**

### **1. Restart Claude Desktop**
- **Quit** Claude Desktop completely (Claude → Quit Claude)
- **Restart** Claude Desktop 
- Look for the 🔌 hammer icon in the Claude interface indicating MCP servers are connected

### **2. Verify Connection**
In a new Claude Desktop chat, type:
> "Can you see my Alfresco server? What tools do you have available for document management?"

### **3. Test Basic Queries**
Try these example queries:

#### **🔍 Search & Browse:**
- *"Show me all documents in my Alfresco repository"*
- *"Browse the root directory structure"*
- *"Search for PDF files in the repository"*

#### **📁 Repository Management:**
- *"List the contents of the Company Home folder"*
- *"What folders are available in the repository?"*
- *"Show me information about my Alfresco server"*

#### **📄 Document Operations:**
- *"Create a new folder called 'Projects' in my home space"*
- *"Upload a document to the repository"*
- *"Show me the properties of a specific document"*

## 🎯 **Expected Results:**

### **✅ Success Indicators:**
- 🔌 **Connection icon** appears in Claude Desktop
- 📋 **15 tools available** for Alfresco operations
- 🔍 **Search results** return actual documents from your repository
- 📁 **Browse operations** show your folder structure

### **🛠️ Available Tools:**
1. `search_content` - Find documents by content/metadata
2. `browse_repository` - Navigate folder structures
3. `upload_document` - Upload new files
4. `download_document` - Download existing files
5. `create_folder` - Create new folders
6. `get_node_properties` - Get document/folder metadata
7. `update_node_properties` - Update metadata
8. `delete_node` - Delete files/folders
9. `checkout_document` - Lock for editing
10. `checkin_document` - Save changes and unlock
11. `cancel_checkout` - Cancel edit session
12. `advanced_search` - Advanced search with filtering
13. `search_by_metadata` - Search by specific metadata
14. `cmis_search` - Database-level queries
15. `get_repository_info_tool` - Server information

## 🐛 **Troubleshooting:**

### **If connection fails:**
1. **Check Alfresco is running:**
   ```bash
   curl http://localhost:8080/alfresco/
   ```

2. **Test MCP server manually:**
   ```bash
   cd /Users/tombrooke/Code/trust-server/alfresco/acs-deployment/python-alfresco-mcp-server
   export ALFRESCO_URL="http://localhost:8080"
   export ALFRESCO_USERNAME="admin"
   export ALFRESCO_PASSWORD="admin"
   uv run python-alfresco-mcp-server --transport stdio
   ```

3. **Check Claude Desktop logs** in Console.app for MCP-related errors

### **Common Issues:**
- **"No MCP servers"** → Restart Claude Desktop completely
- **"Connection failed"** → Verify Alfresco is running at localhost:8080
- **"Authentication error"** → Check admin/admin credentials work in Alfresco Share

## 🎉 **You're Ready!**

Your Claude Desktop now has AI-powered access to your Alfresco document management system! Ask Claude natural language questions about your documents, and it will automatically use the MCP server to search, browse, and manage your Alfresco repository.

**Happy AI-powered document management!** 🚀📁