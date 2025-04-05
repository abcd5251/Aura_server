# Aura Backend
API for the latest news of RWA Diamonds and a RAG for RWA Diamonds information.

## Execution
Put your API key into .env file
```bash
OPENAI_MODEL=""
OPENAI_API_KEY=""
SERPER_API=""
```
Install Package
```
pip install -r requirements.txt
```

Server
```
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```