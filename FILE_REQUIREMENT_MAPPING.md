# File-to-Requirement Mapping
## Agentic AI Internship: Evaluation Task

**This document maps each requirement from the task description to the specific files and code sections that implement it.**

---

## 📋 Task Requirements Breakdown

Based on the task description, here are the core requirements:

1. **Multi-user AI chatbot** using LangChain and LangGraph
2. **Simulates patient behavior** (interacts naturally, describes symptoms progressively, accepts treatments)
3. **Flask backend API** that communicates with LangChain/LangGraph
4. **React/JavaScript frontend** (visually appealing interface)
5. **Deployed on Vercel**
6. **Multi-user capability** with independent sessions
7. **Session isolation** for each user
8. **Minimal logging** (without sensitive data)

---

## 🗂️ Complete File Mapping

### Requirement 1: Multi-User AI Chatbot

**Required:** Multi-user AI chatbot application

**Implementation Files:**
- `backend/app.py` (Lines 16-17, 19-29)
  ```python
  AGENTS = {}     # session_id -> agent object
  LOGS = {}       # session_id -> list of messages
  
  @app.route("/api/session", methods=["POST"])
  def create_session():
      session_id = str(uuid.uuid4())
      agent = get_or_create_agent_for_session(session_id)
      AGENTS[session_id] = agent
  ```
- `backend/agent_logic_langgraph.py` (Lines 393-419)
  ```python
  SESSIONS = {}  # session_id -> agent data
  
  def get_or_create_agent_for_session(session_id: str):
      # Creates unique agent per session
  ```
- `frontend/src/components/Chat.jsx` (Lines 15-29)
  ```javascript
  useEffect(() => {
    const sid = await createSession();
    setSessionId(sid);
  }, []);
  ```

---

### Requirement 2: LangChain Integration

**Required:** "Use LangChain and LangGraph for chatbot flow, state management, etc."

**Implementation Files:**
- `backend/requirements.txt` (Line 5)
  ```
  langchain==0.1.0
  ```
- `backend/agent_logic_langgraph.py` (Line 4)
  ```python
  from langchain.memory import ConversationBufferMemory
  ```
- `backend/agent_logic_langgraph.py` (Lines 110, 150, 190, 230)
  - Uses LangChain memory for conversation history management

---

### Requirement 3: LangGraph State Management

**Required:** "Use LangChain and LangGraph for chatbot flow, state management, etc."

**Implementation Files:**
- `backend/requirements.txt` (Line 13)
  ```
  langgraph==0.0.20
  ```
- `backend/agent_logic_langgraph.py` (Line 7)
  ```python
  from langgraph.graph import StateGraph, END
  ```
- `backend/agent_logic_langgraph.py` (Lines 95-105) - **State Schema**
  ```python
  class PatientState(TypedDict):
      session_id: str
      user_message: str
      patient_response: str
      conversation_history: Annotated[list, ...]
      current_state: Literal["initial", "questioning", "progressive", "treatment"]
      symptom_level: int
      treatment_detected: bool
      treatment_accepted: bool
      patient_profile: dict
  ```
- `backend/agent_logic_langgraph.py` (Lines 111-256) - **Nodes**
  - Line 111-135: `initial_greeting_node`
  - Line 137-177: `questioning_node`
  - Line 179-219: `progressive_revelation_node`
  - Line 221-256: `treatment_node`
- `backend/agent_logic_langgraph.py` (Lines 329-387) - **StateGraph Creation**
  ```python
  def create_patient_graph():
      workflow = StateGraph(PatientState)
      workflow.add_node("initial_greeting", initial_greeting_node)
      workflow.add_node("questioning", questioning_node)
      workflow.add_node("progressive_revelation", progressive_revelation_node)
      workflow.add_node("treatment", treatment_node)
      workflow.set_entry_point("initial_greeting")
      # ... conditional edges ...
      app = workflow.compile()
      return app
  ```
- `backend/agent_logic_langgraph.py` (Lines 421-491) - **Graph Invocation**
  ```python
  def handle_user_message(agent_obj: dict, session_id: str, user_message: str):
      # Invokes LangGraph nodes based on state
  ```

---

### Requirement 4: Patient Behavior Simulation

**Required:** "Simulates patient behavior. The chatbot must interact naturally with users, describe symptoms, and accept prescribed treatments."

**Implementation Files:**
- `backend/agent_logic_langgraph.py` (Lines 112-123) - **Patient Profile**
  ```python
  prompt = f"""You are a simulated patient. Your patient profile:
  - Name: {profile["patient_name"]}
  - Age: {profile["age"]}
  - MedicalHistory: {profile["med_history"]}
  """
  ```
- `backend/agent_logic_langgraph.py` (Lines 111-135) - **Initial Greeting**
  - Patient introduces with mild symptoms
- `backend/agent_logic_langgraph.py` (Lines 137-177) - **Natural Interaction**
  - Patient answers questions naturally
- `backend/agent_logic_langgraph.py` (Lines 179-219) - **Progressive Symptom Description**
  - Patient reveals more symptoms when asked
- `backend/agent_logic_langgraph.py` (Lines 221-256) - **Treatment Acceptance**
  - Patient evaluates and accepts/rejects treatments

---

### Requirement 5: Progressive Symptom Description

**Required:** "Describe symptoms progressively"

**Implementation Files:**
- `backend/agent_logic_langgraph.py` (Line 118) - **Initial State (Mild)**
  ```python
  "You are starting a conversation with a doctor. Introduce yourself briefly and mention only MILD symptoms."
  ```
- `backend/agent_logic_langgraph.py` (Line 193) - **Symptom Level Tracking**
  ```python
  symptom_level = min(state["symptom_level"] + 1, 2)  # Increment but cap at 2
  ```
- `backend/agent_logic_langgraph.py` (Lines 197-202) - **Progressive Details**
  ```python
  "Reveal MORE detailed symptoms now. Be more specific about:
  - When symptoms started
  - Severity and frequency
  - Any triggers or patterns
  - Impact on daily life"
  ```

---

### Requirement 6: Treatment Acceptance

**Required:** "Accept prescribed treatments from the user"

**Implementation Files:**
- `backend/agent_logic_langgraph.py` (Lines 157-159) - **Treatment Detection**
  ```python
  treatment_keywords = ["prescribe", "medication", "treatment", "take", "medicine", "drug"]
  treatment_detected = any(keyword in state["user_message"].lower() for keyword in treatment_keywords)
  ```
- `backend/agent_logic_langgraph.py` (Lines 221-256) - **Treatment Node**
  ```python
  prompt = """...Evaluate if it's reasonable for your condition:
  - If reasonable: Accept it clearly by saying "I accept the treatment: ..."
  - If unclear: Ask clarifying questions
  - If unreasonable: Politely express concern"""
  ```
- `backend/agent_logic_langgraph.py` (Line 248) - **Acceptance Detection**
  ```python
  treatment_accepted = "accept" in response.lower() and "treatment" in response.lower()
  ```

---

### Requirement 7: Flask Backend API

**Required:** "Backend: A Flask-based API that communicates with the LangChain/LangGraph logic"

**Implementation Files:**
- `backend/requirements.txt` (Line 1)
  ```
  Flask==2.3.2
  ```
- `backend/app.py` (Line 11)
  ```python
  app = Flask(__name__)
  CORS(app)
  ```
- `backend/app.py` (Line 7) - **LangGraph Integration**
  ```python
  from agent_logic_langgraph import get_or_create_agent_for_session, handle_user_message
  ```
- `backend/app.py` (Lines 19-29) - **POST /api/session**
  ```python
  @app.route("/api/session", methods=["POST"])
  def create_session():
      session_id = str(uuid.uuid4())
      agent = get_or_create_agent_for_session(session_id)
      return jsonify({"session_id": session_id}), 201
  ```
- `backend/app.py` (Lines 31-60) - **POST /api/message**
  ```python
  @app.route("/api/message", methods=["POST"])
  def message():
      reply = handle_user_message(AGENTS[session_id], session_id, text)
      return jsonify({"reply": reply})
  ```
- `backend/app.py` (Lines 62-68) - **GET /api/logs/<session_id>**
  ```python
  @app.route("/api/logs/<session_id>", methods=["GET"])
  def logs(session_id):
      return jsonify(LOGS.get(session_id, []))
  ```
- `backend/app.py` (Lines 70-72) - **GET /api/health**
  ```python
  @app.route("/api/health", methods=["GET"])
  def health():
      return jsonify({"status": "healthy", "service": "patient-chatbot-api"}), 200
  ```

---

### Requirement 8: React Frontend

**Required:** "Frontend: A visually appealing interface developed in React.js or HTML/JavaScript"

**Implementation Files:**
- `frontend/package.json` (Lines 13-14)
  ```json
  "react": "^19.2.0",
  "react-dom": "^19.2.0"
  ```
- `frontend/src/App.jsx` (Entire file)
  ```javascript
  import Chat from "./components/Chat";
  export default function App() {
    return <Chat />;
  }
  ```
- `frontend/src/components/Chat.jsx` (Lines 1-167) - **Main Chat Component**
  - Line 6-11: State management (sessionId, messages, text, loading, error)
  - Line 15-29: Session creation on mount
  - Line 31-70: Message sending handler
  - Line 72-90: Message rendering
  - Line 92-167: JSX with UI components
- `frontend/src/components/Chat.css` (Lines 1-361) - **Visual Styling**
  - Modern gradient backgrounds
  - Message bubbles (user/patient styles)
  - Responsive design
  - Loading states
  - Animations
- `frontend/src/sessionservice.js` (Entire file) - **API Communication**
  ```javascript
  export async function createSession() {
    const response = await fetch("/api/session", { method: "POST" });
    return session_id;
  }
  
  export async function sendMessage(sessionId, message) {
    const response = await fetch("/api/message", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId, message: message })
    });
    return reply;
  }
  ```
- `frontend/vite.config.js` (Lines 1-9) - **Development Proxy**
  ```javascript
  server: {
    proxy: {
      "/api": "http://localhost:8000"
    }
  }
  ```

---

### Requirement 9: Multi-User Capability

**Required:** "Multi-user Capability: Ensure that multiple users can interact with independent chatbot sessions simultaneously"

**Implementation Files:**
- `backend/app.py` (Lines 16-17)
  ```python
  AGENTS = {}     # session_id -> agent object
  LOGS = {}       # session_id -> list of messages
  ```
- `backend/app.py` (Lines 22-25)
  ```python
  session_id = str(uuid.uuid4())  # Unique ID per session
  agent = get_or_create_agent_for_session(session_id)
  AGENTS[session_id] = agent
  ```
- `backend/agent_logic_langgraph.py` (Lines 393-419)
  ```python
  SESSIONS = {}  # session_id -> agent data
  
  def get_or_create_agent_for_session(session_id: str):
      if session_id not in SESSIONS:
          # Create unique agent per session
          graph = create_patient_graph()
          SESSIONS[session_id] = {...}
  ```
- `frontend/src/components/Chat.jsx` (Lines 15-29)
  - Each browser instance creates a new session

---

### Requirement 10: Session Isolation

**Required:** "Maintain session isolation for each user to ensure independent interactions"

**Implementation Files:**
- `backend/agent_logic_langgraph.py` (Lines 393-419)
  ```python
  SESSIONS = {}  # Dictionary keyed by session_id
  
  def get_or_create_agent_for_session(session_id: str):
      if session_id not in SESSIONS:
          profile = {...}  # Unique profile per session
          graph = create_patient_graph()  # Unique graph instance
          SESSIONS[session_id] = {
              "graph": graph,
              "profile": profile,
              "conversation_history": [],  # Isolated history
              "current_state": "initial",
              "symptom_level": 0,
              ...
          }
  ```
- `backend/app.py` (Lines 47-50)
  ```python
  if session_id not in AGENTS:
      # Create lazily if missing
      AGENTS[session_id] = get_or_create_agent_for_session(session_id)
      LOGS[session_id] = []  # Separate logs per session
  ```
- `backend/app.py` (Lines 52-56)
  ```python
  # Each session has isolated logs
  LOGS[session_id].append({"role": "user", "text": text})
  LOGS[session_id].append({"role": "agent", "text": reply})
  ```

---

### Requirement 11: Logging

**Required:** "Integrate minimal logging for tracking conversations (without storing sensitive data)"

**Implementation Files:**
- `backend/app.py` (Line 17)
  ```python
  LOGS = {}  # session_id -> list of {"role","text"}
  ```
- `backend/app.py` (Lines 52-56) - **Logging Messages**
  ```python
  # Only stores role and text, no sensitive data
  LOGS[session_id].append({"role": "user", "text": text})
  LOGS[session_id].append({"role": "agent", "text": reply})
  ```
- `backend/app.py` (Lines 62-68) - **Log Retrieval Endpoint**
  ```python
  @app.route("/api/logs/<session_id>", methods=["GET"])
  def logs(session_id):
      return jsonify(LOGS.get(session_id, []))
  ```
- **Note:** Logs only contain `role` and `text` - no API keys, user IDs, or other sensitive data

---

### Requirement 12: Vercel Deployment

**Required:** "Hosting: The entire app should be deployed on Vercel"

**Implementation Files:**
- `backend/vercel.json` (Lines 1-9) - **Backend Deployment Config**
  ```json
  {
    "version": 3,
    "builds": [{ "src": "app.py", "use": "@vercel/python" }],
    "routes": [{ "src": "/api/(.*)", "dest": "/app.py" }]
  }
  ```
- `backend/Procfile` - **Process Configuration**
  ```
  web: gunicorn app:app
  ```
- `backend/requirements.txt` (Line 21)
  ```
  gunicorn==20.1.0
  ```
- **Note:** Configuration ready, but not yet deployed to Vercel

---

## 📊 Quick Reference Table

| Requirement | Primary File | Key Lines | Status |
|------------|--------------|-----------|--------|
| **LangChain** | `backend/agent_logic_langgraph.py` | 4 | ✅ |
| **LangGraph State** | `backend/agent_logic_langgraph.py` | 7, 95-105, 329-387 | ✅ |
| **LangGraph Nodes** | `backend/agent_logic_langgraph.py` | 111-256 | ✅ |
| **Flask API** | `backend/app.py` | 11, 19-72 | ✅ |
| **React Frontend** | `frontend/src/components/Chat.jsx` | 1-167 | ✅ |
| **Patient Sim** | `backend/agent_logic_langgraph.py` | 112-123, 111-256 | ✅ |
| **Progressive Symptoms** | `backend/agent_logic_langgraph.py` | 111-135, 179-219 | ✅ |
| **Treatment Acceptance** | `backend/agent_logic_langgraph.py` | 221-256 | ✅ |
| **Multi-User** | `backend/app.py` | 16-17, 22-25 | ✅ |
| **Session Isolation** | `backend/agent_logic_langgraph.py` | 393-419 | ✅ |
| **Logging** | `backend/app.py` | 17, 52-56, 62-68 | ✅ |
| **Vercel Config** | `backend/vercel.json` | 1-9 | ⚠️ |

---

## 🎯 Additional Implementation Files

### Supporting Files (Not Direct Requirements):

1. **Environment Configuration:**
   - `backend/.env` - Stores `GEMINI_API_KEY`

2. **API Key Management:**
   - `backend/agent_logic_langgraph.py` (Lines 17-29) - API key loading

3. **Model Selection:**
   - `backend/agent_logic_langgraph.py` (Lines 49-89) - Dynamic model selection

4. **Error Handling:**
   - `backend/agent_logic_langgraph.py` (Lines 262-289) - Rate limiting retry logic

5. **Styling:**
   - `frontend/src/components/Chat.css` - Visual design (361 lines)
   - `frontend/src/index.css` - Global styles
   - `frontend/src/App.css` - App container styles

6. **Frontend Build:**
   - `frontend/vite.config.js` - Vite configuration
   - `frontend/index.html` - HTML entry point
   - `frontend/package.json` - Dependencies

---

## 📁 Complete File Structure

```
rockfrog_chatbot/
├── backend/
│   ├── app.py                          # Flask API (ALL endpoints)
│   ├── agent_logic_langgraph.py       # LangGraph implementation (ALL nodes, state, graph)
│   ├── agent_logic_alternative.py     # Legacy (not used)
│   ├── agent_logic.py                 # Legacy (not used)
│   ├── requirements.txt                # Dependencies (LangChain, LangGraph, Flask)
│   ├── vercel.json                    # Vercel deployment config
│   ├── Procfile                       # Process config for deployment
│   └── .env                           # Environment variables (API key)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # React root component
│   │   ├── components/
│   │   │   ├── Chat.jsx               # Main chat UI component
│   │   │   └── Chat.css               # Chat styling (visually appealing)
│   │   ├── sessionservice.js          # API service (createSession, sendMessage)
│   │   ├── index.css                  # Global styles
│   │   └── App.css                    # App styles
│   ├── index.html                     # HTML entry point
│   ├── package.json                   # React dependencies
│   └── vite.config.js                 # Dev proxy config
│
└── Documentation/
    ├── FILE_REQUIREMENT_MAPPING.md    # This file
    ├── COMPLETE_EVALUATION.md         # Full evaluation
    └── PROJECT_STATUS_REPORT.md       # Status report
```

---

## 🔍 How to Verify Each Requirement

### Test LangGraph:
```bash
# Check if LangGraph is used
grep -n "StateGraph\|add_node" backend/agent_logic_langgraph.py
# Should show lines: 333, 336-339
```

### Test Flask API:
```bash
curl -X POST http://localhost:8000/api/session
# Should return: {"session_id": "uuid"}
```

### Test Multi-User:
```bash
# Open 2 browser tabs, each creates separate session
# Check backend/app.py line 16-17 for AGENTS dictionary
```

### Test Progressive Symptoms:
```bash
# In chat: "Hello" → Mild symptoms
# Then: "Tell me more" → Detailed symptoms
# Check backend/agent_logic_langgraph.py line 193 for symptom_level increment
```

### Test Treatment Acceptance:
```bash
# In chat: "I prescribe paracetamol"
# Patient should respond: "I accept the treatment: ..."
# Check backend/agent_logic_langgraph.py line 248 for acceptance detection
```

---

**Summary:** Every requirement from the task description is implemented in specific files with exact line numbers provided above.

