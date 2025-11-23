# Quick Start Guide

## Setup and Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API server**:
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:8000`

3. **Access the UI**:
   Open your browser and go to: `http://localhost:8000/ui`

## Using the UI

### Basic Usage

1. **Load a word embedding**:
   - Enter a word in the "Word to Embed" field (e.g., "quantum")
   - Click "Load Embedding"
   - View the quantum parameters (alpha, beta, gamma) in the parameters panel

2. **Add to 3D space**:
   - After loading an embedding, click "Add to 3D Space"
   - The word will appear as a point in the 3D visualization

3. **Load multiple words**:
   - Load several words one by one
   - Each will be added to the same 3D space
   - Use "Visualize Full Space" to see all loaded embeddings

4. **Compute quantum interactions**:
   - Enter two words
   - Click "Compute Quantum Interaction"
   - See the similarity score and combined wavefunction

### 3D Visualization

- **Rotate**: Click and drag to rotate the view
- **Zoom**: Use mouse wheel to zoom in/out
- **Axes**: 
  - Red = Alpha (displacement)
  - Green = Beta (chirp rate)
  - Blue = Gamma (global phase)

## API Usage Examples

### Get word parameters
```bash
curl http://localhost:8000/api/word/quantum
```

### Load an embedding
```bash
curl -X POST http://localhost:8000/api/embedding \
  -H "Content-Type: application/json" \
  -d '{"word": "quantum"}'
```

### Compute interaction
```bash
curl -X POST http://localhost:8000/api/interaction \
  -H "Content-Type: application/json" \
  -d '{"word1": "quantum", "word2": "physics"}'
```

### Get 3D space coordinates
```bash
curl "http://localhost:8000/api/space/3d?words=quantum,physics,love"
```

## Generating Embeddings for 500 Words

See `generate_embeddings_prompt.md` for instructions on creating a script to generate embeddings for the 500 most frequent English words.

## Troubleshooting

- **GloVe download**: First run will download GloVe vectors (~400MB). This is automatic.
- **Port already in use**: Change the port in `app.py` or kill the process using port 8000
- **CORS errors**: The API allows all origins by default. Adjust in `app.py` for production.

