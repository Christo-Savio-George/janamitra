import fitz  # PyMuPDF


def extract_text(uploaded_file) -> str:
    """
    Extract text from uploaded PDF or TXT file.
    Returns extracted text as a string.
    """
    try:
        file_type = uploaded_file.type

        # ── PDF ──────────────────────────────────────────────────────────────
        if file_type == "application/pdf":
            file_bytes = uploaded_file.read()
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page_text
            doc.close()
            return text.strip()

        # ── TXT ──────────────────────────────────────────────────────────────
        elif file_type == "text/plain":
            return uploaded_file.read().decode("utf-8").strip()

        else:
            return ""

    except Exception as e:
        return f"Error extracting text: {str(e)}"
