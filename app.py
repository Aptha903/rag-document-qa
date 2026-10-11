
import re
from pathlib import Path

import requests
import streamlit as st

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://127.0.0.1:8000"

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""

if "upload_status" not in st.session_state:
    st.session_state.upload_status = None

# ---------------- STYLING ----------------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.5rem;
        border: 1px solid rgba(128,128,128,0.3);
        border-radius: 18px;
        margin-bottom: 1.5rem;
    }
    .subtitle {
        color: #888888;
        font-size: 1rem;
    }
    div.stButton > button {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- HELPERS ----------------

def clean_filename(filename):
    filename = str(filename or "Unknown file")
    match = re.fullmatch(r"\[([^\]]+)\]\(mailto:[^)]+\)", filename)

    if match:
        filename = match.group(1)

    return Path(filename).name


def api_error_message(exc):
    try:
        if exc.response is not None:
            body = exc.response.json()

            if isinstance(body, dict) and body.get("detail"):
                return str(body["detail"])
    except (ValueError, requests.exceptions.RequestException):
        pass

    return str(exc)


def ask_question(question):
    question = question.strip()

    if not question:
        return

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    try:
        with st.spinner("Searching your study documents..."):
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question},
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()

        st.session_state.messages.append({
            "role": "assistant",
            "content": data.get("answer", "No answer returned."),
            "sources": data.get("sources", []),
        })

    except requests.exceptions.RequestException as exc:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Could not get an answer: {api_error_message(exc)}",
            "sources": [],
        })


def show_sources(sources):
    if not sources:
        st.caption("No source details returned.")
        return

    with st.expander(f"📚 Sources ({len(sources)})"):
        for number, source in enumerate(sources, start=1):
            filename = clean_filename(source.get("file"))
            page = source.get("page", "N/A")
            score = source.get("score", "N/A")

            st.markdown(f"**{number}. {filename}**")
            st.caption(f"Page: {page} · Relevance score: {score}")


def upload_pdf(uploaded_file):
    try:
        with st.spinner("Uploading and indexing your PDF..."):
            response = requests.post(
                f"{API_URL}/upload",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    )
                },
                timeout=300,
            )
            response.raise_for_status()
            result = response.json()

        st.session_state.upload_status = result

        st.success(
            f"Uploaded {result.get('filename', uploaded_file.name)} successfully."
        )

    except requests.exceptions.RequestException as exc:
        st.error(f"Upload failed: {api_error_message(exc)}")


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("📚 Study Assistant")
    st.caption("Your personal AI study companion")

    st.divider()
    st.subheader("📄 Add study notes")

    uploaded_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"],
        help="Text-based PDFs are supported. Scanned PDFs may require OCR.",
    )

    if st.button(
        "Upload and index PDF",
        type="primary",
        use_container_width=True,
        disabled=uploaded_file is None,
    ):
        upload_pdf(uploaded_file)

    if st.session_state.upload_status:
        result = st.session_state.upload_status
        st.caption(f"Last upload: {result.get('filename', 'PDF')}")
        st.caption(f"Pages read: {result.get('pages', 'N/A')}")
        st.caption(f"Chunks added: {result.get('chunks_added', 'N/A')}")

    st.divider()
    st.subheader("💡 Example questions")

    examples = [
        "What is NumPy broadcasting?",
        "What is a Python list?",
        "Explain NumPy masking.",
        "Summarize the main concepts in my notes.",
    ]

    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_question = example
            st.rerun()

    st.divider()

    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = ""
        st.rerun()

    st.caption("Clearing chat does not delete indexed documents.")


# ---------------- MAIN HEADER ----------------

st.markdown(
    """
    <div class="hero">
        <h1>📚 Your Study Assistant</h1>
        <p class="subtitle">
            Ask questions about your study notes, get AI-powered explanations,
            and explore the source pages behind each answer.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- OVERVIEW ----------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Questions asked",
        sum(1 for m in st.session_state.messages if m["role"] == "user"),
    )

with col2:
    st.metric(
        "Answers received",
        sum(1 for m in st.session_state.messages if m["role"] == "assistant"),
    )

st.divider()
st.subheader("💬 Ask your documents")

# ---------------- CHAT HISTORY ----------------

if not st.session_state.messages:
    st.info(
        "Welcome! Enter a question below or choose an example "
        "from the sidebar to get started."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            show_sources(message.get("sources", []))

# ---------------- QUESTION FORM ----------------

with st.form("question_form", clear_on_submit=True):
    question = st.text_input(
        "Your question",
        value=st.session_state.pending_question,
        placeholder="e.g. Explain NumPy broadcasting with an example",
    )

    submitted = st.form_submit_button(
        "Ask Question",
        type="primary",
        use_container_width=True,
    )

if submitted:
    st.session_state.pending_question = ""

    if question.strip():
        ask_question(question)
        st.rerun()
    else:
        st.warning("Please enter a question.")

# ---------------- FOOTER ----------------

st.divider()
st.caption(
    "AI-generated answers may contain mistakes. "
    "Check the cited source pages to verify important information."
)