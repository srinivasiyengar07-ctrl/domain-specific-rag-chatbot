import os

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq

from prompt import SYSTEM_PROMPT


load_dotenv()


def split_documents(documents):
    """
    Split extracted PDF pages into smaller overlapping chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for document in documents:

        split_texts = text_splitter.split_text(
            document["text"]
        )

        for text in split_texts:

            chunks.append({
                "text": text,
                "metadata": document["metadata"]
            })

    return chunks


def generate_answer(question, retrieved_documents):
    """
    Generate an answer using only the retrieved PDF context.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured in the .env file."
        )

    context_parts = []

    for document in retrieved_documents:

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        page = document.metadata.get(
            "page",
            "Unknown"
        )

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{document.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=api_key
    )

    response = llm.invoke(prompt)

    return response.content