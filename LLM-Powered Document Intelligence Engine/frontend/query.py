import streamlit as st

st.set_page_config(page_title="Query", layout="wide")

st.title("Ask Questions")
st.write("Send a question to the RAG-style backend and inspect the returned answer.")

api_url = st.text_input("API base URL", value="http://127.0.0.1:8000")
question = st.text_area("Question", placeholder="What does this document say about ...?")

if st.button("Ask") and question.strip():
    try:
        import requests

        response = requests.post(f"{api_url}/query", json={"question": question}, timeout=60)
        if response.ok:
            st.success("Query completed")
            st.write(response.json().get("answer", ""))
            sources = response.json().get("sources", [])
            if sources:
                st.caption(f"Sources: {sources}")
        else:
            st.error(f"Query failed: {response.text}")
    except Exception as exc:
        st.error(f"Connection error: {exc}")
