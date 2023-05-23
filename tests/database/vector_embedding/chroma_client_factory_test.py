from src.database.vector_embedding.chroma_client_factory import ChromaClientFactory
from src.database.vector_embedding.chroma_client import ImageChromaClient, PdfChromaClient

class TestChromaClientFactory:
    def test_get_client(self):
        pdf_file = '/path/to/file.pdf'
        img_file = '/path/to/file.jpg'
        other_file = '/path/to/file.txt'

        pdf_client = ChromaClientFactory.get_client(pdf_file)
        img_client = ChromaClientFactory.get_client(img_file)
        other_client = ChromaClientFactory.get_client(other_file)

        assert isinstance(pdf_client, PdfChromaClient)
        assert isinstance(img_client, ImageChromaClient)
        assert other_client is None