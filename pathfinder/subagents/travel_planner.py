from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
from google.adk.tools import google_search
from pathfinder.prompts import travel_planner_instructions

def create_travel_planner_agent() -> LlmAgent:
    """
    Creates and returns a specialized LlmAgent (subagent) 
    for travel planning.
    
    This agent will be exposed as a tool to the main agent.
    """
    content_config = types.GenerateContentConfig(
        temperature=0.5
    )
    
    travel_planner_agent = LlmAgent(
        model='gemini-2.5-flash-lite',
        name='travel_planner_agent',
        description='A professional travel planning assistant',
        instruction=travel_planner_instructions,
        generate_content_config=content_config,
        output_key="current_plan",
        tools=[google_search]
    )
    return travel_planner_agent

travel_planner_subagent = create_travel_planner_agent()