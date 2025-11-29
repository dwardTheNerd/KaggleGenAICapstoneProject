from google.adk.agents.llm_agent import LlmAgent
from pathfinder.tools.mcp_tools import obsidian_mcp_tool
from pathfinder.prompts import obsidian_agent_instructions

def create_obsidian_agent() -> LlmAgent:
    """
    Creates and returns a specialized LlmAgent (subagent) 
    for interacting with Obsidian via Notion MCP server.
    
    This agent will be exposed as a tool to the main agent.
    """
    obsidian_agent = LlmAgent(
        model='gemini-2.5-flash-lite',
        name='obsidian_agent',
        description='An intelligent agent that manages your Obsidian vault using MCP tools to search, read, and create content.',
        instruction=obsidian_agent_instructions,
        tools=[obsidian_mcp_tool]
    )
    return obsidian_agent

obsidian_subagent = create_obsidian_agent()