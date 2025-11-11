"""
OpenAPI/Swagger specification for the RAG Chatbot API.
This covers PDF upload, query, and (optionally) webhook endpoints.
"""

from src.schemas.responses import (
	QueryRequest
)

upload_endpoint = {
	"summary": "Upload and process PDF documents",
	"description": "Upload one or more PDF files. The files will be processed, embedded, and stored in the vector database. Returns processing metadata.",
	"requestBody": {
		"content": {
			"multipart/form-data": {
				"schema": {
					"type": "object",
					"properties": {
						"uploaded_files": {
							"type": "array",
							"items": {"type": "string", "format": "binary"},
							"description": "List of PDF files to upload."
						}
					},
					"required": ["uploaded_files"]
				}
			}
		}
	},
	"responses": {
		200: {
			"description": "Documents processed and stored successfully",
			"content": {
				"application/json": {
					"example": {
						"statusCode": 200,
						"success": True,
						"message": "PDF documents processed and stored successfully",
						"documents_processed": 2,
						"vectors_stored": 10
					}
				}
			}
		},
		400: {
			"description": "Invalid file type (not PDF)",
			"content": {
				"application/json": {
					"example": {
						"error": "File example.txt is not a PDF."
					}
				}
			}
		},
		500: {
			"description": "Error during document processing",
			"content": {
				"application/json": {
					"example": {
						"statusCode": 500,
						"statusMessage": "Internal Server Error",
						"errorMessage": "Failed to process documents."
					}
				}
			}
		}
	}
}

query_endpoint = {
	"summary": "Ask a question to the RAG chatbot",
	"description": "Submit a query to get an answer based on the processed PDF documents. You can optionally filter the search to a specific filename.",
	"requestBody": {
		"content": {
			"application/json": {
				"schema": QueryRequest.schema(),
				"example": {
					"query": "What are the online services does APMC provide?",
					"top_k": 5,
					"min_score": 0.8
				}
			}
		}
	},
	"responses": {
		200: {
			"description": "Successfully retrieved an answer",
			"content": {
				"application/json": {
					"example": {
						"statusCode": 200,
						"success": True,
						"message": "Answer retrieved successfully",
						"query": "How do I contact APMC?",
						"answer": "You can contact APMC at contact@apmedicalcouncil.in.",
						"source_url": "https://apmedicalcouncil.in/contact"
					}
				}
			}
		},
		404: {
			"description": "No relevant information found to answer the query",
			"content": {
				"application/json": {
					"example": {
						"statusCode": 404,
						"success": False,
						"message": "Information not found",
						"query": "What is the company's policy on space travel?",
						"answer": "I could not find any relevant information to answer that question in the provided documents."
					}
				}
			}
		},
		500: {
			"description": "Error during query processing",
			"content": {
				"application/json": {
					"example": {
						"statusCode": 500,
						"statusMessage": "Internal Server Error",
						"errorMessage": "Failed to process the query."
					}
				}
			}
		},
		422: {
			"description": "Validation error (Unprocessable Entity)",
			"content": {
				"application/json": {
					"example": {
						"detail": [
							{
								"loc": ["body", "query"],
								"msg": "Field required",
								"type": "value_error.missing"
							}
						]
					}
				}
			}
		}
	}
}


# Export endpoints for use in FastAPI docs or OpenAPI generator
swagger_spec = {
	"upload": upload_endpoint,
	"query": query_endpoint
}
