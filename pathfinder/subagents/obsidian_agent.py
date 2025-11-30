from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
from pathfinder.tools.mcp_tools import obsidian_mcp_tool
from pathfinder.helpers.config_manager import config
from pathfinder.prompts import obsidian_agent_instructions

def create_obsidian_agent() -> LlmAgent:
    """
    Creates and returns a specialized LlmAgent (subagent) 
    for interacting with Obsidian via Notion MCP server.
    
    This agent will be exposed as a tool to the main agent.
    """
    content_config = types.GenerateContentConfig(
        temperature=0
    )

    obsidian_agent = LlmAgent(
        model=config.obsidian_agent_model,
        name='obsidian_agent',
        description='An intelligent agent that manages your Obsidian vault using MCP tools to search, read, and create content.',
        instruction=obsidian_agent_instructions,
        generate_content_config=content_config,
        tools=[obsidian_mcp_tool]
    )
    return obsidian_agent

obsidian_subagent = create_obsidian_agent()