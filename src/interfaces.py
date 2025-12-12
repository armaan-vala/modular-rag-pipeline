from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Document:
    """Standard data unit for the pipeline."""
    content: str
    metadata: Dict[str, Any]

class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Takes a list of strings and returns a list of vector embeddings."""
        pass

class BaseVectorStore(ABC):
    @abstractmethod
    async def add_documents(self, documents: List[Document]) -> None:
        """Stores documents in the database."""
        pass

    @abstractmethod
    async def similarity_search(self, query_vector: List[float], limit: int = 5) -> List[Document]:
        """Returns top-k documents similar to the query vector."""
        pass

class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generates a text response based on the prompt."""
        pass