import fitz
import docx
import streamlit as st

def process_resume(uploaded_file):
    pdf_data = uploaded_file
    with fitz.open(stream=pdf_data, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        st.text_area("Resume Content", value=text)
