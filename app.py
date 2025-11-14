import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("RAG Chatbot")

option = st.sidebar.selectbox("Choose an option:", ["Upload Data", "Q/A"])

if option == "Upload Data":
    st.header("Upload PDF Files")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            # Replace with your actual backend upload endpoint
            response = requests.post("http://localhost:8000/upload", files=files)
            if response.status_code == 200:
                st.success(f"Uploaded {uploaded_file.name} successfully!")
            else:
                st.error(f"Failed to upload {uploaded_file.name}.")

elif option == "Q/A":
    st.header("Ask a Question")
    user_input = st.text_input("Enter your question:")
    if st.button("Send"):
        if user_input:
            # Replace with your actual backend chat endpoint
            response = requests.post("http://localhost:8000/query", json={"query": user_input})
            if response.status_code == 200:
                st.write("Bot:", response.json().get("answer", "No answer returned."))
            else:
                st.write("Error communicating with backend.")
