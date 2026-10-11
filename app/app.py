import sys
import os

# Add parent directory to Python path to resolve 'agent' module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from agent.tools import (
    add_book_to_club,
    rate_book,
    update_reading_progress
)
from agent.agent import ReadingClubAgent


st.set_page_config(
    page_title="AI Reading Club Copilot",
    page_icon="📚",
    layout="centered",
)


def get_agent():
    """Initialize the reading club agent once per session."""

    if "agent" not in st.session_state:
        try:
            st.session_state.agent = ReadingClubAgent()
        except RuntimeError as exc:
            st.session_state.agent = None
            st.session_state.agent_error = str(exc)

    return st.session_state.agent


def ask_agent(prompt):
    """Send a prompt to the agent and display the conversation."""

    agent = get_agent()

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if agent is None:
            response = (
                "Agent not initialized. Please configure the "
                "MODEL_SERVING_ENDPOINT environment variable."
            )
            st.warning(response)
        else:
            with st.spinner("Asking the Reading Copilot..."):
                result = agent.answer(prompt)

            response = result.get("message", "")

            if result.get("error"):
                st.error(response)
            else:
                st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )


st.title("📚 Reading Club Copilot")
st.caption("Your AI-powered reading companion, built with Databricks")

if "messages" not in st.session_state:
    st.session_state.messages = []

agent = get_agent()

if agent is None:
    st.warning(
        "Agent is not initialized. Chat will be unavailable until "
        "the MODEL_SERVING_ENDPOINT environment variable is configured."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

suggestions = [
    "Find a mystery book for our club",
    "Compare two popular fantasy books",
    "Create a reading plan for beginners",
    "Suggest a book for our next discussion",
]

st.markdown("**Try asking**")

suggestion_columns = st.columns(len(suggestions))

for column, suggestion in zip(suggestion_columns, suggestions):
    if column.button(suggestion, use_container_width=True):
        ask_agent(suggestion)

prompt = st.chat_input("What would you like help with?")

if prompt:
    ask_agent(prompt)

with st.expander("Manage your reading club"):
    tab_add, tab_rate, tab_progress = st.tabs(
        ["Add a book to a club", "Rate a book", "Update reading progress"]
    )

    with tab_add:
        with st.form("add_book_to_club"):
            club_id = st.number_input(
                "Club ID", min_value=1, step=1, key="add_club_id"
            )
            book_id = st.number_input(
                "Book ID", min_value=1, step=1, key="add_book_id"
            )
            submitted = st.form_submit_button("Add book to club")

            if submitted:
                try:
                    result = add_book_to_club(club_id, book_id)
                    st.success(
                        f"Book {result['book_id']} added to "
                        f"club {result['club_id']}."
                    )
                except Exception as exc:
                    st.error(str(exc))

    with tab_rate:
        with st.form("rate_book_form"):
            user_id = st.number_input(
                "User ID", min_value=1, step=1, key="rate_user_id"
            )
            book_id = st.number_input(
                "Book ID", min_value=1, step=1, key="rate_book_id"
            )
            rating = st.slider(
                "Rating", min_value=1, max_value=5, value=5, key="rate_rating"
            )
            review = st.text_area(
                "Review (optional)", key="rate_review"
            )
            submitted = st.form_submit_button("Save rating")

            if submitted:
                try:
                    rate_book(user_id, book_id, rating, review or None)
                    st.success("Rating saved.")
                except Exception as exc:
                    st.error(str(exc))

    with tab_progress:
        with st.form("update_reading_progress_form"):
            user_id = st.number_input(
                "User ID", min_value=1, step=1, key="progress_user_id"
            )
            book_id = st.number_input(
                "Book ID", min_value=1, step=1, key="progress_book_id"
            )
            pages_read = st.number_input(
                "Pages read", min_value=0, step=1, key="progress_pages"
            )
            status = st.select_slider(
                "Status",
                options=["not_started", "in_progress", "finished"],
                key="progress_status",
            )
            submitted = st.form_submit_button("Update progress")

            if submitted:
                try:
                    result = update_reading_progress(
                        user_id, book_id, pages_read, status
                    )
                    st.success(
                        f"Progress updated: {result['pages_read']} pages "
                        f"read, status '{result['status']}''."
                    )
                except Exception as exc:
                    st.error(str(exc))