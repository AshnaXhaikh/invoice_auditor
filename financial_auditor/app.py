# Folder: ai-financial-auditor/

# --- app.py ---
import streamlit as st
import pandas as pd
from utils.ocr_utils import extract_text_from_pdf
from utils.benford_check import run_benford_analysis
from utils.report_generator import create_audit_report
import tempfile

st.set_page_config(page_title="AI Financial Document Auditor")
st.title("\U0001F50D AI Financial Document Auditor")

uploaded_file = st.file_uploader("Upload a PDF, Excel, or CSV file", type=["pdf", "csv", "xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    if uploaded_file.name.endswith(".pdf"):
        text_data = extract_text_from_pdf(file_path)
        st.success("Text extracted from PDF.")
    else:
        text_data = pd.read_csv(file_path) if uploaded_file.name.endswith("csv") else pd.read_excel(file_path)
        st.success("Spreadsheet loaded.")

    results, fig = run_benford_analysis(text_data)
    st.subheader("Benford's Law Analysis")
    st.pyplot(fig)

    if st.button("Generate Report"):
        pdf_path = create_audit_report(results)
        with open(pdf_path, "rb") as file:
            st.download_button("Download Report", file, file_name="audit_report.pdf")

