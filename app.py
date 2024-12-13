import streamlit as st
import random
import pandas as pd
from io import StringIO, BytesIO
from PyPDF2 import PdfReader, PdfWriter

def process_uploaded_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        # For text files
        content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        # For PDF files
        reader = PdfReader(uploaded_file)
        content = "".join([page.extract_text() for page in reader.pages])
    else:
        st.error("Unsupported file type. Please upload a .txt or .pdf file.")
        return None
    return content

def randomize_keywords(content):
    keywords = [kw.strip() for kw in content.replace("\n", ",").split(",") if kw.strip()]
    random.shuffle(keywords)
    return keywords

def save_to_text_file(keywords):
    output = "\n".join(keywords)
    return StringIO(output)

def save_to_pdf_file(keywords):
    output_pdf = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)  # Adjust page size if needed
    for kw in keywords:
        writer.add_page_text(kw + "\n")
    writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf

def main():
    st.title("Keyword Randomizer")
    st.write("Upload a text or PDF file with keywords, and get a randomized list in a new file.")

    uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])

    if uploaded_file:
        content = process_uploaded_file(uploaded_file)
        if content:
            keywords = randomize_keywords(content)
            st.write("### Randomized Keywords:")
            st.write(keywords)

            output_format = st.selectbox("Select output format", ["Text", "PDF"])

            if st.button("Download Randomized Keywords"):
                if output_format == "Text":
                    text_file = save_to_text_file(keywords)
                    st.download_button(
                        label="Download Text File",
                        data=text_file.getvalue(),
                        file_name="randomized_keywords.txt",
                        mime="text/plain",
                    )
                elif output_format == "PDF":
                    pdf_file = save_to_pdf_file(keywords)
                    st.download_button(
                        label="Download PDF File",
                        data=pdf_file.getvalue(),
                        file_name="randomized_keywords.pdf",
                        mime="application/pdf",
                    )

if __name__ == "__main__":
    main()
