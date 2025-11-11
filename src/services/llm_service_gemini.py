import google.generativeai as genai
from src.core.exceptions import LLMServiceUnexpectedException
from src.config.settings import settings
from src.core.prompts import get_document_answer_prompt
from src.core.constants import FALLBACK_MESSAGE

class GeminiLLMService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiLLMService, cls).__new__(cls)
            genai.configure(api_key=settings.GEMINI_API_KEY)
            cls._client = genai.GenerativeModel(settings.GEMINI_LLM_MODEL)
        return cls._instance

    def generate_answer(self, context: str, question: str) -> str:
        try:
            formatted_prompt = get_document_answer_prompt(context, question, "", FALLBACK_MESSAGE)
            response = self._client.generate_content(contents=formatted_prompt)
            return response.text.strip()
        except Exception as e:
            raise LLMServiceUnexpectedException(str(e))

gemini_llm_service = GeminiLLMService()