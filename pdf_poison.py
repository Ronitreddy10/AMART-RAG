from fpdf import FPDF
import os

def create_poisoned_pdf(hidden_text, output_path="poisoned_doc.pdf"):
    """
    Creates a benign-looking PDF with hidden malicious text.
    The text is white on a white background.
    """
    print(f"📄 Creating poisoned PDF with hidden text...")
    
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Add visible benign text
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0) # Black
        pdf.cell(200, 10, txt="Confidential Report - Q1 2025", ln=1, align='C')
        pdf.cell(200, 10, txt="This document contains sensitive financial projections.", ln=1, align='L')
        
        # Add HIDDEN malicious text (White on White)
        pdf.set_text_color(255, 255, 255) # White
        pdf.set_font("Arial", size=1) # Tiny font for extra stealth (optional, but requested white on white is main)
        # We can put it in a place that might be read by a parser but invisible to humans
        pdf.set_xy(10, 100) 
        pdf.multi_cell(0, 5, txt=hidden_text)
        
        pdf.output(output_path)
        print(f"✅ PDF saved to {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return None
