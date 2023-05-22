from abc import ABC, abstractmethod
from src.utils.singleton import Singleton
from typing import Sequence

class TextExtractor(metaclass=Singleton):
    """
    Abstract base singleton class for text extractors.
    """

    @abstractmethod
    def extract_texts(self, path: str) -> Sequence[str]:
        pass