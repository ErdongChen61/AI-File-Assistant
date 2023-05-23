import cProfile
import logging
import os

from chromadb.errors import NoIndexException
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from src.model.instructor_xl_embedding_model import InstructorXlEmbeddingModel
from src.utils.singleton import Singleton
from typing import Dict, Sequence

logger = logging.getLogger(__name__)

class ChromaClient(metaclass=Singleton):
    """ChromaClient is the main interface for interacting with the Chroma database."""
    def __init__(self):
        self.type = None

    def __init__(self, collection_name: str, embedding_model: InstructorXlEmbeddingModel) -> None:
        # Directory to persist the database.
        self.persist_directory = './database/chroma'
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self.db = Chroma(self.collection_name, embedding_model.model, self.persist_directory)  
       
    def similarity_search(self, query: str) -> Sequence[Document]:
        """Perform a similarity search with the given query, returns the top 4 most similar documents."""
        try:
            logging.info(f"ChromaClient: search: {query}, {self.type}")
            return self.db.similarity_search(query, 4)
        except (NoIndexException, RuntimeError) as e:
            logging.info(f"ChromaClient: Error in search: {query}, {str(e)} {self.type}")
            return []

    def add_texts(self, texts: Sequence[str], metadatas: Sequence[Dict[str, str]]) -> None:
        """Add texts and their corresponding metadatas to the database."""
        if len(texts) != len(metadatas):
            raise ValueError("The lengths of texts and metadatas must match. {} : {}".format(len(texts), len(metadatas)))
        logging.info(f"ChromaClient: add_texts: {self.type}")
        profiler = cProfile.Profile()
        profiler.enable()
        self.db.add_texts(texts, metadatas)
        profiler.disable()
        profiler.print_stats()
        logging.info(f"ChromaClient: add_texts persist: {self.type}")
        self.db.persist()
    
    def delete(self, path: str) -> None:
        logging.info(f"ChromaClient: Delete: {path} {self.type}")
        self.db._collection.delete(where={'source': path})
        self.db.persist()

    def as_retriever(self) -> VectorStoreRetriever:
        """Get a retriever for the database."""
        return self.db.as_retriever()

class ImageChromaClient(ChromaClient):

    def __init__(self, embedding_model: InstructorXlEmbeddingModel) -> None:
        super().__init__('image_embedding', embedding_model)
        self.type = 'image'

class PdfChromaClient(ChromaClient):

    def __init__(self, embedding_model: InstructorXlEmbeddingModel) -> None:
        super().__init__('pdf_embedding', embedding_model)
        self.type = 'pdf'
