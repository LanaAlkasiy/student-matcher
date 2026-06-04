import fitz  # PyMuPDF


def extract_text_from_pdf(file_bytes):
    text = ""

    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")

        for page in pdf_document:
            text += page.get_text()

        pdf_document.close()
        return text.strip()

    except Exception as error:
        return f"Error reading PDF: {error}"