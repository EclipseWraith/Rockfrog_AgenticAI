# Rockfrog — Multi-User Patient Chatbot

A professional, production-ready README for the Rockfrog project — a multi-user AI chatbot that simulates patient behaviour for medical consultation training and assessment.

---

## Project Overview

Rockfrog is a full‑stack AI chatbot system that simulates patient behavior to support clinical training and evaluation. Multiple clinicians can interact with independent AI patient sessions simultaneously. The patient reveals symptoms progressively and evaluates prescribed treatments.

Key goals:

* Provide realistic, progressive patient simulations for clinical training
* Support isolated multi-user sessions with persistent conversation state
* Allow flexible customization of patient profiles and treatment-evaluation logic

---

## Features

* **AI Patient Simulation** — realistic patient persona with conditional behaviour and progressive symptom disclosure
* **Multi-User Sessions** — isolated session per user with unique `session_id`
* **State Machine** — LangGraph-driven state management (initial → questioning → progressive → treatment)
* **Treatment Evaluation** — patient evaluates prescribed treatments and responds appropriately
* **Web UI** — modern, responsive React frontend for real-time chat
* **Extensible Backend** — Flask API with modular agent logic for easy extension and testing
* **Deployment Ready** — configuration for Vercel / serverless deployment with production recommendations

---

## Architecture

```
┌─────────────────┐
│  React Frontend │  (User interface)
└────────┬────────┘
         │ HTTP/REST / WebSocket
         ▼
┌─────────────────┐
│  Flask Backend  │  (API + session manager)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LangGraph     │  (State machine)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Provider   │  (e.g. Google Gemini, OpenAI)
└─────────────────┘
```

---

## Technology Stack

| Layer         | Technology             | Notes                                                         |
| ------------- | ---------------------- | ------------------------------------------------------------- |
| Frontend      | React (Vite)           | Component-based, fast HMR for development                     |
| Backend       | Flask                  | Lightweight REST API and integration point for LangGraph      |
| Orchestration | LangChain, LangGraph   | Session memory and state machine orchestration                |
| Model         | LLM API (configurable) | Google Gemini or other model APIs; pluggable provider pattern |
| Deployment    | Vercel / Gunicorn      | Serverless frontend and backend options                       |
| Optional Prod | Redis, PostgreSQL      | Session persistence, queuing, and long-term logs              |

---

## Project Structure

```
rockfrog_chatbot/
├── backend/
│   ├── app.py                    # Flask API server & endpoints
│   ├── agent_logic_langgraph.py  # LangGraph state machine implementation
│   ├── requirements.txt          # Python dependencies
│   ├── vercel.json               # Vercel deployment configuration
│   └── Procfile                  # Process configuration for deployment
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
└── README.md                    # Project documentation
```

---

## API Reference

| Method |                 Endpoint | Description                                                                      |
| ------ | -----------------------: | -------------------------------------------------------------------------------- |
| POST   |           `/api/session` | Create a new chat session. Returns `session_id`.                                 |
| POST   |           `/api/message` | Send a message to the patient. Body: `{ session_id, message }`. Returns `reply`. |
| GET    | `/api/logs/<session_id>` | Retrieve conversation logs for a session.                                        |
| GET    |            `/api/health` | Health check for backend services.                                               |

### Example

**Create Session**

```bash
curl -X POST http://localhost:8000/api/session
# Response: {"session_id": "uuid-here"}
```

**Send Message**

```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -d '{"session_id": "uuid-here", "message": "Hello, how are you feeling?"}'
# Response: {"reply": "Patient's response..."}
```

---

## Local Development — Quick Start

### Prerequisites

* Python 3.11+
* Node.js 18+
* LLM API key (configured as environment variable)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# set environment variable
export GEMINI_API_KEY=your_api_key_here   # Linux / Mac
# or set in .env for local use
python app.py
```

Service available at `http://localhost:8000` (default port). Adjust `PORT` env var as needed.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at `http://localhost:5173`.

---

## Deployment

### Vercel (recommended for frontend; backend can be serverless or containerized)

1. Install Vercel CLI: `npm install -g vercel`
2. Backend: `cd backend && vercel --prod`
3. Frontend: set `VITE_API_URL=https://<your-backend-url>` in project settings and deploy: `cd frontend && vercel --prod`
4. Add environment variables (e.g. `GEMINI_API_KEY`, `VITE_API_URL`) in the Vercel dashboard.

**Production considerations:**

* Use a persistent session store (Redis) instead of in-memory sessions.
* Use a database (Postgres) for logs and analytics if required.
* Configure centralized logging and monitoring (Sentry, Prometheus, Grafana).
* Add rate limiting and request throttling to avoid LLM provider rate limits.

---

## How It Works

### State Machine (LangGraph)

The conversational logic is implemented as a 4-node state machine:

1. **Initial** — greeting and baseline symptom introduction
2. **Questioning** — responds to clinician questions and clarifies symptoms
3. **Progressive** — reveals deeper or time-sensitive symptoms as conversation progresses
4. **Treatment** — evaluates prescribed treatments and responds (accept/refuse/ask for clarification)

Transitions are triggered by conversation context, keywords, and session history. Each session maintains separate memory to prevent leakage across users.

### Multi-User Support

* Each user session is identified by a UUID `session_id` and backed by a session store.
* By default sessions are in-memory for development; production should use Redis for persistence and horizontal scalability.

---

## Configuration & Environment Variables

**Backend**

| Name             | Required | Description                                          |
| ---------------- | -------: | ---------------------------------------------------- |
| `GEMINI_API_KEY` |      Yes | LLM API key (or credentials for chosen LLM provider) |
| `PORT`           |       No | Server port (default: 8000)                          |
| `REDIS_URL`      |       No | Optional Redis connection for session persistence    |

**Frontend**

| Name           |         Required | Description                                             |
| -------------- | ---------------: | ------------------------------------------------------- |
| `VITE_API_URL` | Yes (production) | URL of the backend API (e.g. `https://api.example.com`) |

---

## Troubleshooting & Common Issues

**429 Rate Limit from LLM provider**

* Implement exponential backoff and retry logic.
* Cache model responses where possible and batch requests when appropriate.
* Consider upgrading your LLM plan or adding request queuing.

**Frontend cannot connect**

* Verify `VITE_API_URL` and CORS settings.
* Check backend health endpoint: `/api/health`.

**Sessions reset on server restart**

* In-memory sessions will be lost. Use Redis or a database for session persistence in production.

---

## Security & Privacy

* Do not log sensitive patient data in plaintext to external logging services.
* Use TLS in production and secure any API keys in environment variables.
* Implement role-based access control (RBAC) if exposing administrative endpoints.

---

## Extensibility

* Add new LangGraph states for more complex patient flows.
* Plug in other LLM providers by implementing the provider interface in `agent_logic_langgraph.py`.
* Add user authentication and ACLs to restrict access to training materials and logs.

---

## References & Resources

* LangChain documentation — [https://python.langchain.com/](https://python.langchain.com/)
* LangGraph documentation — [https://langchain-ai.github.io/langgraph/](https://langchain-ai.github.io/langgraph/)
* Google Generative AI (or provider of choice) — configure via provider SDK docs
* Flask documentation — [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* Vercel deployment guide — [https://vercel.com/docs](https://vercel.com/docs)

---

## License

The project is provided under a permissive license. Include a `LICENSE` file in the repository root with the text of the chosen license (for example, MIT).

---

## Contact

For questions or contributions, open an issue or pull request in the repository. Include clear reproduction steps and environment details.

