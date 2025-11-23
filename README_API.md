# Quantum Embedding Visualization API

FastAPI-based backend service for visualizing quantum semantic embeddings based on PATTERN3.py.

## Features

- **Word Parameter Retrieval**: Get quantum pattern parameters (alpha, beta, gamma) for any word
- **Embedding Loading**: Load quantum embeddings with full wavefunction data
- **3D Space Visualization**: Visualize embeddings in 3D space using (alpha, beta, gamma) as coordinates
- **Quantum Interactions**: Compute quantum interactions between two embeddings
- **Batch Operations**: Load multiple embeddings at once
- **Similarity Search**: Find words most similar to a given word

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API Server**:
   ```bash
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the UI**:
   - Open your browser and navigate to: `http://localhost:8000/ui`
   - Or use the API directly at: `http://localhost:8000/api/`

## API Endpoints

### GET `/`
Root endpoint with API information.

### GET `/api/word/{word}`
Get quantum pattern parameters for a word.

**Example**:
```bash
curl http://localhost:8000/api/word/quantum
```

**Response**:
```json
{
  "word": "quantum",
  "alpha": 1.234,
  "beta": -0.567,
  "gamma": 2.890
}
```

### POST `/api/embedding`
Load a quantum embedding for a word.

**Request**:
```json
{
  "word": "quantum"
}
```

**Response**:
```json
{
  "word": "quantum",
  "alpha": 1.234,
  "beta": -0.567,
  "gamma": 2.890,
  "wavefunction": {
    "x": [-12, -11.97, ...],
    "real": [0.123, 0.124, ...],
    "imag": [0.456, 0.457, ...],
    "magnitude": [0.789, 0.790, ...]
  }
}
```

### POST `/api/embeddings/batch`
Load multiple embeddings at once.

**Request**:
```json
{
  "words": ["quantum", "physics", "love", "hate"]
}
```

### POST `/api/interaction`
Compute quantum interaction between two embeddings.

**Request**:
```json
{
  "word1": "quantum",
  "word2": "physics"
}
```

**Response**:
```json
{
  "word1": "quantum",
  "word2": "physics",
  "similarity": 0.932,
  "combined_wavefunction": { ... },
  "params1": { "alpha": 1.234, "beta": -0.567, "gamma": 2.890 },
  "params2": { "alpha": 0.987, "beta": -0.123, "gamma": 1.456 }
}
```

### GET `/api/space/3d`
Get 3D coordinates for embedding space visualization.

**Query Parameters**:
- `words` (optional): Comma-separated list of words

**Example**:
```bash
curl "http://localhost:8000/api/space/3d?words=quantum,physics,love"
```

**Response**:
```json
{
  "points": [
    {
      "word": "quantum",
      "x": 1.234,
      "y": -0.567,
      "z": 2.890,
      "alpha": 1.234,
      "beta": -0.567,
      "gamma": 2.890
    },
    ...
  ],
  "count": 3
}
```

### POST `/api/similar`
Find words most similar to a given word.

**Request**:
```json
{
  "word": "quantum",
  "top_k": 10,
  "exclude_words": ["physics"]
}
```

**Response**:
```json
{
  "word": "quantum",
  "similar_words": [
    { "word": "mechanics", "similarity": 0.923 },
    { "word": "particle", "similarity": 0.891 },
    ...
  ]
}
```

### GET `/api/health`
Health check endpoint.

## UI Features

The web UI (`/ui`) provides:

1. **Word Input**: Enter a word to load its quantum embedding
2. **Parameter Display**: View alpha, beta, and gamma parameters for loaded words
3. **3D Visualization**: Interactive 3D space showing embeddings as points
4. **Wavefunction Visualization**: 2D plot of the wavefunction's real part
5. **Quantum Interactions**: Compute and visualize interactions between two words
6. **Word List**: Track all loaded words and switch between them

## Architecture

- **`pattern_embedding_service.py`**: Core service class handling all quantum embedding operations
- **`app.py`**: FastAPI application with REST endpoints
- **`static/index.html`**: Frontend UI with Three.js for 3D visualization
- **`PATTERN3.py`**: Original quantum embedding engine (used as reference)

## Notes

- The service uses GloVe 300d vectors, which are downloaded automatically on first run (~400MB)
- Embeddings are cached in memory for performance
- The 3D visualization uses (alpha, beta, gamma) as (x, y, z) coordinates
- Wavefunctions are normalized according to quantum mechanics principles

## Next Steps

1. Generate embeddings for 500 most frequent words using `generate_embeddings_prompt.md`
2. Pre-load common embeddings for faster access
3. Add more advanced visualization options
4. Implement embedding composition operations

