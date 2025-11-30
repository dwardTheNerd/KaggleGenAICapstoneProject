from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
from google.adk.tools import google_search
from pathfinder.helpers.config_manager import config
from pathfinder.prompts import goal_planner_instructions

def create_goal_planner_agent() -> LlmAgent:
    """
    Creates and returns a specialized LlmAgent (subagent) 
    for goal planning.
    
    This agent will be exposed as a tool to the main agent.
    """
    content_config = types.GenerateContentConfig(
        temperature=0.5
    )

    goal_planner_agent = LlmAgent(
        model=config.goal_planner_model,
        name='goal_planner_agent',
        description='A professional goal planning assistant',
        instruction=goal_planner_instructions,
        generate_content_config=content_config,
        tools=[google_search]
    )
    return goal_planner_agent

goal_planner_subagent = create_goal_planner_agent()