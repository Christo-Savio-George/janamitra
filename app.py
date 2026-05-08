import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def summarize_document(text):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{
            "role": "user",
            "content": f"Summarize this legal document in very simple English that a common person can understand. Use bullet points.\n\n{text[:3000]}"
        }]
    )
    return response.choices[0].message.content

def answer_question(doc_text, question):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{
            "role": "user",
            "content": f"Based on this document:\n{doc_text[:3000]}\n\nAnswer this question simply: {question}"
        }]
    )
    return response.choices[0].message.content