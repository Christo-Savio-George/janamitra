import streamlit as st
import os
import json
from dotenv import load_dotenv
load_dotenv()

from utils.extractor import extract_text
from utils.ai_engine import summarize_document, get_glossary, answer_question
from utils.translator import translate_text, LANGUAGES
from utils.tts import speak_text

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jana Mitra — जन मित्र",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700&family=Noto+Sans+Kannada:wght@400;600&family=Noto+Sans+Tamil:wght@400;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #e2e4ef;
}

/* ── Background ── */
.stApp {
    background: #080b14;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(255,140,50,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 100%, rgba(56,189,248,0.06) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(99,102,241,0.04) 0%, transparent 60%);
    min-height: 100vh;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO SECTION ── */
.hero {
    text-align: center;
    padding: 3.5rem 2rem 2rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,140,50,0.12);
    border: 1px solid rgba(255,140,50,0.3);
    color: #FF8C32;
    border-radius: 100px;
    padding: 5px 18px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    background: linear-gradient(135deg, #FF8C32 0%, #FFD580 35%, #fff 60%, #7dd3fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.hero-scripts {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin: 0.8rem 0 0.6rem;
}

.script-hi {
    font-family: 'Noto Sans Devanagari', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: rgba(255,140,50,0.85);
}

.script-kn {
    font-family: 'Noto Sans Kannada', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: rgba(255,213,100,0.7);
}

.script-ta {
    font-family: 'Noto Sans Tamil', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: rgba(125,211,252,0.7);
}

.script-sep {
    color: rgba(255,255,255,0.15);
    font-size: 1.2rem;
}

.hero-sub {
    font-size: 1rem;
    color: rgba(226,228,239,0.45);
    font-weight: 300;
    max-width: 520px;
    margin: 0.8rem auto 0;
    line-height: 1.6;
}

/* ── UPLOAD AREA (center) ── */
.upload-section {
    max-width: 680px;
    margin: 0 auto 2rem;
    padding: 0 1.5rem;
}

.upload-card {
    background: rgba(255,255,255,0.03);
    border: 2px dashed rgba(255,140,50,0.25);
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    transition: border-color 0.3s, background 0.3s;
    position: relative;
}

.upload-card:hover {
    border-color: rgba(255,140,50,0.5);
    background: rgba(255,140,50,0.03);
}

.upload-icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
    display: block;
}

.upload-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e4ef;
    margin-bottom: 0.4rem;
}

.upload-hint {
    font-size: 0.82rem;
    color: rgba(226,228,239,0.35);
    margin-bottom: 1.2rem;
}

/* Override Streamlit file uploader */
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stFileUploader"] > div {
    background: rgba(255,140,50,0.08) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 14px !important;
    padding: 0.7rem 1rem !important;
}

[data-testid="stFileDropzone"] {
    background: transparent !important;
    border: none !important;
}

/* ── OR DIVIDER ── */
.or-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.2rem 0;
    color: rgba(226,228,239,0.2);
    font-size: 0.78rem;
    letter-spacing: 0.08em;
}

.or-divider::before, .or-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ── DEMO BUTTONS ── */
.demo-grid {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    justify-content: center;
}

/* ── MAIN CONTENT AREA ── */
.content-wrap {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 1.5rem 3rem;
}

/* ── DOC STATUS BAR ── */
.doc-bar {
    background: rgba(74,222,128,0.06);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 14px;
    padding: 0.9rem 1.4rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.doc-bar-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: #4ade80;
}

.doc-bar-meta {
    font-size: 0.78rem;
    color: rgba(226,228,239,0.35);
    margin-top: 0.15rem;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
    padding: 5px !important;
    gap: 4px !important;
    margin-bottom: 1.5rem !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    color: rgba(226,228,239,0.4) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 10px 22px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF8C32, #e07010) !important;
    color: #000 !important;
    font-weight: 700 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #FF8C32, #d96b0a) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-size: 0.875rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.2) !important;
    letter-spacing: 0.01em !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.35) !important;
}

/* ── GLASS CARD ── */
.glass {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.8rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
}

.glass::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
}

/* ── SUMMARY BOX ── */
.summary-content {
    font-size: 0.95rem;
    line-height: 1.85;
    color: #cdd0e0;
}

.summary-content .sec-head {
    font-size: 0.95rem;
    font-weight: 700;
    color: #e2e4ef;
    margin-top: 1.2rem;
    margin-bottom: 0.4rem;
    display: block;
}

/* ── HOVER TOOLTIP for glossary ── */
.glossary-word {
    border-bottom: 1px dashed rgba(255,140,50,0.5);
    color: #FFD580;
    cursor: help;
    position: relative;
    display: inline-block;
}

.glossary-word .tooltip {
    visibility: hidden;
    opacity: 0;
    background: #1a1d2e;
    border: 1px solid rgba(255,140,50,0.3);
    color: #e2e4ef;
    font-size: 0.78rem;
    line-height: 1.4;
    border-radius: 10px;
    padding: 8px 12px;
    position: absolute;
    bottom: 130%;
    left: 50%;
    transform: translateX(-50%);
    width: 220px;
    z-index: 9999;
    transition: opacity 0.2s;
    pointer-events: none;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}

.glossary-word .tooltip::after {
    content: '';
    position: absolute;
    top: 100%; left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: rgba(255,140,50,0.3);
}

.glossary-word:hover .tooltip {
    visibility: visible;
    opacity: 1;
}

/* ── TRANSLATION BOX ── */
.translation-box {
    background: rgba(99,179,237,0.04);
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    line-height: 2;
    font-size: 1rem;
    color: #d0d1dc;
    margin-top: 1rem;
}

/* ── LANG SELECTOR ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e4ef !important;
}

/* ── CHAT ── */
.chat-user {
    background: rgba(255,140,50,0.07);
    border-left: 3px solid #FF8C32;
    padding: 0.9rem 1.2rem;
    border-radius: 0 14px 14px 0;
    margin: 0.7rem 0;
    font-size: 0.9rem;
    color: #e2e4ef;
}

.chat-bot {
    background: rgba(74,222,128,0.05);
    border-left: 3px solid #4ade80;
    padding: 0.9rem 1.2rem;
    border-radius: 0 14px 14px 0;
    margin: 0.7rem 0;
    font-size: 0.9rem;
    color: #cdd0e0;
    line-height: 1.7;
}

/* ── INPUT ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e4ef !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 0.7rem 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(255,140,50,0.4) !important;
    box-shadow: 0 0 0 2px rgba(255,140,50,0.08) !important;
}

/* ── EMPTY STATE ── */
.empty {
    text-align: center;
    padding: 4rem 2rem;
    color: rgba(226,228,239,0.2);
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 1.5rem;
    color: rgba(226,228,239,0.12);
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    border-top: 1px solid rgba(255,255,255,0.04);
}

/* ── Audio ── */
audio {
    width: 100%;
    height: 40px;
    border-radius: 12px;
    outline: none;
    margin-top: 0.5rem;
}

/* ── Spinner color ── */
.stSpinner > div { border-top-color: #FF8C32 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,140,50,0.25); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "doc_text": "",
        "doc_name": "",
        "doc_loaded": False,
        "summary": "",
        "glossary": {},
        "translated": "",
        "translated_lang": "",
        "messages": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def reset_doc():
    st.session_state.doc_text = ""
    st.session_state.doc_name = ""
    st.session_state.doc_loaded = False
    st.session_state.summary = ""
    st.session_state.glossary = {}
    st.session_state.translated = ""
    st.session_state.translated_lang = ""
    st.session_state.messages = []

# ─────────────────────────────────────────────────────────────────────────────
# DEMO DOCUMENTS
# ─────────────────────────────────────────────────────────────────────────────
DEMO_DOCS = {
    "🏠 Rental Agreement": {
        "name": "Rental Agreement",
        "text": """RENTAL AGREEMENT

This Rental Agreement is entered into on 1st April 2025, between Mr. Ramesh Kumar (Landlord), 45 MG Road, Bengaluru, and Mr. Suresh Nayak (Tenant), 12 Brigade Road, Bengaluru.

Property: Flat No. 302, Sunrise Apartments, Koramangala, Bengaluru - 560034.

1. TERM: April 1, 2025 to February 28, 2026 (11 months).

2. RENT: Rs. 15,000 per month, due on or before the 5th of each month. Late payment attracts 2% penalty per week.

3. SECURITY DEPOSIT: Rs. 45,000 refundable deposit, returned within 30 days of vacating, subject to deductions for damages.

4. UTILITIES: Tenant pays electricity, water, and maintenance directly.

5. TERMINATION: One month written notice required from either party.

6. SUBLETTING: Not permitted without written landlord consent.

7. MAINTENANCE: Tenant must maintain premises in good condition. No structural changes without written permission.

8. DEFAULT: Two consecutive months of unpaid rent gives Landlord the right to repossess the property.

9. DISPUTE RESOLUTION: Disputes shall be settled under the Bangalore Rent Control Act."""
    },
    "📋 RTI Government Notice": {
        "name": "BBMP RTI Response",
        "text": """OFFICE OF THE PUBLIC INFORMATION OFFICER
BRUHAT BENGALURU MAHANAGARA PALIKE (BBMP)
N.R. Square, Bengaluru - 560002
NOTICE NO: BBMP/RTI/2025/4521 | DATE: 15 March 2025

TO: Shri Venkatesh Murthy, #23 5th Cross, Rajajinagar, Bengaluru - 560010

SUBJECT: Response to RTI Application dated 28 February 2025 under the Right to Information Act, 2005.

Information provided regarding road repair works on 3rd Main Road, Rajajinagar:

1. Tender BBMP/2024-25/ROADS/771 awarded to M/s Karnataka Constructions Pvt. Ltd. on 15 January 2025.
2. Contract value: Rs. 42,50,000.
3. Stipulated completion date: 30 June 2025.
4. Completion status as of 15 March 2025: 35%.
5. Inspection records available for public viewing at BBMP Zone Office, Rajajinagar.

RTI Fee of Rs. 10 received via IPO No. 45231.

APPEAL: If unsatisfied, file a First Appeal to the First Appellate Authority within 30 days per Section 19(1) of the RTI Act, 2005.

Public Information Officer, BBMP Bengaluru."""
    },
    "🏥 Medical Consent Form": {
        "name": "Surgical Consent Form",
        "text": """INFORMED CONSENT FOR MEDICAL PROCEDURE

Patient: Mrs. Lakshmi Devi | DOB: 12/05/1975
Hospital: City General Hospital, Bengaluru | Date: 20 April 2025
Procedure: Laparoscopic Cholecystectomy (gallbladder removal)
Surgeon: Dr. Arvind Sharma, MS General Surgery

PROCEDURE: Minimally invasive surgery under general anesthesia. Small incisions made in abdomen. Camera and instruments used to remove gallbladder.

RISKS: Anesthetic reactions, bleeding requiring transfusion, infection, bile duct injury (rare, <1%), conversion to open surgery, blood clots.

BENEFITS: Permanent relief from gallstone pain, faster recovery than open surgery, short hospital stay (1-2 days).

ALTERNATIVES: (1) Medications — manages symptoms but does not remove stones. (2) Open surgery — higher recovery time. (3) No treatment — risk of acute cholecystitis, pancreatitis.

PATIENT RIGHTS: You may withdraw consent at any time before surgery begins. You have the right to a second opinion, to ask questions, and to receive information in your preferred language.

DECLARATION: I confirm I understand the above and voluntarily consent to the procedure."""
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Build summary HTML with glossary tooltips
# ─────────────────────────────────────────────────────────────────────────────
def build_summary_html(summary: str, glossary: dict) -> str:
    """Replace difficult words in summary with hover tooltip spans."""
    import html as html_lib
    
    # Escape HTML first
    text = html_lib.escape(summary)
    
    # Re-apply emoji (html.escape won't touch them but restore newlines)
    text = text.replace("\n", "<br>")
    
    # Section headers — make them bold
    for emoji in ["📄", "🔑", "📅", "✅", "⚠️", "🛡️"]:
        text = text.replace(
            emoji,
            f'<br><span style="font-weight:700;color:#e2e4ef;font-size:0.95rem;">{emoji}'
        )
        # Close the span at the next <br>
    
    # Apply glossary tooltips (case-insensitive)
    if glossary:
        for word, definition in glossary.items():
            safe_def = html_lib.escape(definition)
            # Only replace whole words
            import re
            pattern = re.compile(r'\b(' + re.escape(html_lib.escape(word)) + r')\b', re.IGNORECASE)
            replacement = f'<span class="glossary-word">\\1<span class="tooltip">📖 {safe_def}</span></span>'
            text = pattern.sub(replacement, text, count=1)  # replace first occurrence only
    
    return f'<div class="summary-content">{text}</div>'

# ─────────────────────────────────────────────────────────────────────────────
# ── HERO SECTION ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🤝 AI Legal Literacy · NLP Track · Hackathon 2025</div>
    <h1 class="hero-title">Jana Mitra</h1>
    <div class="hero-scripts">
        <span class="script-hi">जन मित्र</span>
        <span class="script-sep">·</span>
        <span class="script-kn">ಜನ ಮಿತ್ರ</span>
        <span class="script-sep">·</span>
        <span class="script-ta">ஜன மித்ரா</span>
    </div>
    <center><p class="hero-sub">Upload any legal or government document. We simplify it, translate it, and answer your questions — in your language.</p></center>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ── UPLOAD SECTION (CENTER) ───────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.doc_loaded:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="upload-card">
        <span class="upload-icon">📄</span>
        <div class="upload-title">Upload your document</div>
        <div class="upload-hint">Supports PDF (text or scanned) and TXT files · Free · Secure</div>
    </div>
    """, unsafe_allow_html=True)

    # Center the file uploader
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        uploaded_file = st.file_uploader(
            "Upload",
            type=["pdf", "txt"],
            label_visibility="collapsed",
        )
        if uploaded_file:
            with st.spinner("📖 Reading document..."):
                extracted = extract_text(uploaded_file)
            if extracted and len(extracted.strip()) > 20:
                st.session_state.doc_text = extracted
                st.session_state.doc_name = uploaded_file.name
                st.session_state.doc_loaded = True
                st.rerun()
            else:
                st.error("Could not read text. Try a different file or a text-based PDF.")

    # OR divider + demo
    st.markdown('<div class="or-divider">or try a demo document</div>', unsafe_allow_html=True)

    dcol1, dcol2, dcol3 = st.columns(3)
    for col, (label, data) in zip([dcol1, dcol2, dcol3], DEMO_DOCS.items()):
        with col:
            if st.button(label, key=f"demo_{label}"):
                st.session_state.doc_text = data["text"]
                st.session_state.doc_name = data["name"]
                st.session_state.doc_loaded = True
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Feature pills
    st.markdown("""
    <div style="text-align:center; margin-top:2rem; display:flex; justify-content:center; gap:0.6rem; flex-wrap:wrap;">
        <span style="background:rgba(255,140,50,0.08);border:1px solid rgba(255,140,50,0.2);color:rgba(255,140,50,0.8);border-radius:100px;padding:5px 14px;font-size:0.75rem;font-weight:600;">📄 PDF &amp; Scanned OCR</span>
        <span style="background:rgba(255,140,50,0.08);border:1px solid rgba(255,140,50,0.2);color:rgba(255,140,50,0.8);border-radius:100px;padding:5px 14px;font-size:0.75rem;font-weight:600;">🤖 AI Summary</span>
        <span style="background:rgba(255,140,50,0.08);border:1px solid rgba(255,140,50,0.2);color:rgba(255,140,50,0.8);border-radius:100px;padding:5px 14px;font-size:0.75rem;font-weight:600;">🌐 12 Indian Languages</span>
        <span style="background:rgba(255,140,50,0.08);border:1px solid rgba(255,140,50,0.2);color:rgba(255,140,50,0.8);border-radius:100px;padding:5px 14px;font-size:0.75rem;font-weight:600;">🔊 Voice Readout</span>
        <span style="background:rgba(255,140,50,0.08);border:1px solid rgba(255,140,50,0.2);color:rgba(255,140,50,0.8);border-radius:100px;padding:5px 14px;font-size:0.75rem;font-weight:600;">💬 Ask AI</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ── MAIN CONTENT (after doc loaded) ──────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
else:
    st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

    # Doc status bar
    col_doc, col_clear = st.columns([5, 1])
    with col_doc:
        st.markdown(f"""
        <div class="doc-bar">
            <div>
                <div class="doc-bar-name">✅ {st.session_state.doc_name}</div>
                <div class="doc-bar-meta">{len(st.session_state.doc_text):,} characters extracted and ready</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_clear:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✕ New Doc"):
            reset_doc()
            st.rerun()

    # ── TABS ─────────────────────────────────────────────────────────────────
    tab_summary, tab_chat = st.tabs(["📄  Summary & Translation", "💬  Ask AI Assistant"])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — SUMMARY + TRANSLATION (combined)
    # ══════════════════════════════════════════════════════════════════════════
    with tab_summary:

        # Generate button at top
        if not st.session_state.summary:
            g1, g2, g3 = st.columns([1, 2, 1])
            with g2:
                if st.button("✨ Simplify This Document"):
                    with st.spinner("🤖 Analyzing and simplifying..."):
                        st.session_state.summary = summarize_document(st.session_state.doc_text)
                    with st.spinner("🔍 Finding difficult words..."):
                        st.session_state.glossary = get_glossary(st.session_state.summary)
                    st.rerun()

            st.markdown("""
            <div class="empty">
                <div style="font-size:2.5rem;margin-bottom:1rem;">🤖</div>
                <div style="font-size:1rem;font-weight:500;">Click the button above to simplify your document</div>
                <div style="font-size:0.85rem;margin-top:0.5rem;opacity:0.6;">AI will explain it in simple English — no legal jargon</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # ── SUMMARY ──────────────────────────────────────────────────────
            # Glossary hint
            if st.session_state.glossary:
                st.markdown("""
                <div style="background:rgba(255,213,100,0.06);border:1px solid rgba(255,213,100,0.15);
                            border-radius:10px;padding:0.6rem 1rem;font-size:0.8rem;
                            color:rgba(255,213,100,0.7);margin-bottom:1rem;">
                    💡 <b>Tip:</b> Hover over <span style="border-bottom:1px dashed rgba(255,140,50,0.5);
                    color:#FFD580;">highlighted words</span> to see their simple meaning.
                </div>
                """, unsafe_allow_html=True)

            # Summary with glossary tooltips
            summary_html = build_summary_html(st.session_state.summary, st.session_state.glossary)
            st.markdown(f'<div class="glass">{summary_html}</div>', unsafe_allow_html=True)

            # Audio row
            a1, a2, a3 = st.columns([1, 1, 2])
            with a1:
                if st.button("🔊 Listen (English)"):
                    with st.spinner("Generating audio..."):
                        speak_text(st.session_state.summary, lang="en")
            with a2:
                if st.button("🔄 Re-generate"):
                    st.session_state.summary = ""
                    st.session_state.glossary = {}
                    st.session_state.translated = ""
                    st.session_state.translated_lang = ""
                    st.rerun()

            # ── TRANSLATION (directly below summary) ─────────────────────────
            st.markdown("---")
            st.markdown("""
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;
                        text-transform:uppercase;color:rgba(255,140,50,0.7);margin-bottom:0.8rem;">
                🌐 Translate to Regional Language
            </div>
            """, unsafe_allow_html=True)

            t1, t2, t3 = st.columns([2, 1, 1])
            with t1:
                lang_label = st.selectbox(
                    "Language",
                    list(LANGUAGES.keys()),
                    label_visibility="collapsed"
                )
            lang_code = LANGUAGES.get(lang_label)

            with t2:
                translate_btn = st.button("🌐 Translate")
            with t3:
                if st.session_state.translated and st.session_state.translated_lang == lang_code:
                    st.markdown('<div style="padding-top:0.65rem;font-size:0.8rem;color:#4ade80;">✓ Ready</div>', unsafe_allow_html=True)

            if translate_btn:
                if not lang_code:
                    st.warning("Please select a language first.")
                else:
                    with st.spinner(f"Translating to {lang_label.split('(')[0].strip()}..."):
                        result = translate_text(st.session_state.summary, lang_code)
                        st.session_state.translated = result
                        st.session_state.translated_lang = lang_code

            # Show translation
            if st.session_state.translated and st.session_state.translated_lang == lang_code:
                st.markdown(f'<div class="translation-box">{st.session_state.translated}</div>', unsafe_allow_html=True)

                # Audio for translation
                b1, b2 = st.columns([1, 3])
                with b1:
                    if st.button(f"🔊 Listen"):
                        with st.spinner("Generating regional audio..."):
                            speak_text(st.session_state.translated, lang=lang_code)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — AI ASSISTANT (fully dynamic, uses uploaded doc)
    # ══════════════════════════════════════════════════════════════════════════
    with tab_chat:
        st.markdown("""
        <div style="font-size:0.82rem;color:rgba(226,228,239,0.35);margin-bottom:1rem;">
            Ask anything about your document. The AI reads your uploaded file and answers from it.
        </div>
        """, unsafe_allow_html=True)

        # Quick question chips
        st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,140,50,0.6);margin-bottom:0.6rem;">Quick Questions</div>', unsafe_allow_html=True)
        q1, q2, q3, q4 = st.columns(4)
        quick = None
        with q1:
            if st.button("🛡️ My rights"):
                quick = "What are my rights in this document? Explain simply."
        with q2:
            if st.button("⚠️ Key risks"):
                quick = "What are the important risks or warnings I should know about?"
        with q3:
            if st.button("📅 Important dates"):
                quick = "What are all the important dates and deadlines in this document?"
        with q4:
            if st.button("✅ What to do"):
                quick = "What actions do I need to take based on this document?"

        st.markdown("<br>", unsafe_allow_html=True)

        # Display chat history
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">🧑&nbsp;&nbsp;{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">🤝&nbsp;&nbsp;{msg["content"]}</div>', unsafe_allow_html=True)

        # Handle quick question
        if quick:
            st.session_state.messages.append({"role": "user", "content": quick})
            with st.spinner("Reading your document..."):
                reply = answer_question(
                    st.session_state.doc_text,
                    quick,
                    [m for m in st.session_state.messages if m["role"] != "system"][:-1]
                )
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        # Type question
        i1, i2, i3 = st.columns([5, 1, 1])
        with i1:
            user_q = st.text_input(
                "Question",
                placeholder="e.g. Can the landlord increase rent during the agreement?",
                label_visibility="collapsed"
            )
        with i2:
            ask_btn = st.button("Ask ➤")
        with i3:
            if st.button("🗑️ Clear"):
                st.session_state.messages = []
                st.rerun()

        if ask_btn and user_q.strip():
            st.session_state.messages.append({"role": "user", "content": user_q})
            with st.spinner("Finding answer in your document..."):
                reply = answer_question(
                    st.session_state.doc_text,
                    user_q,
                    [m for m in st.session_state.messages][:-1]
                )
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align:center;padding:2.5rem;color:rgba(226,228,239,0.18);font-size:0.85rem;">
                Use the quick buttons above, or type any question below
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🤝 Jana Mitra &nbsp;·&nbsp; जन मित्र &nbsp;·&nbsp; ಜನ ಮಿತ್ರ &nbsp;·&nbsp;
    Because every citizen deserves to understand their rights &nbsp;·&nbsp;
    Hackathon 2025 &nbsp;·&nbsp; NLP Track &nbsp;·&nbsp; RNSIT Bengaluru
</div>
""", unsafe_allow_html=True)
