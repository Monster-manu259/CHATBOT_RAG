from fastapi import APIRouter, UploadFile, File
from src.schemas.responses import QueryRequest, QuerySuccessResponse
from src.db.upload import process_uploaded_files
from src.services.rag_services import get_rag_response

router = APIRouter()

@router.post("/upload")
async def upload_files(uploaded_files: list[UploadFile] = File(...)):
    """
    Upload and process PDF files, returning processing result.
    """
    # Only allow PDF files
    for file in uploaded_files:
        if file.content_type != "application/pdf":
            return {"error": f"File {file.filename} is not a PDF."}
    result = process_uploaded_files(uploaded_files)
    return result

@router.post("/query", response_model=QuerySuccessResponse)
async def query_rag_service(request: QueryRequest):
    """
    Query the RAG service and return the response.
    """
    response = get_rag_response(
        query=request.query,
        top_k=request.top_k if request.top_k is not None else 5,
        min_score=request.min_score if request.min_score is not None else 0.0
    )
    return response
