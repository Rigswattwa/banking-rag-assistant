import os
import streamlit as st
import requests

# Configuration
API_URL = os.environ["API_URL"]

st.set_page_config(
    page_title="Intelligent Banking Knowledge Assistant",
    page_icon="🏦",
    layout="centered"
)


st.title("🏦 Intelligent Banking Knowledge Assistant")
st.markdown(
    """
    Ask questions about **Loan Policies, KYC/AML guidelines, RBI circulars**, and more.
    
    Powered by **RAG (FAISS + OpenAI)**.
    """
)


query = st.text_area(
    "Enter your question",
    placeholder="e.g. What are RBI KYC requirements for banks?",
    height=100
)

ask_btn = st.button("Ask Question")

if ask_btn and query.strip():
    with st.spinner("Searching policy documents..."):
        try:
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": query},
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()

                st.subheader("Answer")
                st.write(data.get("answer"))

                sources = data.get("sources", [])
                if sources:
                    st.subheader("Source References")
                    for idx, src in enumerate(sources, 1):
                        with st.expander(f"Source {idx}: {src['source']}"):
                            st.write(src["snippet"])
            else:
                st.error(f"API Error: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {str(e)}")


st.markdown("---")
st.caption("Built with FastAPI, FAISS, OpenAI & Streamlit | LLMOps Capstone")
