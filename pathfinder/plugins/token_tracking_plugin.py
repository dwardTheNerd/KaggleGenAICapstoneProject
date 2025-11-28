import datetime
from pathlib import Path
import sqlite3
import aiosqlite
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.adk.plugins.base_plugin import BasePlugin

class TokenTrackingPlugin(BasePlugin):

    """
    A simple plugin that stores token counts after each after_model_callback in a sqlite database.
    This can be extended to record other related data in other types of callbacks to help with context optimizations.
    """

    def __init__(self) -> None:
        super().__init__(name="token_tracking_plugin")

        root_path = Path(__file__).resolve().parent.parent
        self.db_path = root_path / "db" / "token_usage.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db(self.db_path)

    def init_db(self, db_path) -> None:
        """ Use for initializing sqlite database """
        # Connect (creates DB if doesn't exist)
        conn = sqlite3.connect(db_path)
        
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")

        # Create tables if they don't exist
        self.create_tables(conn)

        # Close the connection when done
        conn.close()

    def create_tables(self, conn: sqlite3.Connection) -> None:
        """Create tables if they don't exist."""

        cursor = conn.cursor()

         # Token usage table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS token_usage (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_id TEXT NOT NULL,
                            invocation_id TEXT NOT NULL,
                            agent_name TEXT NOT NULL,
                            timestamp TIMESTAMP NOT NULL DEFAULT (datetime('now', 'utc')),
                            prompt_tokens INTEGER NOT NULL,
                            candidate_tokens INTEGER NOT NULL,
                            total_tokens INTEGER NOT NULL
                        )
         """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_token_usage_session 
            ON token_usage(session_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_token_usage_timestamp 
            ON token_usage(timestamp)
        """)

        conn.commit()

    async def after_model_callback(self, callback_context: CallbackContext, llm_response: LlmResponse):

        invocation_id = callback_context.invocation_id or ""
        agent_name = callback_context.agent_name or ""
        session_id = callback_context.session.id or ""

        if llm_response.usage_metadata:
            metadata = llm_response.usage_metadata

            prompt_count = metadata.prompt_token_count or 0
            candidates_count = metadata.candidates_token_count or 0
            total_count = metadata.total_token_count or 0

            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO token_usage 
                    (session_id, invocation_id,agent_name, prompt_tokens, candidate_tokens, total_tokens)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (session_id, invocation_id, agent_name, prompt_count, candidates_count, total_count))

                await db.commit()
