from deep_translator import GoogleTranslator

MAX_CHARS = 4500  # Google Translate limit per call


def translate_text(text: str, lang_code: str) -> str:
    """
    Translates text to the target language.
    lang_code: 'kn' for Kannada, 'hi' for Hindi
    """
    try:
        # Split into chunks if text is too long
        chunks = _split_text(text, MAX_CHARS)
        translated_chunks = []

        for chunk in chunks:
            if chunk.strip():
                translated = GoogleTranslator(
                    source='auto',
                    target=lang_code
                ).translate(chunk)
                translated_chunks.append(translated)

        return "\n".join(translated_chunks)

    except Exception as e:
        return f"⚠️ Translation failed. Error: {str(e)}\n\nTip: Check your internet connection."


def _split_text(text: str, max_chars: int) -> list:
    """Splits text into chunks under max_chars."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    while len(text) > max_chars:
        # Try to split at sentence boundary
        split_at = text.rfind('. ', 0, max_chars)
        if split_at == -1:
            split_at = max_chars
        chunks.append(text[:split_at + 1])
        text = text[split_at + 1:].strip()

    if text:
        chunks.append(text)

    return chunks
