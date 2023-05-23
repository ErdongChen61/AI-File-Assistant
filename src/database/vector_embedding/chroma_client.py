import cProfile
import logging
import os

from chromadb.errors import NoIndexException
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from src.model.embedding_model import EmbeddingModel
from src.utils.singleton import Singleton
from typing import Dict, Sequence

logger = logging.getLogger(__name__)

class ChromaClient:
    """ChromaClient is the main interface for interacting with the Chroma database."""

    def __init__(self, collection_name: str, embedding_model: EmbeddingModel) -> None:
        self.collection_name = collection_name
        # Directory to persist the database.
        self.persist_directory = './database/chroma/' + collection_name
        self.embedding_model = embedding_model
        self.db = Chroma(self.collection_name, embedding_model.model, self.persist_directory)  
       
    def similarity_search(self, query: str) -> Sequence[Document]:
        """Perform a similarity search with the given query, returns the top 4 most similar documents."""
        try:
            return self.db.similarity_search(query, 4)
        except (NoIndexException, RuntimeError) as e:
            logger.info(f"ChromaClient: search error: {str(e)}")
            return []

    def add_texts(self, texts: Sequence[str], metadatas: Sequence[Dict[str, str]]) -> None:
        """Add texts and their corresponding metadatas to the database."""
        if len(texts) != len(metadatas):
            raise ValueError("The lengths of texts and metadatas must match. {} : {}".format(len(texts), len(metadatas)))
        
        #profiler = cProfile.Profile()
        #profiler.enable()
        self.db.add_texts(texts, metadatas)
        #profiler.disable()
        #profiler.print_stats()
    
    def delete(self, path: str) -> None:
        self.db._collection.delete(where={'source': path})
        

    def as_retriever(self) -> VectorStoreRetriever:
        """Get a retriever for the database."""
        return self.db.as_retriever()

class ImageChromaClient(ChromaClient, metaclass=Singleton):

    def __init__(self, embedding_model: EmbeddingModel) -> None:
        super().__init__('image_embedding', embedding_model)

class PdfChromaClient(ChromaClient, metaclass=Singleton):

    def __init__(self, embedding_model: EmbeddingModel) -> None:
        super().__init__('pdf_embedding', embedding_model)
