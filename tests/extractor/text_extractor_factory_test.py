from src.extractor.image_text_extractor import ImageTextExtractor
from src.extractor.pdf_text_extractor import PdfTextExtractor
from src.extractor.text_extractor_factory import TextExtractorFactory

class TestTextExtractorFactory:
    def test_get_text_extractor(self):
        pdf_file = '/path/to/file.pdf'
        img_file = '/path/to/file.jpg'
        other_file = '/path/to/file.txt'

        pdf_extractor = TextExtractorFactory.get_text_extractor(pdf_file)
        img_extractor = TextExtractorFactory.get_text_extractor(img_file)
        other_extractor = TextExtractorFactory.get_text_extractor(other_file)

        assert isinstance(pdf_extractor, PdfTextExtractor)
        assert isinstance(img_extractor, ImageTextExtractor)
        assert other_extractor is None