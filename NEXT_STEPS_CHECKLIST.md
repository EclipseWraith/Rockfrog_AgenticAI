# Next Steps Checklist
## Quick Reference Guide

---

## ✅ Immediate Next Steps (In Order)

### 1. Final Local Testing
- [ ] Start backend: `cd backend && python app.py`
- [ ] Test backend API endpoints (health, session, message)
- [ ] Start frontend: `cd frontend && npm run dev`
- [ ] Test chat functionality in browser
- [ ] Verify multi-user (open 2 browser tabs)

---

### 2. Deploy Backend to Vercel
- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Login: `vercel login`
- [ ] Navigate: `cd backend`
- [ ] Initialize: `vercel` (follow prompts)
- [ ] Set environment variable: `GEMINI_API_KEY` (via dashboard or CLI)
- [ ] Deploy: `vercel --prod`
- [ ] **Note your backend URL:** `https://your-backend.vercel.app`

---

### 3. Update Frontend Configuration
- [ ] Open `frontend/src/sessionservice.js`
- [ ] Update API_BASE URL to your Vercel backend URL
- [ ] OR: Create `frontend/.env` with `VITE_API_URL=https://your-backend.vercel.app`
- [ ] Update `sessionservice.js` to use `import.meta.env.VITE_API_URL`

---

### 4. Deploy Frontend to Vercel
- [ ] Navigate: `cd frontend`
- [ ] Initialize: `vercel` (follow prompts)
- [ ] Set environment variable (if using .env): `VITE_API_URL`
- [ ] Deploy: `vercel --prod`
- [ ] **Note your frontend URL:** `https://your-frontend.vercel.app`

---

### 5. Test Deployed Application
- [ ] Test backend: `curl https://your-backend.vercel.app/api/health`
- [ ] Open frontend URL in browser
- [ ] Test chat: "Hello" → should get patient response
- [ ] Test progressive symptoms: "Tell me more" → detailed response
- [ ] Test treatment: "I prescribe paracetamol" → acceptance
- [ ] Test multi-user: Open 2 browser windows → separate sessions

---

### 6. Create Presentation Deck (6 slides max)
- [ ] Slide 1: Title & Overview
- [ ] Slide 2: Architecture Diagram
- [ ] Slide 3: Key Technologies
- [ ] Slide 4: Key Features
- [ ] Slide 5: Design Choices
- [ ] Slide 6: Demo & Challenges

---

### 7. Record Video (5-7 minutes)
- [ ] Introduction (30 sec)
- [ ] Architecture Explanation (1 min)
- [ ] Live Demo (3-4 min):
  - Multi-user demonstration
  - Progressive symptoms
  - Treatment acceptance
- [ ] Challenges & Learnings (1 min)
- [ ] Conclusion (30 sec)

---

### 8. Upload to ICAPP
- [ ] Upload source code
- [ ] Upload presentation deck
- [ ] Upload video presentation

---

## 📝 Quick Commands Reference

```bash
# Backend
cd backend
python app.py                    # Local testing
vercel                           # Deploy
vercel --prod                    # Production deploy
vercel env add GEMINI_API_KEY    # Add env var

# Frontend
cd frontend
npm run dev                      # Local testing
npm run build                    # Build
vercel                           # Deploy
vercel --prod                    # Production deploy

# General
vercel login                     # Login
vercel logs                      # View logs
```

---

## 🎯 Estimated Timeline

- **Step 1 (Testing):** 15-30 minutes
- **Step 2 (Backend Deploy):** 15-30 minutes
- **Step 3 (Frontend Config):** 5 minutes
- **Step 4 (Frontend Deploy):** 15-30 minutes
- **Step 5 (Deployed Testing):** 15 minutes
- **Step 6 (Presentation):** 1-2 hours
- **Step 7 (Video):** 30-60 minutes
- **Step 8 (Upload):** 15 minutes

**Total:** 3-5 hours

---

## 🚨 Common Issues

**Backend deployment fails:**
- Check `vercel.json` exists
- Verify `requirements.txt` has all dependencies
- Check environment variables are set

**Frontend can't connect to backend:**
- Update `sessionservice.js` with correct backend URL
- Check CORS is enabled in backend
- Verify backend URL is correct

**API rate limiting:**
- Wait 1 minute between requests
- Code already has retry logic

---

**Detailed instructions:** See `DEPLOYMENT_STEPS.md`

