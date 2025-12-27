# backend/app.py
import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
# Using LangGraph implementation for state management# Runtime-adaptive agent API (will use LangGraph if available, else fallback Gemini)
from agent_runtime_adapter import get_or_create_agent_for_session, handle_user_message

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# Enable CORS for frontend communication
CORS(app)

# Simple in-memory stores (for dev). Use Redis for production.
AGENTS = {}     # session_id -> agent object
LOGS = {}       # session_id -> list of {"role","text","ts"}

@app.route("/api/session", methods=["POST"])
def create_session():
    try:
        session_id = str(uuid.uuid4())
        agent = get_or_create_agent_for_session(session_id)  # initializes the LangGraph/agent
        AGENTS[session_id] = agent
        LOGS[session_id] = []
        return jsonify({"session_id": session_id}), 201
    except Exception as e:
        print(f"Error in /api/session: {str(e)}")
        return jsonify({"error": "Failed to create session", "message": str(e)}), 500

@app.route("/api/message", methods=["POST"])
def message():
    try:
        if not request.json:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        data = request.json
        session_id = data.get("session_id")
        text = data.get("message", "")
        
        if not session_id:
            return jsonify({"error": "session_id is required"}), 400
        
        if not text:
            return jsonify({"error": "message cannot be empty"}), 400
        
        if session_id not in AGENTS:
            # create lazily if missing
            AGENTS[session_id] = get_or_create_agent_for_session(session_id)
            LOGS[session_id] = []

        # add user message to logs
        LOGS[session_id].append({"role": "user", "text": text})
        # send to agent
        reply = handle_user_message(AGENTS[session_id], session_id, text)
        LOGS[session_id].append({"role": "agent", "text": reply})
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error in /api/message: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route("/api/logs/<session_id>", methods=["GET"])
def logs(session_id):
    try:
        return jsonify(LOGS.get(session_id, []))
    except Exception as e:
        print(f"Error in /api/logs: {str(e)}")
        return jsonify({"error": "Failed to retrieve logs", "message": str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "patient-chatbot-api"}), 200

#if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=True)
