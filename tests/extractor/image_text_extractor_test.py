import pytest
from src.extractor.image_text_extractor import ImageTextExtractor

class TestImageTextExtractor:
    def test_extract_texts(self):
        extractor = ImageTextExtractor()
        texts = extractor.extract_texts('/Users/samchen/Documents/GitHub/AI-File-Assistant/tests/extractor/data/simple_image.jpeg')
        assert len(texts) == 1
        assert texts[0] == 'STRESS RELAX'
