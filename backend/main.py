from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
import traceback

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HDFC RAG Backend")

# Enable CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Assistant lazily — catch and log errors
assistant = None
startup_error = None

try:
    from src.rag_assistant import MutualFundAssistant
    assistant = MutualFundAssistant()
    print("✅ MutualFundAssistant initialized successfully", flush=True)
except Exception as e:
    startup_error = traceback.format_exc()
    print(f"❌ Failed to initialize assistant:\n{startup_error}", flush=True)

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    if not assistant:
        raise HTTPException(status_code=503, detail=f"Assistant not initialized: {startup_error}")
    
    if not request.query:
        raise HTTPException(status_code=400, detail="Query text is required")
    
    try:
        response = assistant.ask(request.query)
        return {"response": response}
    except Exception as e:
        print(f"Error during ask: {e}", flush=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if assistant else "degraded",
        "assistant_loaded": assistant is not None,
        "error": startup_error[:200] if startup_error else None
    }

@app.get("/")
async def root():
    return {"message": "HDFC RAG Backend is running", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
