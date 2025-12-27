# backend/agent_fallback_gemini.py
"""
Fallback agent using Gemini directly (no LangChain / LangGraph dependencies).
Implements:
- get_or_create_agent_for_session(session_id) -> returns agent_obj (dict)
- handle_user_message(agent_obj, session_id, user_message) -> str (reply)
"""

import os
import time
import uuid
from typing import Dict

# Try new client first
try:
    from google import genai as genai_client
    NEW_GENAI = True
except Exception:
    try:
        import google.generativeai as genai_client
        NEW_GENAI = False
    except Exception:
        genai_client = None
        NEW_GENAI = False

# Ensure GEMINI key is present
GEMINI_API_KEY = (
    os.environ.get("GEMINI_API_KEY") or
    os.environ.get("GOOGLE_API_KEY") or
    os.environ.get("Gemini_API_KEY") or
    os.environ.get("gemini_api_key")
)
if not GEMINI_API_KEY:
    # Do not raise here; allow startup but operations will fail later with clear message
    print("⚠️ GEMINI_API_KEY not set. Set GEMINI_API_KEY in environment for fallback agent to work.")
else:
    # configure older client if needed
    if not NEW_GENAI and genai_client:
        genai_client.configure(api_key=GEMINI_API_KEY)
    elif NEW_GENAI and genai_client:
        # new client: create a client instance
        try:
            client = genai_client.Client(api_key=GEMINI_API_KEY)
        except Exception:
            client = None
    else:
        client = None

# In-memory session store
_SESSIONS: Dict[str, Dict] = {}

# Simple prompt templates to mimic LangGraph behavior
SYSTEM_RULES = """You are a simulated patient. Follow these rules:
1) Reveal symptoms progressively — start mild and provide more detail only when asked.
2) If a treatment is prescribed, either accept it (echoing the treatment), ask a clarifying question, or politely decline.
3) Speak in first person and be realistic.
"""

def _choose_model_candidate():
    # choose a safe default; administrators should set GEMINI model via env if desired
    preferred = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    return preferred

def _generate_text(prompt: str) -> str:
    """Call Gemini (tries new client, else older). Includes simple retry/backoff."""
    if not genai_client:
        raise RuntimeError("Gemini client library is not installed or configured (genai missing).")
    model = _choose_model_candidate()
    max_retries = 3
    delay = 1.5
    for attempt in range(max_retries):
        try:
            if NEW_GENAI:
                c = genai_client.Client(api_key=GEMINI_API_KEY)
                resp = c.models.generate_content(model=model, contents=prompt)
                return getattr(resp, "text", "") or str(resp)
            else:
                m = genai_client.GenerativeModel(model)
                resp = m.generate_content(prompt)
                # older client exposes .text as well
                return getattr(resp, "text", "") or str(resp)
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower() or "RESOURCE_EXHAUSTED" in err:
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))
                    continue
                else:
                    return "I'm experiencing high load or quota limits. Please try again shortly."
            else:
                # non-rate-limit errors: return user-friendly message
                print("Fallback generation error:", err)
                return "I'm having trouble responding right now. Please try again later."
    return "I'm having trouble responding right now."

def get_or_create_agent_for_session(session_id: str):
    """Return an agent dict with session storage. Mirrors LangGraph session shape."""
    if not session_id:
        session_id = str(uuid.uuid4())
    if session_id not in _SESSIONS:
        profile = {
            "patient_name": "FallbackPatient",
            "age": 30,
            "med_history": "No major illnesses."
        }
        _SESSIONS[session_id] = {
            "session_id": session_id,
            "profile": profile,
            "conversation_history": [],  # list of {"role":..., "content":...}
            "current_state": "initial",
            "symptom_level": 0,
            "treatment_detected": False,
            "treatment_accepted": False
        }
        print(f"✅ Created fallback agent for session {session_id}")
    return _SESSIONS[session_id]

def _format_history_for_prompt(history):
    if not history:
        return ""
    out = []
    for m in history[-12:]:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "user":
            out.append(f"Doctor: {content}")
        else:
            out.append(f"Patient: {content}")
    return "\n".join(out)

def handle_user_message(agent_obj: dict, session_id: str, user_message: str) -> str:
    """Produce patient response and update the agent_obj (in-place)."""
    # safety
    if agent_obj is None:
        agent_obj = get_or_create_agent_for_session(session_id)
    profile = agent_obj.get("profile", {})
    history = agent_obj.get("conversation_history", [])
    state = agent_obj.get("current_state", "initial")
    sym_level = agent_obj.get("symptom_level", 0)

    # decide which "node" to run (mirror langgraph logic)
    lower = user_message.lower()
    treatment_keywords = ["prescribe", "medication", "treatment", "take", "medicine", "drug"]

    if not history:
        # initial greeting
        prompt = f"""{SYSTEM_RULES}
Patient profile:
Name: {profile.get('patient_name')}
Age: {profile.get('age')}
Medical history: {profile.get('med_history')}

Doctor: {user_message}
Patient:"""
    elif any(k in lower for k in treatment_keywords):
        prompt = f"""{SYSTEM_RULES}
Patient profile:
Name: {profile.get('patient_name')}
Age: {profile.get('age')}
Medical history: {profile.get('med_history')}

The doctor has prescribed a treatment. Evaluate and respond:
Doctor: {user_message}
Patient:"""
    elif any(word in lower for word in ["more", "detail", "describe", "tell me"]) and sym_level < 2:
        prompt = f"""{SYSTEM_RULES}
Patient profile:
Name: {profile.get('patient_name')}
Age: {profile.get('age')}
Medical history: {profile.get('med_history')}

The doctor asked for more detail. Reveal more specific symptoms (onset, severity, triggers).
Conversation history:
{_format_history_for_prompt(history)}

Doctor: {user_message}
Patient:"""
    else:
        prompt = f"""{SYSTEM_RULES}
Patient profile:
Name: {profile.get('patient_name')}
Age: {profile.get('age')}
Medical history: {profile.get('med_history')}

Answer succinctly and factually to the doctor's question.
Conversation history:
{_format_history_for_prompt(history)}

Doctor: {user_message}
Patient:"""

    reply = _generate_text(prompt)
    # Update session state
    history.append({"role": "user", "content": user_message})
    history.append({"role": "patient", "content": reply})
    agent_obj["conversation_history"] = history
    # increment symptom_level if asked for detail
    if any(word in lower for word in ["more", "detail", "describe", "tell me"]):
        agent_obj["symptom_level"] = min(sym_level + 1, 2)
    if any(k in lower for k in treatment_keywords):
        agent_obj["treatment_detected"] = True
        # naive check for acceptance
        if "accept" in reply.lower() or "i accept" in reply.lower():
            agent_obj["treatment_accepted"] = True
    return reply
