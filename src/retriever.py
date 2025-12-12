from typing import List
from src.interfaces import Document
from src.embedder import Embedder
from src.vector_store import VectorStore

class Retriever:
    """
    Orchestrates the retrieval pipeline: Query -> Embedding -> Vector Search
    """
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = VectorStore()

    async def retrieve(self, query: str, k: int = 5) -> List[Document]:
        """
        1. Embed the user's query.
        2. Search the vector store for top-k similar documents.
        """
        # Generate vector for the query text
        # embed() returns a list of lists, we take the first one
        query_vector = self.embedder.embed([query])[0]
        
        # Search DB
        documents = await self.vector_store.similarity_search(query_vector, limit=k)
        
        return documents