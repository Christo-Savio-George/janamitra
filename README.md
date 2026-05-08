

# 🌍 ಜನಮಿತ್ರ | जनमित्र | Janamitra

**AI for Public Understanding**

*Making government and legal documents understandable for everyone.*

Built at **Hackathon 2025** · NLP Track · Team Janamitra  
RNS Institute of Technology, Bengaluru


## 📌 The Problem

Millions of Indians receive critical documents every day — government notices, rental agreements, legal forms, medical documents, and public circulars. Most are written in complex English or dense legal language that ordinary citizens struggle to understand.

This creates:
- Confusion and misinformation
- Fear and anxiety around legal obligations
- Unhealthy dependency on middlemen and brokers

**Janamitra bridges this gap.**

---

## 💡 What is Janamitra?

Janamitra (ಜನಮಿತ್ರ | जनमित्र — *"Friend of the People"*) is an AI-powered multilingual assistant that:

- 📄 **Simplifies** complex documents into plain, everyday language
- 💬 **Answers questions** about the document in natural language
- 🌐 **Translates** content into regional languages (Kannada, Hindi)
- 🤝 **Empowers** common citizens to understand their rights and responsibilities

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Document Upload | Upload TXT or PDF files directly |
| 🤖 AI Summarization | Simplifies complex text using Llama 3 via Groq |
| 💬 Smart Q&A | Ask any question about your uploaded document |
| 🌐 Regional Translation | Translate summaries to Kannada or Hindi |
| ⚡ Fast AI Inference | Powered by Groq API for low-latency responses |
| 🧠 Plain Language Output | Designed specifically for common citizens |

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| [Streamlit](https://streamlit.io/) | Frontend UI |
| [Groq API](https://groq.com/) | AI inference engine |
| [Llama 3](https://llama.meta.com/) | Summarization & Q&A |
| [PyMuPDF](https://pymupdf.readthedocs.io/) | PDF text extraction |
| [deep-translator](https://pypi.org/project/deep-translator/) | Regional language translation |
| Python | Backend logic |

---

## 📂 Project Structure

```
janamitra/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md
├── .env                    # API keys (not committed)
├── .gitignore
│
├── sample_pdfs/
│   ├── rental_agreement.pdf
│   └── govt_notice.pdf
│
└── utils/
    ├── extractor.py        # PDF/TXT text extraction
    ├── summarizer.py       # Llama 3 summarization via Groq
    ├── translator.py       # Regional language translation
    └── chatbot.py          # Document Q&A logic
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/janamitra.git
cd janamitra

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run the App

```bash
streamlit run app.py
```

Open your browser and go to `http://localhost:8501`.

---

## 📖 How to Use

1. **Upload** a government notice, rental agreement, or any legal document (PDF or TXT)
2. **Click Summarize** — Janamitra will instantly generate a plain-language explanation
3. **Ask questions** — Type anything like *"What is my last date to pay?"* or *"What are my rights here?"*
4. **Translate** — Switch the summary to Kannada or Hindi with one click

---

## 🗂️ Sample Documents

Try Janamitra with the included samples in the `sample_pdfs/` folder:

- `rental_agreement.pdf` — A typical residential rental agreement
- `govt_notice.pdf` — A sample government public notice

---

## 🌐 Supported Languages

| Language | Code |
|---|---|
| English | `en` |
| Kannada | `kn` |
| Hindi | `hi` |

*More regional languages coming soon.*

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve Janamitra:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 👥 Team Janamitra

Built with ❤️ at Hackathon 2025 — NLP Track  
**RNS Institute of Technology, Bengaluru**  
Department of Computer Science & Engineering


---

"When people understand their documents, they understand their rights."
