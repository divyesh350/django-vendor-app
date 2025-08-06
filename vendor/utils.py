from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

def generate_quotation_pdf(cx_name, date, processes, products, total_area, total_amount):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(Paragraph("Quotation", styles['h1']))
    story.append(Spacer(1, 0.2 * inch))

    # Customer and Date
    story.append(Paragraph(f"<b>Customer Name:</b> {cx_name}", styles['Normal']))
    story.append(Paragraph(f"<b>Date:</b> {date}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Tables
    # Process Table
    story.append(Paragraph("<b>Processes:</b>", styles['Normal']))
    process_data = [['Process']] + [[p] for p in processes]
    process_table = Table(process_data, colWidths=[4 * inch])
    process_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(process_table)
    story.append(Spacer(1, 0.2 * inch))

    # Product Table
    story.append(Paragraph("<b>Products:</b>", styles['Normal']))
    product_data = [['Product']] + [[p] for p in products]
    product_table = Table(product_data, colWidths=[4 * inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(product_table)
    story.append(Spacer(1, 0.2 * inch))

    # Total Area
    story.append(Paragraph(f"<b>Total Area:</b> {total_area}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Total Amount
    story.append(Paragraph(f"<b>Total Amount:</b> ${total_amount:.2f}", styles['h2']))

    doc.build(story)
    buffer.seek(0)
    return buffer