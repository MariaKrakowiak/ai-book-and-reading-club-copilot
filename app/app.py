import sys
import os

# Add parent directory to Python path to resolve 'agent' module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify

from agent.tools import (
    add_book_to_club,
    rate_book,
    update_reading_progress
)
from agent.agent import ReadingClubAgent


app = Flask(__name__)

# Initialize the reading club agent
try:
    agent = ReadingClubAgent()
except Exception as e:
    agent = None
    print(f"Warning: Agent not initialized - {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/add-book")
def add_book():
    data = request.json

    try:
        result = add_book_to_club(
            data["club_id"],
            data["book_id"]
        )

        return jsonify(result)

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 400


@app.post("/api/rate")
def rate():
    data = request.json

    try:
        result = rate_book(
            data["user_id"],
            data["book_id"],
            data["rating"],
            data.get("review")
        )

        return jsonify(result)

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 400


@app.post("/api/progress")
def progress():
    data = request.json

    try:
        result = update_reading_progress(
            data["user_id"],
            data["book_id"],
            data["pages_read"],
            data["status"]
        )

        return jsonify(result)

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 400


@app.post("/api/agent")
def agent_chat():
    """Handle conversational agent requests"""
    data = request.json

    if not agent:
        return jsonify({
            "success": False,
            "error": "Agent not initialized. Please configure MODEL_SERVING_ENDPOINT environment variable."
        }), 503

    try:
        user_message = data.get("message")
        context = data.get("context")

        if not user_message:
            return jsonify({
                "success": False,
                "error": "Missing 'message' field in request"
            }), 400

        result = agent.answer(user_message, context)

        return jsonify({
            "success": True,
            "response": result
        })

    except NotImplementedError as exc:
        return jsonify({
            "success": False,
            "error": "Agent implementation incomplete. Please connect ReadingClubAgent to your Databricks Model Serving endpoint."
        }), 501

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )