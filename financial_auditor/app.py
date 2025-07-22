# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdfplumber
from fpdf import FPDF
import tempfile
import re
from collections import Counter

# Streamlit UI setup
st.set_page_config(page_title="AI Financial Document Auditor")
st.title("🔍 AI Financial Document Auditor")

# Upload file
uploaded_file = st.file_uploader("Upload a PDF, Excel, or CSV file", type=["pdf", "csv", "xlsx"])

# --- Functions ---

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def run_benford_analysis(data):
    try:
        if isinstance(data, str):
            numbers = list(map(float, re.findall(r"\b\d+(?:\.\d+)?\b", data)))
        else:
            numbers = pd.to_numeric(data.select_dtypes(include=["number"]).stack(), errors='coerce').dropna().values

        # Filter out zero and invalid entries
        numbers = [num for num in numbers if num != 0 and str(abs(num))[0].isdigit()]
        if len(numbers) == 0:
            raise ValueError("No valid numeric data found.")

        first_digits = [int(str(abs(num))[0]) for num in numbers]
        observed = Counter(first_digits)

        total = sum(observed.values())
        observed_freq = [observed.get(d, 0)/total for d in range(1,10)]
        expected_freq = [np.log10(1 + 1/d) for d in range(1,10)]

        fig, ax = plt.subplots()
        ax.bar(range(1,10), observed_freq, label="Observed", alpha=0.7)
        ax.plot(range(1,10), expected_freq, label="Expected", color="red", marker="o")
        ax.set_title("Benford's Law Distribution")
        ax.set_xlabel("Leading Digit")
        ax.set_ylabel("Frequency")
        ax.legend()

        summary = {"observed": observed_freq, "expected": expected_freq}
        return summary, fig
    except Exception as e:
        raise ValueError(f"Benford analysis failed: {e}")

def create_audit_report(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Audit Report Based on Benford's Law", ln=True, align='C')
    pdf.ln(10)

    for d in range(1, 10):
        obs = results['observed'][d-1]
        exp = results['expected'][d-1]
        pdf.cell(200, 10, txt=f"Digit {d}: Observed = {obs:.3f}, Expected = {exp:.3f}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="End of Report", ln=True, align='C')

    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(temp_path)
    return temp_path

# --- Processing ---

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    try:
        if uploaded_file.name.endswith(".pdf"):
            text_data = extract_text_from_pdf(file_path)
            st.success("✅ Text successfully extracted from PDF.")
        elif uploaded_file.name.endswith(".csv"):
            text_data = pd.read_csv(file_path)
            st.success("✅ CSV file loaded.")
        else:
            text_data = pd.read_excel(file_path)
            st.success("✅ Excel file loaded.")
        
        st.subheader("📊 Benford's Law Analysis")
        results, fig = run_benford_analysis(text_data)
        st.pyplot(fig)

        if st.button("📄 Generate Report"):
            report_path = create_audit_report(results)
            with open(report_path, "rb") as file:
                st.download_button("⬇️ Download Report", file, file_name="audit_report.pdf")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
