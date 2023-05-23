import os

from langchain import HuggingFaceHub
from langchain.embeddings import HuggingFaceInstructEmbeddings
from src.utils.singleton import Singleton

class InstructorXlEmbeddingModel(metaclass=Singleton):
    """A singleton class that loads the 'hkunlp/instructor-xl' model for embedding text."""

    def __init__(self) -> None:
        self.model_name = 'hkunlp/instructor-xl'
        self.model_kwargs = {'device': 'cpu'}
        self.model = HuggingFaceInstructEmbeddings(model_name=self.model_name, model_kwargs=self.model_kwargs)
