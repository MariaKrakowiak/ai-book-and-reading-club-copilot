import os
import json
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

from agent.prompts import SYSTEM_PROMPT
from agent.tools import (
    search_books,
    get_club_ratings,
    add_book_to_club,
    rate_book,
    update_reading_progress,
    save_note
)


TOOLS = [
    search_books,
    get_club_ratings,
    add_book_to_club,
    rate_book,
    update_reading_progress,
    save_note
]


class ReadingClubAgent:

    def __init__(self):
        self.model_endpoint = os.environ.get(
            "MODEL_SERVING_ENDPOINT"
        )

        if not self.model_endpoint:
            raise RuntimeError(
                "MODEL_SERVING_ENDPOINT is not configured."
            )

    def answer(self, user_message, context=None):
        """
        Process a natural-language reading-club request.

        The production implementation should connect this class
        to the configured Databricks Model Serving endpoint and
        expose TOOLS as callable functions.
        """
        
        # TODO: Replace this mock with real Model Serving endpoint integration
        return {
            "message": f"Mock response: I received your message '{user_message}'. "
                      f"To enable real AI responses, implement this method to call "
                      f"the Model Serving endpoint: {self.model_endpoint}",
            "tools_available": [tool.__name__ for tool in TOOLS]
        }