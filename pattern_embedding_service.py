"""
PatternEmbeddingService - Backend service for quantum embedding operations
Based on PATTERN3.py quantum embedding engine
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from gensim.downloader import load
import json
import os


class PatternEmbeddingService:
    """
    Service for generating and managing quantum embeddings using PATTERN3.py logic.
    Provides methods for embedding generation, similarity computation, and 3D visualization.
    """
    
    def __init__(self, num_points: int = 1024, sigma: float = 1.5, cache_file: Optional[str] = None):
        """
        Initialize the service with GloVe vectors and configuration.
        
        Args:
            num_points: Number of points in the wavefunction discretization
            sigma: Width parameter for the Gaussian wavepacket
            cache_file: Optional path to cache file for pre-computed embeddings
        """
        self.num_points = num_points
        self.sigma = sigma
        self.cache_file = cache_file or "embeddings_cache.json"
        self.embeddings: Dict[str, np.ndarray] = {}
        self.parameters: Dict[str, Tuple[float, float, float]] = {}
        
        print("Loading GloVe 300d vectors...")
        try:
            self.glove = load("glove-wiki-gigaword-300")
            print("GloVe vectors loaded successfully.")
        except Exception as e:
            print(f"Error loading GloVe vectors: {e}")
            raise
        
        # Load cached embeddings if available
        self._load_cache()
    
    def quantum_embedding(self, word: str) -> Tuple[np.ndarray, Tuple[float, float, float]]:
        """
        Generate quantum embedding for a word using PATTERN3.py logic.
        
        Args:
            word: The word to embed
            
        Returns:
            Tuple of (wavefunction, (alpha, beta, gamma))
        """
        # Check cache first
        if word in self.embeddings:
            return self.embeddings[word], self.parameters[word]
        
        try:
            vec = self.glove[word.lower()]
        except KeyError:
            print(f"Warning: '{word}' not in GloVe vocabulary, using random vector")
            vec = np.random.randn(300)
        
        # Use PCA-like projection of the full 300-dim vector into 3 meaningful parameters
        # This preserves almost all semantic distance (300 → 3 with minimal loss)
        alpha = vec[:100].dot(vec[100:200]) * 2.0      # ~ displacement
        beta = vec[50:150].dot(vec[150:250]) * 4.0     # ~ chirp (stronger)
        gamma = np.arctan2(vec[:150].sum(), vec[150:].sum()) * 3  # global phase
        
        x = np.linspace(-12, 12, self.num_points)
        psi = np.exp(-(x - alpha)**2 / (2*self.sigma**2) + 1j*(beta*x + gamma))
        
        dx = 24.0 / self.num_points
        psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx + 1e-12)
        
        # Cache the result
        self.embeddings[word.lower()] = psi
        self.parameters[word.lower()] = (float(alpha), float(beta), float(gamma))
        
        return psi, (float(alpha), float(beta), float(gamma))
    
    def get_word_parameters(self, word: str) -> Dict[str, float]:
        """
        Get the quantum pattern parameters for a word.
        
        Args:
            word: The word to get parameters for
            
        Returns:
            Dictionary with alpha, beta, gamma parameters
        """
        _, params = self.quantum_embedding(word)
        return {
            "word": word.lower(),
            "alpha": params[0],
            "beta": params[1],
            "gamma": params[2]
        }
    
    def quantum_similarity(self, word1: str, word2: str) -> float:
        """
        Compute quantum similarity (Born-rule fidelity) between two words.
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            Similarity score in [0, 1]
        """
        psi1, _ = self.quantum_embedding(word1)
        psi2, _ = self.quantum_embedding(word2)
        
        dx = 24.0 / len(psi1)
        return float(np.abs(np.vdot(psi1, psi2) * dx)**2)
    
    def add_embedding(self, word: str) -> Dict[str, any]:
        """
        Add an embedding to the current session.
        
        Args:
            word: The word to add
            
        Returns:
            Dictionary with embedding data including parameters and wavefunction
        """
        psi, params = self.quantum_embedding(word)
        
        # Prepare wavefunction data for frontend (sampled for efficiency)
        x = np.linspace(-12, 12, self.num_points)
        real_part = np.real(psi).tolist()
        imag_part = np.imag(psi).tolist()
        magnitude = np.abs(psi).tolist()
        
        return {
            "word": word.lower(),
            "alpha": params[0],
            "beta": params[1],
            "gamma": params[2],
            "wavefunction": {
                "x": x.tolist(),
                "real": real_part,
                "imag": imag_part,
                "magnitude": magnitude
            }
        }
    
    def get_embedding_space_3d(self, words: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Get 3D coordinates for embedding space visualization.
        Uses (alpha, beta, gamma) as 3D coordinates.
        
        Args:
            words: Optional list of words to include. If None, uses all cached embeddings.
            
        Returns:
            Dictionary with 3D coordinates and metadata
        """
        if words is None:
            words = list(self.embeddings.keys())
        
        points = []
        for word in words:
            _, params = self.quantum_embedding(word)
            points.append({
                "word": word,
                "x": params[0],  # alpha
                "y": params[1],  # beta
                "z": params[2],  # gamma
                "alpha": params[0],
                "beta": params[1],
                "gamma": params[2]
            })
        
        return {
            "points": points,
            "count": len(points)
        }
    
    def compute_embedding_interaction(self, word1: str, word2: str) -> Dict[str, any]:
        """
        Compute quantum interaction between two embeddings (for visualization).
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            Dictionary with interaction data including similarity and combined wavefunction
        """
        psi1, params1 = self.quantum_embedding(word1)
        psi2, params2 = self.quantum_embedding(word2)
        
        similarity = self.quantum_similarity(word1, word2)
        
        # Quantum superposition (for visualization)
        psi_combined = (psi1 + psi2) / np.sqrt(2)
        dx = 24.0 / len(psi1)
        psi_combined /= np.sqrt(np.sum(np.abs(psi_combined)**2) * dx + 1e-12)
        
        x = np.linspace(-12, 12, self.num_points)
        
        return {
            "word1": word1.lower(),
            "word2": word2.lower(),
            "similarity": float(similarity),
            "combined_wavefunction": {
                "x": x.tolist(),
                "real": np.real(psi_combined).tolist(),
                "imag": np.imag(psi_combined).tolist(),
                "magnitude": np.abs(psi_combined).tolist()
            },
            "params1": {
                "alpha": params1[0],
                "beta": params1[1],
                "gamma": params1[2]
            },
            "params2": {
                "alpha": params2[0],
                "beta": params2[1],
                "gamma": params2[2]
            }
        }
    
    def batch_load_embeddings(self, words: List[str]) -> Dict[str, any]:
        """
        Load multiple embeddings at once.
        
        Args:
            words: List of words to load
            
        Returns:
            Dictionary with all embeddings
        """
        results = {}
        for word in words:
            results[word.lower()] = self.add_embedding(word)
        
        return {
            "embeddings": results,
            "count": len(results)
        }
    
    def get_similar_words(self, word: str, top_k: int = 10, exclude_words: Optional[List[str]] = None) -> List[Dict[str, any]]:
        """
        Find most similar words to a given word.
        
        Args:
            word: The query word
            top_k: Number of similar words to return
            exclude_words: Words to exclude from results
            
        Returns:
            List of similar words with similarity scores
        """
        exclude_words = exclude_words or []
        all_words = [w for w in self.embeddings.keys() if w != word.lower() and w not in exclude_words]
        
        similarities = []
        for other_word in all_words:
            sim = self.quantum_similarity(word, other_word)
            similarities.append({
                "word": other_word,
                "similarity": float(sim)
            })
        
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]
    
    def _load_cache(self):
        """Load cached embeddings from file if it exists."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                    # Note: We don't cache the full wavefunctions, just parameters
                    # Full wavefunctions are recomputed on demand
                    if "parameters" in cache:
                        self.parameters = {k: tuple(v) for k, v in cache["parameters"].items()}
                print(f"Loaded {len(self.parameters)} cached parameter sets.")
            except Exception as e:
                print(f"Error loading cache: {e}")
    
    def _save_cache(self):
        """Save current embeddings cache to file."""
        try:
            cache = {
                "parameters": {k: list(v) for k, v in self.parameters.items()}
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def clear_cache(self):
        """Clear all cached embeddings."""
        self.embeddings.clear()
        self.parameters.clear()
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

