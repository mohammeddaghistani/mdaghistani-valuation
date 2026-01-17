from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def generate_formal_report(data):
    from io import BytesIO
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # تصميم الترويسة (Header)
    c.setFillColor(colors.HexColor("#1B4F72")) # لون رسمي كحلي
    c.rect(0, 780, 600, 100, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, 810, "VALUATION REPORT - MDAGHISTANI")
    
    # محتوى التقرير الفني
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 730, "1. VALUATION BASIS:")
    c.setFont("Helvetica", 10)
    c.drawString(60, 715, f"- Basis: {data['basis']} (Market Rent)")
    c.drawString(60, 700, f"- Standard: Saudi Authority for Accredited Valuers (TAQEEM)")
    
    # مربع النتيجة (الخلاصة)
    c.setStrokeColor(colors.HexColor("#D4AF37")) # إطار ذهبي
    c.rect(50, 550, 500, 80, stroke=1)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(300, 600, "FINAL ESTIMATED ANNUAL RENT")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 570, f"{data['value']:,.2f} SAR")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
