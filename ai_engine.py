import os
from groq import Groq

# ── Client Init ───────────────────────────────────────────────────────────────
# Reads GROQ_API_KEY from .env or Streamlit secrets automatically
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MAX_CHARS = 3000  # Safe limit for Groq free tier


def summarize_document(text: str) -> str:
    """
    Takes raw document text and returns a plain-language summary.
    """
    try:
        truncated = text[:MAX_CHARS]

        prompt = f"""You are NyayaVaani, a legal literacy assistant for common Indian citizens.

A user has uploaded the following document. Your job is to explain it in very simple language that even a person with basic education can understand.

Document:
{truncated}

Please provide:
1. **What this document is** (1 sentence)
2. **Key points to know** (bullet points, simple language)
3. **Important dates or deadlines** (if any)
4. **What the person must do** (action steps, if applicable)
5. **Rights of the person** (what they are entitled to)
6. **Risks or things to be careful about**

Use simple English. No legal jargon. Write as if you are explaining to a first-generation literate citizen."""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.3
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Could not generate summary. Error: {str(e)}\n\nPlease check your GROQ_API_KEY in the .env file."


def answer_question(doc_text: str, question: str) -> str:
    """
    Answers a user question based on the uploaded document.
    """
    try:
        truncated = doc_text[:MAX_CHARS]

        prompt = f"""You are NyayaVaani, a legal literacy assistant for common Indian citizens.

Based on the following document, answer the user's question in simple, clear language. 
If the answer is not in the document, say so honestly and give general guidance.

Document:
{truncated}

User's Question: {question}

Answer in 3-5 simple sentences. Use bullet points if listing multiple things.
Be helpful, honest, and clear. Avoid legal jargon."""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.3
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Could not answer question. Error: {str(e)}"