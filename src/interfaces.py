from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Document:
    """
    Standard data unit for the pipeline.
    
    Attributes:
        content (str): The text content of the document.
        metadata (Dict[str, Any]): Contextual metadata (Must contain 'source').
    """
    content: str
    metadata: Dict[str, Any]

class BaseEmbedder(ABC):
    """
    Abstract Interface for Embedding Models.
    """
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Takes a list of strings and returns a list of vector embeddings.
        
        Args:
            texts (List[str]): List of text chunks to embed.
            
        Returns:
            List[List[float]]: List of float vectors.
        """
        pass

class BaseVectorStore(ABC):
    """
    Abstract Interface for Vector Database interactions.
    """
    @abstractmethod
    async def add_documents(self, documents: List[Document], embeddings: List[List[float]]) -> None:
        """
        Stores documents in the database.
        
        Args:
            documents (List[Document]): List of document objects.
            embeddings (List[List[float]]): Corresponding vectors for the documents.
        """
        pass

    @abstractmethod
    async def similarity_search(self, query_vector: List[float], limit: int = 5) -> List[Document]:
        """
        Returns top-k documents similar to the query vector.
        
        Args:
            query_vector (List[float]): The query embedding.
            limit (int): Number of results to return.
            
        Returns:
            List[Document]: The most similar documents.
        """
        pass

class BaseLLM(ABC):
    """
    Abstract Interface for Large Language Models.
    """
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Generates a text response based on the prompt.
        
        Args:
            prompt (str): The full prompt string.
            
        Returns:
            str: The LLM's response text.
        """
        pass
# from abc import ABC, abstractmethod
# from typing import List, Dict, Any, Optional
# from dataclasses import dataclass

# @dataclass
# class Document:
#     """Standard data unit for the pipeline."""
#     content: str
#     metadata: Dict[str, Any]

# class BaseEmbedder(ABC):
#     @abstractmethod
#     def embed(self, texts: List[str]) -> List[List[float]]:
#         """Takes a list of strings and returns a list of vector embeddings."""
#         pass

# class BaseVectorStore(ABC):
#     @abstractmethod
#     async def add_documents(self, documents: List[Document]) -> None:
#         """Stores documents in the database."""
#         pass

#     @abstractmethod
#     async def similarity_search(self, query_vector: List[float], limit: int = 5) -> List[Document]:
#         """Returns top-k documents similar to the query vector."""
#         pass

# class BaseLLM(ABC):
#     @abstractmethod
#     async def generate(self, prompt: str) -> str:
#         """Generates a text response based on the prompt."""
#         pass