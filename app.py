"""
FastAPI application for Quantum Embedding Visualization
Provides REST API endpoints for quantum embedding operations
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os

from pattern_embedding_service import PatternEmbeddingService

app = FastAPI(
    title="Quantum Embedding Visualization API",
    description="API for quantum semantic embeddings based on PATTERN3.py",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize the service
service = PatternEmbeddingService()

# Request/Response models
class WordRequest(BaseModel):
    word: str

class WordsRequest(BaseModel):
    words: List[str]

class SimilarWordsRequest(BaseModel):
    word: str
    top_k: int = 10
    exclude_words: Optional[List[str]] = None

class InteractionRequest(BaseModel):
    word1: str
    word2: str

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Quantum Embedding Visualization API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/word/{word}": "Get quantum parameters for a word",
            "POST /api/embedding": "Load a quantum embedding",
            "POST /api/embeddings/batch": "Load multiple embeddings",
            "POST /api/interaction": "Compute quantum interaction between two words",
            "GET /api/space/3d": "Get 3D embedding space coordinates",
            "POST /api/similar": "Find similar words"
        }
    }

@app.get("/api/word/{word}")
async def get_word_parameters(word: str):
    """
    Get the quantum pattern parameters (alpha, beta, gamma) for a word.
    
    Returns:
        Dictionary with word and its quantum parameters
    """
    try:
        params = service.get_word_parameters(word)
        return params
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/embedding")
async def load_embedding(request: WordRequest):
    """
    Load a quantum embedding for a word.
    Returns full wavefunction data and parameters for 3D visualization.
    
    Returns:
        Dictionary with embedding data including wavefunction and parameters
    """
    try:
        embedding_data = service.add_embedding(request.word)
        return embedding_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/embeddings/batch")
async def load_embeddings_batch(request: WordsRequest):
    """
    Load multiple quantum embeddings at once.
    
    Returns:
        Dictionary with all embeddings
    """
    try:
        result = service.batch_load_embeddings(request.words)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interaction")
async def compute_interaction(request: InteractionRequest):
    """
    Compute quantum interaction between two embeddings.
    Shows quantum computation/superposition of embeddings.
    
    Returns:
        Dictionary with interaction data including similarity and combined wavefunction
    """
    try:
        interaction = service.compute_embedding_interaction(request.word1, request.word2)
        return interaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/space/3d")
async def get_embedding_space_3d(words: Optional[str] = None):
    """
    Get 3D coordinates for embedding space visualization.
    Uses (alpha, beta, gamma) as (x, y, z) coordinates.
    
    Query parameter:
        words: Comma-separated list of words (optional, uses all cached if not provided)
    
    Returns:
        Dictionary with 3D points for visualization
    """
    try:
        word_list = None
        if words:
            word_list = [w.strip() for w in words.split(",")]
        
        space_data = service.get_embedding_space_3d(word_list)
        return space_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/similar")
async def get_similar_words(request: SimilarWordsRequest):
    """
    Find words most similar to a given word based on quantum similarity.
    
    Returns:
        List of similar words with similarity scores
    """
    try:
        similar = service.get_similar_words(
            request.word,
            top_k=request.top_k,
            exclude_words=request.exclude_words
        )
        return {"word": request.word, "similar_words": similar}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "quantum_embedding"}

@app.get("/ui", response_class=HTMLResponse)
async def serve_ui():
    """Serve the main UI."""
    ui_path = os.path.join(static_dir, "index.html")
    if os.path.exists(ui_path):
        with open(ui_path, "r") as f:
            return f.read()
    return HTMLResponse(content="<h1>UI not found</h1>", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

