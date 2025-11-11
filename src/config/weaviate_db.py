import weaviate
from src.core.exceptions import WeaviateConnectionException
from src.config.settings import settings
from weaviate.classes.init import Auth


def weaviate_connection():
    """
    Establishes a connection to the Weaviate vector database.

    Returns:
        weaviate.Client: Connected Weaviate client instance.
    Raises:
        WeaviateConnectionException: If connection fails.
    """
    try:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=settings.WEAVIATE_URL,                     # Weaviate URL: "REST Endpoint" in Weaviate Cloud console
            auth_credentials=Auth.api_key(settings.WEAVIATE_API_KEY),  # Weaviate API key: "ADMIN" API key in Weaviate Cloud console
        )
        if not client.is_ready():
            raise WeaviateConnectionException("Weaviate client is not ready.")
        print("Weaviate client is ready.")
        return client
    except Exception as e:
        raise WeaviateConnectionException(str(e))