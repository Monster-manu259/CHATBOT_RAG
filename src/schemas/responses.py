from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field

# Response Models
class ErrorResponse(BaseModel):
    statusCode: int
    statusMessage: str
    errorMessage: str

class DocumentProcessSuccessResponse(BaseModel):
    statusCode: int = 200
    success: bool
    message: str
    documents_processed: int
    vectors_stored: int

class QueryNotFoundResponse(BaseModel):
    statusCode: int = 404
    success: bool = False
    message: str
    query: str
    answer: str

class QuerySuccessResponse(BaseModel):
    statusCode: int = 200
    success: bool = True
    message: str
    query: str
    answer: str
    source_url: Optional[str] = None

# Request Model
class QueryRequest(BaseModel):
    query: str = Field(..., examples=["What online services did APMC provide?"])
    top_k: int = 5
    min_score: float = 0.8
