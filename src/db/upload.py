import tempfile
import os

from src.utils.document_processing import DocumentProcessor
from src.config.weaviate_db import weaviate_connection
from src.core.exceptions import DocumentProcessingException
from src.schemas.responses import DocumentProcessSuccessResponse

def process_uploaded_files(uploaded_files) -> dict:
    """
    Process uploaded PDF files:
    1. Save files to temp directory
    2. Load documents
    3. Convert to embeddings
    4. Store in Weaviate vector database

    Args:
        uploaded_files: List of FastAPI UploadFile objects

    Returns:
        dict: Result containing success status and metadata
    """
    try:
        weaviate_client = weaviate_connection()
        from src.config.settings import settings
        class_name = settings.WEAVIATE_CLASS_NAME or "DemoCollection"
        embedding_model = settings.EMBEDDING_MODEL or "Snowflake/snowflake-arctic-embed-l-v2.0"

        with tempfile.TemporaryDirectory() as tmpdirname:
            file_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join(tmpdirname, uploaded_file.filename)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.file.read())
                file_paths.append(file_path)

            # Process each file
            all_chunks = []
            for file_path in file_paths:
                rag = DocumentProcessor(file_path=file_path)
                pages = rag.load_documents() or []
                chunks = rag.split_chunks(pages)
                all_chunks.extend(chunks)

            # Create Weaviate collection if needed
            processor = DocumentProcessor()
            processor.create_weaviate_collection(weaviate_client, class_name)
            # Add objects to Weaviate (let Weaviate handle vectorization)
            vectors_stored = processor.add_objects_to_weaviate(all_chunks, weaviate_client, class_name)

            return DocumentProcessSuccessResponse(
                success=True,
                message="PDF documents processed and stored successfully",
                documents_processed=len(all_chunks),
                vectors_stored=vectors_stored,
            ).dict()
            
    except Exception as e:
        raise DocumentProcessingException()
