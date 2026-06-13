import streamlit as st

st.set_page_config(page_title="Login", layout="wide")

st.title("Authentication")
st.write("Register or log in to get a token for protected API requests.")

api_url = st.text_input("API base URL", value="http://127.0.0.1:8000")
name = st.text_input("Name (for registration)", value="")
email = st.text_input("Email", value="demo@example.com")
password = st.text_input("Password", type="password")

if st.button("Register"):
    try:
        import requests

        response = requests.post(
            f"{api_url}/auth/register",
            json={"name": name or "Demo User", "email": email, "password": password},
            timeout=60,
        )
        if response.ok:
            st.success("Registration succeeded")
            st.json(response.json())
        else:
            st.error(f"Registration failed: {response.text}")
    except Exception as exc:
        st.error(f"Connection error: {exc}")

if st.button("Login"):
    try:
        import requests

        response = requests.post(
            f"{api_url}/auth/login",
            json={"email": email, "password": password},
            timeout=60,
        )
        if response.ok:
            st.session_state.token = response.json().get("access_token", "")
            st.success("Login succeeded")
            st.json(response.json())
        else:
            st.error(f"Login failed: {response.text}")
    except Exception as exc:
        st.error(f"Connection error: {exc}")
