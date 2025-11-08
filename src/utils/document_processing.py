import os
from typing import List
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import numpy as np
import weaviate
import uuid
from weaviate.auth import AuthApiKey

class DocumentProcessor:
    _embedding_model = None  # Class-level cache for the embedding model

    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5", weaviate_url: str = "https://your-weaviate-instance.weaviate.network", api_key: str = "YOUR-WEAVIATE-API-KEY"):
        # Use cached model if available
        if DocumentProcessor._embedding_model is None:
            DocumentProcessor._embedding_model = SentenceTransformer(model_name)
        self.model = DocumentProcessor._embedding_model

        self.client = weaviate.Client(
            url=weaviate_url,
            auth_client_secret=AuthApiKey(api_key)
        )

        # Ensure schema exists
        class_obj = {
            "class": "DocumentChunk",
            "vectorizer": "none",
            "properties": [
                {"name": "text", "dataType": ["text"]}
            ]
        }
        if not self.client.schema.exists("DocumentChunk"):
            self.client.schema.create_class(class_obj)

    def load_pdf(self, file_path: str) -> str:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += str(page.get_text() or "")
        return text

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    def get_embeddings(self, chunks: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(chunks)
        return embeddings.tolist()

    def add_embeddings_to_weaviate(self, chunks: List[str], embeddings: List[List[float]]):
        for chunk, embedding in zip(chunks, embeddings):
            self.client.data_object.create(
                data_object={"text": chunk},
                class_name="DocumentChunk",
                vector=embedding,
                uuid=str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk))
            )

    def Retrieve_chunks(self, file_path: str):
        text = self.load_pdf(file_path)
        chunks = self.chunk_text(text)
        embeddings = self.get_embeddings(chunks)
        self.add_embeddings_to_weaviate(chunks, embeddings)
        print(f"Loaded {len(chunks)} chunks and uploaded embeddings to Weaviate.")

# Example usage:
if __name__ == "__main__":
    processor = DocumentProcessor(
        weaviate_url="https://your-weaviate-instance.weaviate.network",
        api_key="YOUR-WEAVIATE-API-KEY"
    )
    pdf_path = "your_pdf_file.pdf"
    processor.Retrieve_chunks(pdf_path)
