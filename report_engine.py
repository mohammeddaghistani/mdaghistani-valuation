from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
import os

def generate_professional_report(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4

    # الشعار والعلامة المائية
    if os.path.exists("logo.png"):
        c.drawImage("logo.png", 1.5*cm, H-3.5*cm, width=2.5*cm, preserveAspectRatio=True)

    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(W-1.5*cm, H-2.5*cm, "Valuation Report - mdaghistani")
    
    # تفاصيل الامتثال (إلزامي في دليل تقييم)
    c.setFont("Helvetica", 10)
    c.drawString(1.5*cm, H-5*cm, "1. Scope of Work:")
    c.drawString(2*cm, H-5.6*cm, f"- Basis of Value: {data['basis']}")
    c.drawString(2*cm, H-6.2*cm, "- Approach: Market Approach (Comparative)")
    c.drawString(2*cm, H-6.8*cm, f"- Grace Period (Art. 24): {data['grace']} Years")

    # إطار النتيجة النهائية
    c.setStrokeColorRGB(0.8, 0.7, 0.4)
    c.setFillColorRGB(0.98, 0.97, 0.94)
    c.rect(1.5*cm, H-10*cm, W-3*cm, 2.5*cm, fill=1)
    
    c.setFillColorRGB(0.2, 0.1, 0)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W/2, H-8.5*cm, "ESTIMATED MARKET RENT")
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W/2, H-9.5*cm, f"{data['value']:,.2f} SAR")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
