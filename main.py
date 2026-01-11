from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
def web_search(query: str, max_results: int = 5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title"),
                "body": r.get("body"),
                "url": r.get("href")
            })
    return results

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": ""llama-3.1-8b-instant"
",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": req.message}
        ]
    }

    r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()

    return {
        "reply": data["choices"][0]["message"]["content"]
    }