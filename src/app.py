import streamlit as st
from ocr import extract_text
from langdetect import detect
from document_classifier import classify_document
from information_extractor import extract_information
from summarizer import generate_summary
from ner_extractor import extract_entities
from question_answering import answer_question
from pdf_extractor import extract_pdf_text
from semantic_search import build_index, search
from s3_upload import upload_file

# =========================

# PAGE CONFIG

# =========================

st.set_page_config(
page_title="DocuSense AI",
page_icon="📄",
layout="wide"
)

# =========================

# CUSTOM CSS

# =========================

st.markdown("""

<style>

.main {
    background-color: #0f172a;
}

.big-title {
    text-align:center;
    color:#38bdf8;
    font-size:50px;
    font-weight:bold;
}

.subtitle {
    text-align:center;
    color:white;
    font-size:18px;
    margin-bottom:20px;
}

.result-card {
    padding:15px;
    border-radius:10px;
    background:#1e293b;
    border-left:5px solid #38bdf8;
    margin-bottom:10px;
}

</style>

""", unsafe_allow_html=True)

# =========================

# SIDEBAR

# =========================

st.sidebar.title("📄 DocuSense AI")

st.sidebar.info("""
Features

✅ OCR

✅ PDF Processing

✅ Language Detection

✅ Document Classification

✅ Information Extraction

✅ AI Summary

✅ Named Entity Recognition

✅ Question Answering

✅ Semantic Search
""")

# =========================

# HEADER

# =========================

st.markdown("""

<div class='big-title'>
📄 DocuSense AI
</div>

<div class='subtitle'>
Multilingual Document Intelligence Platform
</div>
""", unsafe_allow_html=True)

# =========================

# FILE UPLOAD

# =========================

uploaded_file = st.file_uploader(
"Upload Document",
type=["png", "jpg", "jpeg", "pdf"]
)

if uploaded_file:


# =========================
# PREVIEW
# =========================

    if uploaded_file.name.lower().endswith(".pdf"):

        st.success("📄 PDF uploaded successfully")

        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        upload_file("temp.pdf")   # Upload to Amazon S3

        text = extract_pdf_text("temp.pdf")

    else:

        st.image(
            uploaded_file,
            caption="Uploaded Document",
            use_container_width=True
        )

        with open("temp_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())

        upload_file("temp_image.png")   # Upload image to S3

        text = extract_text("temp_image.png")

    # =========================
    # PROCESSING
    # =========================

    entities = extract_entities(text)

    summary = generate_summary(text)

    info = extract_information(text)

    document_type = classify_document(text)

    index, chunks = build_index(text)

    # =========================
    # LANGUAGE
    # =========================

    try:
        language = detect(text)

    except:
        language = "Unknown"

    # =========================
    # METRICS
    # =========================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Document Type",
            document_type
        )

    with col2:
        st.metric(
            "Language",
            language
        )

    with col3:
        st.metric(
            "Characters",
            len(text)
        )

    # =========================
    # SUMMARY
    # =========================

    st.subheader("🤖 AI Summary")

    st.markdown(
        f"""
        <div class='result-card'>
        {summary}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # EXTRACTED INFORMATION
    # =========================

    st.subheader("📌 Extracted Information")

    if info:

        for key, value in info.items():

            st.write(f"### {key}")

            for item in value:
                st.write(item)

    else:
        st.warning("No structured information found")

    # =========================
    # TABS
    # =========================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📄 Extracted Text",
            "🏷️ Named Entities",
            "❓ Ask Questions",
            "🔍 Semantic Search"
        ]
    )

    # =========================
    # TAB 1 - OCR TEXT
    # =========================

    with tab1:

        st.text_area(
            "OCR Output",
            text,
            height=400
        )

    # =========================
    # TAB 2 - ENTITIES
    # =========================

    with tab2:

        if entities:

            for entity in entities:

                st.markdown(
                    f"""
                    <div class='result-card'>
                    <b>{entity['label']}</b> :
                    {entity['text']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.warning("No entities found")

    # =========================
    # TAB 3 - QA
    # =========================

    with tab3:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input(
            "Ask about the document..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):
                st.markdown(question)

            results = search(
                question,
                index,
                chunks
            )

            context = " ".join(results)

            answer = answer_question(question, context)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            with st.chat_message("assistant"):
                st.markdown(answer)


    # =========================
    # TAB 4 - SEARCH
    # =========================

    with tab4:

        search_query = st.text_input(
            "Search document by meaning"
        )

        if search_query:

            results = search(
                search_query,
                index,
                chunks
            )

            st.subheader("📋 Search Results")

            for result in results:

                st.markdown(
                    f"""
                    <div class='result-card'>
                    {result}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
