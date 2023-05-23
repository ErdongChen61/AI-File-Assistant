import os

from src.extractor.image_text_extractor import ImageTextExtractor
from src.extractor.pdf_text_extractor import PdfTextExtractor
from src.extractor.text_extractor import TextExtractor
from src.utils.constants import IMAGE_EXT, PDF_EXT
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
        if ext.lower() in PDF_EXT:
            return PdfTextExtractor()
        elif ext.lower() in IMAGE_EXT:
            return ImageTextExtractor()
        else:
            return None