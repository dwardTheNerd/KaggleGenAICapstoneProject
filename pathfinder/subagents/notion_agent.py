from google.adk.agents.llm_agent import LlmAgent
from pathfinder.tools.function_tools import create_notion_page_tool, search_notion_pages_by_title_tool
from pathfinder.prompts import notion_agent_instructions

def create_notion_agent() -> LlmAgent:
    """
    Creates and returns a specialized LlmAgent (subagent) 
    for interacting with Notion via a FunctionTool.
    
    This agent will be exposed as a tool to the main agent.
    """
    notion_agent = LlmAgent(
        model='gemini-2.5-flash-lite',
        name='notion_agent',
        description='An helpful agent that helps to create and upload content to new Notion page.',
        instruction=notion_agent_instructions,
        tools=[create_notion_page_tool, search_notion_pages_by_title_tool]
    )
    return notion_agent

notion_subagent = create_notion_agent()