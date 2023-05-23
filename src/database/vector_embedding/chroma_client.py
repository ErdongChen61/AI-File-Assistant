import os

from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from src.model.instructor_xl_embedding_model import InstructorXlEmbeddingModel
from src.utils.singleton import Singleton
from typing import Dict, List, Sequence

class ChromaClient(metaclass=Singleton):
    """ChromaClient is the main interface for interacting with the Chroma database."""

    def __init__(self, collection_name: str, embedding_model: InstructorXlEmbeddingModel) -> None:
        # Directory to persist the database.
        self.persist_directory = './db/chroma'
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self.db = Chroma(self.collection_name, embedding_model.model, self.persist_directory)  
       
    def similarity_search(self, query: str) -> List[Document]:
        """Perform a similarity search with the given query, returns the top 4 most similar documents."""
        return self.db.similarity_search(query, 4)

    def add_texts(self, texts: Sequence[str], metadatas: Sequence[Dict[str, str]]) -> None:
        """Add texts and their corresponding metadatas to the database."""
        if len(texts) != len(metadatas):
            raise ValueError("The lengths of texts and metadatas must match. {} : {}".format(len(texts), len(metadatas)))
        self.db.add_texts(texts, metadatas)

    def as_retriever(self) -> VectorStoreRetriever:
        """Get a retriever for the database."""
        return self.db.as_retriever()

class ImageChromaClient(ChromaClient):
    def __init__(self, embedding_model: InstructorXlEmbeddingModel) -> None:
        super().__init__('image_embedding', embedding_model)

class PdfChromaClient(ChromaClient):
    def __init__(self, embedding_model: InstructorXlEmbeddingModel) -> None:
        super().__init__('pdf_embedding', embedding_model)
