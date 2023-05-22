from abc import ABC, abstractmethod
from typing import Sequence

class TextExtractor(ABC):

    @abstractmethod
    def extract_texts(self, path: str) -> Sequence[str]:
        pass