from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_poisoned_pdf(hidden_text, output_path="poisoned_doc.pdf"):
    """
    Creates a benign-looking PDF with semi-hidden malicious text using ReportLab.
    The text is gray and small to be stealthy but copyable.
    """
    print(f"📄 Creating poisoned PDF with hidden text...")
    
    try:
        # Create canvas
        c = canvas.Canvas(output_path, pagesize=letter)
        
        # Add visible benign text
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0, 0, 0) # Black
        # Center the title
        width, height = letter
        c.drawCentredString(width / 2, 750, "Confidential Report - Q1 2025")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, "This document contains sensitive financial projections.")
        
        # Add SEMI-HIDDEN malicious text
        # User requested semi-visible so it can be copied.
        # Using light gray (0.8) to be subtle but present in OCR/Copy.
        c.setFillColorRGB(0.8, 0.8, 0.8)  
        c.setFont("Helvetica", 6)  # Small font
        
        # Simple text wrapping could be complex, for now we just place it at the bottom or specific location
        # If text is very long, it might go off screen, but for the attack prompt it's usually one paragraph.
        c.drawString(100, 50, hidden_text)
        
        c.save()
        print(f"✅ PDF saved to {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return None

if __name__ == "__main__":
    create_poisoned_pdf("This is a test hidden message.", "test_poison.pdf")
