
# CHAT-BOT RAG

A Retrieval-Augmented Generation (RAG) chatbot application with document upload, vector search, and context-aware response generation. Built with Python, FastAPI, and Streamlit, it integrates Weaviate and Gemini for powerful retrieval and language modeling.

---

## Backend
The backend handles document processing, vector search, and response generation. Built with Python using FastAPI, it exposes API endpoints for the frontend and manages the workflow from query to response.

### Features
- API routing and query handling
- Document ingestion and embedding
- Vector database integration (Weaviate)
- Response generation using Gemini LLM

### Installation
Clone the repository:
```powershell
git clone https://github.com/Monster-manu259/CHATBOT_RAG.git
cd CHAT-BOT
```
Set up a virtual environment (recommended):
```powershell
python -m venv venv
.\venv\Scripts\activate
```
Install dependencies:
```powershell
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the root directory and add the following environment variables:
```
# Weaviate Vector Database Credentials
WEAVIATE_URL="your-weaviate-url"
WEAVIATE_API_KEY="your-weaviate-api-key"
WEAVIATE_COLLECTION="your-weaviate-collection"

# Gemini LLM Provider Credentials
GEMINI_API_KEY="your-gemini-api-key"

# Other Configuration
UPLOAD_FOLDER="your-upload-folder-path"
```

### Usage
Start the backend server:
```powershell
uvicorn main:app --reload
```

---

## Frontend
The frontend is built with Streamlit and provides a user-friendly interface for interacting with the RAG chatbot. Users can upload PDF documents and ask questions directly from the browser. The frontend communicates with the backend to process documents and retrieve answers.

### Features
- Upload PDF files for processing
- Chat interface for Q/A
- Displays context-aware responses
- Connects to backend endpoints

### Usage
To run the frontend:
```powershell
streamlit run app.py
```
See `app.py` for implementation details.

---

## Workflow
1. The user uploads PDF documents via the frontend.
2. The backend processes and embeds documents into the vector database (Weaviate).
3. The user sends a question to the chatbot.
4. The backend retrieves relevant information using the RAG pipeline and generates a response using Gemini LLM.
5. The frontend displays the answer to the user.

---

## Technologies Used
- Python 3.11 – Core programming language
- FastAPI – Backend API server
- Streamlit – Frontend web application
- Weaviate – Vector database for similarity search
- Gemini (google-generativeai) – Language model integration
- LangChain (langchain_community, langchain_text_splitters) – Document loading and text splitting
- Sentence Transformers (sentence_transformers) – Text embedding
- PyMuPDF – PDF document loader via LangChain
- Pydantic – Data validation and settings management
- dotenv (python-dotenv) – Environment variable management
- tempfile – Temporary file handling
- JSON – Format for storing FAQs and context documents

