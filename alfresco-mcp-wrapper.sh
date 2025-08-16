#!/bin/bash
# Simple wrapper script for Alfresco MCP Server

cd "/Users/tombrooke/Code/trust-server/alfresco/acs-deployment/python-alfresco-mcp-server"

# Set environment variables
export ALFRESCO_URL="http://localhost:8080"
export ALFRESCO_USERNAME="admin" 
export ALFRESCO_PASSWORD="admin"

# Run the MCP server using UV
exec /Users/tombrooke/.local/bin/uv run python-alfresco-mcp-server --transport stdio