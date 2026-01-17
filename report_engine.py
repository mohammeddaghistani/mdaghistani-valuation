from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO
import os

def generate_formal_report(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4

    # خلفية وترويسة فخمة
    c.setFillColor(colors.HexColor("#1a4731"))
    c.rect(0, H-4*cm, W, 4*cm, fill=1)
    
    if os.path.exists("logo.png"):
        c.drawImage("logo.png", 1*cm, H-3.5*cm, width=2.5*cm, preserveAspectRatio=True)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(4*cm, H-2*cm, "PROPERTY VALUATION CERTIFICATE")
    c.setFont("Helvetica", 10)
    c.drawString(4*cm, H-2.6*cm, "Based on Municipal Property Disposal Law & TAQEEM Standards")

    # تفاصيل القيمة
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W/2, H-7*cm, "ESTIMATED ANNUAL MARKET RENT")
    
    # مربع ذهبي للقيمة
    c.setStrokeColor(colors.HexColor("#c5a059"))
    c.setFillColor(colors.HexColor("#fdfaf4"))
    c.roundRect(W/2-4*cm, H-9*cm, 8*cm, 1.5*cm, 10, fill=1, stroke=1)
    
    c.setFillColor(colors.HexColor("#1a4731"))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W/2, H-8.6*cm, f"{data['value']:,.2f} SAR")

    # بنود الامتثال (المادة 24)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2*cm, H-11*cm, "Valuation Notes:")
    c.setFont("Helvetica", 9)
    c.drawString(2*cm, H-11.6*cm, f"- Grace Period Applied: {data['grace']} Years (According to Article 24)")
    c.drawString(2*cm, H-12.2*cm, f"- Valuation Methodology: Comparative Market Approach (TAQEEM p.34)")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
