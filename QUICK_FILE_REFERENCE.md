# Quick File Reference
## Which File Contains What (From Task Description)

---

## 🎯 Core Requirements → Files

### 1. **LangChain Integration**
**File:** `backend/agent_logic_langgraph.py`
- **Line 4:** `from langchain.memory import ConversationBufferMemory`
- **Line 110, 150, 190, 230:** Uses LangChain memory

---

### 2. **LangGraph State Machine**
**File:** `backend/agent_logic_langgraph.py`
- **Line 7:** `from langgraph.graph import StateGraph, END`
- **Lines 95-105:** State schema definition (`PatientState`)
- **Lines 111-256:** 4 nodes (initial_greeting, questioning, progressive_revelation, treatment)
- **Lines 329-387:** StateGraph creation with edges

---

### 3. **Flask Backend API**
**File:** `backend/app.py`
- **Line 11:** `app = Flask(__name__)`
- **Lines 19-29:** `POST /api/session` (create session)
- **Lines 31-60:** `POST /api/message` (send message)
- **Lines 62-68:** `GET /api/logs/<session_id>` (get logs)
- **Lines 70-72:** `GET /api/health` (health check)
- **Line 7:** Imports LangGraph logic

---

### 4. **React Frontend**
**Files:**
- `frontend/src/App.jsx` - Root component
- `frontend/src/components/Chat.jsx` - Main chat UI (Lines 1-167)
- `frontend/src/components/Chat.css` - Styling (361 lines)
- `frontend/src/sessionservice.js` - API calls

---

### 5. **Patient Behavior Simulation**
**File:** `backend/agent_logic_langgraph.py`
- **Lines 112-123:** Patient profile and prompt
- **Lines 111-135:** Initial greeting with mild symptoms
- **Lines 137-177:** Natural question answering
- **Lines 179-219:** Progressive symptom revelation
- **Lines 221-256:** Treatment acceptance

---

### 6. **Progressive Symptom Description**
**File:** `backend/agent_logic_langgraph.py`
- **Line 118:** Initial (mild symptoms only)
- **Line 193:** Symptom level increment
- **Lines 197-202:** Detailed symptom prompts

---

### 7. **Treatment Acceptance**
**File:** `backend/agent_logic_langgraph.py`
- **Lines 157-159:** Treatment keyword detection
- **Lines 221-256:** Treatment evaluation node
- **Line 248:** Acceptance detection

---

### 8. **Multi-User Support**
**Files:**
- `backend/app.py` (Lines 16-17, 22-25): Session dictionary
- `backend/agent_logic_langgraph.py` (Lines 393-419): Session management
- `frontend/src/components/Chat.jsx` (Lines 15-29): Session creation

---

### 9. **Session Isolation**
**File:** `backend/agent_logic_langgraph.py`
- **Lines 393-419:** `SESSIONS` dictionary with isolated data per session_id

---

### 10. **Logging**
**File:** `backend/app.py`
- **Line 17:** `LOGS = {}` dictionary
- **Lines 52-56:** Log message storage
- **Lines 62-68:** Log retrieval endpoint

---

### 11. **Vercel Deployment Config**
**File:** `backend/vercel.json`
- **Lines 1-9:** Deployment configuration

---

## 📋 File-by-File Breakdown

### `backend/app.py`
**Contains:**
- ✅ Flask application setup
- ✅ All API endpoints (4 routes)
- ✅ Session management (AGENTS, LOGS dictionaries)
- ✅ Integration with LangGraph logic

**Lines:**
- 1-13: Imports and setup
- 16-17: Session storage
- 19-29: Session creation endpoint
- 31-60: Message handling endpoint
- 62-68: Logs endpoint
- 70-72: Health check

---

### `backend/agent_logic_langgraph.py`
**Contains:**
- ✅ LangChain imports
- ✅ LangGraph StateGraph implementation
- ✅ State schema (PatientState)
- ✅ 4 nodes (all conversation logic)
- ✅ Patient simulation prompts
- ✅ Progressive symptom logic
- ✅ Treatment detection/acceptance
- ✅ Session isolation
- ✅ API rate limiting (retry logic)

**Key Sections:**
- 4: LangChain import
- 7: LangGraph import
- 95-105: State schema
- 111-135: Initial greeting node
- 137-177: Questioning node
- 179-219: Progressive revelation node
- 221-256: Treatment node
- 262-289: Rate limiting/retry logic
- 329-387: StateGraph creation
- 393-419: Session management
- 421-491: Message handling

---

### `frontend/src/components/Chat.jsx`
**Contains:**
- ✅ React chat component
- ✅ Session creation on mount
- ✅ Message sending/receiving
- ✅ UI rendering
- ✅ Error handling
- ✅ Loading states

**Lines:**
- 1-14: Imports and state
- 15-29: Session initialization
- 31-70: Message handling
- 72-167: UI rendering

---

### `frontend/src/components/Chat.css`
**Contains:**
- ✅ Visually appealing design
- ✅ Gradient backgrounds
- ✅ Message bubbles
- ✅ Responsive layout
- ✅ Animations
- ✅ Black text for patient messages
- ✅ Black text for input field

**361 lines of styling**

---

### `frontend/src/sessionservice.js`
**Contains:**
- ✅ API service functions
- ✅ `createSession()` - creates new session
- ✅ `sendMessage()` - sends message to backend

---

### `backend/requirements.txt`
**Contains:**
- ✅ LangChain dependency (line 5)
- ✅ LangGraph dependency (line 13)
- ✅ Flask dependency (line 1)
- ✅ Google Generative AI (lines 8-10)
- ✅ All other dependencies

---

### `backend/vercel.json`
**Contains:**
- ✅ Vercel deployment configuration
- ✅ Python build settings
- ✅ API route mapping

---

## 🔍 Verification Commands

**Check LangGraph:**
```bash
grep -n "StateGraph\|add_node" backend/agent_logic_langgraph.py
```

**Check Flask Endpoints:**
```bash
grep -n "@app.route" backend/app.py
```

**Check React Components:**
```bash
ls frontend/src/components/
```

**Check Dependencies:**
```bash
cat backend/requirements.txt
cat frontend/package.json
```

---

**Summary:** Every requirement from the task description maps to specific files with exact line numbers in `FILE_REQUIREMENT_MAPPING.md`

