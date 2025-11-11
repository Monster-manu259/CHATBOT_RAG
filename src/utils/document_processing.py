from typing import Optional
from typing import List, Dict, Any
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from weaviate.classes.config import Configure, Property, DataType
from src.core.exceptions import (
    NoContentToSplitException,
    RuntimeError,
    EmbeddingModelException,
    WeaviateUpsertException,
    WeaviateQueryException
)

class DocumentProcessor:
    _embedding_model = None  # Class-level cache

    def __init__(self, file_path: Optional[str] = None):
        if DocumentProcessor._embedding_model is None:
            DocumentProcessor._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding_model = DocumentProcessor._embedding_model
        self.file_path = file_path

    def load_documents(self):
        """Loads a PDF document """
        try:
            if self.file_path and self.file_path.lower().endswith(".pdf"):
                with fitz.open(self.file_path) as doc:
                    pages = []
                    for i in range(doc.page_count):
                        page = doc.load_page(i)
                        raw_text = page.get_text("text")
                        pages.append({
                            "page_content": raw_text,
                            "filename": self.file_path,
                            "page_number": i + 1
                        })
                return pages
        except Exception as e:
            raise RuntimeError(f"Failed to load PDF: {e}")


    def split_chunks(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = []
        for doc in pages:
            if not doc.get("page_content") or not doc["page_content"].strip():
                raise NoContentToSplitException()
            split_docs = text_splitter.create_documents(
                [doc["page_content"]], metadatas=[{"filename": doc["filename"], "page_number": doc["page_number"]}]
            )
            for split_doc in split_docs:
                chunks.append({
                    "chunk_text": split_doc.page_content,
                    "metadata": split_doc.metadata,
                })
        return chunks
    
    def create_embeddings(self, chunks: List[Dict[str, Any]]):
        if not chunks:
            raise NoContentToSplitException()
        try:
            embeddings = self.embedding_model.encode(
                [chunk["chunk_text"] for chunk in chunks],
                normalize_embeddings=True,
                show_progress_bar=True,
                batch_size=32
            )

            if hasattr(embeddings, "tolist"):
                embeddings = embeddings.tolist()
            return embeddings
        except Exception as e:
            raise EmbeddingModelException()

    def add_objects_to_weaviate(self, embed_docs: List[Dict[str, Any]], weaviate_client, class_name: str) -> int:
        if not embed_docs:
            return 0
        collection = weaviate_client.collections.use(class_name)
        total_added = 0
        with collection.batch.fixed_size(batch_size=200) as batch:
            for doc in embed_docs:
                batch.add_object(
                    properties={
                        "chunk_text": doc["chunk_text"],
                        "filename": doc["metadata"].get("filename", ""),
                        "page_number": doc["metadata"].get("page_number", 0),
                    },
                    vector=doc["embedding"]    # Insert your embedding
                )
                total_added += 1
        return total_added

    def retrieve_relevant_chunks(self, query: str, weaviate_client, class_name: str, top_k: int = 5):
        try:
            collection = weaviate_client.collections.use(class_name)
            query_vector = self.embedding_model.encode(query).tolist()

            # Fix: Ensure limit is set before calling objects(), and handle GenerativeReturn
            query_obj = collection.query.near_vector(query_vector)
            if hasattr(query_obj, 'limit'):
                query_obj = query_obj.limit(top_k)
            if hasattr(query_obj, 'objects'):
                response = query_obj.objects() if callable(query_obj.objects) else query_obj.objects
            else:
                response = query_obj

            docs = []
            best_filename = None
            # Robustly handle response type
            if isinstance(response, list):
                iterable_response = response
            # Remove .objects() call; use response directly
            # If response is not a list, wrap in list
            elif response is not None:
                iterable_response = [response]
            else:
                iterable_response = []

            for obj in iterable_response:
                # Defensive: skip if obj is None or doesn't have 'properties' dict
                properties = getattr(obj, 'properties', None)
                if obj is None or not isinstance(properties, dict):
                    continue
                chunk_text = properties.get("chunk_text", "")
                filename = properties.get("filename", "")
                page_number = properties.get("page_number", "")
                docs.append({
                    "chunk_text": chunk_text,
                    "metadata": {"filename": filename, "page_number": page_number}
                })
                if best_filename is None:
                    best_filename = filename
            return docs, best_filename
        except Exception as e:
            raise WeaviateQueryException(str(e))
