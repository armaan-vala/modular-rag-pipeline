from typing import List
from src.interfaces import BaseEmbedder

# Try importing the local embedding library
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

class Embedder(BaseEmbedder):
    """
    Concrete implementation using a generic, free, local model.
    This runs entirely on your machine (CPU or GPU).
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        
        if SentenceTransformer:
            # This downloads a small, fast, high-quality model (~80MB)
            print(f"Loading local embedding model: {model_name}...")
            self.model = SentenceTransformer(model_name)
            print("Model loaded successfully.")
        else:
            print("Warning: 'sentence-transformers' not installed. Embedder running in MOCK mode.")

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts.
        """
        if not texts:
            return []

        # 1. Mock Mode
        if not self.model:
            # Return dummy 384-dimensional vectors (standard for MiniLM)
            return [[0.0] * 384 for _ in texts]

        # 2. Real Implementation (Local)
        try:
            # encode() returns numpy arrays, convert to list for consistency
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
        
        except Exception as e:
            print(f"Error during embedding generation: {e}")
            return [[0.0] * 384 for _ in texts]