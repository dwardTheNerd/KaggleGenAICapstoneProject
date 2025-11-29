import os
from dotenv import load_dotenv
from pathlib import Path
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

root_path = Path(__file__).resolve().parent.parent 

load_dotenv(root_path / '.env') 

# Fetching obsidian keys and other relevant info
obsidian_key = os.getenv('OBSIDIAN_API_KEY')
obsidian_host = os.getenv('OBSIDIAN_HOST')
obsidian_port = os.getenv('OBSIDIAN_PORT')

def get_obsidian_mcp() -> McpToolset:
    obsidian_mcp = McpToolset(
        connection_params=StdioConnectionParams(
            server_params = StdioServerParameters(
                command = "uvx",
                args = ["mcp-obsidian"],
                env = {
                    "OBSIDIAN_API_KEY": obsidian_key,
                    "OBSIDIAN_HOST": obsidian_host,
                    "OBSIDIAN_PORT": obsidian_port
                }
            ),
            timeout=60
        )
    )

obsidian_mcp_tool = get_obsidian_mcp()
