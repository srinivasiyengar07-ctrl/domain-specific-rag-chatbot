from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from every page of an uploaded PDF.
    Keeps document name and page number as metadata.
    """

    reader = PdfReader(uploaded_file)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        # Skip empty pages
        if not text or not text.strip():
            continue

        documents.append({
            "text": text.strip(),
            "metadata": {
                "source": uploaded_file.name,
                "page": page_number
            }
        })

    return documents