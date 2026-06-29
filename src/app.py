import streamlit as st
from datetime import datetime
import uuid

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
from dynamodb import save_document_metadata

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="DocuSense AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# THEME TOKENS
# =========================

THEMES = {
    "light": {
        "bg": "#f6f7fb",
        "sidebar_bg": "#ffffff",
        "card_bg": "#ffffff",
        "border": "#e8e9f1",
        "text": "#0f172a",
        "muted": "#6b7280",
        "primary": "#4f46e5",
        "primary_dark": "#3730a3",
        "primary_light": "#eef0fd",
        "shadow": "0 1px 3px rgba(15, 23, 42, 0.06)",
        "sidebar_text": "#0f172a",
    },
    "dark": {
        "bg": "#0b1120",
        "sidebar_bg": "#0f172a",
        "card_bg": "#151e32",
        "border": "#26324a",
        "text": "#e7eaf3",
        "muted": "#94a3b8",
        "primary": "#818cf8",
        "primary_dark": "#a5b4fc",
        "primary_light": "rgba(129,140,248,0.16)",
        "shadow": "0 1px 3px rgba(0, 0, 0, 0.35)",
        "sidebar_text": "#e7eaf3",
    },
}

FEATURES = [
    ("OCR", "Extract text from scanned images and documents", "🅰️", "#3b82f6"),
    ("Classification", "Automatically classify document types", "🏷️", "#10b981"),
    ("Information Extraction", "Extract important information and entities", "🧾", "#f59e0b"),
    ("Semantic Search", "Search documents by meaning, not just keywords", "🔍", "#8b5cf6"),
    ("Q&A", "Ask questions and get answers from your documents", "💬", "#06b6d4"),
    ("AI Summary", "Generate concise summaries of long documents", "📊", "#ec4899"),
]

BADGE_COLORS = {
    "id card": ("#ede9fe", "#6d28d9"),
    "certificate": ("#d1fae5", "#047857"),
    "invoice": ("#fef3c7", "#b45309"),
    "resume": ("#dbeafe", "#1d4ed8"),
    "contract": ("#fee2e2", "#b91c1c"),
}
DEFAULT_BADGE = ("#e5e7eb", "#374151")

NAV_PAGES = ["Home", "Upload Document", "My Documents", "Semantic Search", "Ask Questions", "Analytics"]
NAV_ICONS = ["🏠", "📤", "📁", "🔍", "💬", "📊"]

# =========================
# SESSION STATE INIT
# =========================

defaults = {
    "theme": "light",
    "page": "Home",
    "recent_docs": [],
    "docs_store": {},
    "active_doc_id": None,
    "last_uploaded_sig": None,
    "storage_bytes": 0,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

T = THEMES[st.session_state.theme]

# =========================
# CSS
# =========================

st.markdown(f"""
<style>

#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none; }}
[data-testid="stDecoration"] {{ display: none; }}
header[data-testid="stHeader"] {{ background: transparent; }}

html, body, [data-testid="stAppViewContainer"] {{
    background-color: {T['bg']};
    color: {T['text']};
}}

.block-container {{
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    background-color: {T['sidebar_bg']};
    border-right: 1px solid {T['border']};
}}
section[data-testid="stSidebar"] .block-container {{
    padding-top: 1.5rem;
}}

.ds-logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 6px 18px 6px;
}}
.ds-logo-icon {{
    width: 38px; height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, {T['primary']}, {T['primary_dark']});
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}}
.ds-logo-title {{
    font-size: 19px; font-weight: 800; color: {T['sidebar_text']}; line-height: 1.1;
}}
.ds-logo-title span {{ color: {T['primary']}; }}
.ds-logo-sub {{
    font-size: 11.5px; color: {T['muted']}; margin-top: 2px;
}}

.ds-section-label {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: {T['muted']};
    margin: 18px 6px 6px 6px;
}}

/* ---------- Sidebar nav buttons — highest specificity, must win ---------- */
section[data-testid="stSidebar"] div[data-testid="stButton"] > button,
section[data-testid="stSidebar"] div[data-testid="stButton"] > button:focus,
section[data-testid="stSidebar"] div[data-testid="stButton"] > button:active {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    color: {T['sidebar_text']} !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-size: 15px !important;
    padding: 8px 14px !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button * {{
    color: {T['sidebar_text']} !important;
}}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover,
section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover * {{
    background-color: {T['primary_light']} !important;
    color: {T['primary']} !important;
}}

.ds-storage-card {{
    background: {T['card_bg']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    padding: 14px 14px 12px 14px;
    margin: 16px 6px 10px 6px;
}}
.ds-storage-title {{
    font-size: 12.5px; font-weight: 700; color: {T['muted']};
    display: flex; align-items: center; gap: 6px; margin-bottom: 6px;
}}
.ds-storage-value {{ font-size: 13.5px; color: {T['text']}; margin-bottom: 8px; }}
.ds-progress-track {{
    width: 100%; height: 6px; border-radius: 4px;
    background: {T['border']}; overflow: hidden;
}}
.ds-progress-fill {{
    height: 100%; border-radius: 4px;
    background: linear-gradient(90deg, {T['primary']}, {T['primary_dark']});
}}
.ds-storage-pct {{ font-size: 11px; color: {T['muted']}; margin-top: 6px; }}

.ds-profile {{
    display: flex; align-items: center; gap: 10px;
    margin: 4px 6px 6px 6px; padding: 10px 8px;
    border-radius: 12px;
}}
.ds-avatar {{
    width: 34px; height: 34px; border-radius: 50%;
    background: {T['primary']}; color: white;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px; flex-shrink: 0;
}}
.ds-profile-name {{ font-size: 13.5px; font-weight: 700; color: {T['sidebar_text']}; }}
.ds-profile-role {{ font-size: 11.5px; color: {T['muted']}; display: flex; align-items: center; gap: 5px; }}
.ds-status-dot {{ width: 7px; height: 7px; border-radius: 50%; background: #22c55e; display: inline-block; }}

/* ---------- Top bar ---------- */
.ds-topbar-spacer {{ height: 4px; }}
div[data-testid="column"] .stButton > button {{
    border-radius: 10px;
}}

/* ---------- Hero ---------- */
.ds-hero {{ text-align: center; padding: 10px 0 6px 0; }}
.ds-hero h1 {{
    font-size: 38px; font-weight: 800; color: {T['text']}; margin-bottom: 4px;
}}
.ds-hero h1 span {{ color: {T['primary']}; }}
.ds-hero p.lead {{ font-size: 16px; color: {T['muted']}; margin: 4px 0 2px 0; }}
.ds-hero p.sub {{ font-size: 14px; color: {T['muted']}; max-width: 640px; margin: 0 auto 18px auto; }}

/* dropzone-style file uploader */
[data-testid="stFileUploaderDropzone"] {{
    background: {T['primary_light']} !important;
    border: 2px dashed {T['primary']} !important;
    border-radius: 14px !important;
    padding: 26px !important;
}}
[data-testid="stFileUploaderDropzone"] section {{
    background: transparent !important;
}}
[data-testid="stFileUploaderDropzone"] button {{
    background: {T['primary']} !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
}}
.ds-upload-hint {{
    text-align: center; font-size: 12.5px; color: {T['muted']}; margin-top: 8px;
}}

/* ---------- Feature cards ---------- */
.ds-feature-grid {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 14px;
    margin: 22px 0 28px 0;
}}
@media (max-width: 1100px) {{ .ds-feature-grid {{ grid-template-columns: repeat(3, 1fr); }} }}
@media (max-width: 700px) {{ .ds-feature-grid {{ grid-template-columns: repeat(2, 1fr); }} }}

.ds-feat-card {{
    background: {T['card_bg']};
    border: 1px solid {T['border']};
    border-radius: 14px;
    padding: 16px;
    box-shadow: {T['shadow']};
}}
.ds-feat-icon {{
    width: 36px; height: 36px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; margin-bottom: 10px;
}}
.ds-feat-title {{ font-weight: 700; font-size: 14.5px; color: {T['text']}; margin-bottom: 4px; }}
.ds-feat-desc {{ font-size: 12.5px; color: {T['muted']}; line-height: 1.35; }}

/* ---------- Generic cards / sections ---------- */
.ds-card {{
    background: {T['card_bg']};
    border: 1px solid {T['border']};
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: {T['shadow']};
    margin-bottom: 18px;
}}
.ds-section-title {{
    font-size: 16px; font-weight: 700; color: {T['text']};
    margin: 6px 0 12px 0; display: flex; align-items: center; gap: 8px;
}}
.ds-link {{ color: {T['primary']}; font-weight: 600; font-size: 13.5px; text-decoration: none; }}

/* metrics */
.ds-metric-label {{ font-size: 12.5px; color: {T['muted']}; margin-bottom: 2px; }}
.ds-metric-value {{ font-size: 26px; font-weight: 800; color: {T['text']}; }}

/* badges */
.ds-badge {{
    display: inline-block; padding: 3px 10px; border-radius: 7px;
    font-size: 12px; font-weight: 600;
}}

/* document row */
.ds-doc-row {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 4px; border-bottom: 1px solid {T['border']};
}}
.ds-doc-icon {{ font-size: 18px; }}
.ds-doc-name {{ font-size: 13.5px; font-weight: 600; color: {T['text']}; }}
.ds-table-head {{
    font-size: 11.5px; font-weight: 700; color: {T['muted']};
    letter-spacing: 0.04em; padding: 0 4px 8px 4px; border-bottom: 1px solid {T['border']};
}}

.ds-empty {{
    text-align: center; color: {T['muted']}; padding: 30px 10px; font-size: 13.5px;
}}

/* result card (summary) */
.ds-summary-box {{
    background: {T['primary_light']};
    border-left: 4px solid {T['primary']};
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 14.5px;
    line-height: 1.55;
    color: {T['text']};
}}

.ds-entity-chip {{
    display: inline-block; background: {T['primary_light']};
    border-radius: 9px; padding: 8px 12px; margin: 4px 6px 4px 0;
    font-size: 13px; color: {T['text']};
}}
.ds-entity-chip b {{ color: {T['primary_dark']}; }}

/* ---------- Chat bubbles ---------- */
[data-testid="stChatMessage"] {{
    background: {T['card_bg']};
    border: 1px solid {T['border']};
    border-radius: 12px;
}}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li {{
    color: {T['text']} !important;
}}

/* Fix chat avatar icons — prevent them inheriting the dark card-bg */
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessage"] img,
[data-testid="stChatMessage"] [data-baseweb="avatar"] {{
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

[data-testid="stChatInput"] {{
    background-color: {T['card_bg']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
}}
[data-testid="stChatInput"] textarea {{
    color: {T['text']} !important;
    background-color: transparent !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: {T['muted']} !important;
}}

/* ---------- Tabs ---------- */
[data-testid="stTabs"] button[role="tab"] * {{
    color: {T['muted']} !important;
    font-weight: 500 !important;
}}
[data-testid="stTabs"] button[aria-selected="true"] * {{
    color: {T['primary']} !important;
    font-weight: 700 !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-border"] {{
    background-color: {T['border']} !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
    background-color: {T['primary']} !important;
}}

/* ---------- Main-area buttons (explicitly NOT the sidebar) ---------- */
/* Using :not() to exclude sidebar so the sidebar rule above keeps priority */
:not(section[data-testid="stSidebar"]) div[data-testid="stButton"] > button,
:not(section[data-testid="stSidebar"]) div[data-testid="stPopover"] > button {{
    background-color: {T['card_bg']};
    color: {T['text']};
    border: 1px solid {T['border']};
    border-radius: 10px;
}}
:not(section[data-testid="stSidebar"]) div[data-testid="stButton"] > button *,
:not(section[data-testid="stSidebar"]) div[data-testid="stPopover"] > button * {{
    color: {T['text']} !important;
}}
:not(section[data-testid="stSidebar"]) div[data-testid="stButton"] > button:hover,
:not(section[data-testid="stSidebar"]) div[data-testid="stPopover"] > button:hover {{
    border-color: {T['primary']};
    color: {T['primary_dark']} !important;
}}
:not(section[data-testid="stSidebar"]) div[data-testid="stButton"] > button:hover *,
:not(section[data-testid="stSidebar"]) div[data-testid="stPopover"] > button:hover * {{
    color: {T['primary_dark']} !important;
}}

[data-testid="stPopoverBody"] {{
    background-color: {T['card_bg']} !important;
    border: 1px solid {T['border']} !important;
}}
[data-testid="stPopoverBody"] * {{
    color: {T['text']} !important;
}}

</style>
""", unsafe_allow_html=True)


# =========================
# HELPERS
# =========================

def badge_html(label):
    bg, fg = BADGE_COLORS.get(str(label).strip().lower(), DEFAULT_BADGE)
    return f"<span class='ds-badge' style='background:{bg};color:{fg};'>{label}</span>"


def new_doc_id():
    return uuid.uuid4().hex[:10]


def process_uploaded_file(uploaded_file):
    """Runs the full processing pipeline and caches results in session state."""

    if uploaded_file.name.lower().endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        s3_key = upload_file("temp.pdf")
        text = extract_pdf_text("temp.pdf")
        preview_path = "temp.pdf"
    else:
        with open("temp_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        s3_key = upload_file("temp_image.png")
        text = extract_text("temp_image.png")
        preview_path = "temp_image.png"

    entities = extract_entities(text)
    summary = generate_summary(text)
    info = extract_information(text)
    document_type = classify_document(text)
    index, chunks = build_index(text)

    try:
        language = detect(text)
    except Exception:
        language = "Unknown"

    save_document_metadata(
        filename=uploaded_file.name,
        language=language,
        document_type=document_type,
        s3_key=s3_key,
    )

    doc_id = new_doc_id()
    st.session_state.docs_store[doc_id] = {
        "name": uploaded_file.name,
        "preview_path": preview_path,
        "is_pdf": uploaded_file.name.lower().endswith(".pdf"),
        "text": text,
        "entities": entities,
        "summary": summary,
        "info": info,
        "document_type": document_type,
        "language": language,
        "index": index,
        "chunks": chunks,
        "messages": [],
        "search_results": [],
    }
    st.session_state.recent_docs.insert(0, {
        "id": doc_id,
        "name": uploaded_file.name,
        "type": document_type,
        "language": language,
        "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "chars": len(text),
    })
    st.session_state.storage_bytes += uploaded_file.size
    return doc_id


# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown(f"""
    <div class="ds-logo">
        <div class="ds-logo-icon">📄</div>
        <div>
            <div class="ds-logo-title">DocuSense <span>AI</span></div>
            <div class="ds-logo-sub">AI-Powered Document Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    current_main_page = st.session_state.page if st.session_state.page in NAV_PAGES else "Home"

    for label, icon in zip(NAV_PAGES, NAV_ICONS):
        nav_key = f"nav_btn_{label.replace(' ', '_')}"
        if st.button(f"{icon}  {label}", key=nav_key, use_container_width=True):
            st.session_state.page = label
            st.rerun()

    # Highlight the active nav item
    active_key = f"nav_btn_{current_main_page.replace(' ', '_')}"
    st.markdown(f"""
    <style>
    .st-key-{active_key} div[data-testid="stButton"] button,
    .st-key-{active_key} div[data-testid="stButton"] button * {{
        background-color: {T['primary_light']} !important;
        color: {T['primary']} !important;
        font-weight: 700 !important;
        border-color: {T['primary_light']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='ds-section-label'>SYSTEM</div>", unsafe_allow_html=True)
    if st.button("⚙️  Settings", use_container_width=True, key="nav_settings"):
        st.session_state.page = "Settings"
        st.rerun()
    if st.button("↩️  Logout", use_container_width=True, key="nav_logout"):
        st.session_state.page = "Logout"
        st.rerun()

    storage_mb = st.session_state.storage_bytes / (1024 * 1024)
    quota_gb = 5
    pct = min((storage_mb / (quota_gb * 1024)) * 100, 100) if storage_mb else 0.0
    st.markdown(f"""
    <div class="ds-storage-card">
        <div class="ds-storage-title">☁️ STORAGE USAGE</div>
        <div class="ds-storage-value">{storage_mb:.1f} MB / {quota_gb} GB</div>
        <div class="ds-progress-track"><div class="ds-progress-fill" style="width:{max(pct, 1.2):.2f}%;"></div></div>
        <div class="ds-storage-pct">{pct:.2f}% used</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ds-profile">
        <div class="ds-avatar">G</div>
        <div>
            <div class="ds-profile-name">Guest User</div>
            <div class="ds-profile-role"><span class="ds-status-dot"></span> Online</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# TOP BAR
# =========================

top_l, top_r1, top_r2 = st.columns([6, 1.1, 1])
with top_r1:
    if st.button("🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode",
                 use_container_width=True, key="theme_toggle"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()
with top_r2:
    with st.popover("❔ Help", use_container_width=True):
        st.markdown("""
**Getting started**
1. Go to **Home** and drop an image or PDF in the upload box.
2. DocuSense AI runs OCR, classification, extraction, NER, and summarization automatically.
3. Use **Ask Questions** or **Semantic Search** to dig into the document.
4. Find every document you've processed under **My Documents**.
        """)

st.markdown("<div class='ds-topbar-spacer'></div>", unsafe_allow_html=True)


# =========================
# SHARED RENDER PIECES
# =========================

def render_recent_documents_table(limit=None, key_prefix="home"):
    docs = st.session_state.recent_docs
    docs_to_show = docs[:limit] if limit else docs

    if not docs_to_show:
        st.markdown("<div class='ds-empty'>No documents yet — upload one above to get started.</div>",
                    unsafe_allow_html=True)
        return

    h1, h2, h3, h4, h5 = st.columns([3.2, 1.4, 1, 1.6, 1.4])
    for col, label in zip((h1, h2, h3, h4, h5), ("Document Name", "Type", "Language", "Upload Time", "Actions")):
        col.markdown(f"<div class='ds-table-head'>{label}</div>", unsafe_allow_html=True)

    for doc in docs_to_show:
        c1, c2, c3, c4, c5 = st.columns([3.2, 1.4, 1, 1.6, 1.4])
        icon = "📕" if doc["name"].lower().endswith(".pdf") else "🖼️"
        with c1:
            st.markdown(
                f"<div class='ds-doc-row' style='border-bottom:none;'>"
                f"<span class='ds-doc-icon'>{icon}</span>"
                f"<span class='ds-doc-name'>{doc['name']}</span></div>",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(f"<div style='padding-top:8px;'>{badge_html(doc['type'])}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='padding-top:10px;'>{doc['language']}</div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div style='padding-top:10px;font-size:13px;'>{doc['time']}</div>", unsafe_allow_html=True)
        with c5:
            a1, a2, a3 = st.columns(3)
            if a1.button("👁️", key=f"{key_prefix}_view_{doc['id']}"):
                st.session_state.active_doc_id = doc["id"]
                st.session_state.page = "Home"
                st.rerun()
            if a2.button("💬", key=f"{key_prefix}_chat_{doc['id']}"):
                st.session_state.active_doc_id = doc["id"]
                st.session_state.page = "Ask Questions"
                st.rerun()
            if a3.button("🗑️", key=f"{key_prefix}_del_{doc['id']}"):
                st.session_state.recent_docs = [d for d in st.session_state.recent_docs if d["id"] != doc["id"]]
                st.session_state.docs_store.pop(doc["id"], None)
                if st.session_state.active_doc_id == doc["id"]:
                    st.session_state.active_doc_id = None
                st.rerun()


def render_document_detail(doc_id, key_prefix="detail"):
    doc = st.session_state.docs_store.get(doc_id)
    if not doc:
        return

    st.markdown("<div class='ds-card'>", unsafe_allow_html=True)
    if doc["is_pdf"]:
        st.caption(f"📕 {doc['name']}")
    else:
        st.image(doc["preview_path"], caption=doc["name"], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='ds-card'><div class='ds-metric-label'>Document Type</div>"
                    f"<div class='ds-metric-value'>{doc['document_type']}</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='ds-card'><div class='ds-metric-label'>Language</div>"
                    f"<div class='ds-metric-value'>{doc['language']}</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='ds-card'><div class='ds-metric-label'>Characters</div>"
                    f"<div class='ds-metric-value'>{len(doc['text'])}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='ds-section-title'>🤖 AI Summary</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ds-summary-box'>{doc['summary']}</div>", unsafe_allow_html=True)
    st.write("")

    st.markdown("<div class='ds-section-title'>📌 Extracted Information</div>", unsafe_allow_html=True)
    if doc["info"]:
        st.markdown("<div class='ds-card'>", unsafe_allow_html=True)
        for key, value in doc["info"].items():
            st.markdown(f"**{key}**")
            for item in value:
                st.write(item)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No structured information found")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Extracted Text", "🏷️ Named Entities", "❓ Ask Questions", "🔍 Semantic Search"]
    )

    with tab1:
        st.text_area("OCR Output", doc["text"], height=350, key=f"{key_prefix}_text_{doc_id}")

    with tab2:
        if doc["entities"]:
            for entity in doc["entities"]:
                st.markdown(
                    f"<div class='ds-entity-chip'><b>{entity['label']}</b> : {entity['text']}</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.warning("No entities found")

    with tab3:
        render_qa_block(doc_id, key_prefix=f"{key_prefix}_tab")

    with tab4:
        render_search_block(doc_id, key_prefix=f"{key_prefix}_tab")


def render_qa_block(doc_id, key_prefix="qa"):
    doc = st.session_state.docs_store[doc_id]

    for message in doc["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask about the document...", key=f"{key_prefix}_chat_input_{doc_id}")

    if question:
        doc["messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        results = search(question, doc["index"], doc["chunks"])
        context = " ".join(results)
        answer = answer_question(question, context)

        doc["messages"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)


def render_search_block(doc_id, key_prefix="search"):
    doc = st.session_state.docs_store[doc_id]
    search_query = st.text_input("Search document by meaning", key=f"{key_prefix}_input_{doc_id}")

    if search_query:
        results = search(search_query, doc["index"], doc["chunks"])
        st.markdown("<div class='ds-section-title'>📋 Search Results</div>", unsafe_allow_html=True)
        for result in results:
            st.markdown(f"<div class='ds-card'>{result}</div>", unsafe_allow_html=True)


# =========================
# PAGE: HOME / UPLOAD DOCUMENT
# =========================

def render_home():
    st.markdown(f"""
    <div class="ds-hero">
        <h1>Welcome to <span>DocuSense AI</span></h1>
        <p class="lead">Your intelligent document analysis assistant</p>
        <p class="sub">Upload any document (Image or PDF) and let AI extract, analyze, and understand the content for you in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["png", "jpg", "jpeg", "pdf"],
        label_visibility="collapsed",
    )
    st.markdown("<div class='ds-upload-hint'>Supported formats: PNG, JPG, JPEG, PDF (Max 10MB)</div>",
                unsafe_allow_html=True)

    if uploaded_file is not None:
        sig = f"{uploaded_file.name}-{uploaded_file.size}"
        if st.session_state.last_uploaded_sig != sig:
            with st.spinner("Analyzing document..."):
                new_id = process_uploaded_file(uploaded_file)
            st.session_state.last_uploaded_sig = sig
            st.session_state.active_doc_id = new_id
            st.rerun()

    cards_html = "<div class='ds-feature-grid'>"
    for title, desc, emoji, color in FEATURES:
        cards_html += (
            f"<div class='ds-feat-card'>"
            f"<div class='ds-feat-icon' style='background:{color}1A;color:{color};'>{emoji}</div>"
            f"<div class='ds-feat-title'>{title}</div>"
            f"<div class='ds-feat-desc'>{desc}</div>"
            f"</div>"
        )
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    head_l, head_r = st.columns([6, 1])
    with head_l:
        st.markdown("<div class='ds-section-title'>Recent Documents</div>", unsafe_allow_html=True)
    with head_r:
        st.markdown("<div style='text-align:right;padding-top:8px;'><span class='ds-link'>View All</span></div>",
                     unsafe_allow_html=True)
    render_recent_documents_table(limit=5, key_prefix="home")

    if st.session_state.active_doc_id and st.session_state.active_doc_id in st.session_state.docs_store:
        st.write("")
        st.markdown("---")
        active = st.session_state.docs_store[st.session_state.active_doc_id]
        st.markdown(f"<div class='ds-section-title'>📂 Viewing: {active['name']}</div>", unsafe_allow_html=True)
        render_document_detail(st.session_state.active_doc_id, key_prefix="home")


# =========================
# PAGE: MY DOCUMENTS
# =========================

def render_my_documents():
    st.markdown("<div class='ds-section-title'>📁 My Documents</div>", unsafe_allow_html=True)
    render_recent_documents_table(key_prefix="mydocs")


# =========================
# PAGE: SEMANTIC SEARCH (standalone)
# =========================

def render_semantic_search_page():
    st.markdown("<div class='ds-section-title'>🔍 Semantic Search</div>", unsafe_allow_html=True)
    doc_id = st.session_state.active_doc_id
    if not doc_id or doc_id not in st.session_state.docs_store:
        st.info("Upload or select a document first (from Home or My Documents) to search inside it.")
        return
    doc = st.session_state.docs_store[doc_id]
    st.caption(f"Searching within: **{doc['name']}**")
    render_search_block(doc_id, key_prefix="standalone_search")


# =========================
# PAGE: ASK QUESTIONS (standalone)
# =========================

def render_ask_questions_page():
    st.markdown("<div class='ds-section-title'>💬 Ask Questions</div>", unsafe_allow_html=True)
    doc_id = st.session_state.active_doc_id
    if not doc_id or doc_id not in st.session_state.docs_store:
        st.info("Upload or select a document first (from Home or My Documents) to ask questions about it.")
        return
    doc = st.session_state.docs_store[doc_id]
    st.caption(f"Chatting about: **{doc['name']}**")
    render_qa_block(doc_id, key_prefix="standalone_qa")


# =========================
# PAGE: ANALYTICS
# =========================

def render_analytics():
    st.markdown("<div class='ds-section-title'>📊 Analytics</div>", unsafe_allow_html=True)
    docs = st.session_state.recent_docs

    total = len(docs)
    languages = sorted({d["language"] for d in docs}) if docs else []
    types = {}
    for d in docs:
        types[d["type"]] = types.get(d["type"], 0) + 1

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='ds-card'><div class='ds-metric-label'>Documents Processed</div>"
                    f"<div class='ds-metric-value'>{total}</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='ds-card'><div class='ds-metric-label'>Languages Detected</div>"
                    f"<div class='ds-metric-value'>{len(languages)}</div></div>", unsafe_allow_html=True)
    with c3:
        total_chars = sum(d["chars"] for d in docs)
        st.markdown(f"<div class='ds-card'><div class='ds-metric-label'>Total Characters Extracted</div>"
                    f"<div class='ds-metric-value'>{total_chars}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='ds-section-title'>Documents by Type</div>", unsafe_allow_html=True)
    if types:
        st.markdown("<div class='ds-card'>", unsafe_allow_html=True)
        for doc_type, count in types.items():
            st.markdown(f"{badge_html(doc_type)} &nbsp; **{count}** document(s)", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='ds-empty'>No data yet — process a document to see analytics.</div>",
                     unsafe_allow_html=True)


# =========================
# PAGE: SETTINGS
# =========================

def render_settings():
    st.markdown("<div class='ds-section-title'>⚙️ Settings</div>", unsafe_allow_html=True)
    st.markdown("<div class='ds-card'>", unsafe_allow_html=True)
    st.markdown("**Appearance**")
    st.toggle("Dark mode", value=(st.session_state.theme == "dark"), key="settings_dark_toggle",
              on_change=lambda: st.session_state.update(
                  theme="dark" if st.session_state.settings_dark_toggle else "light"))
    st.markdown("---")
    st.markdown("**Notifications**")
    st.checkbox("Email me when a document finishes processing", value=True, key="settings_notif")
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# PAGE: LOGOUT
# =========================

def render_logout():
    st.markdown("<div class='ds-section-title'>👋 Logged out</div>", unsafe_allow_html=True)
    st.success("You've been logged out of this demo session.")
    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()


# =========================
# ROUTER
# =========================

page = st.session_state.page

if page in ("Home", "Upload Document"):
    render_home()
elif page == "My Documents":
    render_my_documents()
elif page == "Semantic Search":
    render_semantic_search_page()
elif page == "Ask Questions":
    render_ask_questions_page()
elif page == "Analytics":
    render_analytics()
elif page == "Settings":
    render_settings()
elif page == "Logout":
    render_logout()
else:
    render_home()