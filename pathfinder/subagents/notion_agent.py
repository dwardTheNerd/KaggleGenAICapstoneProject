from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import FunctionTool
from pathfinder.tools.mcp_tools import notion_mcp_tool
from pathfinder.prompts import notion_agent_instructions

def create_notion_agent() -> LlmAgent:
    """
    Creates and returns a specialized LlmAgent (subagent) 
    for interacting with Notion via Notion MCP server.
    
    This agent will be exposed as a tool to the main agent.
    """
    notion_agent = LlmAgent(
        model='gemini-2.5-flash-lite',
        name='notion_agent',
        description='Assist with creating Notion page.',
        instruction=notion_agent_instructions,
        tools=[notion_mcp_tool]
    )
    return notion_agent

notion_subagent = create_notion_agent()