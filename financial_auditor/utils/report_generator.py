# --- utils/report_generator.py ---
from fpdf import FPDF
import tempfile

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
