import fitz
import pytesseract
from PIL import Image
import io


def extract_text(uploaded_file) -> str:
    try:
        file_type = uploaded_file.type

        if file_type == "text/plain":
            return uploaded_file.read().decode("utf-8").strip()

        if file_type == "application/pdf":
            file_bytes = uploaded_file.read()
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            full_text = ""
            for page_num, page in enumerate(doc):
                page_text = page.get_text().strip()
                if len(page_text) > 30:
                    full_text += f"\n[Page {page_num + 1}]\n{page_text}\n"
                else:
                    ocr_text = _ocr_page(page)
                    if ocr_text.strip():
                        full_text += f"\n[Page {page_num + 1}]\n{ocr_text}\n"
            doc.close()
            return full_text.strip()

        return ""
    except Exception as e:
        return f"Error reading file: {str(e)}"


def _ocr_page(page) -> str:
    try:
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))
        try:
            text = pytesseract.image_to_string(image, lang="eng+kan+hin")
        except Exception:
            text = pytesseract.image_to_string(image, lang="eng")
        return text
    except Exception as e:
        return f"[OCR failed: {str(e)}]"
