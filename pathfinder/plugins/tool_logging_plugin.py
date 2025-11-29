# Adapted from https://github.com/google/adk-python/blame/main/src/google/adk/plugins/logging_plugin.py
# This plugin is used for logging information around tool callbacks. 
# The generated logs can be used for monitoring and debugging tool calls.

import logging
from logging.handlers import RotatingFileHandler
import datetime
from pathlib import Path
from typing import Any
from typing import Optional
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool

class ToolLoggingPlugin(BasePlugin):

    def __init__(self) -> None:
        super().__init__(name="tool_logging_plugin")
        self.logger = self.init_logger()

    def init_logger(self):
        logger = logging.getLogger("ToolLoggingPlugin")

        # Get project root path
        root_path = Path(__file__).resolve().parent.parent

        # Configuring logging options
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_filename = f"tool_{current_date}.log"
        log_path = root_path / "logs" / log_filename
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Set the logging level to be the same the global logging level
        logger.setLevel(logging.getLogger(__name__).level)

        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=100*1024*1024,
            backupCount=5
        )

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    async def before_tool_callback(self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext) -> Optional[dict]:
        """Log tool execution start."""
        self.logger.debug("****** Start before_tool_callback ******")
        self.logger.debug(f"🔧 TOOL STARTING")
        self.logger.debug(f"   Tool Name: {tool.name}")
        self.logger.debug(f"   Agent: {tool_context.agent_name}")
        self.logger.debug(f"   Function Call ID: {tool_context.function_call_id}")
        self.logger.debug(f"   Arguments: {self._format_args(tool_args)}")
        self.logger.debug("****** End before_tool_callback ******")
        return None
        
    async def after_tool_callback(self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext, result: dict) -> Optional[dict]:
        """Log tool execution completion."""
        self.logger.debug("****** Start after_tool_callback ******")
        self.logger.debug(f"🔧 TOOL COMPLETED")
        self.logger.debug(f"   Tool Name: {tool.name}")
        self.logger.debug(f"   Agent: {tool_context.agent_name}")
        self.logger.debug(f"   Function Call ID: {tool_context.function_call_id}")
        self.logger.debug(f"   Result: {self._format_args(result)}")
        self.logger.debug("****** End after_tool_callback ******")
        return None

    def _format_args(self, args: dict[str, Any], max_length: int = 5000) -> str:
        """Format arguments dictionary for logging."""
        if not args:
            return "{}"
        
        formatted = str(args)
        if len(formatted) > max_length:
            formatted = formatted[:max_length] + "...}"
        return formatted