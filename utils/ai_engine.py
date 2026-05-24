import os
from groq import Groq
import json

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MAX_CHARS = 3500


def summarize_document(text: str) -> str:
    try:
        prompt = f"""You are Jana Mitra — a legal literacy assistant for common Indian citizens.

Explain this document in very simple language. Imagine you are explaining to a person who has studied only up to Class 8.

DOCUMENT:
{text[:MAX_CHARS]}

Format your response EXACTLY like this (use these exact emoji headers):

📄 WHAT IS THIS DOCUMENT
[One simple sentence]

🔑 KEY POINTS
• [point in simple words]
• [point in simple words]
• [point in simple words]
• [more if needed]

📅 IMPORTANT DATES
• [date and what it means, or write: No specific dates mentioned]

✅ WHAT YOU SHOULD DO
• [clear action step, or: No action needed right now]

⚠️ BE CAREFUL ABOUT
• [risk or warning in simple words]

🛡️ YOUR RIGHTS
• [right in simple words]

Keep every bullet point SHORT — one line each. NO legal jargon."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900,
            temperature=0.2
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Could not generate summary. Error: {str(e)}\n\nPlease check your GROQ_API_KEY."


def get_glossary(summary_text: str) -> dict:
    """Extract difficult words from summary and return simple definitions."""
    try:
        prompt = f"""From the following text, find 6-10 difficult or legal/medical/technical words that a common person might not understand.

TEXT:
{summary_text[:2000]}

Return ONLY a valid JSON object like this (no extra text, no markdown):
{{"word1": "simple definition in one sentence", "word2": "simple definition", ...}}

Pick only words that actually appear in the text. Keep definitions very simple — for a Class 8 student."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.1
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except Exception:
        return {}


def answer_question(doc_text: str, question: str, chat_history: list = None) -> str:
    try:
        messages = [
            {
                "role": "system",
                "content": f"""You are Jana Mitra — a helpful legal literacy assistant for Indian citizens.
Answer based ONLY on the document below. If the answer is not in the document, say so clearly and give brief general guidance.
Keep answers simple and short — 3 to 5 sentences. Use bullet points (•) if listing multiple things and give every point in new line.


DOCUMENT:
{doc_text[:MAX_CHARS]}"""
            }
        ]

        if chat_history:
            for msg in chat_history[-6:]:
                messages.append(msg)

        messages.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=400,
            temperature=0.3
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
