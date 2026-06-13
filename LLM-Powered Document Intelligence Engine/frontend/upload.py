import streamlit as st

st.set_page_config(page_title="Upload", layout="wide")

st.title("Document Upload")
st.write("Upload a PDF, DOCX, or TXT file to the FastAPI backend.")

api_url = st.text_input("API base URL", value="http://127.0.0.1:8000")
file = st.file_uploader("Choose a document", type=["pdf", "docx", "txt"])

if st.button("Upload") and file is not None:
    files = {"file": (file.name, file.getvalue(), file.type or "application/octet-stream")}
    try:
        import requests

        response = requests.post(f"{api_url}/documents/upload", files=files, timeout=60)
        if response.ok:
            st.success("Upload completed successfully")
            st.json(response.json())
        else:
            st.error(f"Upload failed: {response.text}")
    except Exception as exc:
        st.error(f"Connection error: {exc}")
