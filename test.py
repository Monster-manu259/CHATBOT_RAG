from src.utils.document_processing import DocumentProcessor
from src.services.rag_services import get_rag_response  # Adjust import as needed

processor = DocumentProcessor("C:\\Users\\SAI MANOGNA\\Downloads\\APMC\\APMC_DOCUMENTATION.pdf")

query = input("Enter your query: ")
response = get_rag_response(query)
print("Answer:", response)