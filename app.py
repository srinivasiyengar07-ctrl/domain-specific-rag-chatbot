import streamlit as st

from document_loader import extract_text_from_pdf
from rag_pipeline import split_documents, generate_answer
from vector_store import create_vector_store, retrieve_documents


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Domain-Specific RAG Chatbot",
    page_icon="📚",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.title("📚 Domain-Specific RAG Chatbot")

st.subheader("PDF Question Answering System")


# -----------------------------
# Initialize Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("📄 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


# -----------------------------
# Clear Chat
# -----------------------------

if st.sidebar.button("🧹 Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# -----------------------------
# Document Processing
# -----------------------------

if uploaded_files:

    st.success(
        f"{len(uploaded_files)} PDF file(s) uploaded successfully!"
    )

    st.subheader("Uploaded Documents")

    for file in uploaded_files:

        st.write(
            f"📄 {file.name}"
        )


    # -----------------------------
    # Process Documents
    # -----------------------------

    if st.button("🔍 Process & Chunk Documents"):

        with st.spinner(
            "📚 Processing documents and creating embeddings..."
        ):

            all_documents = []

            # Extract text from every PDF

            for file in uploaded_files:

                pages = extract_text_from_pdf(
                    file
                )

                all_documents.extend(
                    pages
                )


            # Split documents into chunks

            chunks = split_documents(
                all_documents
            )


            st.success(
                "Documents processed successfully!"
            )

            st.write(
                f"📄 Pages extracted: {len(all_documents)}"
            )

            st.write(
                f"🧩 Chunks created: {len(chunks)}"
            )


            # -----------------------------
            # Create FAISS Vector Store
            # -----------------------------

            vector_store = create_vector_store(
                chunks
            )

            st.session_state.vector_store = (
                vector_store
            )

            st.session_state.documents_processed = True


            st.success(
                "Embeddings created and stored in FAISS!"
            )


            st.success(
                "✅ Documents are ready! You can now ask questions."
            )


        # -----------------------------
        # Sample Chunk
        # -----------------------------

        st.subheader(
            "Sample Chunk"
        )

        if chunks:

            st.write(
                f"**Source:** "
                f"{chunks[0]['metadata']['source']}"
            )

            st.write(
                f"**Page:** "
                f"{chunks[0]['metadata']['page']}"
            )

            st.text(
                chunks[0]["text"]
            )


else:

    st.info(
        "Please upload one or more PDF documents "
        "from the sidebar."
    )


# -----------------------------
# Document Ready Status
# -----------------------------

if st.session_state.documents_processed:

    st.sidebar.success(
        "✅ Documents Ready"
    )


# -----------------------------
# Display Previous Chat Messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


        # Display sources for assistant

        if message["role"] == "assistant":

            sources = message.get(
                "sources",
                []
            )


            if sources:

                st.markdown(
                    "### 📚 Sources"
                )


                for source, page in sources:

                    st.write(
                        f"📄 **{source}** — Page {page}"
                    )


# -----------------------------
# Chat Interface
# -----------------------------

if st.session_state.vector_store is not None:

    question = st.chat_input(
        "Ask a question about your uploaded documents..."
    )


    if question:

        # -----------------------------
        # User Message
        # -----------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        with st.chat_message("user"):

            st.write(
                question
            )


        # -----------------------------
        # Retrieve Documents
        # -----------------------------

        results = retrieve_documents(
            st.session_state.vector_store,
            question,
            k=4
        )


        # -----------------------------
        # Generate Answer
        # -----------------------------

        try:

            answer = generate_answer(
                question,
                results
            )


            # -----------------------------
            # Collect Sources
            # -----------------------------

            sources = []

            not_found_message = (
                "I could not find this information in the uploaded documents."
            )


            # Only show sources when information
            # was found in the uploaded documents

            if not_found_message not in answer:

                for result in results:

                    source = result.metadata.get(
                        "source",
                        "Unknown"
                    )

                    page = result.metadata.get(
                        "page",
                        "Unknown"
                    )

                    source_item = (
                        source,
                        page
                    )


                    if source_item not in sources:

                        sources.append(
                            source_item
                        )


            # -----------------------------
            # Save Assistant Message
            # -----------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                }
            )


            # -----------------------------
            # Display Assistant Answer
            # -----------------------------

            with st.chat_message(
                "assistant"
            ):

                st.write(
                    answer
                )


                # -----------------------------
                # Display Sources
                # -----------------------------

                if sources:

                    st.markdown(
                        "### 📚 Sources"
                    )


                    for source, page in sources:

                        st.write(
                            f"📄 **{source}** — Page {page}"
                        )


        except Exception as e:

            st.error(
                f"Unable to generate answer: {e}"
            )


else:

    st.info(
        "Please upload and process PDF documents "
        "before asking questions."
    )