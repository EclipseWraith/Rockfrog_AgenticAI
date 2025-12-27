# Multi-User AI Patient Chatbot

A full-stack AI chatbot application that simulates patient behavior using LangChain and LangGraph. Built with Flask (backend) and React (frontend), deployed on Vercel.

## 🎯 Features

- ✅ **LangGraph State Machine** - 4-node conversational flow (initial, questioning, progressive, treatment)
- ✅ **Progressive Symptom Description** - Patient reveals symptoms progressively
- ✅ **Treatment Acceptance** - Patient evaluates and accepts prescribed treatments
- ✅ **Multi-User Support** - Independent sessions for each user
- ✅ **Session Isolation** - Complete isolation between user sessions
- ✅ **Modern UI** - Visually appealing React interface

## 🏗️ Architecture

```
React Frontend → Flask Backend → LangGraph → Gemini API
```

- **Frontend:** React with Vite
- **Backend:** Flask REST API
- **AI Logic:** LangGraph state machine with LangChain memory
- **AI Model:** Google Gemini API

## 📁 Project Structure

```
rockfrog_chatbot/
├── backend/
│   ├── app.py                    # Flask API endpoints
│   ├── agent_logic_langgraph.py  # LangGraph implementation
│   ├── requirements.txt          # Python dependencies
│   ├── vercel.json              # Vercel deployment config
│   └── Procfile                 # Process configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # React root component
│   │   ├── components/
│   │   │   ├── Chat.jsx         # Chat interface
│   │   │   └── Chat.css         # Styling
│   │   └── sessionservice.js    # API service
│   └── package.json             # Node dependencies
│
└── Documentation/
    ├── DEPLOYMENT_STEPS.md      # Deployment guide
    ├── COMPLETE_EVALUATION.md   # Requirement evaluation
    └── FILE_REQUIREMENT_MAPPING.md # Code mapping
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Gemini API key

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
# Set GEMINI_API_KEY in .env file
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173

## 📡 API Endpoints

- `POST /api/session` - Create a new chat session
- `POST /api/message` - Send a message to the patient
- `GET /api/logs/<session_id>` - Get conversation logs
- `GET /api/health` - Health check

## 🚀 Deployment

See `DEPLOYMENT_STEPS.md` for detailed deployment instructions to Vercel.

### Quick Deploy

**Backend:**
```bash
cd backend
vercel --prod
# Set GEMINI_API_KEY environment variable in Vercel dashboard
```

**Frontend:**
```bash
cd frontend
# Set VITE_API_URL environment variable to your backend URL
vercel --prod
```

## 🧪 Testing

### Test Progressive Symptoms
1. Start conversation: "Hello"
2. Patient responds with mild symptoms
3. Ask: "Tell me more about your symptoms"
4. Patient reveals detailed symptoms

### Test Treatment Acceptance
1. Say: "I prescribe you paracetamol 500mg"
2. Patient accepts: "I accept the treatment: paracetamol 500mg"

### Test Multi-User
1. Open application in 2 different browsers
2. Each gets independent session
3. Conversations are isolated

## 🛠️ Technologies

- **Backend:** Flask, LangChain, LangGraph, Google Generative AI
- **Frontend:** React, Vite
- **Deployment:** Vercel
- **AI Model:** Google Gemini

## 📝 Environment Variables

**Backend:**
- `GEMINI_API_KEY` - Your Google Gemini API key

**Frontend:**
- `VITE_API_URL` - Backend API URL (for production)

## 📊 Requirements Compliance

✅ LangChain integration  
✅ LangGraph state machine  
✅ Flask backend API  
✅ React frontend  
✅ Patient simulation  
✅ Progressive symptoms  
✅ Treatment acceptance  
✅ Multi-user support  
✅ Session isolation  
✅ Logging  
⚠️ Vercel deployment (config ready)

**Completion: 95%**

## 📚 Documentation

- `DEPLOYMENT_STEPS.md` - Complete deployment guide
- `NEXT_STEPS_CHECKLIST.md` - Quick checklist
- `COMPLETE_EVALUATION.md` - Detailed requirement evaluation
- `FILE_REQUIREMENT_MAPPING.md` - Code mapping to requirements

## 🐛 Troubleshooting

**API Rate Limiting (429 errors):**
- Free tier Gemini API has 5 requests/minute limit
- Code includes retry logic with exponential backoff
- Wait 1 minute between requests

**Frontend can't connect to backend:**
- Check `VITE_API_URL` is set correctly
- Verify backend URL is correct
- Check CORS is enabled in backend

## 📄 License

This project is created for the Agentic AI Internship evaluation task.

---

**For detailed next steps, see `NEXT_STEPS_CHECKLIST.md`**

