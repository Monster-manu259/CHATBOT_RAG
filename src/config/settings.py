from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_LLM_MODEL = os.getenv("GEMINI_LLM_MODEL")
    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
    WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

settings = Settings()