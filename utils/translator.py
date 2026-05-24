from deep_translator import GoogleTranslator
import streamlit as st

LANGUAGES = {
    "Select language...": None,
    "Kannada (ಕನ್ನಡ)": "kn",
    "Hindi (हिंदी)": "hi",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te",
    "Malayalam (മലയാളം)": "ml",
    "Marathi (मराठी)": "mr",
    "Bengali (বাংলা)": "bn",
    "Gujarati (ગુજરાતી)": "gu",
    "Punjabi (ਪੰਜਾਬੀ)": "pa",
    "Odia (ଓଡ଼ିଆ)": "or",
    "Assamese (অসমীয়া)": "as",
    "Urdu (اردو)": "ur",
}

MAX_CHARS = 4000


@st.cache_data(show_spinner=False)
def translate_text(summary_text: str, lang_code: str) -> str:
    """Translates only the AI summary. Skips if language unavailable."""
    if not summary_text or not lang_code:
        return ""
    try:
        clean = _clean_for_translation(summary_text)
        chunks = _chunk_text(clean, MAX_CHARS)
        parts = []
        for chunk in chunks:
            if chunk.strip():
                result = GoogleTranslator(source="auto", target=lang_code).translate(chunk)
                if result:
                    parts.append(result)
        return "\n".join(parts)
    except Exception as e:
        err = str(e).lower()
        if "no support" in err or "invalid" in err or "language" in err:
            return f"⚠️ This language is not available right now. Please try another."
        return f"⚠️ Translation failed: {str(e)}"


def _clean_for_translation(text: str) -> str:
    for sym in ["**", "__", "##", "# "]:
        text = text.replace(sym, "")
    return text


def _chunk_text(text: str, max_chars: int) -> list:
    if len(text) <= max_chars:
        return [text]
    chunks = []
    while len(text) > max_chars:
        split_at = text.rfind(". ", 0, max_chars)
        if split_at == -1:
            split_at = max_chars
        chunks.append(text[:split_at + 1])
        text = text[split_at + 1:].strip()
    if text:
        chunks.append(text)
    return chunks
