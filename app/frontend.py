import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Study Q&A Assistant", page_icon="📚")
st.title("Study Material Q&A Assistant")

st.header("Upload Study MAterial")
uploaded_file=st.file_uploader("Choose a PDF",type=["pdf"])

if uploaded_file is not None:
    if st.button("Upload and Process"):
        with st.spinner("Processing...") :
            files={"file":(uploaded_file.name,uploaded_file,"application/pdf")}
            response=requests.post(f"{API_URL}/upload",files=files)
        if response.status_code==200:
            st.success(f"Uploaded and processed: {uploaded_file.name}")
        else:
            st.error(f"Upload failed: {response.text}")

st.header("Ask a question")
question=st.text_input("What do you want to know")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{API_URL}/ask",
                json={"question":question,"top_k":5},
            )
        if response.status_code==200:
            result=response.json()
            st.subheader("Answer")
            st.write(result["answer"])
            st.subheader("Sources")
            for s in result["sources"]:
                st.write(f"- {s['source_file']},page {s['page_number']},section: {s['section_title']}")
        else:
            st.error(f"Request failed: {response.text}")