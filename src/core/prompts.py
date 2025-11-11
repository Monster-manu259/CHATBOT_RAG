# src/core/prompts.py

# Prompts for accurate chatbot responses tailored for document-based Q&A

SYSTEM_PROMPT = (
    "You are a helpful and professional assistant. "
    "Answer user questions using only the information provided in the context documents. "
    "Do not use external knowledge or make assumptions beyond the given context. "
    "If the answer is not found in the documents, state that clearly."
)

DOCUMENT_ANSWER_PROMPT = (
    "Instructions:\n"
    "- Carefully read all DOCUMENTS provided in the context.\n"
    "- Use relevant information from the documents to answer the user's question.\n"
    "- If multiple documents are relevant, combine their information for a complete answer.\n"
    "- Do not mention document numbers, titles, or sources in your answer.\n"
    "- If the answer is not found in any document, reply with: {fallback_message}\n"
    "- Do not include introductory phrases; answer the question directly.\n\n"
    "Context:\n{context}\n\n"
    "Question:\n{question}\n"
)

def get_system_prompt():
    return SYSTEM_PROMPT

def get_document_answer_prompt(context, question, answer, fallback_message):
    return DOCUMENT_ANSWER_PROMPT.format(
        context=context,
        question=question,
        answer=answer,
        fallback_message=fallback_message
    )