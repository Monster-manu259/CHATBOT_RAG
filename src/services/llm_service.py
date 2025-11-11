from src.core.exceptions import LLMServiceAPIException
from src.config.settings import settings
from src.core.prompts import get_document_answer_prompt
from src.core.constants import FALLBACK_MESSAGE

import google.generativeai as genai

class LLMService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            # Configure Gemini client with API key
            genai.configure(api_key=settings.GEMINI_API_KEY)
            cls._client = genai.GenerativeModel(settings.GEMINI_LLM_MODEL)
        return cls._instance

    def generate_answer(self, context: str, question: str) -> str:
        """
        Generates an answer using the Gemini 2.5 Flash LLM model.
        """
        try:
            formatted_prompt = get_document_answer_prompt(context, question, "", FALLBACK_MESSAGE)
            response = self._client.generate_content(
                contents=formatted_prompt
            )
            return response.text.strip()
        except Exception as e:
            raise LLMServiceAPIException(str(e))
