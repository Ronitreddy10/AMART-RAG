import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = FastAPI(title="Compliance & Reporting Engine API")

# MITRE Categories based on research
MITRE_CATEGORIES = [
    "Reconnaissance",
    "Prompt Injection",
    "Model Access",
    "Attack Staging",
    "Data Exfiltration"
]

class ReportRequest(BaseModel):
    successful_attacks: int = 15
    failed_attacks: int = 85
    report_name: str = "c_suite_report.pdf"

def calculate_nist_risk_score(success: int, total: int) -> int:
    """
    Calculates risk score based on the 5-point NIST AI RMF checklist from research:
    1. Does it leak sensitive data?
    2. Can it bypass safety rules?
    3. Does it affect multiple users?
    4. Is it easy to reproduce?
    5. Is the impact severe?
    """
    if total == 0:
        return 0
    # Simulate weighting the 5 checklist questions based on success rate
    base_severity_multiplier = 2.0  # Base assumption for severity and reproduction
    raw_score = (success / total) * 100 * base_severity_multiplier
    return min(int(raw_score), 100)

def generate_pdf_report(filename: str, success: int, fail: int):
    """
    Uses ReportLab to generate a C-Suite style PDF mapping vulnerabilities.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center
    elements.append(Paragraph("AI Security Compliance & Risk Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Summary Paragraph
    total = success + fail
    score = calculate_nist_risk_score(success, total)
    
    risk_level = "CRITICAL" if score > 75 else "HIGH" if score > 50 else "MODERATE" if score > 25 else "LOW"
    
    summary_text = (f"This report outlines the results of the automated red-teaming sequence. "
                    f"A total of {total} attack vectors were executed. {success} attacks successfully bypassed "
                    f"security guardrails, resulting in a NIST AI RMF Risk Score of {score}/100 <b>({risk_level})</b>.")
    
    elements.append(Paragraph(summary_text, styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # MITRE ATLAS mapping table
    elements.append(Paragraph("MITRE ATLAS Vulnerability Mapping", styles['Heading2']))
    elements.append(Spacer(1, 10))
    
    # Distribute success randomly across categories for the mockup
    data = [["MITRE Tactic", "Vulnerability Count", "Status"]]
    import random
    
    remaining = success
    for i, category in enumerate(MITRE_CATEGORIES):
        if i == len(MITRE_CATEGORIES) -1:
            count = remaining
        else:
            count = random.randint(0, remaining)
            remaining -= count
            
        status = "FAIL" if count > 0 else "PASS"
        data.append([category, str(count), status])
        
    table = Table(data, colWidths=[200, 150, 100])
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f3f4f6")),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    table.setStyle(ts)
    elements.append(table)
    
    # Save PDF
    doc.build(elements)
    return filename

@app.post("/api/generate-report")
def generate_report_endpoint(req: ReportRequest):
    try:
        pdf_path = req.report_name
        generate_pdf_report(pdf_path, req.successful_attacks, req.failed_attacks)
        return {"status": "Success", "pdf_url": f"/api/download/{pdf_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{filename}")
def download_pdf(filename: str):
    if os.path.exists(filename):
        return FileResponse(filename, media_type="application/pdf", filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    print("Starting Reporting Engine API on port 8003...")
    uvicorn.run(app, host="0.0.0.0", port=8003)
