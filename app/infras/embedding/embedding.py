from abc import ABC, abstractmethod
import os
from typing import List, Union
import logging
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)

class EmbeddingService(ABC):
    """Abstract base class for embedding services"""

    @abstractmethod
    def generate_embedding(self, text: Union[str, List[str]]) -> List[float]:
        """Generate embeddings for the given text"""
        pass

class OpenAIEmbeddingService(EmbeddingService):
    """OpenAI API-based embedding service using LangChain"""

    def __init__(self, model_name: str = "text-embedding-ada-002"):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.embeddings = OpenAIEmbeddings(
            model=model_name
        )

    def generate_embedding(self, text: Union[str, List[str]]) -> List[float]:
        try:
            if isinstance(text, list):
                # For list input, return the first embedding
                embeddings = self.embeddings.embed_query(text[0])
            else:
                # For single text input
                embeddings = self.embeddings.embed_query(text)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating OpenAI embedding: {str(e)}")
            raise

class EmbeddingFactory:
    """Factory class to create embedding services"""

    @staticmethod
    def create_embedding_service(service_type: str = "openai", **kwargs) -> EmbeddingService:
        """
        Create an embedding service based on the specified type
        
        Args:
            service_type: Type of embedding service ("local" or "openai")
            **kwargs: Additional arguments for the service (e.g., model_name)
        
        Returns:
            EmbeddingService: An instance of the specified embedding service
        """
        if service_type == "openai":
            model_name = kwargs.get("model_name", "text-embedding-ada-002")
            return OpenAIEmbeddingService(model_name=model_name)
        else:
            raise ValueError(f"Unknown embedding service type: {service_type}")