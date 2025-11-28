from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.google_llm import Gemini
from google.adk.apps.app import EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.genai import types
from pathfinder.subagents.goal_planner import goal_planner_subagent
from pathfinder.subagents.travel_planner import travel_planner_subagent
from pathfinder.subagents.notion_agent import notion_subagent
from pathfinder.prompts import root_agent_instructions

"""
This is where the root_agent resides. The settings and tools used by the root_agent are declared here.
"""

# Defining sub-agents to be used as tools
goal_planner_tool = AgentTool(goal_planner_subagent)
travel_planner_tool = AgentTool(travel_planner_subagent)
notion_agent_tool = AgentTool(notion_subagent)

# Defining retry options
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=2,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# Define the AI model to be used for summarization:
summarization_llm = Gemini(model="gemini-2.5-flash")

# Create the summarizer with the custom model:
summarizer = LlmEventSummarizer(llm=summarization_llm)

# Defining events compaction config
events_compact_config = EventsCompactionConfig(
    summarizer=summarizer,
    compaction_interval=3,
    overlap_size=1
)

# Configure the model with retry options
llm_model = Gemini(
    model='gemini-2.5-flash',
    retry_options=retry_config,
    events_compact_config=events_compact_config
)

# Define root agent
root_agent = Agent(
    model=llm_model,
    name='root_agent',
    description='A helpful personal planning assistant for goals and travel itinerary',
    instruction=root_agent_instructions,
    tools=[goal_planner_tool, travel_planner_tool, notion_agent_tool]
)
