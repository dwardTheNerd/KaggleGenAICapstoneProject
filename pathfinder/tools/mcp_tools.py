import os
from dotenv import load_dotenv
from pathlib import Path
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

root_path = Path(__file__).resolve().parent.parent 

load_dotenv(root_path / '.env') 

# Fetching Notion Token from .env
notion_key = os.getenv('NOTION_TOKEN')

def get_notion_mcp() -> McpToolset :
    """" 
    Create MCP toolset for using Notion MCP. This will be used for interaction with Notion.
    
    Pre-requisites: 
    Meke sure to obtain Notion token from https://www.notion.so/profile/integrations and save it in .env
    """
    notion_mcp = McpToolset(
        connection_params=StdioConnectionParams(
            server_params = StdioServerParameters(
                command = "npx",
                args = ["-q", "-y", "@notionhq/notion-mcp-server"],
                env = {
                    "NOTION_TOKEN": notion_key
                }
            )
        )
    )
    return notion_mcp

notion_mcp_tool = get_notion_mcp()
