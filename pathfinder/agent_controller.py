import logging
from pathlib import Path
from dotenv import load_dotenv
from google.adk.apps.app import App
from google.adk.sessions import Session, DatabaseSessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part
from pathfinder.agent import root_agent
from google.adk.plugins import ReflectAndRetryToolPlugin
from pathfinder.plugins.tool_logging_plugin import ToolLoggingPlugin
from pathfinder.plugins.token_tracking_plugin import TokenTrackingPlugin

load_dotenv() 

class AgentController():

    """
    A controller class that exposes several methods that front-end app can use to
    manage and interact with root agent.
    """

    APP_NAME = 'pathfinder_app'

    def __init__(self):
        # Retrieve logger
        self.logger = logging.getLogger(__name__)
        
        db_path = Path(__file__).parent / "db" / "pathfinder_sessions.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Setting up DatabaseSessioNService
        db_url = f"sqlite+aiosqlite:///{db_path}"  # Local SQLite file
        self.session_service = DatabaseSessionService(db_url=db_url)
        
        # session to be set later
        self.session = None   

        self.app = self.create_app()

        # Preparing Runner
        self.runner = Runner(app=self.app, session_service=self.session_service)

    def create_app(self) -> App:
        plugins = [ReflectAndRetryToolPlugin(max_retries=3), ToolLoggingPlugin(), TokenTrackingPlugin()]

        app = App(
            name=AgentController.APP_NAME,
            root_agent=root_agent,
            plugins=plugins
        )
        return app

    async def start_session(self, user_id):
        """
        Used to start a session. This checks if a session already exists, and fetch the session.
        If the session does not exiet, create a new session.

        Args:
            user_id: string containing user id
        """
        session_id = f"{user_id}_session"
        try:
            self.session = await self.session_service.create_session(
                app_name=self.app.name, 
                user_id=user_id, 
                session_id=session_id
            )
            self.logger.info(f"***** Created new session: {self.session.id} *****")
        except:
            self.session = await self.session_service.get_session(
                app_name=self.app.name, 
                user_id=user_id, 
                session_id=session_id
            )
            self.logger.info(f"***** Retrieved existing session: {self.session.id} *****")
    
    async def delete_session(self):
        """ Used for deleting existing session """
        if self.session:
            await self.session_service.delete_session(app_name=self.app.name, user_id=self.session.user_id, session_id=self.session.id)
            self.logger.info(f"**** Deleted session: {self.session.id} *****")
            self.session = None

    async def call_agent(self, user_id: str, queries: list[str] | str = None):
        """
        Used for calling agent via Runner.run_async()

        Args:
            user_id: A user id to identify the user
            queries: Queries that user want to send to agent
        """
        # Start session if session has not been started previously
        if self.session is None:
            await self.start_session(user_id)

        if queries:
            # Convert single query to list for uniform processing
            if type(queries) == str:
                queries = [queries]

        # Process each query in the list sequentially
        for query in queries:

            # Convert the query string to the ADK Content format
            user_msg = Content(role="user", parts=[Part(text=query)])

            session_total_tokens = 0
            
            full_response_text = ""
            async for event in self.runner.run_async(user_id=user_id, session_id=self.session.id, new_message=user_msg):

                # If encounter error
                if event.error_code and event.error_message:
                    # Logs error using logger
                    error_msg = f"Agent error - Code: {event.error_code}, Message: {event.error_message}"
                    self.logger.error(f"User: {user_id}, Session: {self.session.id}, {error_msg}")

                    # Store error details for caller to handle
                    error_info = {
                        "error_code": event.error_code,
                        "error_message": event.error_message,
                        "user_id": user_id,
                        "session_id": self.session.id,
                        "query": query
                    }

                    # Return error response
                    return {"error": True, "details": error_info}

                # If usage metadata exist, grab the total token count and add to the current session total token count
                if event.usage_metadata:
                    turn_total = event.usage_metadata.total_token_count
                    session_total_tokens += turn_total

                if event.partial and event.content and event.content.parts and event.content.parts[0].text:
                    full_response_text += event.content.parts[0].text

                if event.is_final_response():
                    if event.content and event.content.parts and event.content.parts[0].text:
                        final_text = full_response_text + (event.content.parts[0].text if not event.partial else "")
                        if session_total_tokens > 0:
                            return f"Total token count: {session_total_tokens}\n----------\n\n{final_text}"
                        else:
                            return final_text
    
    async def close(self) -> None:
        """ This is used for closing the runner """
        if self.runner:
            await self.runner.close()