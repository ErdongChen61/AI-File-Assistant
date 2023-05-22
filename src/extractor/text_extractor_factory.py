import os

from src.extractor.image_text_extractor import ImageTextExtractor
from src.extractor.pdf_text_extractor import PdfTextExtractor
from src.extractor.text_extractor import TextExtractor
from typing import Optional

class TextExtractorFactory:
    """
    A factory class that produces the correct text extractor based on file extension.
    """

    @staticmethod
    def get_text_extractor(path: str) -> Optional[TextExtractor]:
        """
        Return the correct text extractor based on file extension.

        Args:
            path (str): Path of the file.

        Returns:
            An instance of a text extractor or None if no suitable extractor found.
        """
        _, ext = os.path.splitext(path)
        if ext.lower() == '.pdf':
            return PdfTextExtractor()
        elif ext.lower() in ['.jpg', '.jpeg', '.png']:
            return ImageTextExtractor()
        else:
            return None