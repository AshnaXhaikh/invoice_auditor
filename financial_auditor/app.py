# --- app.py ---
import streamlit as st
import pandas as pd
import tempfile
from utils.ocr_utils import extract_text_from_pdf
from utils.benford_check import run_benford_analysis
from utils.report_generator import create_audit_report

st.set_page_config(page_title="AI Financial Document Auditor")
st.title("🔍 AI Financial Document Auditor")

st.markdown("""
Upload a financial document (PDF, CSV, or Excel) to analyze using **Benford's Law**.  
Only numeric columns (like invoice totals, sales figures) are used for fraud detection.
""")

uploaded_file = st.file_uploader("📤 Upload a file", type=["pdf", "csv", "xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    try:
        if uploaded_file.name.endswith(".pdf"):
            text_data = extract_text_from_pdf(file_path)
            if not text_data.strip():
                st.warning("No extractable text found in PDF.")
                st.stop()
            st.success("✅ Text successfully extracted from PDF.")
        
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(file_path)
            numeric_df = df.select_dtypes(include=["number"])
            if numeric_df.empty:
                st.warning("No numeric columns found in CSV file.")
                st.stop()
            text_data = numeric_df
            st.success("✅ CSV file loaded and numeric columns detected.")
        
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            numeric_df = df.select_dtypes(include=["number"])
            if numeric_df.empty:
                st.warning("No numeric columns found in Excel file.")
                st.stop()
            text_data = numeric_df
            st.success("✅ Excel file loaded and numeric columns detected.")
        
        else:
            st.error("Unsupported file type.")
            st.stop()

        # Benford Analysis
        st.subheader("📊 Benford's Law Analysis")
        results, fig = run_benford_analysis(text_data)
        st.pyplot(fig)

        # Generate Report
        if st.button("📝 Generate Report"):
            pdf_path = create_audit_report(results)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Audit Report", f, file_name="audit_report.pdf")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
