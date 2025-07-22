# AI Financial Document Auditor

A smart Streamlit app that performs fraud detection on financial documents using OCR, Benford’s Law, and report generation.

## Features
- ✂ Upload PDFs, Excel or CSV files
- 🧪 Detect anomalies using Benford's Law
- 📄 Generate downloadable audit reports

## Stack
- Python, Streamlit, Pandas, Matplotlib
- FPDF for report creation
- pdfplumber for PDF OCR

## Usage
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Folder Structure
- `app.py`: Main Streamlit UI
- `utils/`: Supporting logic (OCR, Benford, PDF report)
- `sample_data/`: Demo files
- `.streamlit/`: Streamlit config
