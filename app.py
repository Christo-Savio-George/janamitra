import streamlit as st
#from utils.extractor import extract_text
from utils.ai_engine import summarize_document, answer_question
from utils.translator import translate_text
#from utils.tts import speak_text
import os

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NyayaVaani",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Hindi&family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main { background-color: #0f1117; }

    .hero-title {
        font-family: 'Tiro Devanagari Hindi', serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF9933 0%, #ffffff 50%, #138808 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }

    .hero-sub {
        color: #8b8fa8;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .card {
        background: #1a1d2e;
        border: 1px solid #2a2d3e;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .stat-card {
        background: linear-gradient(135deg, #1a1d2e, #12151f);
        border: 1px solid #FF993340;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
    }

    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FF9933;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #8b8fa8;
        margin-top: 0.2rem;
    }

    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #FF9933;
        margin-bottom: 0.5rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #1a1d2e;
        border-radius: 12px;
        padding: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #8b8fa8;
        padding: 8px 20px;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: #FF9933 !important;
        color: #000 !important;
        font-weight: 600;
    }

    div[data-testid="stFileUploader"] {
        background: #1a1d2e;
        border: 2px dashed #2a2d3e;
        border-radius: 12px;
        padding: 1rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #FF9933, #e6871f);
        color: #000;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        width: 100%;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px #FF993360;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #1a1d2e !important;
        border: 1px solid #2a2d3e !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    .chat-user {
        background: #FF993320;
        border-left: 3px solid #FF9933;
        padding: 0.8rem 1rem;
        border-radius: 0 10px 10px 0;
        margin: 0.5rem 0;
        color: #fff;
    }

    .chat-bot {
        background: #13803820;
        border-left: 3px solid #138038;
        padding: 0.8rem 1rem;
        border-radius: 0 10px 10px 0;
        margin: 0.5rem 0;
        color: #fff;
    }

    .badge {
        display: inline-block;
        background: #FF993320;
        color: #FF9933;
        border: 1px solid #FF993340;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }

    .footer {
        text-align: center;
        color: #3a3d4e;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #1a1d2e;
    }

    [data-testid="stSidebar"] {
        background: #12151f;
        border-right: 1px solid #1a1d2e;
    }

    .sidebar-logo {
        text-align: center;
        padding: 1rem 0 1.5rem 0;
    }

    .sidebar-logo-text {
        font-family: 'Tiro Devanagari Hindi', serif;
        font-size: 1.8rem;
        background: linear-gradient(135deg, #FF9933, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .sidebar-tagline {
        font-size: 0.72rem;
        color: #5a5d6e;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ─────────────────────────────────────────────────────────
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "translated" not in st.session_state:
    st.session_state.translated = ""
if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False

# ─── Demo Documents ─────────────────────────────────────────────────────────────
DEMO_DOCS = {
    "🏠 Rental Agreement": """RENTAL AGREEMENT

This Rental Agreement is entered into on the 1st day of April, 2025, between Mr. Ramesh Kumar (hereinafter referred to as the "Landlord") residing at 45, MG Road, Bengaluru - 560001, and Mr. Suresh Nayak (hereinafter referred to as the "Tenant") residing at 12, Brigade Road, Bengaluru - 560025.

WHEREAS the Landlord is the lawful owner of the premises situated at Flat No. 302, Sunrise Apartments, Koramangala, Bengaluru - 560034 (hereinafter referred to as the "Premises").

NOW THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:

1. TERM: The tenancy shall commence on April 1, 2025, and shall continue for a period of eleven (11) months, terminating on February 28, 2026, unless terminated earlier in accordance with the terms hereof.

2. RENT: The Tenant agrees to pay a monthly rent of Rs. 15,000 (Rupees Fifteen Thousand Only), payable on or before the 5th day of each calendar month.

3. SECURITY DEPOSIT: The Tenant shall pay a refundable security deposit of Rs. 45,000 (Rupees Forty-Five Thousand Only) prior to occupancy, which shall be returned within 30 days of vacation of premises, subject to deductions for damages if any.

4. UTILITIES: The Tenant shall be responsible for payment of electricity, water, and maintenance charges directly to the respective authorities.

5. TERMINATION: Either party may terminate this agreement by giving one (1) month's prior written notice to the other party.

6. SUBLETTING: The Tenant shall not sublet, assign or transfer the premises or any part thereof without prior written consent of the Landlord.

7. MAINTENANCE: The Tenant shall maintain the premises in good condition and shall not make any structural alterations without written permission.

8. DEFAULT: In case of default in payment of rent for two consecutive months, the Landlord shall have the right to terminate the tenancy and repossess the premises.""",

    "📋 Government Notice (RTI)": """OFFICE OF THE PUBLIC INFORMATION OFFICER
BRUHAT BENGALURU MAHANAGARA PALIKE (BBMP)
N.R. Square, Bengaluru - 560002

NOTICE NO: BBMP/RTI/2025/4521
DATE: 15th March 2025

TO: Shri. Venkatesh Murthy
    #23, 5th Cross, Rajajinagar
    Bengaluru - 560010

SUBJECT: Response to RTI Application dated 28th February 2025 under Right to Information Act, 2005

Sir/Madam,

With reference to your RTI application received on 28.02.2025, seeking information regarding the status of road repair works on 3rd Main Road, Rajajinagar, Bengaluru, the following information is hereby furnished:

1. INFORMATION REQUESTED: Status of road repair tender, contractor details, and completion timeline for 3rd Main Road, Rajajinagar.

2. INFORMATION PROVIDED:
   a) Tender No. BBMP/2024-25/ROADS/771 was awarded to M/s. Karnataka Constructions Pvt. Ltd. on 15.01.2025.
   b) Total contract value: Rs. 42,50,000 (Rupees Forty Two Lakhs Fifty Thousand Only).
   c) Stipulated date of completion: 30th June 2025.
   d) Current completion status as of 15.03.2025: 35% work completed.

3. FEES: The prescribed RTI fee of Rs. 10 has been received vide IPO No. 45231.

4. APPEAL RIGHTS: If you are not satisfied with this response, you may file a First Appeal before the First Appellate Authority within 30 days from receipt of this letter, as per Section 19(1) of the RTI Act, 2005.

Public Information Officer
BBMP, Bengaluru""",

    "🏥 Medical Consent Form": """INFORMED CONSENT FOR MEDICAL PROCEDURE

PATIENT NAME: Mrs. Lakshmi Devi
DATE OF BIRTH: 12/05/1975
HOSPITAL: City General Hospital, Bengaluru
DATE: 20th April 2025

I, the undersigned patient/guardian, hereby provide my informed consent for the following medical procedure:

PROCEDURE: Laparoscopic Cholecystectomy (Removal of Gallbladder)
SURGEON: Dr. Arvind Sharma, MS (General Surgery)

NATURE OF PROCEDURE:
Laparoscopic cholecystectomy is a minimally invasive surgical procedure performed under general anesthesia to remove the gallbladder through small incisions in the abdomen using a camera and specialized instruments.

RISKS AND COMPLICATIONS:
1. General anesthetic risks including allergic reactions
2. Bleeding requiring blood transfusion
3. Infection at surgical sites
4. Injury to bile duct, bowel, or blood vessels (rare)
5. Conversion to open surgery if complications arise
6. Deep vein thrombosis

BENEFITS:
Relief from gallstone-related pain, prevention of further complications, and faster recovery compared to open surgery.

ALTERNATIVES:
1. Continued medical management with medications
2. Open cholecystectomy (traditional surgery)
3. No treatment (with continued risk of complications)

PATIENT RIGHTS:
You have the right to withdraw consent at any time before the procedure commences. You may ask questions and receive complete information about your treatment.

I certify that I have read and understood the above information and voluntarily consent to the procedure."""
}

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-text">⚖️ NyayaVaani</div>
        <div class="sidebar-tagline">न्यायवाणी • ನ್ಯಾಯವಾಣಿ</div>
        <div class="sidebar-tagline">Your Rights. Your Language.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">📤 Upload Document</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "PDF or TXT file",
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        with st.spinner("Reading document..."):
            text = extract_text(uploaded_file)
            if text.strip():
                st.session_state.doc_text = text
                st.session_state.doc_loaded = True
                st.session_state.summary = ""
                st.session_state.messages = []
                st.session_state.translated = ""
                st.success(f"✅ Loaded! ({len(text)} chars)")
            else:
                st.error("Could not read text. Use a text-based PDF.")

    st.markdown("---")
    st.markdown('<p class="section-label">📋 Or Try a Demo</p>', unsafe_allow_html=True)
    demo_choice = st.selectbox("Choose demo document", list(DEMO_DOCS.keys()), label_visibility="collapsed")
    if st.button("Load Demo Document"):
        st.session_state.doc_text = DEMO_DOCS[demo_choice]
        st.session_state.doc_loaded = True
        st.session_state.summary = ""
        st.session_state.messages = []
        st.session_state.translated = ""
        st.success("✅ Demo loaded!")

    st.markdown("---")
    st.markdown('<p class="section-label">🌐 Translation Language</p>', unsafe_allow_html=True)
    lang_option = st.radio(
        "Language",
        ["Kannada (ಕನ್ನಡ)", "Hindi (हिंदी)"],
        label_visibility="collapsed"
    )
    lang_code = "kn" if "Kannada" in lang_option else "hi"

    st.markdown("---")
    st.markdown("""
    <div style="color:#3a3d4e; font-size:0.72rem; text-align:center;">
        <span class="badge">NLP Track</span><br><br>
        Built at Hackathon 2025<br>
        Team NyayaVaani
    </div>
    """, unsafe_allow_html=True)

# ─── Hero Header ────────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">⚖️ NyayaVaani</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Upload any legal or government document — we simplify it, translate it, and answer your questions.</p>', unsafe_allow_html=True)

# ─── Stats Row ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="stat-card"><div class="stat-number">80Cr+</div><div class="stat-label">Indians face legal language barriers</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-card"><div class="stat-number">22+</div><div class="stat-label">Languages spoken in India</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="stat-card"><div class="stat-number">3sec</div><div class="stat-label">To get a plain summary</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="stat-card"><div class="stat-number">Free</div><div class="stat-label">Always, for every citizen</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── No Doc Loaded ──────────────────────────────────────────────────────────────
if not st.session_state.doc_loaded:
    st.markdown("""
    <div class="card" style="text-align:center; padding: 3rem;">
        <div style="font-size:3rem;">📄</div>
        <h3 style="color:#ffffff; margin-top:1rem;">Upload a document or load a demo to begin</h3>
        <p style="color:#5a5d6e;">Supports rental agreements, government notices, RTI documents, medical forms, and more.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # ─── Tabs ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Summary", "💬 Ask Questions", "🌐 Translate", "📝 Raw Text"])

    # ── TAB 1: Summary ──────────────────────────────────────────────────────────
    with tab1:
        st.markdown('<p class="section-label">Plain Language Summary</p>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("✨ Generate Summary"):
                with st.spinner("Analyzing document..."):
                    st.session_state.summary = summarize_document(st.session_state.doc_text)

        if st.session_state.summary:
            st.markdown(f'<div class="card">{st.session_state.summary}</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown('<p class="section-label">🔊 Listen to Summary</p>', unsafe_allow_html=True)
            col_a, col_b = st.columns([1, 3])
            with col_a:
                if st.button("🔊 Play Audio"):
                    with st.spinner("Generating audio..."):
                        speak_text(st.session_state.summary)
        else:
            st.markdown("""
            <div class="card" style="text-align:center; padding:2rem; color:#5a5d6e;">
                Click <b style="color:#FF9933;">✨ Generate Summary</b> to get a plain-language explanation of your document.
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 2: Chatbot ──────────────────────────────────────────────────────────
    with tab2:
        st.markdown('<p class="section-label">Ask Anything About Your Document</p>', unsafe_allow_html=True)

        # Quick question buttons
        st.markdown("**Quick Questions:**")
        qcol1, qcol2, qcol3 = st.columns(3)
        quick_q = None
        with qcol1:
            if st.button("What are my rights?"):
                quick_q = "What are my rights mentioned in this document?"
        with qcol2:
            if st.button("What should I be careful about?"):
                quick_q = "What are the important things I should be careful about in this document?"
        with qcol3:
            if st.button("What are the key dates?"):
                quick_q = "What are the important dates and deadlines mentioned in this document?"

        # Chat display
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">⚖️ {msg["content"]}</div>', unsafe_allow_html=True)

        # Handle quick question
        if quick_q:
            st.session_state.messages.append({"role": "user", "content": quick_q})
            with st.spinner("Thinking..."):
                reply = answer_question(st.session_state.doc_text, quick_q)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        # Text input
        user_q = st.text_input("Type your question here...", key="chat_input", placeholder="e.g. Can the landlord evict me without notice?")
        ask_col, clear_col = st.columns([2, 1])
        with ask_col:
            if st.button("Ask ➤") and user_q.strip():
                st.session_state.messages.append({"role": "user", "content": user_q})
                with st.spinner("Finding answer..."):
                    reply = answer_question(st.session_state.doc_text, user_q)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
        with clear_col:
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.rerun()

    # ── TAB 3: Translation ──────────────────────────────────────────────────────
    with tab3:
        st.markdown(f'<p class="section-label">Translate to {lang_option.split(" ")[0]}</p>', unsafe_allow_html=True)

        if not st.session_state.summary:
            st.info("💡 Tip: Generate a Summary first, then translate it for best results. Or translate the raw document below.")

        t_col1, t_col2 = st.columns([1, 1])
        with t_col1:
            if st.button(f"🌐 Translate Summary"):
                source = st.session_state.summary if st.session_state.summary else st.session_state.doc_text
                with st.spinner(f"Translating to {lang_option}..."):
                    st.session_state.translated = translate_text(source, lang_code)

        if st.session_state.translated:
            st.markdown(f'<div class="card">{st.session_state.translated}</div>', unsafe_allow_html=True)
            if st.button("🔊 Listen in Regional Language"):
                with st.spinner("Generating audio..."):
                    speak_text(st.session_state.translated, lang=lang_code)
        else:
            st.markdown("""
            <div class="card" style="text-align:center; padding:2rem; color:#5a5d6e;">
                Click <b style="color:#FF9933;">🌐 Translate Summary</b> to get regional language translation.
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 4: Raw Text ─────────────────────────────────────────────────────────
    with tab4:
        st.markdown('<p class="section-label">Extracted Document Text</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><pre style="white-space:pre-wrap; color:#8b8fa8; font-size:0.85rem;">{st.session_state.doc_text[:3000]}{"..." if len(st.session_state.doc_text) > 3000 else ""}</pre></div>', unsafe_allow_html=True)
        st.caption(f"Total characters extracted: {len(st.session_state.doc_text)}")

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚖️ NyayaVaani — Because justice should speak your language<br>
    Built with ❤️ at Hackathon 2025 | NLP Track | Team NyayaVaani
</div>
""", unsafe_allow_html=True)
