from src.schemas.responses import QueryNotFoundResponse, QuerySuccessResponse
from src.utils.document_processing import DocumentProcessor
from src.services.llm_service import LLMService

llm_service = LLMService()

from src.core.constants import FALLBACK_MESSAGE
from src.config.weaviate_db import weaviate_connection

weaviate_client = weaviate_connection()
weaviate_class = "DemoCollection"  # Placeholder: replace with actual class name

def get_rag_response(query: str, top_k: int = 5, min_score: float = 0.8):
	"""
	Orchestrates the RAG process to get a final answer from the LLM.

	Returns a JSON-serializable dict. When a source URL is available it is
	included under the `source_url` key.
	"""
	try:
		# 1. Retrieve relevant document chunks and highest scored vector website
		doc_processor = DocumentProcessor(file_path=None)  # file_path not needed for retrieval
		docs, highest_url = doc_processor.retrieve_relevant_chunks(
			query=query,
			weaviate_client=weaviate_client,
			class_name=weaviate_class,
			top_k=top_k,
		)

		# 2. Handle the case where no relevant information is found
		if not docs:
			return QueryNotFoundResponse(
				statusCode=404,
				success=False,
				message="Information not found",
				query=query,
				answer=FALLBACK_MESSAGE,
			)

		# 3. Prepare the context for the LLM from retrieved documents
		formatted_docs = []
		for i, doc in enumerate(docs):
			title = doc["metadata"].get("filename")
			category = doc["metadata"].get("page_number")
			score = doc["metadata"].get("score", 0)

			formatted_doc = f"DOCUMENT {i+1}:\nTitle: {title}\nCategory: {category}\nRelevance Score: {score:.2f}\nContent:\n{doc['chunk_text']}"
			formatted_docs.append(formatted_doc)
		context = "\n\n" + "\n\n---\n\n".join(formatted_docs)

		# 4. Generate the final answer using the LLM
		final_answer = llm_service.generate_answer(context=context, question=query)

		# Create response object
		response = QuerySuccessResponse(
			statusCode=200,
			success=True,
			message="Answer retrieved successfully",
			query=query,
			answer=final_answer,
		)

		# If the answer is the fallback message, don't include a source URL.
		if final_answer.strip() == FALLBACK_MESSAGE.strip():
			response.source_url = None
			return response

		# Handle source URL with improved validation
		is_valid_url = (
			highest_url and 
			highest_url != "NA" and 
			isinstance(highest_url, str) and 
			(str(highest_url).startswith("http://") or str(highest_url).startswith("https://"))
		)
		if is_valid_url:
			response.source_url = highest_url
		return response

	except Exception as e:
		return QueryNotFoundResponse(
			statusCode=500,
			success=False,
			message=str(e),
			query=query,
			answer="Error occurred while processing your query.",
		)
