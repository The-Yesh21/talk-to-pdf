"""
app.py — Streamlit frontend for Talk-to-PDF.
Premium dark-themed UI with animations and modern chat interface.
"""

import tempfile
import streamlit as st
from ingest import ingest_pdf
from retriever import retrieve_relevant_chunks
from llm import generate_answer

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Talk to your PDF",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Premium CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ──────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Keyframe Animations ─────────────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50%      { transform: scale(1.08); opacity: 1; }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%      { transform: translateY(-12px); }
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes dotBounce {
        0%, 80%, 100% { transform: scale(0); }
        40%           { transform: scale(1); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 5px rgba(102,126,234,0.4); }
        50%      { box-shadow: 0 0 20px rgba(102,126,234,0.8), 0 0 40px rgba(118,75,162,0.3); }
    }

    /* ── Global Styles ───────────────────────────────────────────────── */
    .stApp {
        background: linear-gradient(160deg, #0f0f1a 0%, #1a1a2e 40%, #16213e 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Sidebar ─────────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 30, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(102, 126, 234, 0.15) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #e0e0ff !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        letter-spacing: 0.02em;
    }

    /* ── Sidebar upload card ─────────────────────────────────────────── */
    .sidebar-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.08), rgba(118,75,162,0.08));
        border: 1px solid rgba(102,126,234,0.2);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        animation: fadeIn 0.6s ease;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .sidebar-card:hover {
        border-color: rgba(102,126,234,0.45);
        box-shadow: 0 4px 24px rgba(102,126,234,0.1);
    }

    /* ── Status badge ────────────────────────────────────────────────── */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 0.85rem;
        font-weight: 500;
        animation: fadeIn 0.5s ease;
        letter-spacing: 0.01em;
    }
    .status-ready {
        background: rgba(76, 175, 80, 0.12);
        color: #81c784;
        border: 1px solid rgba(76, 175, 80, 0.3);
        animation: glowPulse 3s ease-in-out infinite;
    }
    .status-waiting {
        background: rgba(255, 183, 77, 0.1);
        color: #ffb74d;
        border: 1px solid rgba(255, 183, 77, 0.3);
    }

    /* ── Hero / Welcome Section ──────────────────────────────────────── */
    .hero-container {
        text-align: center;
        padding: 60px 20px 40px;
        animation: fadeInUp 0.8s ease;
    }
    .hero-icon {
        font-size: 5rem;
        display: inline-block;
        animation: float 3.5s ease-in-out infinite;
        filter: drop-shadow(0 8px 24px rgba(102,126,234,0.3));
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #a78bfa 50%, #764ba2 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s linear infinite;
        margin: 20px 0 8px;
        line-height: 1.2;
    }
    .hero-subtitle {
        color: #9e9eb8;
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 40px;
        line-height: 1.5;
    }

    /* ── Steps cards ─────────────────────────────────────────────────── */
    .steps-row {
        display: flex;
        gap: 16px;
        justify-content: center;
        flex-wrap: wrap;
        margin: 10px 0 30px;
    }
    .step-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(102,126,234,0.15);
        border-radius: 16px;
        padding: 24px 20px;
        width: 175px;
        text-align: center;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease backwards;
    }
    .step-card:nth-child(1) { animation-delay: 0.15s; }
    .step-card:nth-child(2) { animation-delay: 0.3s; }
    .step-card:nth-child(3) { animation-delay: 0.45s; }
    .step-card:hover {
        transform: translateY(-6px);
        border-color: rgba(102,126,234,0.4);
        box-shadow: 0 8px 32px rgba(102,126,234,0.12);
        background: rgba(255,255,255,0.05);
    }
    .step-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .step-number {
        font-size: 0.7rem;
        font-weight: 600;
        color: #667eea;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 6px;
    }
    .step-label {
        color: #c8c8e0;
        font-size: 0.9rem;
        font-weight: 400;
        line-height: 1.4;
    }

    /* ── Chat header ─────────────────────────────────────────────────── */
    .chat-header {
        text-align: center;
        padding: 10px 0 6px;
        animation: fadeIn 0.5s ease;
    }
    .chat-header-title {
        font-size: 1.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .chat-header-sub {
        color: #7a7a96;
        font-size: 0.85rem;
        margin-top: 2px;
    }

    /* ── Chat messages ───────────────────────────────────────────────── */
    .stChatMessage {
        animation: fadeInUp 0.4s ease !important;
        border-radius: 16px !important;
        margin-bottom: 8px !important;
    }
    /* User bubble */
    .stChatMessage[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.08)) !important;
        border: 1px solid rgba(102,126,234,0.15) !important;
    }
    /* Assistant bubble */
    .stChatMessage[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }

    /* ── Chat input styling ──────────────────────────────────────────── */
    .stChatInput > div {
        border-radius: 16px !important;
        border: 1px solid rgba(102,126,234,0.25) !important;
        background: rgba(15,15,30,0.6) !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    .stChatInput > div:focus-within {
        border-color: rgba(102,126,234,0.6) !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1) !important;
    }
    .stChatInput textarea {
        color: #e0e0f0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Buttons ──────────────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102,126,234,0.4) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── File uploader ───────────────────────────────────────────────── */
    .stFileUploader {
        border-radius: 12px !important;
    }
    .stFileUploader > div > div {
        border-radius: 12px !important;
        border: 2px dashed rgba(102,126,234,0.3) !important;
        background: rgba(102,126,234,0.03) !important;
        transition: all 0.3s ease !important;
    }
    .stFileUploader > div > div:hover {
        border-color: rgba(102,126,234,0.5) !important;
        background: rgba(102,126,234,0.06) !important;
    }

    /* ── Spinner ──────────────────────────────────────────────────────── */
    .stSpinner > div {
        border-color: #667eea !important;
    }

    /* ── Divider ──────────────────────────────────────────────────────── */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.3), transparent);
        border: none;
        margin: 16px 0;
    }

    /* ── Footer ──────────────────────────────────────────────────────── */
    .app-footer {
        text-align: center;
        color: #4a4a64;
        font-size: 0.75rem;
        padding: 30px 0 15px;
        animation: fadeIn 1s ease;
    }

    /* ── Scrollbar ────────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(102,126,234,0.3);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(102,126,234,0.5); }

    /* ── Misc ─────────────────────────────────────────────────────────── */
    .block-container { max-width: 780px !important; }
    html { scroll-behavior: smooth; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state initialization ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_ingested" not in st.session_state:
    st.session_state.pdf_ingested = False
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗂️ Document Manager")
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Status badge
    if st.session_state.pdf_ingested:
        st.markdown(
            f'<div class="status-badge status-ready">'
            f'<span>●</span> PDF Ready — {st.session_state.chunk_count} chunks'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-badge status-waiting">'
            '<span>◯</span> Waiting for PDF'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")  # spacing

    # Upload area inside a card
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop your PDF here",
        type=["pdf"],
        help="Supports any PDF document. Text is extracted, chunked, and embedded for Q&A.",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None and not st.session_state.pdf_ingested:
        with st.spinner("🔮 Analyzing your document…"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                num_chunks = ingest_pdf(tmp_path)
                st.session_state.pdf_ingested = True
                st.session_state.pdf_name = uploaded_file.name
                st.session_state.chunk_count = num_chunks
                st.session_state.chat_history = []
                st.rerun()
            except Exception as e:
                st.error(f"❌ Ingestion failed: {e}")

    if st.session_state.pdf_ingested:
        st.markdown("")
        if st.button("🔄 Upload a different PDF"):
            st.session_state.pdf_ingested = False
            st.session_state.pdf_name = ""
            st.session_state.chunk_count = 0
            st.session_state.chat_history = []
            st.rerun()

    # Sidebar footer
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#5a5a78; font-size:0.78rem; text-align:center; padding:6px 0;">'
        '⚡ Powered by Cohere + ChromaDB'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Main Content ─────────────────────────────────────────────────────────────

if not st.session_state.pdf_ingested:
    # ── Welcome / Hero Screen ────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-icon">📄</div>
            <div class="hero-title">Talk to your PDF</div>
            <div class="hero-subtitle">
                Upload any PDF and start a conversation with <strong>Doxi</strong> 🤖<br>
                Your friendly PDF reading buddy — powered by AI.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Step cards
    st.markdown(
        """
        <div class="steps-row">
            <div class="step-card">
                <div class="step-icon">📤</div>
                <div class="step-number">Step 1</div>
                <div class="step-label">Upload a PDF from the sidebar</div>
            </div>
            <div class="step-card">
                <div class="step-icon">⚙️</div>
                <div class="step-number">Step 2</div>
                <div class="step-label">Wait while we process &amp; index it</div>
            </div>
            <div class="step-card">
                <div class="step-icon">💬</div>
                <div class="step-number">Step 3</div>
                <div class="step-label">Ask anything about its content</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-footer">Built with ❤️ using Streamlit · Cohere · ChromaDB</div>',
        unsafe_allow_html=True,
    )

else:
    # ── Chat Mode ────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="chat-header">
            <div class="chat-header-title">💬 Chat with Doxi</div>
            <div class="chat-header-sub">Reading <strong>{st.session_state.pdf_name}</strong> for you</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Display chat history using native chat_message
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "📄"):
            st.markdown(msg["content"])

    # Chat input
    user_query = st.chat_input("Ask Doxi anything about your PDF…")

    if user_query:
        # Show user message
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_query)

        # Generate answer
        with st.chat_message("assistant", avatar="📄"):
            with st.spinner("🔍 Searching & generating answer…"):
                chunks = retrieve_relevant_chunks(user_query)
                answer = generate_answer(user_query, chunks)
            st.markdown(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    # Footer
    st.markdown(
        '<div class="app-footer">Tip: Ask Doxi specific questions for the best answers! 🎯</div>',
        unsafe_allow_html=True,
    )
