# Gemini API Setup Guide

## Environment Variable Configuration

The application now uses **Google Gemini API** instead of OpenAI. You need to set up your Gemini API key.

### Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey) or [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new API key for Gemini
3. Copy your API key

### Setting the Environment Variable

The application looks for either `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable.

#### Local Development

Create a `.env` file in the `backend/` directory:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

Or:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

#### Vercel Deployment

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add a new variable:
   - **Name**: `GEMINI_API_KEY` (or `GOOGLE_API_KEY`)
   - **Value**: Your Gemini API key
   - **Environment**: Production, Preview, Development (select all)
4. Save and redeploy

### Testing the Setup

After setting the API key, test it by running:

```bash
cd backend
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', 'SET' if os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY') else 'NOT SET')"
```

### Model Information

- **Model**: `gemini-1.5-flash` (default - faster, cost-effective)
- **Alternative**: `gemini-1.5-pro` (better quality, slower)
- **Temperature**: 0.7 (configurable in `agent_logic.py`)

You can change the model in `backend/agent_logic.py`:
```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Fast and efficient (default)
    # model="gemini-1.5-pro",  # Better quality, slower
    temperature=0.7,
    google_api_key=GEMINI_API_KEY
)
```

**Note**: The old `gemini-pro` model is deprecated. Use `gemini-1.5-flash` or `gemini-1.5-pro` instead.

### Troubleshooting

- **Error: "GEMINI_API_KEY environment variable must be set"**
  - Make sure you've created the `.env` file in the `backend/` directory
  - Verify the variable name is exactly `GEMINI_API_KEY` or `GOOGLE_API_KEY`
  - Restart your Flask server after adding the `.env` file

- **Error: "API key not valid"**
  - Verify your API key is correct
  - Check if you have enabled the Gemini API in Google Cloud Console
  - Ensure your API key has the necessary permissions

