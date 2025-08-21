# Class for extracting named entities from text
from typing import Protocol
from transformers import pipeline

class Tokenizer(Protocol):
    def tokenize(self, text : str) -> list[str]:
        """Returns a list of token strings"""
        ...

class NERModel(Protocol):
    def predict(self, text : str) -> list[dict]:
        """Returns a list of named entities in text in the format 
            {
                'entity_group' : ...
                'score' : ...
                'word' : ...
                'start' : ...
                'end' : ...
            }
        """
        ...
    
    def get_tokenizer(self) -> Tokenizer:
        ...

class Extractor:
    def __init__(self, model : NERModel, chunk_size : int):
        self.model = model
        self.chunk_size = chunk_size
        self.tokenizer = model.get_tokenizer()

    def chunk_text(self, text : str) -> list[str]:
        """Separates text into chunks of size at most chunk_size
            Chunks will only be separated at newlines
        Args:
            text: text to chunk
        """
        lines = text.split("\n")
        chunks = []
        cur_chunk = ""
        cur_chunk_size = 0
        for line in lines:
            t_line = self.tokenizer.tokenize(line)
            if len(t_line) > self.chunk_size:
                raise Exception("Line too long")
            if cur_chunk_size + len(t_line) > self.chunk_size:
                chunks.append(cur_chunk)
                cur_chunk = ""
                cur_chunk_size = 0
            if cur_chunk:
                cur_chunk = cur_chunk + '\n'
            cur_chunk = cur_chunk + line
            cur_chunk_size = cur_chunk_size + len(t_line)
        if cur_chunk:
            chunks.append(cur_chunk)
        return chunks

    def extract_named_entities(self, text : str) -> list[dict]:
        """Returns a list of named entities in text in the format
            {
                'entity_group' : ...
                'score' : ...
                'word' : ...
                'start' : ...
                'end' : ...
            }
        
        Args:
            text: text to perform extraction on
        """
        chunks = self.chunk_text(text)
        entities = []
        for chunk in chunks:
            entities.extend(self.model.predict(chunk))
        return entities

class HuggingFaceTokenizer:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def tokenize(self, text : str) -> list[str]:
        return self.tokenizer.tokenize(text)

class HuggingFaceModel:
    def __init__(self, pipeline):
        self.pipeline = pipeline
    
    def predict(self, text : str) -> list[dict]:
        return self.pipeline(text)

    def get_tokenizer(self) -> Tokenizer:
        return HuggingFaceTokenizer(self.pipeline.tokenizer)