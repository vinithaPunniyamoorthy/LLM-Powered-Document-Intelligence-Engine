import httpx
import streamlit as st

st.set_page_config(page_title="Upload", layout="wide")

st.title("Document Upload")
st.write("Upload a PDF, DOCX, or TXT file to the FastAPI backend.")

api_url = st.text_input("API base URL", value="http://127.0.0.1:8000")
file = st.file_uploader("Choose a document", type=["pdf", "docx", "txt"])

if not st.session_state.get("token"):
    st.warning("Log in on the Login page first. Upload requires a JWT token.")

if st.button("Upload") and file is not None:
    token = st.session_state.get("token", "")
    if not token:
        st.error("Missing token. Please log in first.")
    else:
        try:
            response = httpx.post(
                f"{api_url}/documents/upload",
                files={"file": (file.name, file.getvalue(), file.type or "application/octet-stream")},
                headers={"Authorization": f"Bearer {token}"},
                timeout=60,
            )
            if response.is_success:
                st.success("Upload completed successfully")
                st.json(response.json())
            else:
                st.error(f"Upload failed: {response.text}")
        except Exception as exc:
            st.error(f"Connection error: {exc}")
