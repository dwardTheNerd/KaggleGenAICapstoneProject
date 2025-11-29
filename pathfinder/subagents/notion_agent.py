from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
from pathfinder.tools.function_tools import create_notion_page_tool, search_notion_pages_by_title_tool
from pathfinder.prompts import notion_agent_instructions

def create_notion_agent() -> LlmAgent:
    """
    Creates and returns a specialized LlmAgent (subagent) 
    for interacting with Notion via a FunctionTool.
    
    This agent will be exposed as a tool to the main agent.
    """
    content_config = types.GenerateContentConfig(
        temperature=0
    )

    notion_agent = LlmAgent(
        model='gemini-2.5-flash-lite',
        name='notion_agent',
        description='An helpful agent that helps to create and upload content to new Notion page.',
        instruction=notion_agent_instructions,
        generate_content_config=content_config,
        tools=[create_notion_page_tool, search_notion_pages_by_title_tool]
    )
    return notion_agent

notion_subagent = create_notion_agent()