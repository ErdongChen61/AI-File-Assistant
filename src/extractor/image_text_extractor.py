import easyocr

from src.extractor.text_extractor import TextExtractor
from typing import Sequence

class ImageTextExtractor(TextExtractor):
    """
    A singleton class to extract text from images using EasyOCR.
    """

    def __init__(self):
        """
        Initializes the ImageTextExtractor with the specified languages.
        """
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_texts(self, path: str) -> Sequence[str]:
        """
        Extracts text from the specified image.

        Args:
            path (str): The path to the image from which to extract text.

        Returns:
            Sequence[str]: A sequence of texts.
        """
        texts = self.reader.readtext(path, detail = 0)
        return [' '.join(texts)]
