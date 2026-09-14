from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_vector_store(chunks):
    """
    Create embeddings and store them in FAISS.
    """

    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    return vector_store


def retrieve_documents(vector_store, question, k=4):
    """
    Retrieve the most relevant document chunks.
    """

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results