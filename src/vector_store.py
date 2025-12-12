import os
import uuid
from typing import List
from src.interfaces import BaseVectorStore, Document
from dotenv import load_dotenv
load_dotenv()

# Try importing chromadb
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

class VectorStore(BaseVectorStore):
    """
    Local implementation using ChromaDB.
    Saves data to a folder './chroma_db' in your project directory.
    """
    def __init__(self):
        if not chromadb:
            raise ImportError("chromadb is required. Run: pip install chromadb")
        
        # 1. Initialize persistent client (saves to disk)
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # 2. Get or Create the collection (like a SQL table)
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"} # Use Cosine similarity
        )
        print(f"✅ Connected to Local Vector Store (ChromaDB) at ./chroma_db")

    async def add_documents(self, documents: List[Document], embeddings: List[List[float]]) -> None:
        """
        Stores documents and vectors in Chroma.
        """
        if not documents:
            return

        # Chroma requires unique IDs for every chunk
        ids = [str(uuid.uuid4()) for _ in documents]
        
        # Prepare data structure
        documents_text = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        self.collection.add(
            documents=documents_text,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully stored {len(documents)} chunks locally.")

    async def similarity_search(self, query_vector: List[float], limit: int = 5) -> List[Document]:
        """
        Query the local database.
        """
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=limit
        )
        
        # Parse results back into our generic Document format
        docs = []
        if results['documents']:
            # results is a dictionary of lists (batch format)
            retrieved_texts = results['documents'][0]
            retrieved_metadatas = results['metadatas'][0]
            
            for text, meta in zip(retrieved_texts, retrieved_metadatas):
                docs.append(Document(content=text, metadata=meta))
                
        return docs