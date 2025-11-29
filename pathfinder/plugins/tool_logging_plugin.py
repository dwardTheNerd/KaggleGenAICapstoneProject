"""
Adapted from https://github.com/google/adk-python/blame/main/src/google/adk/plugins/logging_plugin.py
"""

import logging
from typing import Any
from typing import Optional
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool

class ToolLoggingPlugin(BasePlugin):

    def __init__(self) -> None:
        super().__init__(name="tool_logging_plugin")
        self.logger = logging.getLogger(__file__)

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
        self.logger = logging.getLogger(__file__)
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