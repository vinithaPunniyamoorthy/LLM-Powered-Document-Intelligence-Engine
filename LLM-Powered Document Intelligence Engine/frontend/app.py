import httpx
import streamlit as st

st.set_page_config(page_title="LLM Document Intelligence", layout="wide")

API_URL = st.sidebar.text_input("API base URL", value="http://127.0.0.1:8000")

st.title("LLM-Powered Document Intelligence Engine")
st.caption("Upload documents, ask questions, and retrieve relevant context using a FastAPI + RAG backend.")

st.markdown("""
### Features
- PDF, DOCX, TXT upload
- JWT-based auth flow
- Query and document retrieval
- Interview-ready architecture
""")

if "token" not in st.session_state:
    st.session_state.token = ""

with st.sidebar:
    st.header("Navigation")
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_Login.py", label="Login", icon="🔐")
    st.page_link("pages/2_Upload.py", label="Upload", icon="📄")
    st.page_link("pages/3_Query.py", label="Query", icon="💬")
    st.divider()
    st.header("Quick Start")
    st.write("1. Confirm backend status below")
    st.write("2. Register or log in on the Login page")
    st.write("3. Upload a document, then ask a question")

st.subheader("Live backend output")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Health check**")
    try:
        response = httpx.get(f"{API_URL}/health", timeout=10)
        if response.is_success:
            st.success("Backend is online")
            st.json(response.json())
        else:
            st.error(f"Health check failed ({response.status_code})")
            st.code(response.text)
    except Exception as exc:
        st.error("Backend is offline")
        st.code(str(exc))

with col2:
    st.markdown("**Sample query**")
    try:
        response = httpx.post(
            f"{API_URL}/query",
            json={"question": "What is this project about?"},
            timeout=10,
        )
        if response.is_success:
            body = response.json()
            st.success("Query endpoint responded")
            st.write(body.get("answer", ""))
            if body.get("sources"):
                st.caption(f"Sources: {body['sources']}")
        else:
            st.error(f"Query failed ({response.status_code})")
            st.code(response.text)
    except Exception as exc:
        st.error("Could not reach query endpoint")
        st.code(str(exc))

st.subheader("Documents in database")
try:
    response = httpx.get(f"{API_URL}/documents/", timeout=10)
    if response.is_success:
        docs = response.json()
        if docs:
            st.dataframe(docs, use_container_width=True)
        else:
            st.info("No documents uploaded yet. Use the Upload page to add one.")
    else:
        st.warning(f"Could not list documents ({response.status_code})")
except Exception as exc:
    st.warning(f"Document list unavailable: {exc}")
