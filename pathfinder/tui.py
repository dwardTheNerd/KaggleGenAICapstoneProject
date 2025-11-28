from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button,  Static, Label
from textual.containers import Horizontal, Container, Grid
from textual.screen import ModalScreen
from textual.widget import Widget
from pathfinder.agent_controller import AgentController

# TUI implementation adapted from https://chaoticengineer.hashnode.dev/textual-and-chatgpt

"""
This contains all the Textual widgets and main TUI app used for presenting a chat interface
for user to interact with agent.

References:
- Textual doc: https://textual.textualize.io/
- Chat interface adapted from https://chaoticengineer.hashnode.dev/textual-and-chatgpt
"""

class FocusableContainer(Container, can_focus=True):
     """Focusable container widget."""

class MessageBox(Widget, can_focus=True):
    """Box widget for the message."""
    def __init__(self, text: str, role: str) -> None:
        self.text = text
        self.role = role
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Static(self.text, classes=f"message {self.role}")

class UserIDScreen(ModalScreen[str]):
    """Screen with a dialog to ask user for for a user id"""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Enter a user ID", id="modal_question"),
            Input(placeholder="Enter your user ID", id="modal_input"),
            Button("Confirm", variant="primary", id="yes"),
            Button("Quit", variant="error", id="cancel"),
            id="input_dialog"
        )

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self) -> None:
        self.query_one("#yes", Button).action_press()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        modal_input = self.query_one("#modal_input", Input).value
        if event.button.id == "yes":
            if modal_input == "":
                # Do nothing if input is empty
                return
            self.dismiss(modal_input)
        else:
            self.dismiss("QUIT")

class QuestionScreen(ModalScreen[bool]):
    """Screen with a dialog to ask user for action confirmation"""

    def __init__(self, question: str) -> None:
        self.question = question
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.question, id="modal_question"),
            Button("Yes", variant="error", id="yes"),
            Button("Cancel", variant="primary", id="cancel"),
            id="question_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)

class PathfinderTUI(App):

    TITLE = "The Pathfinder"
    SUB_TITLE = "Personal goal and travel planner"
    CSS_PATH="static/styles.tcss"

    BINDINGS = [
        ("q", "request_quit", "Quit"),
        ("ctrl+x", "clear", "Clear"),
        ("ctrl+d", "delete_session", "Delete Session")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with FocusableContainer(id="conversation_box"):
            yield MessageBox( 
                "Welcome to Pathfinder, your personal goal and travel planner!\n"
                "Enter your goal, hit ENTER or 'Send' button "
                "and wait for the response.\n"
                "At the bottom you can find few more helpful commands.",
                role="info",
            )
        with Horizontal(id="input_box"):
            yield Input(placeholder="Enter your message", id="message_input")
            yield Button(label="Send", variant="success",id="send_button")
        yield Footer()

    def on_mount(self) -> None:
        # Push a modal screen to ask for a user id
        self.push_user_id_screen()
        # Create AgentController object
        self.agent_controller = AgentController()
        

    def push_user_id_screen(self) -> None:
        """ Display modal box to ask for user id """
        async def check_confirm(confirm: str | None) -> None:
            if confirm == "QUIT":
                self.exit()
            if confirm != "":
                # if confirm has something in it, set it as user_id
                self.user_id = confirm
            
            self.query_one("#message_input", Input).focus()

        self.push_screen(UserIDScreen(), check_confirm)

    async def on_button_pressed(self) -> None:
        """ 
        When Send button is pressed, call process_conversation() to start communicating with agent
        """
        await self.process_conversation()
    
    async def on_input_submitted(self) -> None:
        """ 
        When user hit ENTER in the input box, call process_conversation() to start communicating with agent
        """
        await self.process_conversation()

    def toggle_widgets(self, *widgets: Widget) -> None:
        """ Used for toggling widgets between enabled and disabled state and vice-versa """
        for w in widgets:
            w.disabled = not w.disabled

    async def action_clear(self) -> None:
        """Action to display the clear conversations dialog."""
        async def check_clear(clear: bool | None) -> None:
            """Called when QuestionScreen is dismissed.""" 
            if clear:
                conversation_box = self.query_one("#conversation_box")
                await conversation_box.remove()
                self.mount(FocusableContainer(id="conversation_box"))

        self.push_screen(QuestionScreen("Are you sure want to clear all conversations on screen?"), check_clear)

    async def action_request_quit(self) -> None:
        """Action to display the quit dialog."""
        async def check_quit(quit: bool | None) -> None:
            """Called when QuestionScreen is dismissed."""
            if quit:
                await self.agent_controller.close()
                self.exit()
        
        self.push_screen(QuestionScreen("Are you sure you want to quit?"), check_quit)

    async def action_delete_session(self) -> None:
        """Action to display delete session dialog."""
        async def check_delete(delete: bool | None) -> None:
            if delete:
                conversation_box = self.query_one("#conversation_box")
                await conversation_box.remove()
                self.mount(FocusableContainer(id="conversation_box"))
                await self.agent_controller.delete_session()

        self.push_screen(QuestionScreen("Are you sure want to delete existing session and all past history recorded?"), check_delete)

    async def process_conversation(self) -> None:
        # Retrieve the input box
        message_input = self.query_one("#message_input", Input)

        # Grab the value entered in the input box
        user_input = message_input.value

        # Don't do anything if input is empty
        if user_input == "":
            return
        
        # Retrieve the Send button and conversation box
        button = self.query_one("#send_button")
        conversation_box = self.query_one("#conversation_box")

        # Disable input box and button while message is processing
        self.toggle_widgets(message_input, button)

        # Create question message, add it to the conversation and scroll down
        message_box = MessageBox(user_input, "question")
        conversation_box.mount(message_box)
        conversation_box.scroll_end(animate=True)

        # Replace input with a loading indicator
        message_input.loading = True

        # Clean up the input without triggering events
        with message_input.prevent(Input.Changed):
            message_input.value = ""

        # Start session and begin chatting with agent
        #await self.agent_controller.start_session(self.user_id)
        response = await self.agent_controller.call_agent(user_id=self.user_id, queries=user_input)
        
        if response:
            # Check if the response is *not* the specific error dictionary format.
            if not isinstance(response, dict) or "error" not in response:
                # Add agent response to the conversation
                conversation_box.mount(
                    MessageBox(
                        response,
                        "answer"
                    )
                )
            else:
                error_code = response["details"]["error_code"]
                error_message = response["details"]["error_message"]
                error_response = f"An error was encontered. Check the logs for more information.\n\nError code: {error_code}\nError message: {error_message}"
                # Add error response to the conversation
                conversation_box.mount(
                    MessageBox(
                        error_response,
                        "answer"
                    )
                )

        # Revert the input back to normal state
        message_input.loading = False

        # Focus on the input box again
        message_input.focus()

        # Re-enable message_input and button
        self.toggle_widgets(message_input, button)
        conversation_box.scroll_end(animate=True)