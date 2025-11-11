class RuntimeError(Exception):
    """Exception raised for errors in the runtime operations while loading the pdf."""
    pass
class NoContentToSplitException(Exception):
    """Exception raised when there is no content to split in the document."""
    pass
class EmbeddingModelException(Exception):
    """Exception raised when Failed to create embeddings """
    pass
class WeaviateUpsertException(Exception):
    """Exception raised when Weaviate upsert fails  """
    pass
class WeaviateQueryException(Exception):
    """Exception raised when Weaviate query fails  """
    pass
class DocumentProcessingException(Exception):
    """General exception for document processing errors."""
    pass
class WeaviateConnectionException(Exception):
    """Exception raised when Weaviate connection fails."""
    pass
class LLMServiceAPIException(Exception):
    """Exception raised for errors in the LLM service."""
    pass
class LLMServiceException(Exception):
    """General exception for LLM service errors."""
    pass
class DocumentNotFoundException(Exception):
    """Exception raised when a document is not found in the database."""
    pass
class LLMServiceUnexpectedException(Exception):
    """Exception raised for unexpected errors in the LLM service."""
    pass