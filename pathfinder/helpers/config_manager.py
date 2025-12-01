import json
import os
import logging
from pathlib import Path

class ConfigManager():

    """
    This class is used for fetching the settings stored in config.json and load it for
    easy access later on.
    """

    CONFIG_FILE = 'config.json'
    DEFAULT_MODEL = 'gemini-2.5-flash-lite'
    
    def __init__(self) -> None:
        root_path = Path(__file__).resolve().parent.parent
        
        # Set default values for logging level and models
        self._logging_level = logging.INFO
        self._root_agent_model = ConfigManager.DEFAULT_MODEL
        self._travel_planner_model = ConfigManager.DEFAULT_MODEL
        self._goal_planner_model = ConfigManager.DEFAULT_MODEL
        self._notion_agent_model = ConfigManager.DEFAULT_MODEL
        self._obsidian_agent_model = ConfigManager.DEFAULT_MODEL

        self._context_compact_config = None
        
        # Start loading config
        self.load_config(root_path / ConfigManager.CONFIG_FILE)

    def load_config(self, file_path):
        """Loads configuration data from a JSON file."""
        if not os.path.exists(file_path):
            # Handle the case where the file doesn't exist
            print(f"Error: Configuration file not found at {file_path}")
            return None
        
        # Sets config to None initially
        config = None

        try:
            # Open the file in read mode ('r')
            with open(file_path, 'r') as f:
                # Use json.load() to parse the JSON data from the file and load the config
                config = json.load(f)
                
        except json.JSONDecodeError:
            # Handle invalid JSON format
            print(f"Error: Invalid JSON format in {file_path}")
            return None
        except Exception as e:
            # Handle other potential errors (e.g., permission issues)
            print(f"An unexpected error occurred: {e}")
            return None
        
        # Checks there is config_data, then set the logging level
        if config:

            # Checks if there is logging_level
            if config["logging_level"]:
                logging_level = config.get("logging_level", "INFO")
                if logging_level != "INFO":
                    self._logging_level = logging_level

            # Checks if there is config data for models and load it
            if config["models"]:
                if config["models"]["root_agent"]:
                    self._root_agent_model = config["models"]["root_agent"]

                if config["models"]["travel_planner"]:
                    self._travel_planner_model = config["models"]["travel_planner"]
                
                if config["models"]["goal_planner"]:
                    self._goal_planner_model = config["models"]["goal_planner"]
                
                if config["models"]["notion_agent"]:
                    self._notion_agent_model = config["models"]["notion_agent"]

                if config["models"]["obsidian_agent"]:
                    self._obsidian_agent_model = config["models"]["obsidian_agent"]

            if config["context_compaction"]:
                self._context_compact_config = config["context_compaction"]

    @property
    def logging_level(self):
        return self._logging_level
    
    @property
    def root_agent_model(self):
        return self._root_agent_model
    
    @property
    def travel_planner_model(self):
        return self._travel_planner_model    
    
    @property
    def goal_planner_model(self):
        return self._goal_planner_model
    
    @property
    def notion_agent_model(self):
        return self._notion_agent_model
    
    @property
    def obsidian_agent_model(self):
        return self._obsidian_agent_model
    
    @property
    def context_compact_config(self):
        return self._context_compact_config
    
config = ConfigManager()