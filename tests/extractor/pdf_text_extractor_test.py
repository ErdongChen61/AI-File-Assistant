import pytest
from src.extractor.pdf_text_extractor import PdfTextExtractor

class TestPdfTextExtractor:
    def test_extract_texts(self):
        extractor = PdfTextExtractor()
        texts = extractor.extract_texts('/Users/samchen/Documents/GitHub/AI-File-Assistant/tests/extractor/data/simple_pdf.pdf')
        assert len(texts) == 1
        assert texts[0] == 'This is a simple PDF file for testing purpose.'
