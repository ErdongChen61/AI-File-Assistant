import os

from src.database.vector_embedding.chroma_client import ChromaClient, ImageChromaClient, PdfChromaClient
from src.model.instructor_xl_embedding_model import InstructorXlEmbeddingModel
from src.utils.constants import IMAGE_EXT, PDF_EXT
from typing import Optional

class ChromaClientFactory:
    """
    A factory class that produces the correct Chroma client based on file extension.
    """

    @staticmethod
    def get_client(path: str) -> Optional[ChromaClient]:
        """
        Return the correct client based on file extension.

        Args:
            path (str): Path of the file.

        Returns:
            An instance of a Chroma client or None if no suitable client found.
        """
        _, ext = os.path.splitext(path)
        if ext.lower() in PDF_EXT:
            return PdfChromaClient(InstructorXlEmbeddingModel())
        elif ext.lower() in IMAGE_EXT:
            return ImageChromaClient(InstructorXlEmbeddingModel())
        else:
            return None