# Domain-Specific RAG Chatbot for PDF Question Answering

## Project Description

This project is a Domain-Specific Retrieval-Augmented Generation (RAG) Chatbot that allows users to upload PDF documents and ask questions about their content.

The system extracts text from uploaded PDFs, divides the text into smaller chunks, creates embeddings for those chunks, and stores them in a FAISS vector database.

When a user asks a question, the system retrieves the most relevant document chunks and provides them as context to a Large Language Model (LLM). The chatbot generates an answer using only the retrieved document content.

If the required information is not available in the uploaded documents, the chatbot refuses to invent an answer.

---

## Features

- Upload one or more PDF documents
- Extract text from PDF pages
- Preserve document name and page number
- Split documents into smaller overlapping chunks
- Generate embeddings using Sentence Transformers
- Store embeddings using FAISS
- Retrieve relevant document chunks
- Generate answers using Groq LLM
- Display source document and page number
- Refuse to answer when information is not available
- Chat history support
- Clear chat functionality
- Streamlit web interface

---

## Technologies Used

- Python
- Streamlit
- PyPDF
- LangChain
- LangChain Community
- LangChain Text Splitters
- Sentence Transformers
- FAISS
- Groq
- python-dotenv

---

## Project Structure

```text
domain_rag_chatbot/
│
├── app.py
├── rag_pipeline.py
├── document_loader.py
├── vector_store.py
├── prompt.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── documents/
│
├── vector_store/
│
└── tests/