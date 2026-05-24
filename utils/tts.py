import streamlit as st
from gtts import gTTS
import tempfile
import os
import base64

GTTS_LANG_MAP = {
    "en": "en",
    "kn": "kn",
    "hi": "hi",
    "ta": "ta",
    "te": "te",
    "ml": "ml",
    "mr": "mr",
    "bn": "bn",
    "gu": "gu",
    "pa": "pa",
    "ur": "ur",
    "or": "hi",   # Odia fallback → Hindi
    "as": "bn",   # Assamese fallback → Bengali
}

MAX_TTS_CHARS = 700


def speak_text(text: str, lang: str = "en") -> bool:
    """
    Generates audio and returns base64 string for HTML audio player.
    Returns True on success, False on failure.
    """
    try:
        if not text or not text.strip():
            st.warning("No text to speak.")
            return False

        tts_lang = GTTS_LANG_MAP.get(lang, "en")
        clean = _clean_for_speech(text[:MAX_TTS_CHARS])

        if not clean.strip():
            st.warning("Nothing to speak after cleaning.")
            return False

        tts = gTTS(text=clean, lang=tts_lang, slow=False)

        # Write to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        tmp.close()

        # Read and encode as base64 for reliable HTML audio playback
        with open(tmp.name, "rb") as f:
            audio_data = f.read()
        os.unlink(tmp.name)

        # Use HTML audio tag — more reliable than st.audio in some browsers
        b64 = base64.b64encode(audio_data).decode()
        audio_html = f"""
        <audio controls autoplay style="width:100%; margin-top:0.5rem; border-radius:10px;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        return True

    except Exception as e:
        st.error(f"Audio error: {str(e)}")
        return False


def _clean_for_speech(text: str) -> str:
    subs = [
        ("📄", ""), ("🔑", ""), ("📅", ""), ("✅", ""),
        ("⚠️", ""), ("🛡️", ""), ("•", ""), ("**", ""),
        ("__", ""), ("##", ""), ("\n\n", ". "), ("\n", ". "),
        ("  ", " "), ("...", "."),
    ]
    for old, new in subs:
        text = text.replace(old, new)
    return text.strip()
