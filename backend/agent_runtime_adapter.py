# backend/agent_runtime_adapter.py
"""
Runtime adapter: prefer LangGraph implementation if available (local/dev).
If LangGraph / LangChain imports fail (e.g. on Vercel), fall back to a
Gemini-only implementation (agent_fallback_gemini.py) that mimics the same
function signatures: get_or_create_agent_for_session(session_id) and
handle_user_message(agent_obj, session_id, user_message).
"""

import importlib
import traceback

# Try to import the LangGraph-based logic (assignment implementation)
try:
    langgraph_logic = importlib.import_module("agent_logic_langgraph")
    HAS_LANGGRAPH = True
except Exception as e:
    # LangGraph / LangChain not available in runtime
    HAS_LANGGRAPH = False
    langgraph_logic = None
    # print to logs so deploy shows fallback used
    print("⚠️ LangGraph import failed; falling back to Gemini-only agent.")
    traceback.print_exc()

# Import fallback implementation (we provide this file)
try:
    fallback = importlib.import_module("agent_fallback_gemini")
except Exception as e:
    fallback = None
    print("❌ Failed to import fallback agent (agent_fallback_gemini).")
    traceback.print_exc()

# Public API (used by app.py)
def get_or_create_agent_for_session(session_id: str):
    if HAS_LANGGRAPH and langgraph_logic:
        # delegate to LangGraph implementation (signature preserved)
        return langgraph_logic.get_or_create_agent_for_session(session_id)
    elif fallback:
        return fallback.get_or_create_agent_for_session(session_id)
    else:
        raise RuntimeError("No agent runtime available (LangGraph missing and fallback not loaded).")

def handle_user_message(agent_obj, session_id: str, user_message: str) -> str:
    if HAS_LANGGRAPH and langgraph_logic:
        return langgraph_logic.handle_user_message(agent_obj, session_id, user_message)
    elif fallback:
        return fallback.handle_user_message(agent_obj, session_id, user_message)
    else:
        raise RuntimeError("No agent runtime available (LangGraph missing and fallback not loaded).")
