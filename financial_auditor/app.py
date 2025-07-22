# --- app.py ---
import streamlit as st
import pandas as pd
import tempfile
from utils.ocr_utils import extract_text_from_pdf
from utils.benford_check import run_benford_analysis
from utils.report_generator import create_audit_report

# Page config
st.set_page_config(
    page_title="AI Financial Document Auditor",
    page_icon="🔍",
    layout="centered"
)

# App Title
st.title("🔍 AI Financial Document Auditor")
st.markdown("""
Welcome to the **AI-powered Financial Auditor App**.  
Upload a financial document (`PDF`, `CSV`, or `Excel`) and let our system detect anomalies using **Benford’s Law**.

📌 _Only numeric columns (like invoice totals, transaction amounts) are used for fraud detection._
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📤 Upload a financial document", type=["pdf", "csv", "xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    try:
        # Handle PDF
        if uploaded_file.name.endswith(".pdf"):
            text_data = extract_text_from_pdf(file_path)
            if not text_data.strip():
                st.warning("⚠️ No extractable text found in PDF.")
                st.stop()
            st.success("✅ Text successfully extracted from PDF.")

        # Handle CSV
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(file_path)
            numeric_df = df.select_dtypes(include=["number"])
            if numeric_df.empty:
                st.warning("⚠️ No numeric columns found in the uploaded CSV file.")
                st.stop()
            text_data = numeric_df
            st.success(f"✅ CSV loaded: {df.shape[0]} rows, {df.shape[1]} columns detected.")

        # Handle Excel
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            numeric_df = df.select_dtypes(include=["number"])
            if numeric_df.empty:
                st.warning("⚠️ No numeric columns found in the Excel file.")
                st.stop()
            text_data = numeric_df
            st.success(f"✅ Excel loaded: {df.shape[0]} rows, {df.shape[1]} columns detected.")

        else:
            st.error("❌ Unsupported file type.")
            st.stop()

        # Benford's Law Analysis
        st.subheader("📊 Benford's Law Analysis")
        results, fig = run_benford_analysis(text_data)
        st.pyplot(fig)

        # Report button
        with st.expander("📝 Generate Audit Report"):
            if st.button("📥 Download Report"):
                pdf_path = create_audit_report(results)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Audit Report (PDF)",
                        data=f,
                        file_name="audit_report.pdf",
                        mime="application/pdf"
                    )

    except Exception as e:
        st.error(f"❌ An error occurred during processing:\n\n`{e}`")

# Footer
st.markdown("---")
st.caption("© 2025 | Built with ❤️ using Python, Streamlit, OCR, and Benford's Law.")
