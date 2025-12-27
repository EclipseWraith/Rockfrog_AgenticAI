# LangGraph Implementation for Patient Chatbot
# Uses LangGraph StateGraph for state management with nodes and edges
import os
from typing import TypedDict, Annotated, Literal
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph, END

# Try the newer Client API import, fallback to standard import
try:
    from google import genai
    USE_NEW_CLIENT = True
except ImportError:
    import google.generativeai as genai
    USE_NEW_CLIENT = False

load_dotenv()

# Check for API key
GEMINI_API_KEY = (
    os.environ.get("GEMINI_API_KEY") or 
    os.environ.get("GOOGLE_API_KEY") or 
    os.environ.get("Gemini_API_KEY") or
    os.environ.get("gemini_api_key")
)
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable must be set")

# Set the API key in environment if not already set
if not os.environ.get("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Initialize the client based on available API
if USE_NEW_CLIENT:
    try:
        client = genai.Client()
        print("✅ Using newer Google Generative AI Client API")
    except Exception as e:
        print(f"⚠️  New Client API failed: {e}, falling back to standard API")
        USE_NEW_CLIENT = False
        genai.configure(api_key=GEMINI_API_KEY)
        client = None
else:
    genai.configure(api_key=GEMINI_API_KEY)
    client = None
    print("✅ Using standard Google Generative AI API")

# Find an available model (prioritize free-tier models)
def get_available_model():
    """Try different model names, prioritizing free-tier compatible models"""
    model_names = [
        'gemini-1.5-flash',  # Free tier compatible
        'gemini-1.0-pro',    # Free tier compatible
        'gemini-pro',        # Free tier compatible
        'gemini-2.5-flash',  # May not be on free tier
        'gemini-1.5-pro',    # May not be on free tier
    ]
    
    for model_name in model_names:
        try:
            if USE_NEW_CLIENT and client:
                test_response = client.models.generate_content(
                    model=model_name,
                    contents="test"
                )
            else:
                model = genai.GenerativeModel(model_name)
                test_response = model.generate_content("test")
            print(f"✅ Using model: {model_name}")
            return model_name
        except Exception as e:
            error_msg = str(e)
            if "404" not in error_msg and "not found" not in error_msg.lower() and "429" not in error_msg:
                print(f"✅ Using model: {model_name} (test had minor issue, but will try)")
                return model_name
            print(f"❌ Model {model_name} not available: {error_msg[:50]}")
            continue
    
    raise ValueError("No available Gemini models found. Check API key and quota.")

MODEL_NAME = get_available_model()

# ============================================================================
# LangGraph State Schema Definition
# ============================================================================

class PatientState(TypedDict):
    """State schema for LangGraph patient conversation flow"""
    session_id: str
    user_message: str
    patient_response: str
    conversation_history: Annotated[list, "List of conversation messages"]
    current_state: Literal["initial", "questioning", "progressive", "treatment"]
    symptom_level: int  # 0=mild, 1=moderate, 2=detailed
    treatment_detected: bool
    treatment_accepted: bool
    patient_profile: dict

# ============================================================================
# LangGraph Node Functions
# ============================================================================

def initial_greeting_node(state: PatientState) -> PatientState:
    """Node 1: Initial greeting with mild symptoms"""
    profile = state["patient_profile"]
    
    prompt = f"""You are a simulated patient. Your patient profile:
- Name: {profile["patient_name"]}
- Age: {profile["age"]}
- MedicalHistory: {profile["med_history"]}

You are starting a conversation with a doctor. Introduce yourself briefly and mention only MILD symptoms. Keep it short and natural.

Doctor: {state["user_message"]}
Patient:"""
    
    response = generate_response(prompt)
    
    return {
        "patient_response": response,
        "current_state": "questioning",
        "symptom_level": 0,
        "conversation_history": state["conversation_history"] + [
            {"role": "user", "content": state["user_message"]},
            {"role": "patient", "content": response}
        ]
    }

def questioning_node(state: PatientState) -> PatientState:
    """Node 2: Answer doctor's questions"""
    profile = state["patient_profile"]
    history = format_history(state["conversation_history"])
    
    prompt = f"""You are a simulated patient. Your patient profile:
- Name: {profile["patient_name"]}
- Age: {profile["age"]}
- MedicalHistory: {profile["med_history"]}

You are answering the doctor's questions. Be concise and factual. If asked about symptoms, reveal a bit more detail than before, but still keep it moderate.

Conversation history:
{history}

Doctor: {state["user_message"]}
Patient:"""
    
    response = generate_response(prompt)
    
    # Check if treatment is mentioned
    treatment_keywords = ["prescribe", "medication", "treatment", "take", "medicine", "drug"]
    treatment_detected = any(keyword in state["user_message"].lower() for keyword in treatment_keywords)
    
    # Determine next state
    if treatment_detected:
        next_state = "treatment"
    elif state["symptom_level"] < 2 and any(word in state["user_message"].lower() for word in ["more", "detail", "tell me", "describe"]):
        next_state = "progressive"
    else:
        next_state = "questioning"
    
    return {
        "patient_response": response,
        "current_state": next_state,
        "treatment_detected": treatment_detected,
        "conversation_history": state["conversation_history"] + [
            {"role": "user", "content": state["user_message"]},
            {"role": "patient", "content": response}
        ]
    }

def progressive_revelation_node(state: PatientState) -> PatientState:
    """Node 3: Progressive symptom revelation"""
    profile = state["patient_profile"]
    history = format_history(state["conversation_history"])
    symptom_level = min(state["symptom_level"] + 1, 2)  # Increment but cap at 2
    
    prompt = f"""You are a simulated patient. Your patient profile:
- Name: {profile["patient_name"]}
- Age: {profile["age"]}
- MedicalHistory: {profile["med_history"]}

The doctor is asking for more details. Reveal MORE detailed symptoms now. Be more specific about:
- When symptoms started
- Severity and frequency
- Any triggers or patterns
- Impact on daily life

Conversation history:
{history}

Doctor: {state["user_message"]}
Patient:"""
    
    response = generate_response(prompt)
    
    # Check for treatment
    treatment_keywords = ["prescribe", "medication", "treatment", "take", "medicine", "drug"]
    treatment_detected = any(keyword in state["user_message"].lower() for keyword in treatment_keywords)
    
    next_state = "treatment" if treatment_detected else "questioning"
    
    return {
        "patient_response": response,
        "current_state": next_state,
        "symptom_level": symptom_level,
        "treatment_detected": treatment_detected,
        "conversation_history": state["conversation_history"] + [
            {"role": "user", "content": state["user_message"]},
            {"role": "patient", "content": response}
        ]
    }

def treatment_node(state: PatientState) -> PatientState:
    """Node 4: Treatment detection and acceptance"""
    profile = state["patient_profile"]
    history = format_history(state["conversation_history"])
    
    prompt = f"""You are a simulated patient. Your patient profile:
- Name: {profile["patient_name"]}
- Age: {profile["age"]}
- MedicalHistory: {profile["med_history"]}

The doctor has prescribed a treatment. Evaluate if it's reasonable for your condition:
- If reasonable: Accept it clearly by saying "I accept the treatment: [treatment name]"
- If unclear: Ask clarifying questions
- If unreasonable: Politely express concern

Conversation history:
{history}

Doctor: {state["user_message"]}
Patient:"""
    
    response = generate_response(prompt)
    
    # Check if patient accepted
    treatment_accepted = "accept" in response.lower() and "treatment" in response.lower()
    
    return {
        "patient_response": response,
        "current_state": "treatment",
        "treatment_detected": True,
        "treatment_accepted": treatment_accepted,
        "conversation_history": state["conversation_history"] + [
            {"role": "user", "content": state["user_message"]},
            {"role": "patient", "content": response}
        ]
    }

# ============================================================================
# Helper Functions
# ============================================================================

def generate_response(prompt: str) -> str:
    """Generate response using Gemini API with retry logic for rate limiting"""
    import time
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            if USE_NEW_CLIENT and client:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )
                return response.text
            else:
                model = genai.GenerativeModel(MODEL_NAME)
                response = model.generate_content(prompt)
                return response.text
        except Exception as e:
            error_msg = str(e)
            # Check if it's a rate limit error
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"⚠️  Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                    continue
                else:
                    return "I'm experiencing high demand right now. Please wait a moment and try again."
            else:
                print(f"Error generating response: {error_msg[:100]}")
                return f"I'm having trouble responding right now. Please try again. (Error: {error_msg[:100]})"
    
    return "I'm experiencing technical difficulties. Please try again in a moment."

def format_history(history: list) -> str:
    """Format conversation history for prompt"""
    if not history:
        return "No previous conversation."
    
    formatted = []
    for msg in history[-10:]:  # Last 10 messages
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        if role == "user":
            formatted.append(f"Doctor: {content}")
        elif role == "patient":
            formatted.append(f"Patient: {content}")
    
    return "\n".join(formatted) if formatted else "No previous conversation."

# ============================================================================
# LangGraph State Machine Construction
# ============================================================================

def create_patient_graph():
    """Create and compile LangGraph state machine"""
    
    # Create StateGraph
    workflow = StateGraph(PatientState)
    
    # Add nodes
    workflow.add_node("initial_greeting", initial_greeting_node)
    workflow.add_node("questioning", questioning_node)
    workflow.add_node("progressive_revelation", progressive_revelation_node)
    workflow.add_node("treatment", treatment_node)
    
    # Set entry point
    workflow.set_entry_point("initial_greeting")
    
    # Add conditional edges - route based on next_state from node output
    workflow.add_conditional_edges(
        "initial_greeting",
        lambda state: state.get("current_state", "questioning"),
        {
            "questioning": "questioning",
            "progressive": "progressive_revelation",
            "treatment": "treatment"
        }
    )
    
    workflow.add_conditional_edges(
        "questioning",
        lambda state: state.get("current_state", "questioning"),
        {
            "questioning": "questioning",
            "progressive": "progressive_revelation",
            "treatment": "treatment"
        }
    )
    
    workflow.add_conditional_edges(
        "progressive_revelation",
        lambda state: state.get("current_state", "questioning"),
        {
            "questioning": "questioning",
            "progressive": "progressive_revelation",
            "treatment": "treatment"
        }
    )
    
    # Treatment node routes back to questioning (can continue conversation after treatment)
    workflow.add_edge("treatment", "questioning")
    
    # Compile graph
    app = workflow.compile()
    return app

# ============================================================================
# Session Management with LangGraph
# ============================================================================

SESSIONS = {}  # session_id -> {"graph": graph, "profile": profile, "state": state}

def get_or_create_agent_for_session(session_id: str):
    """Create or retrieve LangGraph agent for session"""
    if session_id not in SESSIONS:
        # Create patient profile
        profile = {
            "patient_name": "Alex",
            "age": 35,
            "med_history": "no known chronic diseases",
        }
        
        # Create LangGraph instance
        graph = create_patient_graph()
        
        SESSIONS[session_id] = {
            "graph": graph,
            "profile": profile,
            "conversation_history": [],
            "current_state": "initial",
            "symptom_level": 0,
            "treatment_detected": False,
            "treatment_accepted": False
        }
        print(f"✅ Created LangGraph agent for session: {session_id}")
    
    return SESSIONS[session_id]

def handle_user_message(agent_obj: dict, session_id: str, user_message: str) -> str:
    """Handle user message using LangGraph state machine"""
    graph = agent_obj["graph"]
    profile = agent_obj["profile"]
    conversation_history = agent_obj.get("conversation_history", [])
    current_state = agent_obj.get("current_state", "initial")
    symptom_level = agent_obj.get("symptom_level", 0)
    treatment_detected = agent_obj.get("treatment_detected", False)
    treatment_accepted = agent_obj.get("treatment_accepted", False)
    
    # Create state for LangGraph
    state: PatientState = {
        "session_id": session_id,
        "user_message": user_message,
        "patient_response": "",
        "conversation_history": conversation_history,
        "current_state": current_state,
        "symptom_level": symptom_level,
        "treatment_detected": treatment_detected,
        "treatment_accepted": treatment_accepted,
        "patient_profile": profile
    }
    
    # Invoke LangGraph - but limit to single step to avoid recursion
    # We'll call the appropriate node directly based on current state
    try:
        # For first message, use initial_greeting node
        if not conversation_history:
            result = initial_greeting_node(state)
        else:
            # Route to appropriate node based on message content and current state
            if any(word in user_message.lower() for word in ["prescribe", "medication", "treatment", "medicine", "drug"]):
                result = treatment_node(state)
            elif any(word in user_message.lower() for word in ["more", "detail", "tell me", "describe"]) and symptom_level < 2:
                result = progressive_revelation_node(state)
            else:
                result = questioning_node(state)
        
        response = result["patient_response"]
        
        # Update session state
        agent_obj["conversation_history"] = result["conversation_history"]
        agent_obj["current_state"] = result.get("current_state", current_state)
        agent_obj["symptom_level"] = result.get("symptom_level", symptom_level)
        agent_obj["treatment_detected"] = result.get("treatment_detected", treatment_detected)
        agent_obj["treatment_accepted"] = result.get("treatment_accepted", treatment_accepted)
        
        return response
    except Exception as e:
        error_msg = str(e)
        print(f"Error in LangGraph execution: {error_msg}")
        import traceback
        traceback.print_exc()
        return f"I'm having trouble responding right now. Please try again. (Error: {error_msg[:100]})"

