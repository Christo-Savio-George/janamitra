import streamlit as st
from gtts import gTTS
import tempfile
import os

MAX_CHARS = 500  # Keep audio short for demo


def speak_text(text: str, lang: str = "en"):
    """
    Converts text to speech and plays it in Streamlit.
    lang: 'en' for English, 'kn' for Kannada, 'hi' for Hindi
    """
    try:
        # Trim to avoid very long audio
        clean_text = text[:MAX_CHARS].strip()

        # Remove markdown symbols that gTTS reads literally
        clean_text = clean_text.replace("**", "").replace("*", "").replace("#", "").replace("- ", "")

        # gTTS doesn't support Kannada well — fallback to English for 'kn'
        tts_lang = "hi" if lang == "kn" else lang

        tts = gTTS(text=clean_text, lang=tts_lang, slow=False)

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            tmp_path = tmp.name

        # Read and play in Streamlit
        with open(tmp_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")

        # Cleanup
        os.unlink(tmp_path)

        if lang == "kn":
            st.caption("ℹ️ Kannada audio uses Hindi TTS as fallback (gTTS limitation)")

    except Exception as e:
        st.error(f"⚠️ Audio generation failed: {str(e)}\n\nTip: Check your internet connection.")