# Agentic AI Internship: Multi-User Patient Chatbot

A sophisticated multi-user AI chatbot application that simulates patient behavior for medical consultation training. Built as part of the Agentic AI Internship evaluation task, this application enables doctors to interact with an AI-powered patient that progressively reveals symptoms and evaluates treatment recommendations.

## 🎯 Project Overview

This project implements a full-stack AI chatbot system where:
- **AI Patient**: Simulates a patient with realistic behavior patterns
- **Doctors (Users)**: Interact with the patient through a web interface
- **Multi-User Support**: Multiple doctors can interact simultaneously with independent sessions
- **Progressive Interaction**: Patient reveals symptoms progressively based on conversation flow
- **Treatment Evaluation**: Patient evaluates and accepts/rejects prescribed treatments

## ✨ Key Features

- 🤖 **LangGraph State Machine**: 4-node conversational flow (initial → questioning → progressive → treatment)
- 📈 **Progressive Symptom Description**: Patient reveals symptoms gradually as conversation deepens
- 💊 **Treatment Acceptance Logic**: Patient intelligently evaluates prescribed treatments
- 👥 **Multi-User Capability**: Independent sessions for each user with complete isolation
- 🎨 **Modern UI**: Clean, responsive React interface with real-time chat
- 🔒 **Session Isolation**: Complete data isolation between different user sessions
- 🚀 **Production Ready**: Deployed on Vercel with proper error handling

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  (User Interface)
│   (Vite + JSX)  │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  Flask Backend  │  (REST API)
│   (Python 3.11) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LangGraph     │  (State Management)
│  State Machine  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Google Gemini  │  (AI Model)
│      API        │
└─────────────────┘
```

### Technology Stack

**Frontend:**
- React 19.2.0
- Vite 7.2.4
- Modern JavaScript (ES6+)
- CSS3 with responsive design

**Backend:**
- Flask 2.3.2 (Python web framework)
- LangChain 1.x (AI orchestration)
- LangGraph 1.x (State machine management)
- Google Generative AI SDK (Gemini API)
- Flask-CORS (Cross-origin support)

**Deployment:**
- Vercel (Serverless hosting)
- Gunicorn (WSGI server)

## 📁 Project Structure

```
rockfrog_chatbot/
├── backend/
│   ├── app.py                    # Flask API server & endpoints
│   ├── agent_logic_langgraph.py  # LangGraph state machine implementation
│   ├── requirements.txt          # Python dependencies
│   ├── vercel.json              # Vercel deployment configuration
│   └── Procfile                 # Process configuration for Vercel
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React application component
│   │   ├── main.jsx             # React entry point
│   │   ├── components/
│   │   │   ├── Chat.jsx         # Chat interface component
│   │   │   └── Chat.css         # Chat styling
│   │   └── sessionservice.js    # API service layer
│   ├── package.json             # Node.js dependencies
│   └── vite.config.js           # Vite configuration
│
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 18+** (for frontend)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

### Local Development Setup

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo GEMINI_API_KEY=your_api_key_here > .env

# Run the Flask server
python app.py
```

The backend will start on `http://localhost:8000`

#### 2. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:5173`

### Testing the Application

1. **Open the application** in your browser at `http://localhost:5173`
2. **Start a conversation** by sending "Hello" or "Hi"
3. **Observe progressive symptoms**: Ask follow-up questions to see the patient reveal more details
4. **Prescribe treatment**: Try "I prescribe you [medication name]"
5. **Test multi-user**: Open the app in multiple browser windows/tabs to see independent sessions

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/session` | Create a new chat session (returns `session_id`) |
| `POST` | `/api/message` | Send a message to the patient (requires `session_id` and `message`) |
| `GET` | `/api/logs/<session_id>` | Retrieve conversation logs for a session |
| `GET` | `/api/health` | Health check endpoint |

### Example API Usage

**Create Session:**
```bash
curl -X POST http://localhost:8000/api/session
# Response: {"session_id": "uuid-here"}
```

**Send Message:**
```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -d '{"session_id": "uuid-here", "message": "Hello, how are you feeling?"}'
# Response: {"reply": "Patient's response..."}
```

## 🚀 Deployment on Vercel

### Backend Deployment

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Deploy backend**:
   ```bash
   cd backend
   vercel --prod
   ```

3. **Set environment variable** in Vercel dashboard:
   - Go to your project settings → Environment Variables
   - Add `GEMINI_API_KEY` with your API key value

### Frontend Deployment

1. **Set backend URL**:
   - Create `.env.production` file in frontend directory:
     ```
     VITE_API_URL=https://your-backend-url.vercel.app
     ```

2. **Deploy frontend**:
   ```bash
   cd frontend
   vercel --prod
   ```

3. **Update environment variable** in Vercel dashboard:
   - Add `VITE_API_URL` pointing to your deployed backend URL

## 🧠 How It Works

### LangGraph State Machine

The chatbot uses a 4-state LangGraph implementation:

1. **Initial State**: Patient greets and introduces basic symptoms
2. **Questioning State**: Patient responds to doctor's questions
3. **Progressive State**: Patient reveals more detailed symptoms as conversation progresses
4. **Treatment State**: Patient evaluates and responds to treatment prescriptions

### State Transitions

- Conversation flow is managed by LangGraph's state machine
- Each state has specific behavior patterns
- Transitions occur based on conversation context and keywords
- Memory is maintained per session using LangChain's memory system

### Multi-User Support

- Each user gets a unique `session_id` when creating a session
- Sessions are completely isolated in memory
- No data leakage between different users
- Each session maintains its own conversation history

## 🛠️ Technologies & Design Choices

### Why LangGraph?
- **State Management**: Provides explicit state machine for complex conversational flows
- **Modularity**: Easy to add/remove states and transitions
- **Debugging**: Clear visualization of conversation flow
- **Scalability**: Can handle complex multi-step interactions

### Why Flask?
- **Lightweight**: Minimal overhead for API endpoints
- **Flexibility**: Easy to integrate with LangChain/LangGraph
- **Vercel Support**: Native support for Python/Flask deployments
- **Simplicity**: Straightforward REST API implementation

### Why React + Vite?
- **Modern Development**: Fast hot module replacement
- **Performance**: Optimized production builds
- **User Experience**: Smooth, responsive interface
- **Maintainability**: Component-based architecture

## 📊 Requirements Compliance

✅ **LangChain Integration** - Full LangChain integration for AI orchestration  
✅ **LangGraph State Machine** - 4-node state machine for conversation flow  
✅ **Flask Backend API** - RESTful API with proper error handling  
✅ **React Frontend** - Modern, responsive user interface  
✅ **Patient Simulation** - Realistic patient behavior patterns  
✅ **Progressive Symptoms** - Symptoms revealed based on conversation depth  
✅ **Treatment Acceptance** - Patient evaluates and accepts treatments  
✅ **Multi-User Support** - Independent sessions for each user  
✅ **Session Isolation** - Complete data isolation between sessions  
✅ **Vercel Deployment** - Both frontend and backend deployed on Vercel  
✅ **Minimal Logging** - Essential logging without verbosity  

## 🐛 Troubleshooting

### Common Issues

**API Rate Limiting (429 errors):**
- Google Gemini free tier has rate limits (typically 5 requests/minute)
- The code includes retry logic with exponential backoff
- Wait 1 minute between requests if you hit the limit
- Consider upgrading to a paid tier for production use

**Frontend can't connect to backend:**
- Verify `VITE_API_URL` environment variable is set correctly
- Check that backend is running and accessible
- Ensure CORS is enabled (already configured in `app.py`)
- Check browser console for specific error messages

**Session not persisting:**
- Sessions are stored in-memory (for development)
- Each server restart clears all sessions
- For production, consider using Redis or a database

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.11+
- Check that virtual environment is activated

## 📝 Environment Variables

### Backend
- `GEMINI_API_KEY` (Required) - Your Google Gemini API key
- `PORT` (Optional) - Server port (default: 8000)

### Frontend
- `VITE_API_URL` (Required for production) - Backend API URL
  - Development: `http://localhost:8000`
  - Production: Your deployed backend URL

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google Gemini API](https://ai.google.dev/)
- [Vercel Deployment Guide](https://vercel.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🎓 Project Deliverables

This project was developed as part of the Agentic AI Internship evaluation task and includes:

- ✅ **Working Application**: Fully functional chatbot deployed on Vercel
- ✅ **Complete Source Code**: All code uploaded to repository
- ✅ **Architecture Documentation**: This README covers architecture and design choices
- ✅ **Technology Stack**: LangChain, LangGraph, Flask, React, Vercel
- ✅ **Multi-User Demonstration**: Supports multiple concurrent users

## 📄 License

This project is created for the Agentic AI Internship evaluation task.

---

**Built with ❤️ using LangChain, LangGraph, Flask, and React**
