from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.rag_assistant import MutualFundAssistant
except ImportError:
    # Fallback for different execution environments
    sys.path.append(os.getcwd())
    from src.rag_assistant import MutualFundAssistant

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HDFC RAG Backend")

# Enable CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update this with Vercel URL after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Assistant
assistant = MutualFundAssistant()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query text is required")
    
    try:
        response = assistant.ask(request.query)
        return {"response": response}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
